import { describe, expect, it, vi } from "vitest";

vi.mock("server-only", () => ({}));

import type Anthropic from "@anthropic-ai/sdk";
import type { Item } from "@/content/types";
import { TUTOR_MODEL, createAnthropicProvider } from "./anthropic";
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

function fakeClient(response: Partial<Anthropic.Message>) {
  const create = vi.fn().mockResolvedValue({ stop_reason: "end_turn", content: [{ type: "text", text: "Try graphing it." }], ...response });
  return { client: { messages: { create } } as unknown as Anthropic, create };
}

const base: TutorContext = {
  item,
  itemId: "t",
  message: "help",
  hintLevel: "nudge",
  calculator: { degreeMode: false, expressions: [{ id: "a", line: 1, kind: "expression", latex: "sqrt(", error: "Too few arguments" }] },
  history: [{ role: "student", text: "hi" }, { role: "tutor", text: "hello" }],
};

describe("Anthropic tutor provider", () => {
  it("sends the pinned model, cached system blocks, the item and the calculator state", async () => {
    const { client, create } = fakeClient({});
    const reply = await createAnthropicProvider(client).reply(base);
    expect(reply.text).toBe("Try graphing it.");
    const req = create.mock.calls[0][0];
    expect(req.model).toBe(TUTOR_MODEL);
    expect(req.system[0].cache_control).toEqual({ type: "ephemeral" });
    expect(req.system[1].text).toContain("Accepted answers: 2/3");
    expect(req.system[1].text).toContain("UNVERIFIED");
    expect(req.messages).toHaveLength(3);
    expect(req.messages[2].content).toContain('ERROR: Too few arguments');
    expect(req.messages[2].content).toContain("Hint level: nudge");
  });

  it("turns a refusal into a neutral redirect", async () => {
    const { client } = fakeClient({ stop_reason: "refusal", content: [] });
    const reply = await createAnthropicProvider(client).reply(base);
    expect(reply.text).toMatch(/only help with the math/);
  });

  it("only loads show-me lines from a verified item, never from the model", async () => {
    const { client } = fakeClient({});
    const unverified = await createAnthropicProvider(client).reply({ ...base, showMe: true, hintLevel: "full-solution" });
    expect(unverified.showMe).toBeUndefined();
    const verifiedItem = { ...item, desmos: { ...item.desmos!, verified: true } };
    const verified = await createAnthropicProvider(client).reply({ ...base, item: verifiedItem, showMe: true, hintLevel: "full-solution" });
    expect(verified.showMe).toEqual([{ latex: "y=6x^2-x-2" }]);
  });
});
