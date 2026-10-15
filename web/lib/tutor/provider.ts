import "server-only";
import { createAnthropicProvider } from "./anthropic";
import type { TutorContext, TutorProvider, TutorReply } from "./types";

/**
 * Placeholder used when no ANTHROPIC_API_KEY is set. It answers from the
 * item's stored by-hand route and Desmos lines, so the UI can be built and
 * tested end to end without any model.
 */
export const stubProvider: TutorProvider = {
  async reply(ctx: TutorContext): Promise<TutorReply> {
    const { item, hintLevel, calculator } = ctx;
    const errors = calculator.expressions.filter((e) => e.error);
    const prefix = errors.length
      ? `Line ${errors[0].line} in your calculator has an error: "${errors[0].error}". `
      : "";

    switch (hintLevel) {
      case "nudge":
        return { text: `${prefix}What is the question really asking for? Try writing it as something you could graph.` };
      case "strategy":
        return { text: `${prefix}Techniques that fit: ${item.techniques.join(", ")}. Route: ${item.route}.` };
      case "worked-step":
        return { text: `${prefix}${item.desmos ? `Start by typing: ${item.desmos.lines[0]}` : item.byHand.split(".")[0] + "."}` };
      case "full-solution":
        return {
          text: [item.desmos && `Desmos: ${item.desmos.read}`, `By hand: ${item.byHand}`].filter(Boolean).join("\n\n"),
          showMe: item.desmos?.verified ? item.desmos.lines.map((latex) => ({ latex })) : undefined,
        };
    }
  },
};

let provider: TutorProvider | undefined;

export function getTutorProvider(): TutorProvider {
  provider ??= process.env.ANTHROPIC_API_KEY ? createAnthropicProvider() : stubProvider;
  return provider;
}
