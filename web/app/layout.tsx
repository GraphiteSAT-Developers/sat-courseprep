import type { Metadata } from "next";
import Link from "next/link";
import "katex/dist/katex.min.css";
import "./globals.css";
import { SatFootnote } from "@/components/SatFootnote";

export const metadata: Metadata = {
  title: "SAT Math 800 — Desmos first",
  description: "Desmos-first SAT Math prep with an AI tutor.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="site-header">
          <Link href="/">SAT Math 800</Link>
        </header>
        <main>{children}</main>
        <SatFootnote />
      </body>
    </html>
  );
}
