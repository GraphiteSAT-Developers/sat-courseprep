import "server-only";
import type { Item } from "./types";

// Placeholder items written for the scaffold so the practice page has something
// to show. All original. Replace with the real bank once the item pipeline exists.
// Never paste College Board items here (see HANDOFF.md, "College Board content").
const items: Item[] = [
  {
    id: "sample-tangent-system",
    format: "mc",
    domain: "algebra",
    skill: "Nonlinear equations in one variable and systems of equations in two variables",
    difficulty: "medium",
    stem: "How many solutions does the system $y = x^2 - 6x + 11$ and $y = 2x - 5$ have?",
    choices: ["Zero", "Exactly one", "Exactly two", "Infinitely many"],
    answerIndex: 1,
    techniques: ["T2"],
    route: "desmos-primary",
    desmos: {
      lines: ["y=x^2-6x+11", "y=2x-5"],
      read: "The line touches the parabola at one point, (4, 3). Zoom in to confirm it doesn't cross twice.",
      verified: false,
    },
    byHand: "Set equal: x^2 - 8x + 16 = 0, so (x - 4)^2 = 0. The discriminant is 0, so there is exactly one solution.",
    provenance: { author: "scaffold", created: "2026-10-15" },
  },
  {
    id: "sample-positive-root",
    format: "spr",
    domain: "advanced-math",
    skill: "Nonlinear equations in one variable and systems of equations in two variables",
    difficulty: "medium",
    stem: "What is the positive solution to $6x^2 - x - 2 = 0$?",
    answers: [{ num: 2, den: 3 }],
    techniques: ["T1", "T11"],
    route: "desmos-primary",
    desmos: {
      lines: ["y=6x^2-x-2"],
      read: "Click the positive x-intercept: 0.667. Enter 2/3, or a full-width decimal like .6667. 0.67 is marked wrong.",
      verified: false,
    },
    byHand: "Factor: (3x - 2)(2x + 1) = 0, so x = 2/3 or x = -1/2.",
    provenance: { author: "scaffold", created: "2026-10-15" },
  },
  {
    id: "sample-tilde-constants",
    format: "spr",
    domain: "advanced-math",
    skill: "Equivalent expressions",
    difficulty: "hard",
    stem: "For all values of $x$, $(2x + c)(x - 3) = 2x^2 + bx - 15$, where $b$ and $c$ are constants. What is the value of $b$?",
    answers: [{ num: -1, den: 1 }],
    techniques: ["T6"],
    route: "either",
    desmos: {
      lines: ["x_1=[1,2,3]", "(2x_1+c)(x_1-3)\\sim2x_1^2+bx_1-15"],
      read: "Read the fitted parameters: c = 5 and b = -1.",
      verified: false,
    },
    byHand: "Match constant terms: -3c = -15, so c = 5. Match x terms: -6 + c = b, so b = -1.",
    provenance: { author: "scaffold", created: "2026-10-15" },
  },
];

export function listItems(): Item[] {
  return items;
}

export function getItem(id: string): Item | undefined {
  return items.find((item) => item.id === id);
}
