import { describe, expect, it, vi } from "vitest";
import type Anthropic from "@anthropic-ai/sdk";
import type { Item } from "@/content/types";
import type { GradeResult } from "@/lib/grading/grade";
import { createStudentSimulator, createTraceTutor, simulateDialogue, type StudentSimulator, type StudentTurn, type TraceTutor } from "./dialogue";
import { applyVerdict, compareDialogues, judgeDialogue } from "./judge";
import { answerRevealedEarly, keyStrings, mentionsKey } from "./leak";
import { UsageMeter, costUsd, type TraceClient } from "./llm";
import { PERSONAS, getPersona } from "./personas";
import { parseDialogue, parseSftLine, parseSolutionTrace, parseJsonl, toJsonl, type Dialogue, type SolutionTrace } from "./schema";
import { sftLines, toSftLine } from "./sft";
import { MAX_SOLVER_RETRIES, solveItem, toGradeResponse } from "./solve";

const sprItem: Item = {
  id: "spr-1",
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

const mcItem: Item = {
  id: "mc-1",
  format: "mc",
  domain: "advanced-math",
  skill: "Nonlinear equations in one variable and systems of equations in two variables",
  difficulty: "medium",
  stem: "How many solutions does the system $y = x^2 - 6x + 11$ and $y = 2x - 5$ have?",
  choices: ["Zero", "Exactly one", "Exactly two", "Infinitely many"],
  answerIndex: 1,
  techniques: ["T2"],
  route: "desmos-primary",
  byHand: "Discriminant is 0.",
  provenance: { author: "test", created: "2026-10-15" },
};

/** A fake Anthropic client that returns the given text blocks in order. */
function fakeClient(texts: (string | object)[], extra: Partial<Anthropic.Message> = {}) {
  const create = vi.fn();
  for (const t of texts) {
    create.mockResolvedValueOnce({
      id: "msg", type: "message", role: "assistant", model: "fake", stop_reason: "end_turn", stop_sequence: null,
      content: [{ type: "text", text: typeof t === "string" ? t : JSON.stringify(t), citations: null }],
      usage: { input_tokens: 100, output_tokens: 20, cache_read_input_tokens: 10, cache_creation_input_tokens: 5 },
      ...extra,
    });
  }
  return { client: { messages: { create } } as unknown as TraceClient, create };
}

const solverOut = (finalAnswer: string) => ({ desmosLines: ["y=6x^{2}-x-2"], readOff: "Click the positive x-intercept.", reasoning: "Roots of the quadratic.", finalAnswer });

describe("solver", () => {
  it("rejects a wrong answer after the retries and never trusts the model", async () => {
    const { client, create } = fakeClient([solverOut("0.67"), solverOut("0.67"), solverOut("-1/2")]);
    const meter = new UsageMeter();
    const trace = await solveItem(client, sprItem, { meter, now: () => "t" });
    expect(create).toHaveBeenCalledTimes(1 + MAX_SOLVER_RETRIES);
    expect(trace.status).toBe("rejected");
    expect(trace.agreesWithKey).toBe(false);
    expect(trace.attempts).toBe(3);
    expect(trace.graderFeedback).toHaveLength(2);
    expect(trace.graderFeedback[0]).toMatch(/rounded too early/);
    expect(trace.graderFeedback[0]).not.toContain("2/3"); // feedback never leaks the key
    expect(trace.finalAnswer).toBe("-1/2");
    expect(trace.usage.inputTokens).toBe(300);
    expect(meter.byModel.get(trace.model)?.calls).toBe(3);
    // The retry carries the grader's feedback back to the model.
    const second = create.mock.calls[1][0];
    expect(second.messages).toHaveLength(3);
    expect(second.messages[2].content).toMatch(/does not match the key/);
    expect(second.output_config.format.type).toBe("json_schema");
    expect(second.output_config.effort).toBe("high");
    expect(second.thinking).toEqual({ type: "adaptive" });
  });

  it("accepts once the grader agrees, as a candidate (not yet run in Desmos)", async () => {
    const { client, create } = fakeClient([solverOut("B"), solverOut(".6667")]);
    const trace = await solveItem(client, sprItem);
    expect(create).toHaveBeenCalledTimes(2);
    expect(trace).toMatchObject({ status: "candidate", agreesWithKey: true, verifiedInDesmos: false, attempts: 2, finalAnswer: ".6667" });
  });

  it("treats malformed output as a failed attempt", async () => {
    const { client } = fakeClient(["not json", { desmosLines: "nope" }, solverOut("2/3")]);
    const trace = await solveItem(client, sprItem);
    expect(trace.status).toBe("candidate");
    expect(trace.attempts).toBe(3);
    expect(trace.graderFeedback[0]).toMatch(/not JSON/);
    expect(trace.graderFeedback[1]).toMatch(/validation/);
  });

  it("maps MC letters to choice indexes for the grader", () => {
    expect(toGradeResponse(mcItem, "b")).toBe(1);
    expect(toGradeResponse(mcItem, "(C)")).toBe(2);
    expect(toGradeResponse(mcItem, "maybe")).toBe(-1);
    expect(toGradeResponse(sprItem, " 2/3 ")).toBe(" 2/3 ");
  });
});

describe("answer-leak check", () => {
  it("knows every accepted entry for an SPR key", () => {
    expect(keyStrings(sprItem)).toEqual(expect.arrayContaining(["2/3", ".6666", ".6667", "0.666", "0.667"]));
    expect(keyStrings(mcItem)).toEqual(["Exactly one"]);
  });

  it("flags standalone keys and choice text, not digits inside expressions", () => {
    expect(mentionsKey(sprItem, "So x = 2/3.")).toBe(true);
    expect(mentionsKey(sprItem, "You should get .6667 or so")).toBe(true);
    expect(mentionsKey(sprItem, "Try graphing y=6x^2-x-2 and click the point.")).toBe(false);
    expect(mentionsKey(sprItem, "The answer is $\\frac{2}{3}$.")).toBe(true);
    expect(mentionsKey(mcItem, "There is exactly one solution.")).toBe(true);
    expect(mentionsKey(mcItem, "Pick B.")).toBe(true);
    expect(mentionsKey(mcItem, "Zoom in near the vertex and count the crossings.")).toBe(false);
  });

  it("catches the key in an early tutor turn and allows it after a graded attempt", () => {
    const messages = [
      { role: "system" as const, content: "rules" },
      { role: "user" as const, content: "help" },
      { role: "assistant" as const, content: "The positive root is 2/3, so type that." },
      { role: "user" as const, content: "ok 0.67" },
      { role: "assistant" as const, content: "Close: 2/3 or .6667 fills the box." },
    ];
    const turns = (early: boolean) => [
      { index: 0, role: "system" as const, attemptPreceded: false },
      { index: 1, role: "user" as const, attemptPreceded: false },
      { index: 2, role: "assistant" as const, attemptPreceded: !early },
      { index: 3, role: "user" as const, attemptPreceded: !early, attempt: { response: "0.67", status: "incorrect" as const } },
      { index: 4, role: "assistant" as const, attemptPreceded: true },
    ];
    expect(answerRevealedEarly(sprItem, messages, turns(true))).toBe(true);
    expect(answerRevealedEarly(sprItem, messages, turns(false))).toBe(false);
  });
});

// A scripted student and a tutor that echoes its inputs, for the loop tests.
function scriptedStudent(turns: StudentTurn[]): StudentSimulator {
  let i = 0;
  return { model: "student", async next() { return { turn: turns[Math.min(i++, turns.length - 1)], usage: { inputTokens: 1, outputTokens: 1, cacheReadTokens: 0, cacheWriteTokens: 0 } }; } };
}
function echoTutor(texts: string[]): { tutor: TraceTutor; seen: Parameters<TraceTutor["reply"]>[0][] } {
  const seen: Parameters<TraceTutor["reply"]>[0][] = [];
  const tutor: TraceTutor = {
    model: "tutor",
    async reply(ctx) {
      seen.push(ctx);
      return { text: texts[Math.min(seen.length - 1, texts.length - 1)], system: "SYS", user: `U${seen.length}: ${ctx.message}`, usage: { inputTokens: 2, outputTokens: 2, cacheReadTokens: 0, cacheWriteTokens: 0 } };
    },
  };
  return { tutor, seen };
}

const trace: SolutionTrace = {
  id: "spr-1#s1", itemId: "spr-1", model: "m", createdAt: "t", desmosLines: ["y=6x^{2}-x-2"], readOff: "click", reasoning: "r", finalAnswer: "2/3",
  agreesWithKey: true, verifiedInDesmos: false, status: "candidate", attempts: 1, graderFeedback: [], usage: { inputTokens: 0, outputTokens: 0, cacheReadTokens: 0, cacheWriteTokens: 0 },
};

describe("dialogue simulation", () => {
  const persona = getPersona("rounds-early")!;
  const student = () =>
    scriptedStudent([
      { message: "just tell me the answer", attempt: null, calculatorLines: [], requestedHint: "full-solution", done: false },
      { message: "I got 0.67", attempt: "0.67", calculatorLines: ["y=6x^{2}-x-2"], requestedHint: "worked-step", done: false },
      { message: "oh, 2/3 then", attempt: "2/3", calculatorLines: ["y=6x^{2}-x-2"], requestedHint: "full-solution", done: true },
    ]);

  it("clamps every tutor turn with the site guardrails, grades attempts and records turn metadata", async () => {
    const { tutor, seen } = echoTutor(["Graph it first.", "Line 1 is right; the box wants the full value.", "Yes: 2/3 or .6667."]);
    const d = await simulateDialogue({ item: sprItem, trace, persona, tutor, student: student(), now: () => "t" });
    expect(seen[0].hintLevel).toBe("worked-step"); // full-solution clamped before any attempt
    expect(seen[0].lastAttempt).toBeUndefined();
    expect(seen[1].lastAttempt?.result).toEqual({ status: "incorrect", hint: "rounded-too-early" });
    expect(seen[2].hintLevel).toBe("full-solution"); // allowed after a graded attempt
    expect(seen[1].item.desmos?.lines).toEqual(trace.desmosLines);
    expect(seen[1].calculator.expressions[0]).toMatchObject({ line: 1, latex: "y=6x^{2}-x-2" });
    expect(seen[2].history).toHaveLength(4);

    expect(d.messages.map((m) => m.role)).toEqual(["system", "user", "assistant", "user", "assistant", "user", "assistant"]);
    expect(d.messages[0].content).toBe("SYS");
    expect(d.messages[1].content).toBe("U1: just tell me the answer");
    expect(d.turns[2]).toMatchObject({ role: "assistant", hintLevel: "worked-step", requestedHintLevel: "full-solution", attemptPreceded: false });
    expect(d.turns[3]).toMatchObject({ role: "user", attemptPreceded: false, attempt: { response: "0.67", status: "incorrect" } });
    expect(d.turns[4]).toMatchObject({ role: "assistant", attemptPreceded: true, calculator: "rad; 1: y=6x^{2}-x-2" });
    expect(d.turns[5].attempt).toEqual({ response: "2/3", status: "correct" });
    expect(d.labels.answerRevealedEarly).toBe(false);
    expect(d.status).toBe("candidate");
    expect(d.persona.id).toBe("rounds-early");
    expect(d.usage.inputTokens).toBe(9);
  });

  it("labels an early reveal when the tutor states the key before a graded attempt", async () => {
    const { tutor } = echoTutor(["The positive root is 2/3.", "Right.", "Done."]);
    const d = await simulateDialogue({ item: sprItem, trace, persona, tutor, student: student() });
    expect(d.labels.answerRevealedEarly).toBe(true);
  });

  it("keeps dialogues between 4 and 8 turns after the system message", async () => {
    const { tutor } = echoTutor(["ok"]);
    const never = scriptedStudent([{ message: "hm", attempt: null, calculatorLines: [], requestedHint: "nudge", done: false }]);
    const long = await simulateDialogue({ item: sprItem, trace, persona, tutor, student: never });
    expect(long.messages.length - 1).toBe(8);
    const quits = scriptedStudent([{ message: "bye", attempt: null, calculatorLines: [], requestedHint: "nudge", done: true }]);
    const short = await simulateDialogue({ item: sprItem, trace, persona, tutor, student: quits });
    expect(short.messages.length - 1).toBe(4);
  });

  it("sends the production tutor prompt and parses the student's structured turn", async () => {
    const { client, create } = fakeClient(["Try graphing both sides."]);
    const tutor = createTraceTutor(client, { model: "tutor-model" });
    const r = await tutor.reply({ item: sprItem, itemId: "spr-1", message: "help", hintLevel: "nudge", calculator: { degreeMode: false, expressions: [] }, history: [] });
    const req = create.mock.calls[0][0];
    expect(req.model).toBe("tutor-model");
    expect(req.system[0].text).toMatch(/^You are a math tutor/);
    expect(req.system[1].text).toContain("Accepted answers: 2/3");
    expect(req.messages[0].content).toMatch(/Hint level: nudge/);
    expect(r.user).toBe(req.messages[0].content);
    expect(r.system).toContain(req.system[1].text);
    expect(r.text).toBe("Try graphing both sides.");

    const studentTurn: StudentTurn = { message: "I typed it", attempt: "0.67", calculatorLines: ["y=6x^{2}-x-2"], requestedHint: "strategy", done: false };
    const s = fakeClient([studentTurn]);
    const sim = createStudentSimulator(s.client, { model: "student-model" });
    const out = await sim.next({ item: sprItem, persona, transcript: [], hintsReceived: 0 });
    expect(out.turn).toEqual(studentTurn);
    const sreq = s.create.mock.calls[0][0];
    expect(sreq.system).toContain(persona.misconception);
    expect(sreq.messages[0].content).not.toContain("2/3"); // the student never sees the key
  });

  it("ships eight personas with distinct named misconceptions", () => {
    expect(PERSONAS).toHaveLength(8);
    expect(new Set(PERSONAS.map((p) => p.id)).size).toBe(8);
    expect(new Set(PERSONAS.map((p) => p.misconception)).size).toBe(8);
  });
});

function dialogueFixture(status: Dialogue["status"], score = 5): Dialogue {
  return {
    id: `spr-1#d${score}`, itemId: "spr-1", traceId: "spr-1#s1", tutorModel: "tutor", studentModel: "student", createdAt: "t",
    persona: { id: "rounds-early", skillLevel: "intermediate", misconception: "m", desmosHabit: "h" },
    messages: [
      { role: "system", content: "SYS" },
      { role: "user", content: "state\n\nStudent says: help" },
      { role: "assistant", content: "Graph it." },
      { role: "user", content: "state\n\nStudent says: 0.67" },
      { role: "assistant", content: "The box wants 2/3." },
    ],
    turns: [
      { index: 0, role: "system", attemptPreceded: false },
      { index: 1, role: "user", attemptPreceded: false, calculator: "rad; (empty)" },
      { index: 2, role: "assistant", attemptPreceded: false, hintLevel: "nudge", requestedHintLevel: "nudge" },
      { index: 3, role: "user", attemptPreceded: false, attempt: { response: "0.67", status: "incorrect" } },
      { index: 4, role: "assistant", attemptPreceded: true, hintLevel: "full-solution", requestedHintLevel: "full-solution" },
    ],
    labels: { answerRevealedEarly: false, reproducibleInBluebook: true, judgeScore: score, judgeNotes: "n", judgeModel: "judge" },
    status,
    usage: { inputTokens: 1, outputTokens: 1, cacheReadTokens: 0, cacheWriteTokens: 0 },
  };
}

describe("judge", () => {
  const verdict = { score: 5, earlyReveal: false, mistakeIdentified: true, mistakeLocated: true, reproducibleInBluebook: true, toneOk: true, notes: "good" };

  it("scores with the configured judge model and folds the verdict into the labels", async () => {
    const { client, create } = fakeClient([verdict]);
    const d = dialogueFixture("candidate", 0);
    const r = await judgeDialogue(client, sprItem, d, { model: "judge-model" });
    expect(create.mock.calls[0][0].model).toBe("judge-model");
    expect(create.mock.calls[0][0].messages[0].content).toContain("Answer key: 2/3");
    const out = applyVerdict(d, r.verdict, r.model);
    expect(out.status).toBe("accepted");
    expect(out.labels).toMatchObject({ judgeScore: 5, reproducibleInBluebook: true, judgeModel: "judge-model", judgeNotes: "good" });
  });

  it("rejects on a low score, a Bluebook failure, or either early-reveal signal", () => {
    const d = dialogueFixture("candidate", 0);
    expect(applyVerdict(d, { ...verdict, score: 3 }, "j").status).toBe("rejected");
    expect(applyVerdict(d, { ...verdict, reproducibleInBluebook: false }, "j").status).toBe("rejected");
    expect(applyVerdict(d, { ...verdict, earlyReveal: true }, "j")).toMatchObject({ status: "rejected", labels: { answerRevealedEarly: true } });
    const leaked = { ...d, labels: { ...d.labels, answerRevealedEarly: true } };
    expect(applyVerdict(leaked, verdict, "j").status).toBe("rejected"); // the deterministic check wins over the judge
  });

  it("randomizes position in pairwise comparison and maps the answer back", async () => {
    const a = dialogueFixture("accepted", 5);
    const b = { ...dialogueFixture("accepted", 4), id: "spr-1#d9" };
    const { client: c1 } = fakeClient([{ preferred: "first", notes: "" }]);
    expect(await compareDialogues(c1, sprItem, a, b, { random: () => 0.9 })).toMatchObject({ preferred: "a", swapped: false });
    const { client: c2 } = fakeClient([{ preferred: "first", notes: "" }]);
    expect(await compareDialogues(c2, sprItem, a, b, { random: () => 0.1 })).toMatchObject({ preferred: "b", swapped: true });
    const { client: c3 } = fakeClient([{ preferred: "tie", notes: "" }]);
    expect((await compareDialogues(c3, sprItem, a, b, { random: () => 0.1 })).preferred).toBe("tie");
  });
});

describe("SFT export", () => {
  it("contains only accepted dialogues and only role/content inside messages", () => {
    const lines = sftLines([dialogueFixture("accepted", 5), dialogueFixture("rejected", 2), dialogueFixture("candidate", 0)]);
    expect(lines).toHaveLength(1);
    expect(lines[0].metadata).toMatchObject({ dialogueId: "spr-1#d5", itemId: "spr-1", persona: "rounds-early", judgeScore: 5 });
    for (const m of lines[0].messages) expect(Object.keys(m).sort()).toEqual(["content", "role"]);
    expect(lines[0].messages[0].role).toBe("system");
    const parsed = JSON.parse(toJsonl(lines).trim());
    expect(Object.keys(parsed).sort()).toEqual(["messages", "metadata"]);
    expect(() => parseSftLine(parsed)).not.toThrow();
    expect(() => parseSftLine({ messages: [{ role: "user", content: "x", hintLevel: "nudge" }], metadata: {} })).toThrow(/unexpected keys/);
  });

  it("strips per-turn metadata even when it sits on the dialogue", () => {
    const line = toSftLine(dialogueFixture("accepted"));
    expect(JSON.stringify(line)).not.toContain("attemptPreceded");
  });
});

describe("schema round-trips", () => {
  it("solution traces and dialogues survive JSONL", () => {
    const traces = parseJsonl(toJsonl([trace]), parseSolutionTrace);
    expect(traces).toEqual([trace]);
    const d = dialogueFixture("accepted");
    expect(parseJsonl(toJsonl([d, { ...d, id: "x" }]), parseDialogue)).toEqual([d, { ...d, id: "x" }]);
    expect(parseJsonl("", parseDialogue)).toEqual([]);
  });

  it("rejects malformed lines with the line number", () => {
    expect(() => parseJsonl('{"id":"a"}\n', parseSolutionTrace)).toThrow(/line 1: Invalid SolutionTrace: missing "itemId"/);
    const bad = { ...dialogueFixture("accepted"), status: "maybe" };
    expect(() => parseDialogue(bad)).toThrow(/bad status/);
    const unbalanced = { ...dialogueFixture("accepted"), turns: [] };
    expect(() => parseDialogue(unbalanced)).toThrow(/parallel/);
  });

  it("prices known models and reports unknown ones", () => {
    const u = { inputTokens: 1_000_000, outputTokens: 0, cacheReadTokens: 0, cacheWriteTokens: 0 };
    expect(costUsd("claude-sonnet-5-5", u)).toBe(2);
    expect(costUsd("claude-opus-5-5", u)).toBe(4);
    expect(costUsd("mystery", u)).toBeNull();
    const meter = new UsageMeter();
    meter.record("claude-opus-5-5", u);
    meter.record("mystery", u);
    expect(meter.totalCostUsd()).toEqual({ known: 4, unknownModels: ["mystery"] });
    expect(meter.total().inputTokens).toBe(2_000_000);
  });

  it("grade results referenced in turn metadata use the grader's vocabulary", () => {
    const statuses: GradeResult["status"][] = ["correct", "incorrect", "invalid"];
    expect(statuses).toHaveLength(3);
  });
});
