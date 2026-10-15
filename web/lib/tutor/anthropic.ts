import "server-only";
import Anthropic from "@anthropic-ai/sdk";
import { getTechnique } from "@/content/techniques";
import type { HintLevel, TutorContext, TutorProvider, TutorReply } from "./types";

// Tutor provider on Anthropic's API. Decision 2026-10-15: Sonnet is the live
// tutoring model (see HANDOFF.md). Pin the ID and change it on purpose; run
// the evals before any model swap.
export const TUTOR_MODEL = process.env.TUTOR_MODEL ?? "claude-sonnet-5-5";

// Frozen rules. Nothing per-request goes in here so the prompt cache holds.
const SYSTEM_RULES = `You are a math tutor for students preparing for the digital SAT, aiming for an 800. The course teaches the Desmos graphing calculator built into the test first and by-hand methods second.

Rules you must follow:
- Never state the final answer unless the hint level is "full-solution".
- Match the hint level exactly: "nudge" is one question or observation that points at the idea; "strategy" names the approach (which Desmos move or which algebra) without doing it; "worked-step" does the first step only; "full-solution" gives the complete Desmos route and the by-hand route.
- Use only the Desmos lines given in the item. Do not invent Desmos syntax or features. If the item's Desmos lines are marked unverified, describe the approach but tell the student to check the graph carefully.
- When the student's calculator has an error or a wrong line, point to it by line number and say what is wrong, but let the student fix it.
- Students type answers under Bluebook rules: fractions or decimals that fill the box, no rounding early.
- Be brief: two to five sentences. Plain language. No headings, no lists unless listing steps in a full solution.
- Stay on SAT math. If asked about anything else, say you can only help with the math.`;

const HINT_INSTRUCTIONS: Record<HintLevel, string> = {
  nudge: "Give a nudge only.",
  strategy: "Name the strategy only. Do not carry it out.",
  "worked-step": "Do the first step only, then stop.",
  "full-solution": "Give the full solution: the Desmos route, then the by-hand route, then the final answer in a form Bluebook accepts.",
};

function describeItem(ctx: TutorContext): string {
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

function describeState(ctx: TutorContext): string {
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

export function createAnthropicProvider(client = new Anthropic()): TutorProvider {
  return {
    async reply(ctx: TutorContext): Promise<TutorReply> {
      const history: Anthropic.MessageParam[] = ctx.history.map((t) => ({
        role: t.role === "student" ? "user" : "assistant",
        content: t.text,
      }));
      const response = await client.messages.create({
        model: TUTOR_MODEL,
        max_tokens: 2048,
        thinking: { type: "adaptive" },
        output_config: { effort: "low" },
        system: [
          { type: "text", text: SYSTEM_RULES, cache_control: { type: "ephemeral" } },
          { type: "text", text: describeItem(ctx), cache_control: { type: "ephemeral" } },
        ],
        messages: [...history, { role: "user", content: `${describeState(ctx)}\n\nStudent says: ${ctx.message}` }],
      });

      if (response.stop_reason === "refusal") {
        return { text: "I can only help with the math on this question. What have you tried so far?" };
      }
      const text = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("")
        .trim();

      // Show-me lines come from the item, never from the model, so the student
      // only ever receives Desmos steps that the verification service has run.
      const showMe =
        ctx.showMe && ctx.item.desmos?.verified ? ctx.item.desmos.lines.map((latex) => ({ latex })) : undefined;
      return { text: text || "Let's look at this together. What does the question ask you to find?", showMe };
    },
  };
}
