import { describe, expect, it, vi } from "vitest";

vi.mock("server-only", () => ({}));

import type { Item } from "@/content/types";
import { chatCompletionsUrl, createOpenAICompatibleProvider, parseExtraBody, stripThinking } from "./openai-compatible";
import { FALLBACK_TEXT, SYSTEM_RULES } from "./prompt";
import type { TutorContext } from "./types";

const item: Item = {
  id: "t",
  format: "spr",
  domain: "advanced-math",
  skill: "Nonlinear functions",
  difficulty: "medium",
  stem: "What is the positive solution to $6x^2 - x - 2 = 0$?",
  answers: [{ num: 2, den: 3 }],
  techniques: ["T1"],
  route: "desmos-primary",
  desmos: { lines: ["y=6x^2-x-2"], read: "Click the positive x-intercept.", verified: false },
  byHand: "Factor: (3x - 2)(2x + 1) = 0.",
  provenance: { author: "test", created: "2026-10-15" },
};

const base: TutorContext = {
  item,
  itemId: "t",
  message: "help",
  hintLevel: "nudge",
  calculator: { degreeMode: false, expressions: [{ id: "a", line: 1, kind: "expression", latex: "sqrt(", error: "Too few arguments" }] },
  history: [{ role: "student", text: "hi" }, { role: "tutor", text: "hello" }],
};

function fakeFetch(init: { status?: number; body?: unknown; reject?: Error }) {
  const fetchFn = vi.fn(async () => {
    if (init.reject) throw init.reject;
    const status = init.status ?? 200;
    return {
      ok: status >= 200 && status < 300,
      status,
      json: async () => init.body ?? { choices: [{ message: { role: "assistant", content: "Try graphing it." } }] },
    } as unknown as Response;
  });
  return fetchFn as unknown as typeof fetch & { mock: { calls: [string, RequestInit][] } };
}

function provider(fetchFn: typeof fetch) {
  return createOpenAICompatibleProvider({
    endpointUrl: "https://example.test/v1",
    apiKey: "secret",
    model: "sat-tutor-qwen3-14b-lora",
    fetch: fetchFn,
  });
}

describe("OpenAI-compatible tutor provider", () => {
  it("posts the model and messages with the system prompt first, then history, then the turn", async () => {
    const fetchFn = fakeFetch({});
    const reply = await provider(fetchFn).reply(base);
    expect(reply.text).toBe("Try graphing it.");

    const [url, init] = fetchFn.mock.calls[0];
    expect(url).toBe("https://example.test/v1/chat/completions");
    expect(init.method).toBe("POST");
    expect((init.headers as Record<string, string>).authorization).toBe("Bearer secret");
    const body = JSON.parse(init.body as string);
    expect(body.model).toBe("sat-tutor-qwen3-14b-lora");
    expect(body.stream).toBe(false);
    expect(body.messages).toHaveLength(4);
    expect(body.messages[0].role).toBe("system");
    expect(body.messages[0].content.startsWith(SYSTEM_RULES)).toBe(true);
    expect(body.messages[0].content).toContain("Accepted answers: 2/3");
    expect(body.messages[0].content).toContain("UNVERIFIED");
    expect(body.messages[1]).toEqual({ role: "user", content: "hi" });
    expect(body.messages[2]).toEqual({ role: "assistant", content: "hello" });
    expect(body.messages[3].role).toBe("user");
    expect(body.messages[3].content).toContain("ERROR: Too few arguments");
    expect(body.messages[3].content).toContain("Hint level: nudge");
    expect(body.messages[3].content).toContain("Student says: help");
  });

  it("falls back to neutral text on a non-200 response", async () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    const reply = await provider(fakeFetch({ status: 503, body: { error: "overloaded" } })).reply(base);
    expect(reply.text).toBe(FALLBACK_TEXT);
    spy.mockRestore();
  });

  it("falls back to neutral text on empty content and on a transport error", async () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    const empty = await provider(fakeFetch({ body: { choices: [{ message: { content: "   " } }] } })).reply(base);
    expect(empty.text).toBe(FALLBACK_TEXT);
    const noChoices = await provider(fakeFetch({ body: {} })).reply(base);
    expect(noChoices.text).toBe(FALLBACK_TEXT);
    const failed = await provider(fakeFetch({ reject: new Error("ECONNRESET") })).reply(base);
    expect(failed.text).toBe(FALLBACK_TEXT);
    spy.mockRestore();
  });

  it("only loads show-me lines from a verified item, never from the model", async () => {
    const modelInventsLines = fakeFetch({
      body: { choices: [{ message: { content: "Type y=x^3 and look." } }] },
    });
    const unverified = await provider(modelInventsLines).reply({ ...base, showMe: true, hintLevel: "full-solution" });
    expect(unverified.showMe).toBeUndefined();
    const verifiedItem = { ...item, desmos: { ...item.desmos!, verified: true } };
    const verified = await provider(modelInventsLines).reply({ ...base, item: verifiedItem, showMe: true, hintLevel: "full-solution" });
    expect(verified.showMe).toEqual([{ latex: "y=6x^2-x-2" }]);
    // And without show-me mode, nothing is loaded even for a verified item.
    const noShowMe = await provider(modelInventsLines).reply({ ...base, item: verifiedItem, hintLevel: "full-solution" });
    expect(noShowMe.showMe).toBeUndefined();
  });

  it("accepts a base URL or a full chat-completions URL, and works without a key", async () => {
    expect(chatCompletionsUrl("http://localhost:8000/v1/")).toBe("http://localhost:8000/v1/chat/completions");
    expect(chatCompletionsUrl("https://x.test/v1/chat/completions")).toBe("https://x.test/v1/chat/completions");
    const fetchFn = fakeFetch({});
    await createOpenAICompatibleProvider({ endpointUrl: "http://localhost:8000/v1", model: "m", fetch: fetchFn }).reply(base);
    expect((fetchFn.mock.calls[0][1].headers as Record<string, string>).authorization).toBeUndefined();
  });

  it("refuses to start without a URL and model", () => {
    expect(() => createOpenAICompatibleProvider({ endpointUrl: "", model: "", fetch: fakeFetch({}) })).toThrow(/TUTOR_ENDPOINT_URL/);
  });
});

describe("endpoint extras for thinking models", () => {
  it("merges extra body fields but never lets them replace model or messages", async () => {
    const fetchFn = fakeFetch({});
    await createOpenAICompatibleProvider({
      endpointUrl: "https://example.test/v1",
      model: "qwen-plus",
      extraBody: { enable_thinking: false, max_tokens: 400, model: "other", messages: [] },
      fetch: fetchFn,
    }).reply(base);
    const body = JSON.parse(String(fetchFn.mock.calls[0][1].body));
    expect(body.enable_thinking).toBe(false);
    expect(body.max_tokens).toBe(400);
    expect(body.model).toBe("qwen-plus");
    expect(body.messages.length).toBeGreaterThan(0);
  });

  it("parses TUTOR_ENDPOINT_EXTRA_BODY and ignores anything but a JSON object", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(parseExtraBody('{"enable_thinking": false}')).toEqual({ enable_thinking: false });
    expect(parseExtraBody(undefined)).toEqual({});
    expect(parseExtraBody("[1]")).toEqual({});
    expect(parseExtraBody("not json")).toEqual({});
    spy.mockRestore();
  });

  it("strips reasoning blocks from the reply", async () => {
    expect(stripThinking("<think>work it out</think>\n\nWhat does line 2 show?")).toBe("What does line 2 show?");
    expect(stripThinking("reasoning only</think>Look at the vertex.")).toBe("Look at the vertex.");
    expect(stripThinking("No tags here.")).toBe("No tags here.");
    const reply = await provider(fakeFetch({ body: { choices: [{ message: { content: "<think>x</think>Try line 1." } }] } })).reply(base);
    expect(reply.text).toBe("Try line 1.");
  });
});
