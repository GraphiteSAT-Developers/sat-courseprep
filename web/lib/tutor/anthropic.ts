import "server-only";
import Anthropic from "@anthropic-ai/sdk";
import { FALLBACK_TEXT, REFUSAL_TEXT, SYSTEM_RULES, describeItem, describeTurn, showMeLines } from "./prompt";
import type { TutorContext, TutorProvider, TutorReply } from "./types";

// Tutor provider on Anthropic's API. Decision 2026-10-15: Sonnet is the
// solver, dialogue generator and judge, and serves as the live tutor until the
// fine-tuned open-weight model (see ./openai-compatible.ts and
// docs/fine-tuning-plan.md) matches it on the evals. Pin the ID and change it
// on purpose; run the evals before any model swap.
export const TUTOR_MODEL = process.env.TUTOR_MODEL ?? "claude-sonnet-5-5";

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
        messages: [...history, { role: "user", content: describeTurn(ctx) }],
      });

      if (response.stop_reason === "refusal") {
        return { text: REFUSAL_TEXT };
      }
      const text = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("")
        .trim();

      return { text: text || FALLBACK_TEXT, showMe: showMeLines(ctx) };
    },
  };
}
