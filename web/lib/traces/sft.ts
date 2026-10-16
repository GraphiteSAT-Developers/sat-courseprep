// SFT export: accepted dialogues only, in the common chat-format JSONL
// ({"messages":[{"role","content"},...]} plus a metadata object) that
// open-weight fine-tuning tools accept. Per-turn metadata and labels stay in
// dialogues.jsonl; nothing but role and content goes inside messages.

import type { ChatMessage, Dialogue, SftLine } from "./schema";

export function toSftLine(d: Dialogue): SftLine {
  const messages: ChatMessage[] = d.messages.map(({ role, content }) => ({ role, content }));
  return {
    messages,
    metadata: {
      dialogueId: d.id,
      itemId: d.itemId,
      traceId: d.traceId,
      persona: d.persona.id,
      judgeScore: d.labels.judgeScore,
      tutorModel: d.tutorModel,
    },
  };
}

export function sftLines(dialogues: Dialogue[]): SftLine[] {
  return dialogues.filter((d) => d.status === "accepted").map(toSftLine);
}
