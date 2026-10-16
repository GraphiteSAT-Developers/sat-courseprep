import { describe, expect, it, vi } from "vitest";

vi.mock("server-only", () => ({}));

import { listItems } from "@/content/items";
import { listTechniques } from "@/content/techniques";
import { EXPORTED_ITEM_FIELDS, itemsToJsonl, skillsExport, techniquesExport, toExportedItem } from "./items";

describe("items export", () => {
  const lines = itemsToJsonl(listItems()).trimEnd().split("\n");

  it("writes one line per item in the bank", () => {
    expect(lines).toHaveLength(listItems().length);
    expect(lines.length).toBeGreaterThanOrEqual(55);
    expect(lines).toHaveLength(listItems().length);
  });

  it("every line is JSON with the provider-neutral fields", () => {
    for (const line of lines) {
      const obj = JSON.parse(line) as Record<string, unknown>;
      for (const field of EXPORTED_ITEM_FIELDS) expect(obj, `${obj.id} lacks ${field}`).toHaveProperty(field);
      expect(["draft", "verified"]).toContain(obj.status);
      if (obj.format === "mc") {
        expect(obj.choices).toHaveLength(4);
        expect(typeof obj.answerIndex).toBe("number");
        expect(obj).not.toHaveProperty("answers");
      } else {
        expect(obj.format).toBe("spr");
        expect(Array.isArray(obj.answers)).toBe(true);
        expect(obj).not.toHaveProperty("answerIndex");
      }
      const desmos = obj.desmos as { lines: string[]; read: string; verified: boolean } | null;
      if (desmos) expect(desmos).toEqual({ lines: desmos.lines, read: desmos.read, verified: desmos.verified });
    }
  });

  it("ids are unique", () => {
    const ids = lines.map((l) => (JSON.parse(l) as { id: string }).id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it("status follows desmos.verified", () => {
    const item = listItems()[0];
    expect(toExportedItem({ ...item, desmos: { lines: ["y=x"], read: "r", verified: true } }).status).toBe("verified");
    expect(toExportedItem({ ...item, desmos: { lines: ["y=x"], read: "r", verified: false } }).status).toBe("draft");
    expect(toExportedItem({ ...item, desmos: undefined }).status).toBe("draft");
  });

  it("skills and techniques exports are complete", () => {
    expect(skillsExport().skills.length).toBeGreaterThan(0);
    expect(techniquesExport(listTechniques()).count).toBe(13);
  });
});
