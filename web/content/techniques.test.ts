import { describe, expect, it } from "vitest";
import { getTechnique, listTechniques } from "./techniques";

const PAIRS: Record<string, string> = { "(": ")", "[": "]", "{": "}" };
const CLOSERS = new Set(Object.values(PAIRS));

/**
 * True when every (, [ and { in a Desmos LaTeX string is closed in order.
 * `<placeholder>` markers are removed first; a bare < or > left over is a
 * Desmos inequality operator, not a bracket.
 */
function balanced(latex: string): boolean {
  const stack: string[] = [];
  for (const ch of latex.replace(/<[^<>]*>/g, "")) {
    if (ch in PAIRS) stack.push(PAIRS[ch]);
    else if (CLOSERS.has(ch) && stack.pop() !== ch) return false;
  }
  return stack.length === 0;
}

const expectedIds = Array.from({ length: 13 }, (_, i) => `T${i + 1}`);

describe("technique library", () => {
  const all = listTechniques();

  it("has exactly T1 through T13, each once", () => {
    const ids = all.map((t) => t.id);
    expect([...ids].sort()).toEqual([...expectedIds].sort());
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("looks up by id", () => {
    expect(getTechnique("T6")?.name).toMatch(/tilde/i);
    expect(getTechnique("T99")).toBeUndefined();
  });

  it.each(all.map((t) => [t.id, t] as const))("%s is complete", (_id, t) => {
    expect(t.name.trim()).not.toBe("");
    expect(t.summary.trim()).not.toBe("");
    expect(t.domains.length).toBeGreaterThan(0);
    expect(t.skills.length).toBeGreaterThan(0);
    expect(t.triggerConditions.length).toBeGreaterThan(0);
    expect(t.desmosLines.length).toBeGreaterThan(0);
    for (const line of t.desmosLines) expect(line.trim()).not.toBe("");
    expect(t.readOff.trim()).not.toBe("");
    expect(t.pitfalls.length).toBeGreaterThanOrEqual(1);
    expect(t.byHand.method.trim()).not.toBe("");
    expect(t.byHand.whenFaster.trim()).not.toBe("");
    expect(t.preflight.length).toBeGreaterThan(0);
    expect(t.sources.length).toBeGreaterThan(0);
    for (const url of t.sources) expect(url).toMatch(/^https?:\/\//);
    expect(t.verified).toBe(false);
  });

  it.each(all.map((t) => [t.id, t] as const))("%s has balanced LaTeX", (_id, t) => {
    for (const line of t.desmosLines) expect(balanced(line), line).toBe(true);
  });

  it("marks the contested moves as hand-primary with caveats", () => {
    for (const id of ["T3", "T10"] as const) {
      const t = getTechnique(id);
      expect(t?.defaultRoute).toBe("hand-primary");
      expect(t?.caveats?.length).toBeGreaterThan(0);
    }
  });

  it("balanced() rejects mismatches", () => {
    expect(balanced("y_1\\sim ab^{x_1")).toBe(false);
    expect(balanced("\\left(x\\right]")).toBe(false);
    expect(balanced("mean([1,2,3])")).toBe(true);
  });
});
