// The seam between the course site and the AI tutor.
//
// The site owns: items, grading, the calculator, and the guardrails below.
// The AI side owns: everything behind TutorProvider (model vendor, prompts,
// technique retrieval, the Solver/Tutor split, headless Desmos verification).
// Nothing in this file names a model vendor, so the provider can change
// (see HANDOFF.md, "Gemini under-18 terms").

import type { Item } from "@/content/types";
import type { CalculatorSnapshot } from "@/lib/desmos/snapshot";
import type { GradeResult } from "@/lib/grading/grade";

/** Staged hints, smallest first. */
export const HINT_LEVELS = ["nudge", "strategy", "worked-step", "full-solution"] as const;
export type HintLevel = (typeof HINT_LEVELS)[number];

export interface TutorTurn {
  role: "student" | "tutor";
  text: string;
}

/** What the browser sends. */
export interface TutorClientRequest {
  itemId: string;
  message: string;
  hintLevel: HintLevel;
  calculator: CalculatorSnapshot;
  history: TutorTurn[];
  /** The student's most recent graded attempt, if any. */
  lastAttempt?: { response: string | number; result: GradeResult };
  /** Student asked the tutor to fill in the calculator ("show me" mode). */
  showMe?: boolean;
}

/** What the provider receives: the client request plus the full item, keys included. */
export interface TutorContext extends TutorClientRequest {
  item: Item;
}

export interface TutorReply {
  text: string;
  /** Expressions to load into the student's calculator. Only allowed in show-me mode. */
  showMe?: { latex: string }[];
}

export interface TutorProvider {
  reply(ctx: TutorContext): Promise<TutorReply>;
}
