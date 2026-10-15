import { NextResponse } from "next/server";
import { getItem } from "@/content/items";
import { gradeItem } from "@/lib/grading/grade";
import { acceptedEntries } from "@/lib/grading/spr";

export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as { itemId?: unknown; response?: unknown } | null;
  const item = typeof body?.itemId === "string" ? getItem(body.itemId) : undefined;
  if (!item) return NextResponse.json({ error: "Unknown item" }, { status: 404 });

  const response = body?.response;
  if (typeof response !== "string" && typeof response !== "number") {
    return NextResponse.json({ error: "Missing response" }, { status: 400 });
  }

  const result = gradeItem(item, response);
  // Reveal the key only once it's answered correctly. A wrong answer gets
  // another try and the hint ladder; the full-solution hint explains it.
  const reveal =
    result.status !== "correct"
      ? undefined
      : item.format === "mc"
        ? { answerIndex: item.answerIndex }
        : { acceptedEntries: item.answers.flatMap(acceptedEntries) };

  return NextResponse.json({ result, reveal });
}
