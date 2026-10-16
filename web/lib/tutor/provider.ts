import "server-only";
import { createAnthropicProvider } from "./anthropic";
import { createOpenAICompatibleProvider, endpointConfigured, type TutorEnv } from "./openai-compatible";
import type { TutorContext, TutorProvider, TutorReply } from "./types";

/**
 * Placeholder used when no model is configured. It answers from the item's
 * stored by-hand route and Desmos lines, so the UI can be built and tested
 * end to end without any model.
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

export const PROVIDER_KINDS = ["endpoint", "anthropic", "stub"] as const;
export type ProviderKind = (typeof PROVIDER_KINDS)[number];

/**
 * Which provider to use. TUTOR_PROVIDER overrides; otherwise the first
 * configured one wins: endpoint vars → the OpenAI-compatible provider (the
 * fine-tuned tutor), else ANTHROPIC_API_KEY → Sonnet, else the stub.
 * Rollback from the fine-tuned model is therefore one env change:
 * TUTOR_PROVIDER=anthropic.
 */
export function resolveProviderKind(env: TutorEnv = process.env): ProviderKind {
  const override = env.TUTOR_PROVIDER?.trim().toLowerCase();
  if (override) {
    if (!(PROVIDER_KINDS as readonly string[]).includes(override)) {
      throw new Error(`TUTOR_PROVIDER must be one of ${PROVIDER_KINDS.join(", ")}; got "${env.TUTOR_PROVIDER}"`);
    }
    return override as ProviderKind;
  }
  if (endpointConfigured(env)) return "endpoint";
  if (env.ANTHROPIC_API_KEY) return "anthropic";
  return "stub";
}

export function createTutorProvider(env: TutorEnv = process.env): TutorProvider {
  switch (resolveProviderKind(env)) {
    case "endpoint":
      // Throws with a clear message if the override is set but the vars are
      // missing: an explicit choice with no config should fail at startup,
      // not quietly serve the stub to students.
      return createOpenAICompatibleProvider({
        endpointUrl: env.TUTOR_ENDPOINT_URL,
        apiKey: env.TUTOR_ENDPOINT_KEY,
        model: env.TUTOR_ENDPOINT_MODEL,
      });
    case "anthropic":
      return createAnthropicProvider();
    case "stub":
      return stubProvider;
  }
}

let provider: TutorProvider | undefined;

export function getTutorProvider(): TutorProvider {
  provider ??= createTutorProvider();
  return provider;
}
