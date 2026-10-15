import type { Rational } from "@/lib/grading/spr";

/** College Board's four Math domains. */
export type Domain = "algebra" | "advanced-math" | "psda" | "geometry-trig";

/** Technique IDs from research_notes/.../desmos_techniques.md (T1–T13, growing to 30–60). */
export type TechniqueId = `T${number}`;

/** Which method the course teaches first for this item. */
export type Route = "desmos-primary" | "hand-primary" | "either";

/**
 * A Desmos solution, written as the lines a student types into the calculator.
 * `verified` stays false until the headless verification service has run the
 * lines and confirmed the answer. The tutor must never show unverified steps.
 */
export interface DesmosSolution {
  lines: string[];
  /** What the student does after typing: click the intersection, read c, etc. */
  read: string;
  verified: boolean;
}

interface ItemBase {
  id: string;
  domain: Domain;
  skill: string;
  difficulty: "easy" | "medium" | "hard";
  /** Prompt text. Inline math goes between $...$ and renders with KaTeX. */
  stem: string;
  techniques: TechniqueId[];
  route: Route;
  desmos?: DesmosSolution;
  byHand: string;
  /** Every item is original. Record who wrote it and when, per the College Board content rules. */
  provenance: { author: string; created: string; notes?: string };
}

export interface MultipleChoiceItem extends ItemBase {
  format: "mc";
  choices: [string, string, string, string];
  answerIndex: 0 | 1 | 2 | 3;
}

export interface SprItem extends ItemBase {
  format: "spr";
  answers: Rational[];
}

export type Item = MultipleChoiceItem | SprItem;

/** What the browser receives: no keys, no solutions. Grading and tutoring happen on the server. */
export type PublicItem =
  | Pick<MultipleChoiceItem, "id" | "domain" | "skill" | "difficulty" | "stem" | "format" | "choices">
  | Pick<SprItem, "id" | "domain" | "skill" | "difficulty" | "stem" | "format">;

export function toPublicItem(item: Item): PublicItem {
  const { id, domain, skill, difficulty, stem } = item;
  return item.format === "mc"
    ? { id, domain, skill, difficulty, stem, format: "mc", choices: item.choices }
    : { id, domain, skill, difficulty, stem, format: "spr" };
}
