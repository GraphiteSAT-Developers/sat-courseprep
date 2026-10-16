import { NextResponse } from "next/server";
import { getItem } from "@/content/items";
import { clampReply, clampRequest } from "@/lib/tutor/guardrails";
import { getTutorProvider } from "@/lib/tutor/provider";
import { HINT_LEVELS, type TutorClientRequest } from "@/lib/tutor/types";

export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as TutorClientRequest | null;
  if (!body || typeof body.message !== "string" || !HINT_LEVELS.includes(body.hintLevel) || !body.calculator) {
    return NextResponse.json({ error: "Bad request" }, { status: 400 });
  }
  const item = getItem(body.itemId);
  if (!item) return NextResponse.json({ error: "Unknown item" }, { status: 404 });

  // TODO(auth): the client reports its own lastAttempt. Once accounts exist,
  // look attempts up server-side instead of trusting the request.
  const req = clampRequest(body);
  const reply = await getTutorProvider().reply({ ...req, item });
  return NextResponse.json(clampReply(req, reply));
}
