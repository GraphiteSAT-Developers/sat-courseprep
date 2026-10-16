// Deterministic answer-leak check. The key (any accepted SPR entry, or the
// correct choice's text or letter) must not appear in a tutor turn before the
// student has made a graded attempt. Errs on the side of flagging.

import type { Item } from "@/content/types";
import { acceptedEntries } from "@/lib/grading/spr";
import type { ChatMessage, TurnMeta } from "./schema";

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** Normalize text for choice matching: drop $, collapse whitespace, lowercase. */
function normalize(s: string): string {
  return s.replace(/\$/g, "").replace(/\s+/g, " ").trim().toLowerCase();
}

/** The strings that count as "the answer" for an item. */
export function keyStrings(item: Item): string[] {
  if (item.format === "spr") {
    const out = new Set<string>();
    for (const key of item.answers) {
      for (const e of acceptedEntries(key)) out.add(e);
      out.add(key.den === 1 ? `${key.num}` : `${key.num}/${key.den}`);
    }
    return [...out];
  }
  return [item.choices[item.answerIndex]];
}

/** True when `text` states the key. */
export function mentionsKey(item: Item, text: string): boolean {
  if (item.format === "mc") {
    const letter = "ABCD"[item.answerIndex];
    if (new RegExp(`\\b(answer|choice|option|pick|select|it's|it is)\\s*(is\\s*|:\\s*)?\\(?${letter}\\)?(?![a-zA-Z])`, "i").test(text)) return true;
    const choice = normalize(item.choices[item.answerIndex]);
    return choice.length > 0 && normalize(text).includes(choice);
  }
  const cleaned = text.replace(/\$/g, "").replace(/\\frac\{(-?\d+)\}\{(\d+)\}/g, "$1/$2");
  return keyStrings(item).some((k) => {
    // Standalone number or fraction: not glued to digits, letters, operators or a decimal point.
    const re = new RegExp(`(?<![\\d./a-zA-Z^_{}-])${escapeRegExp(k)}(?![\\d/a-zA-Z{}])`);
    return re.test(cleaned);
  });
}

/** True when any tutor (assistant) turn that precedes a graded attempt mentions the key. */
export function answerRevealedEarly(item: Item, messages: ChatMessage[], turns: TurnMeta[]): boolean {
  return messages.some((m, i) => m.role === "assistant" && !turns[i]?.attemptPreceded && mentionsKey(item, m.content));
}
