import type { Item } from "@/content/types";
import { gradeSpr, type SprResult } from "./spr";

export type GradeResult =
  | { status: "correct" }
  | { status: "incorrect"; hint?: "rounded-too-early" }
  | { status: "invalid"; reason: string };

/** The deterministic grader. The LLM never decides whether an answer is right. */
export function gradeItem(item: Item, response: string | number): GradeResult {
  if (item.format === "mc") {
    if (typeof response !== "number" || ![0, 1, 2, 3].includes(response)) {
      return { status: "invalid", reason: "Choose one of the four options." };
    }
    return response === item.answerIndex ? { status: "correct" } : { status: "incorrect" };
  }
  if (typeof response !== "string") return { status: "invalid", reason: "Type your answer." };
  return fromSpr(gradeSpr(response, item.answers));
}

function fromSpr(r: SprResult): GradeResult {
  if (r.status === "invalid") return { status: "invalid", reason: r.reason };
  if (r.status === "incorrect") return r.hint ? { status: "incorrect", hint: r.hint } : { status: "incorrect" };
  return { status: "correct" };
}
