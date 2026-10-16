// Prompt assembly shared by every model-backed TutorProvider (Anthropic,
// OpenAI-compatible endpoint). Keeping it in one place means the fine-tuned
// tutor is trained and served on exactly the prompt the Sonnet baseline uses,
// so the eval comparison in docs/fine-tuning-plan.md is like for like.
//
// No vendor imports here. No "server-only" either: this module only formats
// text, and the providers that import it are already server-only.

import { getTechnique } from "@/content/techniques";
import type { HintLevel, TutorContext } from "./types";

// Frozen rules. Nothing per-request goes in here so the prompt cache holds.
export const SYSTEM_RULES = `You are a math tutor for students preparing for the digital SAT, aiming for an 800. The course teaches the Desmos graphing calculator built into the test first and by-hand methods second.

Rules you must follow:
- Never state the final answer unless the hint level is "full-solution".
- Match the hint level exactly: "nudge" is one question or observation that points at the idea; "strategy" names the approach (which Desmos move or which algebra) without doing it; "worked-step" does the first step only; "full-solution" gives the complete Desmos route and the by-hand route.
- Use only the Desmos lines given in the item. Do not invent Desmos syntax or features. If the item's Desmos lines are marked unverified, describe the approach but tell the student to check the graph carefully.
- When the student's calculator has an error or a wrong line, point to it by line number and say what is wrong, but let the student fix it.
- Students type answers under Bluebook rules: fractions or decimals that fill the box, no rounding early.
- Be brief: two to five sentences. Plain language. No headings, no lists unless listing steps in a full solution.
- Stay on SAT math. If asked about anything else, say you can only help with the math.`;

export const HINT_INSTRUCTIONS: Record<HintLevel, string> = {
  nudge: "Give a nudge only.",
  strategy: "Name the strategy only. Do not carry it out.",
  "worked-step": "Do the first step only, then stop.",
  "full-solution": "Give the full solution: the Desmos route, then the by-hand route, then the final answer in a form Bluebook accepts.",
};

/** Neutral text when the model returns nothing usable (empty reply, transport error). */
export const FALLBACK_TEXT = "Let's look at this together. What does the question ask you to find?";

/** Neutral text when the model refuses or goes off topic. */
export const REFUSAL_TEXT = "I can only help with the math on this question. What have you tried so far?";

/** The item block: question, keys, routes and techniques. Cacheable per item. */
export function describeItem(ctx: TutorContext): string {
  const { item } = ctx;
  const techniques = item.techniques
    .map((id) => getTechnique(id))
    .filter((t) => t !== undefined)
    .map((t) => `- ${t.id} ${t.name}: ${t.summary}`)
    .join("\n");
  const answer =
    item.format === "mc"
      ? `Correct choice: ${"ABCD"[item.answerIndex]} (${item.choices[item.answerIndex]})`
      : `Accepted answers: ${item.answers.map((a) => (a.den === 1 ? `${a.num}` : `${a.num}/${a.den}`)).join(", ")}`;
  return [
    `Question: ${item.stem}`,
    item.format === "mc" ? `Choices: ${item.choices.map((c, i) => `${"ABCD"[i]}. ${c}`).join("  ")}` : "Format: student-produced response (typed answer)",
    answer,
    `Default route: ${item.route}`,
    item.desmos
      ? `Desmos route (${item.desmos.verified ? "verified" : "UNVERIFIED"}):\n${item.desmos.lines.map((l, i) => `  line ${i + 1}: ${l}`).join("\n")}\n  then: ${item.desmos.read}`
      : "Desmos route: none",
    `By-hand route: ${item.byHand}`,
    techniques ? `Relevant techniques:\n${techniques}` : "",
  ]
    .filter(Boolean)
    .join("\n");
}

/** The per-turn block: calculator state, last graded attempt, hint level. */
export function describeState(ctx: TutorContext): string {
  const calc = ctx.calculator.expressions.length
    ? ctx.calculator.expressions
        .map((e) => {
          const body = e.kind === "table" ? `table ${JSON.stringify(e.columns)}` : (e.latex ?? e.text ?? "");
          const extra = [e.error && `ERROR: ${e.error}`, e.value !== undefined && `= ${JSON.stringify(e.value)}`].filter(Boolean).join(" ");
          return `  line ${e.line}: ${body}${extra ? `   ${extra}` : ""}`;
        })
        .join("\n")
    : "  (empty)";
  const attempt = ctx.lastAttempt
    ? `Last graded attempt: ${JSON.stringify(ctx.lastAttempt.response)} was ${ctx.lastAttempt.result.status}${
        ctx.lastAttempt.result.status === "incorrect" && ctx.lastAttempt.result.hint ? ` (${ctx.lastAttempt.result.hint})` : ""
      }`
    : "No graded attempt yet.";
  return `Student's calculator (${ctx.calculator.degreeMode ? "degrees" : "radians"}):\n${calc}\n${attempt}\nHint level: ${ctx.hintLevel}. ${HINT_INSTRUCTIONS[ctx.hintLevel]}`;
}

/** The final user turn: state block plus the student's message. */
export function describeTurn(ctx: TutorContext): string {
  return `${describeState(ctx)}\n\nStudent says: ${ctx.message}`;
}

/**
 * Show-me lines come from the item, never from the model, so the student only
 * ever receives Desmos steps that the verification service has run. Every
 * provider applies this rule.
 */
export function showMeLines(ctx: TutorContext): { latex: string }[] | undefined {
  return ctx.showMe && ctx.item.desmos?.verified ? ctx.item.desmos.lines.map((latex) => ({ latex })) : undefined;
}
