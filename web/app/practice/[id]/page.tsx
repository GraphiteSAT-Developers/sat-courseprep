import { notFound } from "next/navigation";
import { getItem } from "@/content/items";
import { toPublicItem } from "@/content/types";
import { PracticeView } from "@/components/PracticeView";

export default async function PracticePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const item = getItem(id);
  if (!item) notFound();
  return <PracticeView item={toPublicItem(item)} />;
}
