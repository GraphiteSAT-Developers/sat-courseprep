import { describe, expect, it } from "vitest";
import { clampReply, clampRequest } from "./guardrails";
import type { TutorClientRequest } from "./types";

const base: TutorClientRequest = {
  itemId: "x",
  message: "",
  hintLevel: "full-solution",
  calculator: { degreeMode: false, expressions: [] },
  history: [],
  showMe: true,
};

describe("tutor guardrails", () => {
  it("holds back the full solution and show-me until a committed attempt", () => {
    expect(clampRequest(base)).toMatchObject({ hintLevel: "worked-step", showMe: false });
    const invalid = { ...base, lastAttempt: { response: "3 1/2", result: { status: "invalid" as const, reason: "" } } };
    expect(clampRequest(invalid)).toMatchObject({ hintLevel: "worked-step", showMe: false });
  });

  it("allows them after a graded attempt, right or wrong", () => {
    const tried = { ...base, lastAttempt: { response: 2, result: { status: "incorrect" as const } } };
    expect(clampRequest(tried)).toMatchObject({ hintLevel: "full-solution", showMe: true });
  });

  it("strips calculator writes from replies outside show-me mode", () => {
    const reply = { text: "t", showMe: [{ latex: "y=x" }] };
    expect(clampReply({ ...base, showMe: false }, reply)).toEqual({ text: "t" });
    expect(clampReply(base, reply)).toEqual(reply);
  });
});
