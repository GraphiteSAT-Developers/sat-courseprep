import type { Domain, Route, TechniqueId } from "./types";

/**
 * One Desmos move from the technique library (T1–T13, growing to 30–60).
 *
 * Both the course lessons and the AI tutor's retrieval read this shape, so
 * every field is plain data. `desmosLines` are the lines a student would type,
 * as Desmos-accepted LaTeX (the same form `DesmosSolution.lines` uses in
 * `types.ts`), with placeholders in angle brackets where an item fills in its
 * own expression. `verified` stays false until the headless verification
 * service has run the lines in the College Board configuration.
 */
export interface Technique {
  id: TechniqueId;
  name: string;
  /** One or two sentences: what the move does and what it is for. */
  summary: string;
  domains: Domain[];
  /** College Board Question Bank skill names (research_notes/.../sat_math_format.md §2). */
  skills: string[];
  /** Phrases or structures in a question that signal this move. Used by retrieval. */
  triggerConditions: string[];
  /** Canonical lines the student types, as Desmos LaTeX. `<...>` marks an item-specific placeholder. */
  desmosLines: string[];
  /** What to click or read after typing the lines. */
  readOff: string;
  pitfalls: string[];
  byHand: {
    /** The by-hand route for the same question type. */
    method: string;
    /** When the by-hand route beats Desmos. */
    whenFaster: string;
  };
  /** Which method the course teaches first for this move. */
  defaultRoute: Route;
  /** Checks the student (or tutor) runs before trusting the Desmos answer. */
  preflight: string[];
  /**
   * Where the notes mark something contested, third-party-only, or untested in
   * the College Board build. Anything listed here is not to be taught as fact
   * until it has been checked in desmos.com/testing/collegeboard/graphing.
   */
  caveats?: string[];
  /** True once the headless service has run `desmosLines` in COLLEGE_BOARD_OPTIONS. */
  verified: false | true;
  /** URLs from the research notes that back this entry. */
  sources: string[];
}
