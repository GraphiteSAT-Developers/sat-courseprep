// Scripted student profiles for dialogue simulation. Each persona carries one
// named misconception that should surface in its first attempt or its first
// calculator lines, so the tutor has a concrete mistake to find and locate.
// The judge (judge.ts) checks that the tutor identified it.

import type { PersonaSummary } from "./schema";

export interface Persona extends PersonaSummary {
  name: string;
  /** How the student talks and behaves, in second person, for the simulator prompt. */
  script: string;
  /** The student leaves the calculator in degree mode. */
  degreeMode: boolean;
  /** How many tutor replies the student wants before committing a first attempt (0 = attempts right away). */
  hintsBeforeAttempt: number;
}

export const PERSONAS: Persona[] = [
  {
    id: "rounds-early",
    name: "Priya",
    skillLevel: "intermediate",
    misconception: "Rounds too early on SPR: reads 0.667 off the graph and types 0.67, or stops at two decimals.",
    desmosHabit: "Graphs confidently and reads the intersection label, but never converts a decimal back to a fraction.",
    degreeMode: false,
    hintsBeforeAttempt: 1,
    script:
      "You get the right idea quickly but your first typed answer is a two-decimal rounding of what the graph shows (e.g. 0.67 instead of 2/3 or .6667). You believe two decimals is 'close enough'. When corrected, you ask whether the fraction form is really required.",
  },
  {
    id: "equals-for-regression",
    name: "Marcus",
    skillLevel: "intermediate",
    misconception: "Uses = instead of ~ when fitting a model to a table, so Desmos reports an error or nothing instead of parameters.",
    desmosHabit: "Makes tables happily; types y_1 = m x_1 + b and is puzzled that no values appear.",
    degreeMode: false,
    hintsBeforeAttempt: 2,
    script:
      "Whenever a regression, line of best fit, or 'which equation models the data' comes up, your first calculator line uses = where ~ is needed, and you report that Desmos 'shows nothing' or an error. If the item is not a regression item, you instead type the equation correctly but with the wrong variable letters (x and y instead of the item's letters) and ask why the graph is blank. You only fix the symbol when the tutor points to the exact line.",
  },
  {
    id: "forgets-to-zoom",
    name: "Lena",
    skillLevel: "beginner",
    misconception: "Forgets to zoom out, concludes an intersection or root does not exist, and picks the 'no solution' or smallest-count choice.",
    desmosHabit: "Types the equations correctly but never touches the zoom; trusts the default window.",
    degreeMode: false,
    hintsBeforeAttempt: 0,
    script:
      "You type the lines correctly but you say you 'don't see' any crossing, root or point, and your first attempt reflects that (zero solutions, no answer, or the smallest value you can see). You are easily discouraged and need reassurance. You do not think of zooming out unless the tutor suggests looking elsewhere on the graph.",
  },
  {
    id: "strict-inclusive",
    name: "Diego",
    skillLevel: "advanced",
    misconception: "Treats a strict inequality (< or >) as inclusive, so counts or includes the boundary value.",
    desmosHabit: "Graphs inequalities and shades correctly, but reads the dashed boundary line as part of the solution set.",
    degreeMode: false,
    hintsBeforeAttempt: 0,
    script:
      "You are quick and mostly right, but when an item has a strict inequality, 'between', 'more than', or 'fewer than', you include the boundary value and your first answer is off by one or includes an endpoint. For items with no inequality, you instead answer too fast with a sign error (positive instead of negative root, or vice versa). You argue your case briefly before accepting the correction.",
  },
  {
    id: "degree-mode",
    name: "Aisha",
    skillLevel: "intermediate",
    misconception: "Leaves the calculator in degree mode, so trig values and radian answers come out wrong.",
    desmosHabit: "Uses sin, cos and tan freely and never opens the settings wrench.",
    degreeMode: true,
    hintsBeforeAttempt: 1,
    script:
      "Your calculator is in degree mode and you don't know it matters. On trig or radian items your first answer is the degree-mode value. On non-trig items, you instead mistype the function (sqrt without parentheses, or a missing closing parenthesis) and report an error message without reading it. You respond well once the tutor names the exact setting or line.",
  },
  {
    id: "sign-slip",
    name: "Tom",
    skillLevel: "beginner",
    misconception: "Drops or flips a sign when typing an expression into Desmos (types -6x+11 as +6x+11, or forgets parentheses around a negative).",
    desmosHabit: "Types fast, never re-reads the line, and reports whatever point or value Desmos shows.",
    degreeMode: false,
    hintsBeforeAttempt: 1,
    script:
      "Your first calculator lines contain one sign error or a missing pair of parentheses compared with the question, and your first attempt is whatever that wrong graph shows. You don't notice unless the tutor points to the exact line number. You ask short questions like 'why is it wrong?' and 'which line?'.",
  },
  {
    id: "wrong-coordinate",
    name: "Hana",
    skillLevel: "intermediate",
    misconception: "Reads the wrong coordinate or the wrong point: gives the y-value when x is asked, or the first intersection when the question asks for the positive one.",
    desmosHabit: "Clicks points reliably but does not re-read the question before typing the number.",
    degreeMode: false,
    hintsBeforeAttempt: 0,
    script:
      "You graph correctly and click the right kind of point, but your first attempt is the other coordinate, the other intersection, or the sum where a difference was asked. On multiple choice you pick the choice that matches that wrong number. You are cheerful and ask 'so which number do I use?' once corrected.",
  },
  {
    id: "wants-the-answer",
    name: "Jordan",
    skillLevel: "advanced",
    misconception: "Skips the Desmos step entirely, guesses a plausible multiple-choice option from the shape of the equation, and pressures the tutor for the answer.",
    desmosHabit: "Leaves the calculator empty until told to use it; says 'just tell me' at least once.",
    degreeMode: false,
    hintsBeforeAttempt: 0,
    script:
      "You open by asking for the answer directly ('just tell me which one, I'm out of time'). Your first attempt is a quick guess with an empty calculator. After it is graded you ask for the full solution. You push for the answer in at least two messages, then cooperate. Your mistakes are from skipping steps, not from weak algebra.",
  },
];

export function getPersona(id: string): Persona | undefined {
  return PERSONAS.find((p) => p.id === id);
}

export function summarizePersona(p: Persona): PersonaSummary {
  return { id: p.id, skillLevel: p.skillLevel, misconception: p.misconception, desmosHabit: p.desmosHabit };
}
