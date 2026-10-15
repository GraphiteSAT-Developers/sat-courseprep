// Trace-generation CLI. Run from web/ with
//   npm run traces:generate -- --items all --dialogues-per-item 2 --out ../data/traces
// (tsx with the react-server condition so the server-only guard on
// content/items.ts is a no-op). Needs ANTHROPIC_API_KEY (or an `ant auth`
// profile). Models: TRACE_SOLVER_MODEL (solver + student, default
// claude-sonnet-5-5), TUTOR_MODEL (tutor, default claude-sonnet-5-5),
// TRACE_JUDGE_MODEL (judge, default claude-opus-5-5).
//
// Writes solutions.jsonl, dialogues.jsonl and sft.jsonl into --out.
// Idempotent: an item with an accepted trace keeps it, and an item that already
// has N accepted dialogues gets no new ones, unless --force.

import Anthropic from "@anthropic-ai/sdk";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { listItems } from "../content/items";
import { createStudentSimulator, createTraceTutor, simulateDialogue } from "../lib/traces/dialogue";
import { applyVerdict, judgeDialogue, DEFAULT_MIN_SCORE } from "../lib/traces/judge";
import { JUDGE_MODEL, SOLVER_MODEL, UsageMeter, costUsd } from "../lib/traces/llm";
import { PERSONAS } from "../lib/traces/personas";
import { isAcceptedTrace, parseDialogue, parseJsonl, parseSolutionTrace, toJsonl, type Dialogue, type SolutionTrace } from "../lib/traces/schema";
import { sftLines } from "../lib/traces/sft";
import { solveItem } from "../lib/traces/solve";

interface Args {
  items: string[] | "all";
  dialoguesPerItem: number;
  out: string;
  force: boolean;
  minScore: number;
  maxExchanges: number;
}

function parseArgs(argv: string[]): Args {
  const args: Args = { items: "all", dialoguesPerItem: 1, out: resolve(__dirname, "../../data/traces"), force: false, minScore: DEFAULT_MIN_SCORE, maxExchanges: 4 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => {
      const v = argv[++i];
      if (v === undefined) throw new Error(`${a} needs a value`);
      return v;
    };
    switch (a) {
      case "--items": {
        const v = next();
        args.items = v === "all" ? "all" : v.split(",").map((s) => s.trim()).filter(Boolean);
        break;
      }
      case "--dialogues-per-item":
        args.dialoguesPerItem = Number(next());
        break;
      case "--out":
        args.out = resolve(next());
        break;
      case "--force":
        args.force = true;
        break;
      case "--min-score":
        args.minScore = Number(next());
        break;
      case "--max-exchanges":
        args.maxExchanges = Number(next());
        break;
      case "--help":
      case "-h":
        console.log("usage: generate-traces --items <id,id|all> --dialogues-per-item N --out <dir> [--force] [--min-score 4] [--max-exchanges 4]");
        process.exit(0);
      // eslint-disable-next-line no-fallthrough
      default:
        throw new Error(`unknown argument ${a}`);
    }
  }
  if (!Number.isInteger(args.dialoguesPerItem) || args.dialoguesPerItem < 0) throw new Error("--dialogues-per-item must be a non-negative integer");
  return args;
}

function readJsonl<T>(path: string, parse: (v: unknown) => T): T[] {
  return existsSync(path) ? parseJsonl(readFileSync(path, "utf8"), parse) : [];
}

function nextSeq(ids: string[], prefix: string): number {
  let max = 0;
  for (const id of ids) {
    if (!id.startsWith(prefix)) continue;
    const n = Number(id.slice(prefix.length));
    if (Number.isInteger(n) && n > max) max = n;
  }
  return max + 1;
}

function pad(s: string | number, w: number): string {
  return String(s).padEnd(w);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const all = listItems();
  const selected = args.items === "all" ? all : args.items.map((id) => {
    const item = all.find((i) => i.id === id);
    if (!item) throw new Error(`unknown item id ${id}`);
    return item;
  });

  mkdirSync(args.out, { recursive: true });
  const solutionsPath = resolve(args.out, "solutions.jsonl");
  const dialoguesPath = resolve(args.out, "dialogues.jsonl");
  const sftPath = resolve(args.out, "sft.jsonl");
  const solutions = readJsonl(solutionsPath, parseSolutionTrace);
  const dialogues = readJsonl(dialoguesPath, parseDialogue);

  const client = new Anthropic();
  const meter = new UsageMeter();
  const tutor = createTraceTutor(client, { meter });
  const student = createStudentSimulator(client, { meter });

  const rows: { id: string; trace: string; dialogues: string; accepted: number; rejected: number }[] = [];
  const save = () => {
    writeFileSync(solutionsPath, toJsonl(solutions));
    writeFileSync(dialoguesPath, toJsonl(dialogues));
    writeFileSync(sftPath, toJsonl(sftLines(dialogues)));
  };

  for (const item of selected) {
    let trace = solutions.find((t) => t.itemId === item.id && isAcceptedTrace(t));
    let traceNote = "kept";
    if (!trace || args.force) {
      const seq = nextSeq(solutions.map((t) => t.id), `${item.id}#s`);
      const fresh = await solveItem(client, item, { meter, seq });
      solutions.push(fresh);
      trace = isAcceptedTrace(fresh) ? fresh : undefined;
      traceNote = fresh.agreesWithKey ? `solved (${fresh.attempts} call${fresh.attempts === 1 ? "" : "s"})` : `REJECTED after ${fresh.attempts} calls`;
      save();
    }
    if (!trace) {
      rows.push({ id: item.id, trace: traceNote, dialogues: "skipped", accepted: 0, rejected: 0 });
      continue;
    }

    const have = args.force ? 0 : dialogues.filter((d) => d.itemId === item.id && d.status === "accepted").length;
    const want = Math.max(0, args.dialoguesPerItem - have);
    let accepted = 0;
    let rejected = 0;
    const existingForItem = dialogues.filter((d) => d.itemId === item.id).length;
    for (let n = 0; n < want; n++) {
      const persona = PERSONAS[(existingForItem + n) % PERSONAS.length];
      const seq = nextSeq(dialogues.map((d) => d.id), `${item.id}#d`);
      let d: Dialogue = await simulateDialogue({ item, trace, persona, tutor, student, maxExchanges: args.maxExchanges, seq });
      const { verdict, model, usage } = await judgeDialogue(client, item, d, { meter });
      d = applyVerdict({ ...d, usage: { ...d.usage, inputTokens: d.usage.inputTokens + usage.inputTokens, outputTokens: d.usage.outputTokens + usage.outputTokens, cacheReadTokens: d.usage.cacheReadTokens + usage.cacheReadTokens, cacheWriteTokens: d.usage.cacheWriteTokens + usage.cacheWriteTokens } }, verdict, model, args.minScore);
      dialogues.push(d);
      if (d.status === "accepted") accepted++;
      else rejected++;
      save();
    }
    rows.push({ id: item.id, trace: traceNote, dialogues: want === 0 ? `kept ${have}` : `${want} new`, accepted, rejected });
  }
  save();

  // Summary
  console.log(`\n${pad("item", 32)} ${pad("trace", 24)} ${pad("dialogues", 12)} ${pad("accepted", 9)} rejected`);
  for (const r of rows) console.log(`${pad(r.id, 32)} ${pad(r.trace, 24)} ${pad(r.dialogues, 12)} ${pad(r.accepted, 9)} ${r.rejected}`);
  const acceptedTraces = solutions.filter(isAcceptedTrace).length;
  const acceptedDialogues = dialogues.filter((d) => d.status === "accepted").length;
  console.log(`\nsolutions.jsonl: ${solutions.length} traces (${acceptedTraces} accepted, ${solutions.filter((t) => t.verifiedInDesmos).length} verified in Desmos)`);
  console.log(`dialogues.jsonl: ${dialogues.length} dialogues (${acceptedDialogues} accepted, ${dialogues.filter((d) => d.labels.answerRevealedEarly).length} with early reveal)`);
  console.log(`sft.jsonl: ${acceptedDialogues} lines`);

  console.log(`\nmodels: solver/student ${SOLVER_MODEL}, tutor ${tutor.model}, judge ${JUDGE_MODEL}`);
  console.log(`${pad("model", 24)} ${pad("calls", 6)} ${pad("input", 10)} ${pad("output", 10)} ${pad("cache read", 11)} ${pad("cache write", 12)} cost`);
  for (const [model, { calls, usage }] of meter.byModel) {
    const c = costUsd(model, usage);
    console.log(`${pad(model, 24)} ${pad(calls, 6)} ${pad(usage.inputTokens, 10)} ${pad(usage.outputTokens, 10)} ${pad(usage.cacheReadTokens, 11)} ${pad(usage.cacheWriteTokens, 12)} ${c === null ? "unknown price" : `$${c.toFixed(4)}`}`);
  }
  const total = meter.totalCostUsd();
  console.log(`total: $${total.known.toFixed(4)}${total.unknownModels.length ? ` (excludes ${total.unknownModels.join(", ")}: no price on file)` : ""}`);
}

main().catch((e) => {
  const msg = e instanceof Error ? e.message : String(e);
  if (/api.?key|authentication|401/i.test(msg)) {
    console.error(`Authentication failed: ${msg}\nSet ANTHROPIC_API_KEY (or run \`ant auth login\`) and retry.`);
  } else {
    console.error(msg);
  }
  process.exit(1);
});
