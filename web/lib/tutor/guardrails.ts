// Site-enforced tutoring rules. These run on the server around whatever
// TutorProvider is plugged in, so they hold no matter how the model behaves.
// Basis: Bastani et al. (PNAS 2025) — unguarded help raised practice scores but
// cut exam scores 17%; hint-only tutoring with guardrails had no exam penalty.

import type { HintLevel, TutorClientRequest, TutorReply } from "./types";

/** The most a student can unlock right now. Full solutions and show-me need a committed attempt. */
export function maxHintLevel(req: TutorClientRequest): HintLevel {
  return req.lastAttempt && req.lastAttempt.result.status !== "invalid" ? "full-solution" : "worked-step";
}

export function clampRequest(req: TutorClientRequest): TutorClientRequest {
  const attempted = maxHintLevel(req) === "full-solution";
  return {
    ...req,
    hintLevel: !attempted && req.hintLevel === "full-solution" ? "worked-step" : req.hintLevel,
    showMe: attempted && req.showMe === true,
  };
}

export function clampReply(req: TutorClientRequest, reply: TutorReply): TutorReply {
  return req.showMe ? reply : { text: reply.text };
}
