import Link from "next/link";
import { listItems } from "@/content/items";
import { MathText } from "@/components/MathText";

export default function Home() {
  const items = listItems();
  return (
    <div className="home">
      <h1>Practice</h1>
      <p>Desmos first, by hand second. Use the calculator the way you will in Bluebook.</p>
      <ul className="item-list">
        {items.map((item) => (
          <li key={item.id}>
            <Link href={`/practice/${item.id}`}>
              <span className="meta">
                {item.domain} · {item.difficulty} · {item.format === "mc" ? "multiple choice" : "student-produced response"}
              </span>
              <MathText text={item.stem} />
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
