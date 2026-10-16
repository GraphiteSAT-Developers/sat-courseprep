// Solver: asks Sonnet for a Desmos solution trace and grades the final answer
// with the deterministic grader. The model is never asked whether it is right,
// and its answer is never trusted: `agreesWithKey` comes from gradeItem alone.

import type Anthropic from "@anthropic-ai/sdk";
import type { Item } from "@/content/types";
import { getTechnique } from "@/content/techniques";
import { gradeItem, type GradeResult } from "@/lib/grading/grade";
import { SOLVER_MODEL, StructuredOutputError, addUsage, emptyUsage, expectObject, expectString, expectStringArray, structured, type TraceClient, type UsageMeter } from "./llm";
import type { SolutionTrace, TokenUsage } from "./schema";

export const MAX_SOLVER_RETRIES = 2;

const SOLVER_SYSTEM = `You solve SAT Math items the way a strong student would in the Bluebook testing app: with the built-in Desmos graphing calculator first, by hand second.

Return JSON only, matching the schema. Fields:
- desmosLines: the lines to type into Desmos, in order, in Desmos LaTeX exactly as the calculator accepts it (for example "y=x^{2}-6x+11", "y=2x-5", "y_{1}\\sim mx_{1}+b"). Use \\sim (~) for regressions, never =. Use only syntax that exists in the College Board build of Desmos: no custom functions, no scripts, no features behind settings other than degree mode. Each line must be something a student could type as-is.
- readOff: what to do after typing: which point to click, which value to read, whether to zoom.
- reasoning: a short summary (two to four sentences) of why the route gives the answer, including a by-hand check if one is quick.
- finalAnswer: for multiple choice, exactly one letter A, B, C or D. For a student-produced response, the exact string to type into the answer box under Bluebook rules: a fraction like 2/3 or -5/4, an integer, or a decimal that fills the box (at most 5 characters, 6 with a leading minus sign; a repeating decimal must be truncated or rounded to fill the box, never rounded short). Prefer the exact fraction when it fits.`;

const SOLVER_SCHEMA = {
  type: "object",
  properties: {
    desmosLines: { type: "array", items: { type: "string" } },
    readOff: { type: "string" },
    reasoning: { type: "string" },
    finalAnswer: { type: "string" },
  },
  required: ["desmosLines", "readOff", "reasoning", "finalAnswer"],
  additionalProperties: false,
} as const;

export interface SolverOutput {
  desmosLines: string[];
  readOff: string;
  reasoning: string;
  finalAnswer: string;
}

function validateSolverOutput(v: unknown): SolverOutput {
  const o = expectObject(v, "output");
  return {
    desmosLines: expectStringArray(o.desmosLines, "desmosLines"),
    readOff: expectString(o.readOff, "readOff"),
    reasoning: expectString(o.reasoning, "reasoning"),
    finalAnswer: expectString(o.finalAnswer, "finalAnswer").trim(),
  };
}

/** The item as the solver sees it: stem, format, techniques. No key, no stored routes. */
export function describeItemForSolver(item: Item): string {
  const techniques = item.techniques
    .map((id) => getTechnique(id))
    .filter((t) => t !== undefined)
    .map((t) => `- ${t.id} ${t.name}: ${t.summary}`)
    .join("\n");
  return [
    `Question: ${item.stem}`,
    item.format === "mc"
      ? `Choices: ${item.choices.map((c, i) => `${"ABCD"[i]}. ${c}`).join("  ")}\nAnswer format: one letter A–D.`
      : "Format: student-produced response. Answer format: the exact entry for the answer box.",
    `Domain: ${item.domain}. Skill: ${item.skill}. Difficulty: ${item.difficulty}.`,
    techniques ? `Desmos techniques that may apply:\n${techniques}` : "",
  ]
    .filter(Boolean)
    .join("\n");
}

/** Turn the solver's finalAnswer into what the grader takes. */
export function toGradeResponse(item: Item, finalAnswer: string): string | number {
  if (item.format === "spr") return finalAnswer;
  const letter = finalAnswer.trim().toUpperCase().replace(/[^A-D]/g, "");
  return letter.length === 1 ? "ABCD".indexOf(letter) : -1;
}

/** Feedback the grader sends back on a retry. States only what the grader knows; never the key. */
export function graderFeedback(item: Item, finalAnswer: string, result: GradeResult): string {
  if (result.status === "invalid") return `Your finalAnswer "${finalAnswer}" is not a valid entry: ${result.reason}`;
  const hint = result.status === "incorrect" && result.hint === "rounded-too-early" ? " It looks rounded too early; fill the answer box or give the exact fraction." : "";
  return item.format === "mc"
    ? `Your finalAnswer "${finalAnswer}" is not the correct choice. Re-check the graph (zoom out, confirm the point you read) and the question wording, then answer again.`
    : `Your finalAnswer "${finalAnswer}" does not match the key.${hint} Re-check the graph and the question wording, then answer again.`;
}

export interface SolveOptions {
  model?: string;
  meter?: UsageMeter;
  /** Sequence number for the trace id. */
  seq?: number;
  now?: () => string;
}

/**
 * Solve one item. Up to MAX_SOLVER_RETRIES retries with grader feedback; after
 * that the trace is rejected. Malformed output counts as a failed attempt too.
 */
export async function solveItem(client: TraceClient, item: Item, opts: SolveOptions = {}): Promise<SolutionTrace> {
  const model = opts.model ?? SOLVER_MODEL;
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: describeItemForSolver(item) }];
  const feedback: string[] = [];
  let usage: TokenUsage = emptyUsage();
  let last: SolverOutput = { desmosLines: [], readOff: "", reasoning: "", finalAnswer: "" };
  let agrees = false;
  let attempts = 0;

  for (let attempt = 0; attempt <= MAX_SOLVER_RETRIES; attempt++) {
    attempts = attempt + 1;
    let out: SolverOutput | undefined;
    let note: string;
    try {
      const r = await structured(client, {
        model,
        system: SOLVER_SYSTEM,
        messages: [...messages],
        schema: SOLVER_SCHEMA as unknown as Record<string, unknown>,
        validate: validateSolverOutput,
        effort: "high",
        meter: opts.meter,
      });
      usage = addUsage(usage, r.usage);
      out = r.value;
      last = out;
      const result = gradeItem(item, toGradeResponse(item, out.finalAnswer));
      if (result.status === "correct") {
        agrees = true;
        break;
      }
      note = graderFeedback(item, out.finalAnswer, result);
      messages.push({ role: "assistant", content: r.raw });
    } catch (e) {
      if (!(e instanceof StructuredOutputError)) throw e;
      note = `Your reply could not be used (${e.message}). Reply with JSON matching the schema only.`;
      messages.push({ role: "assistant", content: "(unusable reply)" });
    }
    if (attempt < MAX_SOLVER_RETRIES) {
      feedback.push(note);
      messages.push({ role: "user", content: note });
    }
  }

  return {
    id: `${item.id}#s${opts.seq ?? 1}`,
    itemId: item.id,
    model,
    createdAt: (opts.now ?? (() => new Date().toISOString()))(),
    desmosLines: last.desmosLines,
    readOff: last.readOff,
    reasoning: last.reasoning,
    finalAnswer: last.finalAnswer,
    agreesWithKey: agrees,
    verifiedInDesmos: false,
    status: agrees ? "candidate" : "rejected",
    attempts,
    graderFeedback: feedback,
    usage,
  };
}
