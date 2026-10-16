// Judge: a different model from the generator (TRACE_JUDGE_MODEL, default
// Opus) scores a dialogue 0–5 on the plan's rubric, or compares two dialogues
// in randomized order. Judges are noisy (MathTutorBench: accuracy < 0.7,
// position-sensitive), so the deterministic leak check always wins over the
// judge's own earlyReveal, and the scores should be calibrated against human
// labels before anyone trusts thresholds.

import type { Item } from "@/content/types";
import { JUDGE_MODEL, expectBoolean, expectObject, expectString, structured, type TraceClient, type UsageMeter } from "./llm";
import { keyStrings } from "./leak";
import type { Dialogue, JudgeVerdict, TokenUsage } from "./schema";

export const DEFAULT_MIN_SCORE = 4;

const RUBRIC = `Score the tutor in this SAT Math tutoring dialogue. The student is a simulated learner with a scripted misconception. Rubric (one point each, 0–5 total):
1. No early reveal: the tutor never states the final answer, the correct choice, or an accepted typed entry before the student has committed a graded attempt. (If it does, this point is lost and earlyReveal is true.)
2. Mistake identified: the tutor names the student's actual error (the misconception listed below, or whatever the student actually did wrong), not a generic one.
3. Mistake located: the tutor points at where it happened (calculator line number, the step, the rounding, the setting), so the student can fix it themselves.
4. Reproducible in Bluebook: every Desmos instruction is something a student could type or click in the College Board build of Desmos as-is (real syntax, no invented features, correct use of ~ for regression, no unverified step presented as certain). If any instruction is not, this point is lost and reproducibleInBluebook is false.
5. Tone and hint discipline: brief, plain, encouraging, matches the requested hint level, no lecturing, no lists outside a full solution.

Judge the tutor (assistant) turns only. The user turns contain the site's state block plus the student's words.`;

const VERDICT_SCHEMA = {
  type: "object",
  properties: {
    score: { type: "integer", minimum: 0, maximum: 5 },
    earlyReveal: { type: "boolean" },
    mistakeIdentified: { type: "boolean" },
    mistakeLocated: { type: "boolean" },
    reproducibleInBluebook: { type: "boolean" },
    toneOk: { type: "boolean" },
    notes: { type: "string" },
  },
  required: ["score", "earlyReveal", "mistakeIdentified", "mistakeLocated", "reproducibleInBluebook", "toneOk", "notes"],
  additionalProperties: false,
} as const;

function validateVerdict(v: unknown): JudgeVerdict {
  const o = expectObject(v, "verdict");
  const score = o.score;
  if (typeof score !== "number" || !Number.isInteger(score) || score < 0 || score > 5) throw new Error("score must be an integer 0–5");
  return {
    score,
    earlyReveal: expectBoolean(o.earlyReveal, "earlyReveal"),
    mistakeIdentified: expectBoolean(o.mistakeIdentified, "mistakeIdentified"),
    mistakeLocated: expectBoolean(o.mistakeLocated, "mistakeLocated"),
    reproducibleInBluebook: expectBoolean(o.reproducibleInBluebook, "reproducibleInBluebook"),
    toneOk: expectBoolean(o.toneOk, "toneOk"),
    notes: expectString(o.notes, "notes"),
  };
}

function describeForJudge(item: Item, d: Dialogue): string {
  const key = item.format === "mc" ? `${"ABCD"[item.answerIndex]} (${item.choices[item.answerIndex]})` : keyStrings(item).join(", ");
  const transcript = d.messages
    .map((m, i) => {
      if (m.role === "system") return null;
      const t = d.turns[i];
      const tag = m.role === "assistant" ? `TUTOR (hint level ${t?.hintLevel ?? "?"}, ${t?.attemptPreceded ? "after" : "before"} a graded attempt)` : `STUDENT${t?.attempt ? ` [attempt ${JSON.stringify(t.attempt.response)}: ${t.attempt.status}]` : ""}`;
      return `--- ${tag} ---\n${m.content}`;
    })
    .filter(Boolean)
    .join("\n\n");
  return [
    `Question: ${item.stem}`,
    item.format === "mc" ? `Choices: ${item.choices.map((c, i) => `${"ABCD"[i]}. ${c}`).join("  ")}` : "Format: typed answer.",
    `Answer key: ${key}`,
    `Student persona: ${d.persona.skillLevel}; misconception: ${d.persona.misconception}; Desmos habit: ${d.persona.desmosHabit}`,
    `Deterministic leak check: ${d.labels.answerRevealedEarly ? "FLAGGED an early reveal" : "no early reveal found"}.`,
    `\nDialogue:\n${transcript}`,
  ].join("\n");
}

export interface JudgeOptions {
  model?: string;
  meter?: UsageMeter;
}

export async function judgeDialogue(client: TraceClient, item: Item, d: Dialogue, opts: JudgeOptions = {}): Promise<{ verdict: JudgeVerdict; usage: TokenUsage; model: string }> {
  const model = opts.model ?? JUDGE_MODEL;
  const r = await structured(client, {
    model,
    system: RUBRIC,
    messages: [{ role: "user", content: `${describeForJudge(item, d)}\n\nReturn the verdict as JSON.` }],
    schema: VERDICT_SCHEMA as unknown as Record<string, unknown>,
    validate: validateVerdict,
    effort: "high",
    maxTokens: 4096,
    meter: opts.meter,
  });
  return { verdict: r.value, usage: r.usage, model };
}

/** Fold a verdict into the dialogue's labels and decide acceptance. */
export function applyVerdict(d: Dialogue, verdict: JudgeVerdict, model: string, minScore = DEFAULT_MIN_SCORE): Dialogue {
  const labels = {
    answerRevealedEarly: d.labels.answerRevealedEarly || verdict.earlyReveal,
    reproducibleInBluebook: verdict.reproducibleInBluebook,
    judgeScore: verdict.score,
    judgeNotes: verdict.notes,
    judgeModel: model,
  };
  const accepted = !labels.answerRevealedEarly && labels.reproducibleInBluebook && verdict.score >= minScore;
  return { ...d, labels, status: accepted ? "accepted" : "rejected" };
}

// ---------------------------------------------------------------------------
// Pairwise comparison, randomized position

const COMPARE_SCHEMA = {
  type: "object",
  properties: {
    preferred: { type: "string", enum: ["first", "second", "tie"] },
    notes: { type: "string" },
  },
  required: ["preferred", "notes"],
  additionalProperties: false,
} as const;

export interface Comparison {
  /** Which of the two dialogues passed in won, in the caller's order. */
  preferred: "a" | "b" | "tie";
  /** True when the judge saw b first. Recorded so position bias can be measured. */
  swapped: boolean;
  notes: string;
  usage: TokenUsage;
  model: string;
}

export async function compareDialogues(
  client: TraceClient,
  item: Item,
  a: Dialogue,
  b: Dialogue,
  opts: JudgeOptions & { random?: () => number } = {},
): Promise<Comparison> {
  const model = opts.model ?? JUDGE_MODEL;
  const swapped = (opts.random ?? Math.random)() < 0.5;
  const [first, second] = swapped ? [b, a] : [a, b];
  const r = await structured(client, {
    model,
    system: `${RUBRIC}\n\nYou will see two dialogues on the same item. Decide which tutor did better on the rubric overall, or "tie". Do not prefer a dialogue because of its position.`,
    messages: [{ role: "user", content: `FIRST DIALOGUE\n${describeForJudge(item, first)}\n\n==========\n\nSECOND DIALOGUE\n${describeForJudge(item, second)}\n\nReturn JSON.` }],
    schema: COMPARE_SCHEMA as unknown as Record<string, unknown>,
    validate: (v) => {
      const o = expectObject(v, "comparison");
      const p = expectString(o.preferred, "preferred");
      if (!["first", "second", "tie"].includes(p)) throw new Error("preferred must be first, second or tie");
      return { preferred: p as "first" | "second" | "tie", notes: expectString(o.notes, "notes") };
    },
    effort: "high",
    maxTokens: 4096,
    meter: opts.meter,
  });
  const p = r.value.preferred;
  const preferred: Comparison["preferred"] = p === "tie" ? "tie" : (p === "first") !== swapped ? "a" : "b";
  return { preferred, swapped, notes: r.value.notes, usage: r.usage, model };
}
