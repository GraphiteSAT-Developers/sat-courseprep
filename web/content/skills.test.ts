import { describe, expect, it, vi } from "vitest";

// items.ts is server-only; stub the guard so the content can be checked here.
vi.mock("server-only", () => ({}));
import { listItems } from "./items";
import { QUESTION_DISTRIBUTION, SKILLS, SKILL_NAMES, isSkillName, skillsForDomain } from "./skills";
import type { Domain } from "./types";

const DOMAINS: Domain[] = ["algebra", "advanced-math", "psda", "geometry-trig"];

describe("skill taxonomy", () => {
  it("has the 19 Table A31 testing points, each named once", () => {
    expect(SKILLS).toHaveLength(19);
    expect(new Set(SKILL_NAMES).size).toBe(SKILL_NAMES.length);
  });

  it("matches Table A31 counts per domain", () => {
    expect(skillsForDomain("algebra")).toHaveLength(5);
    expect(skillsForDomain("advanced-math")).toHaveLength(3);
    expect(skillsForDomain("psda")).toHaveLength(7);
    expect(skillsForDomain("geometry-trig")).toHaveLength(4);
  });

  it("gives every skill at least one testing point", () => {
    for (const s of SKILLS) expect(s.testingPoints.length, s.name).toBeGreaterThan(0);
  });

  it("distributes the 44-question section across the four domains", () => {
    const share = DOMAINS.reduce((sum, d) => sum + QUESTION_DISTRIBUTION[d].share, 0);
    expect(share).toBeCloseTo(1, 6);
    const min = DOMAINS.reduce((sum, d) => sum + QUESTION_DISTRIBUTION[d].min, 0);
    const max = DOMAINS.reduce((sum, d) => sum + QUESTION_DISTRIBUTION[d].max, 0);
    expect(min).toBeLessThanOrEqual(44);
    expect(max).toBeGreaterThanOrEqual(44);
  });
});

describe("items use framework skill names", () => {
  const items = listItems();

  it("every item.skill is an exact SkillName", () => {
    const mismatches = items
      .filter((item) => !isSkillName(item.skill))
      .map((item) => `${item.id}: "${item.skill}"`);
    expect(mismatches, `Items whose skill is not a framework name:\n  ${mismatches.join("\n  ")}`).toEqual([]);
  });

  it("every item.skill belongs to the item's domain", () => {
    const wrongDomain = items
      .filter((item) => isSkillName(item.skill))
      .filter((item) => !skillsForDomain(item.domain).some((s) => s.name === item.skill))
      .map((item) => `${item.id}: "${item.skill}" is not in domain ${item.domain}`);
    expect(wrongDomain, `Items whose skill is filed under another domain:\n  ${wrongDomain.join("\n  ")}`).toEqual([]);
  });
});
