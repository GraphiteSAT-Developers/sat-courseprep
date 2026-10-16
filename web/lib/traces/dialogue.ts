// Dialogue simulation: Sonnet plays the tutor on exactly the production
// prompt (lib/tutor/prompt.ts: SYSTEM_RULES, item block, per-turn state) and a
// second Sonnet call plays a scripted student (personas.ts). The site's
// guardrails (clampRequest) run on every tutor turn as they do in the API
// route, and the deterministic grader scores every attempt. The answer-leak
// label is computed here, deterministically; the judge adds the rest.

import type Anthropic from "@anthropic-ai/sdk";
import type { Item } from "@/content/types";
import type { CalculatorSnapshot } from "@/lib/desmos/snapshot";
import { gradeItem, type GradeResult } from "@/lib/grading/grade";
import { clampRequest } from "@/lib/tutor/guardrails";
import { FALLBACK_TEXT, REFUSAL_TEXT, SYSTEM_RULES, describeItem, describeTurn } from "@/lib/tutor/prompt";
import { HINT_LEVELS, type HintLevel, type TutorClientRequest, type TutorContext, type TutorTurn } from "@/lib/tutor/types";
import { SOLVER_MODEL, addUsage, emptyUsage, expectBoolean, expectObject, expectString, expectStringArray, structured, textOf, usageOf, type TraceClient, type UsageMeter } from "./llm";
import { answerRevealedEarly } from "./leak";
import { summarizePersona, type Persona } from "./personas";
import type { ChatMessage, Dialogue, SolutionTrace, TokenUsage, TurnMeta } from "./schema";
import { toGradeResponse } from "./solve";

/** Mirrors TUTOR_MODEL in lib/tutor/anthropic.ts (not imported: that module is server-only). */
export const TRACE_TUTOR_MODEL = process.env.TUTOR_MODEL ?? "claude-sonnet-5-5";
export const STUDENT_MODEL = process.env.TRACE_STUDENT_MODEL ?? SOLVER_MODEL;

// ---------------------------------------------------------------------------
// Tutor

export interface TutorTurnResult {
  text: string;
  /** The system prompt as sent (rules + item block), for the dialogue's system message. */
  system: string;
  /** The user turn as sent (state block + "Student says: ..."). */
  user: string;
  usage: TokenUsage;
}

export interface TraceTutor {
  model: string;
  reply(ctx: TutorContext): Promise<TutorTurnResult>;
}

/** The production tutor request, byte for byte (see createAnthropicProvider), plus the prompt it sent. */
export function createTraceTutor(client: TraceClient, opts: { model?: string; meter?: UsageMeter } = {}): TraceTutor {
  const model = opts.model ?? TRACE_TUTOR_MODEL;
  return {
    model,
    async reply(ctx) {
      const history: Anthropic.MessageParam[] = ctx.history.map((t) => ({ role: t.role === "student" ? "user" : "assistant", content: t.text }));
      const itemBlock = describeItem(ctx);
      const user = describeTurn(ctx);
      const response = await client.messages.create({
        model,
        max_tokens: 2048,
        thinking: { type: "adaptive" },
        output_config: { effort: "low" },
        system: [
          { type: "text", text: SYSTEM_RULES, cache_control: { type: "ephemeral" } },
          { type: "text", text: itemBlock, cache_control: { type: "ephemeral" } },
        ],
        messages: [...history, { role: "user", content: user }],
      });
      const usage = usageOf(response);
      opts.meter?.record(model, usage);
      const text = response.stop_reason === "refusal" ? REFUSAL_TEXT : textOf(response) || FALLBACK_TEXT;
      return { text, system: `${SYSTEM_RULES}\n\n${itemBlock}`, user, usage };
    },
  };
}

// ---------------------------------------------------------------------------
// Student

export interface StudentTurn {
  message: string;
  /** A committed answer: a letter A–D for MC, a typed entry for SPR; null when not attempting. */
  attempt: string | null;
  /** Everything currently typed into the calculator, one Desmos LaTeX line per entry. */
  calculatorLines: string[];
  requestedHint: HintLevel;
  /** The student is satisfied and would stop here. */
  done: boolean;
}

export interface StudentInput {
  item: Item;
  persona: Persona;
  transcript: TutorTurn[];
  lastAttempt?: { response: string; result: GradeResult };
  /** Tutor replies received so far. */
  hintsReceived: number;
}

export interface StudentSimulator {
  model: string;
  next(input: StudentInput): Promise<{ turn: StudentTurn; usage: TokenUsage }>;
}

const STUDENT_SCHEMA = {
  type: "object",
  properties: {
    message: { type: "string" },
    attempt: { type: ["string", "null"] },
    calculatorLines: { type: "array", items: { type: "string" } },
    requestedHint: { type: "string", enum: [...HINT_LEVELS] },
    done: { type: "boolean" },
  },
  required: ["message", "attempt", "calculatorLines", "requestedHint", "done"],
  additionalProperties: false,
} as const;

function validateStudentTurn(v: unknown): StudentTurn {
  const o = expectObject(v, "turn");
  const hint = expectString(o.requestedHint, "requestedHint");
  if (!(HINT_LEVELS as readonly string[]).includes(hint)) throw new Error(`requestedHint must be one of ${HINT_LEVELS.join(", ")}`);
  return {
    message: expectString(o.message, "message"),
    attempt: o.attempt === null || o.attempt === undefined ? null : expectString(o.attempt, "attempt").trim(),
    calculatorLines: expectStringArray(o.calculatorLines, "calculatorLines"),
    requestedHint: hint as HintLevel,
    done: expectBoolean(o.done, "done"),
  };
}

function studentSystem(p: Persona): string {
  return `You are playing a student in a simulated SAT Math tutoring session. Stay in character for the whole session.

Student profile:
- Name: ${p.name}. Skill level: ${p.skillLevel}.
- Misconception you hold (act on it, do not announce it): ${p.misconception}
- Desmos habit: ${p.desmosHabit}
- How you behave: ${p.script}
- Calculator angle mode: ${p.degreeMode ? "degrees" : "radians"}.
- You want about ${p.hintsBeforeAttempt} hint(s) before you commit a first answer.

Rules:
- You do not know the answer key. Work from the question, your own (flawed) reasoning and the tutor's replies.
- Your first committed attempt must reflect your misconception. Fix it only when the tutor has pointed at the actual mistake.
- Write one or two sentences per message, in a teenager's plain voice. No markdown.
- Ask for hints in order: "nudge", then "strategy", then "worked-step"; ask for "full-solution" only after you have committed an attempt.
- calculatorLines is everything in your calculator right now, one Desmos line per entry in Desmos LaTeX (e.g. "y=x^{2}-6x+11"). Keep earlier lines unless you deliberately delete them.
- attempt is null unless you are committing an answer this turn: a single letter A–D for multiple choice, or the exact entry you would type in the box for a typed answer.
- Set done to true once you have the right answer and understand why, or once you have given up.

Reply with JSON only, matching the schema.`;
}

function describeItemForStudent(item: Item): string {
  return [
    `Question: ${item.stem}`,
    item.format === "mc" ? `Choices: ${item.choices.map((c, i) => `${"ABCD"[i]}. ${c}`).join("  ")}` : "Format: type your answer in the box (fraction, integer or decimal; at most 5 characters, 6 with a minus sign).",
  ].join("\n");
}

export function createStudentSimulator(client: TraceClient, opts: { model?: string; meter?: UsageMeter } = {}): StudentSimulator {
  const model = opts.model ?? STUDENT_MODEL;
  return {
    model,
    async next(input) {
      const transcript = input.transcript.length
        ? input.transcript.map((t) => `${t.role === "student" ? "You" : "Tutor"}: ${t.text}`).join("\n")
        : "(no messages yet; you speak first)";
      const graded = input.lastAttempt
        ? `Your last attempt "${input.lastAttempt.response}" was graded ${input.lastAttempt.result.status}${input.lastAttempt.result.status === "invalid" ? ` (${input.lastAttempt.result.reason})` : ""}.`
        : "You have not committed an attempt yet.";
      const r = await structured(client, {
        model,
        system: studentSystem(input.persona),
        messages: [{ role: "user", content: `${describeItemForStudent(input.item)}\n\nSession so far:\n${transcript}\n\n${graded} Hints received: ${input.hintsReceived}.\n\nWrite your next message.` }],
        schema: STUDENT_SCHEMA as unknown as Record<string, unknown>,
        validate: validateStudentTurn,
        effort: "low",
        maxTokens: 2048,
        meter: opts.meter,
      });
      return { turn: r.value, usage: r.usage };
    },
  };
}

// ---------------------------------------------------------------------------
// The loop

export interface SimulateOptions {
  item: Item;
  trace: SolutionTrace;
  persona: Persona;
  tutor: TraceTutor;
  student: StudentSimulator;
  /** Student+tutor exchanges; 2–4 gives the 4–8 turns the plan asks for. */
  minExchanges?: number;
  maxExchanges?: number;
  seq?: number;
  now?: () => string;
}

export function snapshotFromLines(lines: string[], degreeMode: boolean): CalculatorSnapshot {
  return { degreeMode, expressions: lines.map((latex, i) => ({ id: `s${i + 1}`, line: i + 1, kind: "expression", latex })) };
}

export function summarizeCalculator(snap: CalculatorSnapshot): string {
  const lines = snap.expressions.map((e) => e.latex ?? e.text ?? "").filter(Boolean);
  return `${snap.degreeMode ? "deg" : "rad"}; ${lines.length ? lines.map((l, i) => `${i + 1}: ${l}`).join(" | ") : "(empty)"}`;
}

/** The item the tutor coaches from: the accepted trace stands in for the stored Desmos route. */
export function itemWithTrace(item: Item, trace: SolutionTrace): Item {
  return { ...item, desmos: { lines: trace.desmosLines, read: trace.readOff, verified: trace.verifiedInDesmos } };
}

export async function simulateDialogue(opts: SimulateOptions): Promise<Dialogue> {
  const { item, trace, persona, tutor, student } = opts;
  const minExchanges = Math.max(1, opts.minExchanges ?? 2);
  const maxExchanges = Math.max(minExchanges, opts.maxExchanges ?? 4);
  const tutorItem = itemWithTrace(item, trace);

  const messages: ChatMessage[] = [];
  const turns: TurnMeta[] = [];
  const history: TutorTurn[] = [];
  let usage: TokenUsage = emptyUsage();
  let lastAttempt: TutorClientRequest["lastAttempt"];
  let graded = false; // a correct or incorrect attempt has been made

  for (let k = 0; k < maxExchanges; k++) {
    const { turn, usage: su } = await student.next({
      item,
      persona,
      transcript: history,
      lastAttempt: lastAttempt ? { response: String(lastAttempt.response), result: lastAttempt.result } : undefined,
      hintsReceived: k,
    });
    usage = addUsage(usage, su);

    let attemptMeta: TurnMeta["attempt"];
    if (turn.attempt !== null && turn.attempt !== "") {
      const response = toGradeResponse(item, turn.attempt);
      const result = gradeItem(item, response);
      lastAttempt = { response, result };
      attemptMeta = { response, status: result.status };
      if (result.status !== "invalid") graded = true;
    }
    const attemptPrecededStudent = graded && !attemptMeta; // graded before this message was written
    const calculator = snapshotFromLines(turn.calculatorLines, persona.degreeMode);

    const request = clampRequest({
      itemId: item.id,
      message: turn.message,
      hintLevel: turn.requestedHint,
      calculator,
      history: [...history],
      lastAttempt,
      showMe: false,
    });
    const reply = await tutor.reply({ ...request, item: tutorItem });
    usage = addUsage(usage, reply.usage);

    if (k === 0) {
      messages.push({ role: "system", content: reply.system });
      turns.push({ index: 0, role: "system", attemptPreceded: false });
    }
    const calcSummary = summarizeCalculator(calculator);
    messages.push({ role: "user", content: reply.user });
    turns.push({ index: messages.length - 1, role: "user", calculator: calcSummary, attemptPreceded: attemptPrecededStudent, ...(attemptMeta && { attempt: attemptMeta }) });
    messages.push({ role: "assistant", content: reply.text });
    turns.push({ index: messages.length - 1, role: "assistant", hintLevel: request.hintLevel, requestedHintLevel: turn.requestedHint, calculator: calcSummary, attemptPreceded: graded });

    history.push({ role: "student", text: turn.message }, { role: "tutor", text: reply.text });
    if (turn.done && k + 1 >= minExchanges) break;
  }

  return {
    id: `${item.id}#d${opts.seq ?? 1}`,
    itemId: item.id,
    traceId: trace.id,
    tutorModel: tutor.model,
    studentModel: student.model,
    createdAt: (opts.now ?? (() => new Date().toISOString()))(),
    persona: summarizePersona(persona),
    messages,
    turns,
    labels: {
      answerRevealedEarly: answerRevealedEarly(item, messages, turns),
      reproducibleInBluebook: false,
      judgeScore: 0,
      judgeNotes: "",
    },
    status: "candidate",
    usage,
  };
}
