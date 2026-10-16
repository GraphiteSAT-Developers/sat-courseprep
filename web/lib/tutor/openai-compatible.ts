import "server-only";
import { FALLBACK_TEXT, SYSTEM_RULES, describeItem, describeTurn, showMeLines } from "./prompt";
import type { TutorContext, TutorProvider, TutorReply } from "./types";

// Tutor provider for any OpenAI-compatible chat-completions endpoint: Together,
// Fireworks, vLLM, Bedrock's OpenAI-compatible route, and so on. This is how
// the fine-tuned open-weight tutor (docs/fine-tuning-plan.md) is served.
// Plain fetch, no SDK: the request shape is small and stable, and one fewer
// dependency is one fewer thing to pin.
//
// Prompt assembly is shared with the Anthropic provider (./prompt.ts), so the
// fine-tuned model sees the same system text, item block and turn format it
// was trained on, and the eval compares like with like.

export interface OpenAICompatibleOptions {
  /** Base URL (e.g. https://api.together.xyz/v1) or the full /chat/completions URL. */
  endpointUrl?: string;
  apiKey?: string;
  model?: string;
  timeoutMs?: number;
  /**
   * Extra request fields for this endpoint, e.g. {"enable_thinking": false} for
   * QwenCloud or {"chat_template_kwargs": {"enable_thinking": false}} for vLLM.
   * From TUTOR_ENDPOINT_EXTRA_BODY (JSON). Cannot replace model or messages.
   */
  extraBody?: Record<string, unknown>;
  /** Injected for tests. */
  fetch?: typeof fetch;
}

export const DEFAULT_TIMEOUT_MS = 30_000;

/** A loose view of process.env, so tests can pass plain objects. */
export type TutorEnv = Record<string, string | undefined>;

/** Both env vars needed to select this provider; the key is optional (local vLLM has none). */
export function endpointConfigured(env: TutorEnv = process.env): boolean {
  return Boolean(env.TUTOR_ENDPOINT_URL && env.TUTOR_ENDPOINT_MODEL);
}

/** Accepts either a base URL or the full chat-completions URL. */
export function chatCompletionsUrl(endpointUrl: string): string {
  const trimmed = endpointUrl.replace(/\/+$/, "");
  return trimmed.endsWith("/chat/completions") ? trimmed : `${trimmed}/chat/completions`;
}

/** Parses TUTOR_ENDPOINT_EXTRA_BODY. Anything but a JSON object is ignored, with a log line. */
export function parseExtraBody(raw: string | undefined): Record<string, unknown> {
  if (!raw?.trim()) return {};
  try {
    const value: unknown = JSON.parse(raw);
    if (value && typeof value === "object" && !Array.isArray(value)) return value as Record<string, unknown>;
  } catch {
    // fall through
  }
  console.error("TUTOR_ENDPOINT_EXTRA_BODY is not a JSON object; ignoring it");
  return {};
}

/** Removes reasoning blocks a thinking model may put in its reply (Qwen3, gpt-oss via some servers). */
export function stripThinking(text: string): string {
  return text
    .replace(/<think>[\s\S]*?<\/think>/g, "")
    .replace(/^[\s\S]*?<\/think>/, "") // opening tag consumed by the chat template
    .trim();
}

interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

interface ChatCompletionResponse {
  choices?: { message?: { content?: string | null; refusal?: string | null }; finish_reason?: string }[];
}

export function buildMessages(ctx: TutorContext): ChatMessage[] {
  const history: ChatMessage[] = ctx.history.map((t) => ({
    role: t.role === "student" ? "user" : "assistant",
    content: t.text,
  }));
  return [
    // One system message: the frozen rules, then the item block. The endpoint
    // decides what to cache; the fine-tuning data uses this exact layout.
    { role: "system", content: `${SYSTEM_RULES}\n\n${describeItem(ctx)}` },
    ...history,
    { role: "user", content: describeTurn(ctx) },
  ];
}

export function createOpenAICompatibleProvider(options: OpenAICompatibleOptions = {}): TutorProvider {
  const endpointUrl = options.endpointUrl ?? process.env.TUTOR_ENDPOINT_URL;
  const apiKey = options.apiKey ?? process.env.TUTOR_ENDPOINT_KEY;
  const model = options.model ?? process.env.TUTOR_ENDPOINT_MODEL;
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const extraBody = options.extraBody ?? parseExtraBody(process.env.TUTOR_ENDPOINT_EXTRA_BODY);
  const doFetch = options.fetch ?? fetch;
  if (!endpointUrl || !model) {
    throw new Error("OpenAI-compatible tutor provider needs TUTOR_ENDPOINT_URL and TUTOR_ENDPOINT_MODEL");
  }
  const url = chatCompletionsUrl(endpointUrl);

  return {
    async reply(ctx: TutorContext): Promise<TutorReply> {
      // Show-me lines come from the item, never from the model, whatever the
      // endpoint returns. Computed first so every exit path below carries them.
      const showMe = showMeLines(ctx);
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeoutMs);
      try {
        const response = await doFetch(url, {
          method: "POST",
          headers: {
            "content-type": "application/json",
            ...(apiKey ? { authorization: `Bearer ${apiKey}` } : {}),
          },
          body: JSON.stringify({
            max_tokens: 1024,
            temperature: 0.3,
            ...extraBody,
            model,
            messages: buildMessages(ctx),
            stream: false,
          }),
          signal: controller.signal,
        });
        if (!response.ok) {
          console.error(`tutor endpoint returned ${response.status}`);
          return { text: FALLBACK_TEXT, showMe };
        }
        const data = (await response.json().catch(() => null)) as ChatCompletionResponse | null;
        const text = stripThinking(data?.choices?.[0]?.message?.content ?? "");
        return { text: text || FALLBACK_TEXT, showMe };
      } catch (err) {
        // Timeout (AbortError), DNS, connection reset, bad JSON: all the same
        // neutral line. The student never sees an error string.
        console.error("tutor endpoint request failed", err);
        return { text: FALLBACK_TEXT, showMe };
      } finally {
        clearTimeout(timer);
      }
    },
  };
}
