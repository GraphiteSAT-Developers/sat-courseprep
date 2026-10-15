import type { Item } from "@/content/types";
import { DOMAIN_TITLES, QUESTION_DISTRIBUTION, SKILLS } from "@/content/skills";
import type { Technique } from "@/content/technique-types";

// Provider-neutral feed for the AI side (tutor prompts, technique retrieval,
// evals). Plain JSON only: no vendor types, no site internals. The schema is
// the item schema in content/types.ts plus a `status` the pipeline can key on.

/** "verified" once the headless Desmos service has confirmed the lines; "draft" otherwise. */
export type ItemStatus = "draft" | "verified";

export interface ExportedItemBase {
  id: string;
  domain: Item["domain"];
  skill: string;
  difficulty: Item["difficulty"];
  format: Item["format"];
  stem: string;
  techniques: string[];
  route: Item["route"];
  desmos: { lines: string[]; read: string; verified: boolean } | null;
  byHand: string;
  provenance: Item["provenance"];
  status: ItemStatus;
}

export type ExportedItem =
  | (ExportedItemBase & { format: "mc"; choices: string[]; answerIndex: number })
  | (ExportedItemBase & { format: "spr"; answers: { num: number; den: number }[] });

export const EXPORTED_ITEM_FIELDS = [
  "id", "domain", "skill", "difficulty", "format", "stem", "techniques", "route", "desmos", "byHand", "provenance", "status",
] as const;

export function itemStatus(item: Item): ItemStatus {
  return item.desmos?.verified ? "verified" : "draft";
}

export function toExportedItem(item: Item): ExportedItem {
  const base: ExportedItemBase = {
    id: item.id,
    domain: item.domain,
    skill: item.skill,
    difficulty: item.difficulty,
    format: item.format,
    stem: item.stem,
    techniques: item.techniques,
    route: item.route,
    desmos: item.desmos ? { lines: item.desmos.lines, read: item.desmos.read, verified: item.desmos.verified } : null,
    byHand: item.byHand,
    provenance: item.provenance,
    status: itemStatus(item),
  };
  return item.format === "mc"
    ? { ...base, format: "mc", choices: item.choices, answerIndex: item.answerIndex }
    : { ...base, format: "spr", answers: item.answers.map(({ num, den }) => ({ num, den })) };
}

/** One JSON object per line, stable item order, trailing newline. */
export function itemsToJsonl(items: Item[]): string {
  return items.map((item) => JSON.stringify(toExportedItem(item))).join("\n") + "\n";
}

export function skillsExport() {
  return {
    source: "College Board, Assessment Framework for the Digital SAT Suite, Appendix A (Table A31) and Appendix B (Tables A35–A38)",
    domains: DOMAIN_TITLES,
    questionDistribution: QUESTION_DISTRIBUTION,
    skills: SKILLS,
  };
}

export function techniquesExport(techniques: Technique[]) {
  return { count: techniques.length, techniques };
}
