// Shapes for the trace-generation pipeline (decision 2026-10-15: the live
// tutor will be an open-weight model fine-tuned on verified tutoring
// dialogues; Sonnet is the solver, dialogue generator and judge).
//
// Three JSONL files live in data/traces/ (see data/traces/README.md):
//   solutions.jsonl  one SolutionTrace per line
//   dialogues.jsonl  one Dialogue per line
//   sft.jsonl        one SftLine per line, accepted dialogues only
//
// Everything here is plain JSON. No vendor types leak into the files.

import type { HintLevel } from "@/lib/tutor/types";

// ---------------------------------------------------------------------------
// Solution traces

export type TraceStatus = "candidate" | "verified" | "rejected";

export interface TokenUsage {
  inputTokens: number;
  outputTokens: number;
  cacheReadTokens: number;
  cacheWriteTokens: number;
}

export interface SolutionTrace {
  /** Stable id: `${itemId}#s${n}`. */
  id: string;
  itemId: string;
  model: string;
  createdAt: string;
  /** The Desmos lines the solver proposes, in Desmos LaTeX, in typing order. */
  desmosLines: string[];
  /** What to read off the graph after typing the lines. */
  readOff: string;
  /** Short reasoning summary (not the model's full chain of thought). */
  reasoning: string;
  /** In the item's answer format: a choice letter A–D for MC, a Bluebook entry for SPR. */
  finalAnswer: string;
  /** Computed by the deterministic grader (lib/grading). Never the model's own claim. */
  agreesWithKey: boolean;
  /** False until the headless Desmos service has run desmosLines. */
  verifiedInDesmos: boolean;
  /** "candidate": key agrees, Desmos not yet run. "verified": both. "rejected": wrong after retries. */
  status: TraceStatus;
  /** How many solver calls it took (1 + retries). */
  attempts: number;
  /** Grader feedback sent back on each retry, in order. */
  graderFeedback: string[];
  usage: TokenUsage;
}

/** A trace a dialogue may be built on: the key agrees, whether or not Desmos has run. */
export function isAcceptedTrace(t: SolutionTrace): boolean {
  return t.agreesWithKey && t.status !== "rejected";
}

// ---------------------------------------------------------------------------
// Dialogues

export type ChatRole = "system" | "user" | "assistant";

/** The neutral chat format open-weight fine-tuning tools accept. Only these two keys. */
export interface ChatMessage {
  role: ChatRole;
  content: string;
}

export type DialogueStatus = "candidate" | "accepted" | "rejected";

export interface PersonaSummary {
  id: string;
  skillLevel: "beginner" | "intermediate" | "advanced";
  misconception: string;
  desmosHabit: string;
}

/** Per-turn metadata, parallel to `messages` by index. Not part of the SFT line. */
export interface TurnMeta {
  /** Index into Dialogue.messages. */
  index: number;
  role: ChatRole;
  /** Tutor turns: the hint level the tutor was asked for, after the site's clamp. */
  hintLevel?: HintLevel;
  /** Tutor turns: what the student asked for before the clamp. */
  requestedHintLevel?: HintLevel;
  /** One-line summary of the student's calculator at this turn. */
  calculator?: string;
  /** True when a graded (correct or incorrect) attempt precedes this turn. */
  attemptPreceded: boolean;
  /** Student turns: the attempt submitted with this message, if any, and how the grader scored it. */
  attempt?: { response: string | number; status: "correct" | "incorrect" | "invalid" };
}

export interface DialogueLabels {
  /** Deterministic: the key appeared in a tutor turn before any graded attempt. */
  answerRevealedEarly: boolean;
  /** From the judge: every Desmos instruction is one the student could type in Bluebook. */
  reproducibleInBluebook: boolean;
  /** From the judge, 0–5 on the plan's rubric. */
  judgeScore: number;
  judgeNotes: string;
  judgeModel?: string;
}

export interface Dialogue {
  /** Stable id: `${itemId}#d${n}`. */
  id: string;
  itemId: string;
  traceId: string;
  tutorModel: string;
  studentModel: string;
  createdAt: string;
  persona: PersonaSummary;
  messages: ChatMessage[];
  turns: TurnMeta[];
  labels: DialogueLabels;
  status: DialogueStatus;
  usage: TokenUsage;
}

// ---------------------------------------------------------------------------
// SFT export

export interface SftLine {
  messages: ChatMessage[];
  metadata: {
    dialogueId: string;
    itemId: string;
    traceId: string;
    persona: string;
    judgeScore: number;
    tutorModel: string;
  };
}

// ---------------------------------------------------------------------------
// Judge output

export interface JudgeVerdict {
  score: number;
  earlyReveal: boolean;
  mistakeIdentified: boolean;
  mistakeLocated: boolean;
  reproducibleInBluebook: boolean;
  toneOk: boolean;
  notes: string;
}

// ---------------------------------------------------------------------------
// Parsing (round-trip from JSONL). Light structural checks: enough to catch a
// hand-edited or truncated line, not a full schema validator.

function fail(what: string, msg: string): never {
  throw new Error(`Invalid ${what}: ${msg}`);
}

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function requireKeys(what: string, v: Record<string, unknown>, keys: string[]) {
  for (const k of keys) if (!(k in v)) fail(what, `missing "${k}"`);
}

export function parseTokenUsage(v: unknown): TokenUsage {
  if (!isRecord(v)) fail("usage", "not an object");
  requireKeys("usage", v, ["inputTokens", "outputTokens", "cacheReadTokens", "cacheWriteTokens"]);
  return v as unknown as TokenUsage;
}

export function parseSolutionTrace(v: unknown): SolutionTrace {
  if (!isRecord(v)) fail("SolutionTrace", "not an object");
  requireKeys("SolutionTrace", v, [
    "id", "itemId", "model", "createdAt", "desmosLines", "readOff", "reasoning", "finalAnswer",
    "agreesWithKey", "verifiedInDesmos", "status", "attempts", "graderFeedback", "usage",
  ]);
  if (!Array.isArray(v.desmosLines)) fail("SolutionTrace", "desmosLines not an array");
  if (!["candidate", "verified", "rejected"].includes(String(v.status))) fail("SolutionTrace", `bad status ${String(v.status)}`);
  if (typeof v.agreesWithKey !== "boolean") fail("SolutionTrace", "agreesWithKey not boolean");
  parseTokenUsage(v.usage);
  return v as unknown as SolutionTrace;
}

export function parseChatMessage(v: unknown): ChatMessage {
  if (!isRecord(v)) fail("ChatMessage", "not an object");
  if (!["system", "user", "assistant"].includes(String(v.role))) fail("ChatMessage", `bad role ${String(v.role)}`);
  if (typeof v.content !== "string") fail("ChatMessage", "content not a string");
  const extra = Object.keys(v).filter((k) => k !== "role" && k !== "content");
  if (extra.length) fail("ChatMessage", `unexpected keys ${extra.join(", ")}`);
  return { role: v.role as ChatRole, content: v.content };
}

export function parseDialogue(v: unknown): Dialogue {
  if (!isRecord(v)) fail("Dialogue", "not an object");
  requireKeys("Dialogue", v, [
    "id", "itemId", "traceId", "tutorModel", "studentModel", "createdAt", "persona", "messages", "turns", "labels", "status", "usage",
  ]);
  if (!Array.isArray(v.messages)) fail("Dialogue", "messages not an array");
  v.messages.forEach(parseChatMessage);
  if (!Array.isArray(v.turns) || v.turns.length !== v.messages.length) fail("Dialogue", "turns must parallel messages");
  if (!["candidate", "accepted", "rejected"].includes(String(v.status))) fail("Dialogue", `bad status ${String(v.status)}`);
  const labels = v.labels;
  if (!isRecord(labels)) fail("Dialogue", "labels not an object");
  requireKeys("Dialogue.labels", labels, ["answerRevealedEarly", "reproducibleInBluebook", "judgeScore", "judgeNotes"]);
  if (typeof labels.judgeScore !== "number" || labels.judgeScore < 0 || labels.judgeScore > 5) fail("Dialogue", "judgeScore out of range");
  parseTokenUsage(v.usage);
  return v as unknown as Dialogue;
}

export function parseSftLine(v: unknown): SftLine {
  if (!isRecord(v)) fail("SftLine", "not an object");
  requireKeys("SftLine", v, ["messages", "metadata"]);
  if (!Array.isArray(v.messages)) fail("SftLine", "messages not an array");
  v.messages.forEach(parseChatMessage);
  if (!isRecord(v.metadata)) fail("SftLine", "metadata not an object");
  return v as unknown as SftLine;
}

/** Parse a JSONL file body with a per-line parser; blank lines are skipped. */
export function parseJsonl<T>(text: string, parse: (v: unknown) => T): T[] {
  return text
    .split("\n")
    .filter((line) => line.trim() !== "")
    .map((line, i) => {
      try {
        return parse(JSON.parse(line));
      } catch (e) {
        throw new Error(`line ${i + 1}: ${(e as Error).message}`);
      }
    });
}

export function toJsonl(rows: unknown[]): string {
  return rows.length ? rows.map((r) => JSON.stringify(r)).join("\n") + "\n" : "";
}
