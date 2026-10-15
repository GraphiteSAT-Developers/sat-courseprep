import type { DesmosAnalysisEntry, DesmosExpressionState } from "./types";

/**
 * A compact, serializable view of what the student has typed into the calculator.
 * This is what the tutor reads ("read, don't write"); it is the contract between
 * the site and the AI side. Keep it small: it goes into every tutor request.
 */
export interface CalculatorSnapshot {
  degreeMode: boolean;
  expressions: SnapshotExpression[];
}

export interface SnapshotExpression {
  id: string;
  /** 1-based line number as the student sees it. */
  line: number;
  kind: "expression" | "table" | "text";
  latex?: string;
  text?: string;
  columns?: { latex: string; values: string[] }[];
  error?: string;
  value?: number | number[];
}

export function buildSnapshot(
  expressions: DesmosExpressionState[],
  analysis: Record<string, DesmosAnalysisEntry>,
  degreeMode: boolean,
): CalculatorSnapshot {
  const out: SnapshotExpression[] = [];
  expressions.forEach((e, i) => {
    const line = i + 1;
    if (e.type === "expression") {
      if (!e.latex) return;
      const a = analysis[e.id];
      out.push({
        id: e.id,
        line,
        kind: "expression",
        latex: e.latex,
        ...(a?.isError && { error: a.errorMessage ?? "error" }),
        ...(a?.evaluationDisplayed && a.evaluation && { value: a.evaluation.value }),
      });
    } else if (e.type === "table") {
      out.push({
        id: e.id,
        line,
        kind: "table",
        columns: (e.columns ?? []).map((c) => ({ latex: c.latex, values: c.values ?? [] })),
      });
    } else if (e.type === "text" && e.text) {
      out.push({ id: e.id, line, kind: "text", text: e.text });
    }
  });
  return { degreeMode, expressions: out };
}
