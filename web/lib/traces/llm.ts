// Thin layer over the Anthropic SDK shared by the solver, the student
// simulator and the judge: structured JSON output, usage accounting and the
// minimal client surface the tests fake.

import type Anthropic from "@anthropic-ai/sdk";
import type { TokenUsage } from "./schema";

/** The slice of the SDK client the pipeline calls. A fake only needs `messages.create`. */
export interface TraceClient {
  messages: { create(params: Anthropic.MessageCreateParamsNonStreaming): Promise<Anthropic.Message> };
}

export const SOLVER_MODEL = process.env.TRACE_SOLVER_MODEL ?? "claude-sonnet-5-5";
/** A different model from the generator, as the plan asks (judges are noisy and position-sensitive). */
export const JUDGE_MODEL = process.env.TRACE_JUDGE_MODEL ?? "claude-opus-5-5";

export const emptyUsage = (): TokenUsage => ({ inputTokens: 0, outputTokens: 0, cacheReadTokens: 0, cacheWriteTokens: 0 });

export function usageOf(response: Pick<Anthropic.Message, "usage">): TokenUsage {
  const u = response.usage;
  return {
    inputTokens: u?.input_tokens ?? 0,
    outputTokens: u?.output_tokens ?? 0,
    cacheReadTokens: u?.cache_read_input_tokens ?? 0,
    cacheWriteTokens: u?.cache_creation_input_tokens ?? 0,
  };
}

export function addUsage(a: TokenUsage, b: TokenUsage): TokenUsage {
  return {
    inputTokens: a.inputTokens + b.inputTokens,
    outputTokens: a.outputTokens + b.outputTokens,
    cacheReadTokens: a.cacheReadTokens + b.cacheReadTokens,
    cacheWriteTokens: a.cacheWriteTokens + b.cacheWriteTokens,
  };
}

/** USD per million tokens (Anthropic first-party rates as of 2026-10; cache write = 1.25x input). */
const PRICES: Record<string, { input: number; output: number; cacheRead: number; cacheWrite: number }> = {
  "claude-sonnet-5-5": { input: 2, output: 10, cacheRead: 0.2, cacheWrite: 2.5 },
  "claude-sonnet-5": { input: 2, output: 10, cacheRead: 0.2, cacheWrite: 2.5 },
  "claude-opus-5-5": { input: 4, output: 20, cacheRead: 0.2, cacheWrite: 5 },
  "claude-opus-5": { input: 5, output: 25, cacheRead: 0.5, cacheWrite: 6.25 },
  "claude-haiku-5-5": { input: 0.1, output: 0.5, cacheRead: 0.01, cacheWrite: 0.125 },
};

/** Estimated cost in USD, or null when the model's price is unknown. */
export function costUsd(model: string, u: TokenUsage): number | null {
  const p = PRICES[model];
  if (!p) return null;
  return (u.inputTokens * p.input + u.outputTokens * p.output + u.cacheReadTokens * p.cacheRead + u.cacheWriteTokens * p.cacheWrite) / 1e6;
}

/** Running totals per model, filled by every call that goes through `structured` or `meter`. */
export class UsageMeter {
  readonly byModel = new Map<string, { calls: number; usage: TokenUsage }>();
  record(model: string, usage: TokenUsage) {
    const row = this.byModel.get(model) ?? { calls: 0, usage: emptyUsage() };
    row.calls += 1;
    row.usage = addUsage(row.usage, usage);
    this.byModel.set(model, row);
  }
  total(): TokenUsage {
    let t = emptyUsage();
    for (const { usage } of this.byModel.values()) t = addUsage(t, usage);
    return t;
  }
  totalCostUsd(): { known: number; unknownModels: string[] } {
    let known = 0;
    const unknownModels: string[] = [];
    for (const [model, { usage }] of this.byModel) {
      const c = costUsd(model, usage);
      if (c === null) unknownModels.push(model);
      else known += c;
    }
    return { known, unknownModels };
  }
}

export class StructuredOutputError extends Error {}

export function textOf(response: Pick<Anthropic.Message, "content">): string {
  return response.content
    .filter((b): b is Anthropic.TextBlock => b.type === "text")
    .map((b) => b.text)
    .join("")
    .trim();
}

export interface StructuredCall<T> {
  model: string;
  system: string | Anthropic.TextBlockParam[];
  messages: Anthropic.MessageParam[];
  /** JSON schema for output_config.format. */
  schema: Record<string, unknown>;
  /** Narrow the parsed JSON; throw to reject it. */
  validate: (v: unknown) => T;
  effort?: "low" | "medium" | "high" | "xhigh" | "max";
  maxTokens?: number;
  meter?: UsageMeter;
}

/**
 * One structured-output request. Uses `output_config.format` (JSON schema) and
 * parses the text block ourselves so a fake client only has to return text.
 * Throws StructuredOutputError on refusal, truncation, or JSON that fails `validate`.
 */
export async function structured<T>(client: TraceClient, call: StructuredCall<T>): Promise<{ value: T; usage: TokenUsage; raw: string }> {
  const response = await client.messages.create({
    model: call.model,
    max_tokens: call.maxTokens ?? 16000,
    thinking: { type: "adaptive" },
    output_config: { effort: call.effort ?? "high", format: { type: "json_schema", schema: call.schema } },
    system: call.system,
    messages: call.messages,
  });
  const usage = usageOf(response);
  call.meter?.record(call.model, usage);
  if (response.stop_reason === "refusal") throw new StructuredOutputError("model refused the request");
  if (response.stop_reason === "max_tokens") throw new StructuredOutputError("output truncated at max_tokens");
  const raw = textOf(response);
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new StructuredOutputError(`response was not JSON: ${raw.slice(0, 120)}`);
  }
  try {
    return { value: call.validate(parsed), usage, raw };
  } catch (e) {
    throw new StructuredOutputError(`response failed validation: ${(e as Error).message}`);
  }
}

// Small validators for the shapes we ask for.
export function expectString(v: unknown, name: string): string {
  if (typeof v !== "string") throw new Error(`${name} must be a string`);
  return v;
}
export function expectBoolean(v: unknown, name: string): boolean {
  if (typeof v !== "boolean") throw new Error(`${name} must be a boolean`);
  return v;
}
export function expectStringArray(v: unknown, name: string): string[] {
  if (!Array.isArray(v) || !v.every((x) => typeof x === "string")) throw new Error(`${name} must be an array of strings`);
  return v;
}
export function expectObject(v: unknown, name: string): Record<string, unknown> {
  if (typeof v !== "object" || v === null || Array.isArray(v)) throw new Error(`${name} must be an object`);
  return v as Record<string, unknown>;
}
