import katex from "katex";

/** Renders text with inline math between $...$ using KaTeX. Works in server and client components. */
export function MathText({ text, className }: { text: string; className?: string }) {
  const parts = text.split(/(\$[^$]+\$)/g);
  return (
    <span className={className}>
      {parts.map((part, i) =>
        part.startsWith("$") && part.endsWith("$") && part.length > 2 ? (
          <span
            key={i}
            dangerouslySetInnerHTML={{ __html: katex.renderToString(part.slice(1, -1), { throwOnError: false }) }}
          />
        ) : (
          <span key={i}>{part}</span>
        ),
      )}
    </span>
  );
}
