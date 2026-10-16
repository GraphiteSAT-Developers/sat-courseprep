// The slice of the Desmos API (https://www.desmos.com/api) this app uses.
// Desmos ships no TypeScript types, so keep this list small and add to it as needed.

export interface DesmosExpressionState {
  id: string;
  type: "expression" | "table" | "text" | "image" | "folder" | string;
  latex?: string;
  text?: string;
  columns?: { latex: string; values?: string[] }[];
  hidden?: boolean;
}

export interface DesmosAnalysisEntry {
  isGraphable: boolean;
  isError: boolean;
  errorMessage?: string;
  evaluationDisplayed?: boolean;
  evaluation?: { type: "Number"; value: number } | { type: "ListOfNumber"; value: number[] };
}

export interface DesmosCalculator {
  getState(): { graph: { degreeMode?: boolean } } & Record<string, unknown>;
  setState(state: unknown): void;
  getExpressions(): DesmosExpressionState[];
  setExpressions(expressions: Partial<DesmosExpressionState>[]): void;
  setBlank(): void;
  expressionAnalysis: Record<string, DesmosAnalysisEntry>;
  observe(property: string, callback: () => void): void;
  unobserve(property: string): void;
  observeEvent(event: "change", callback: () => void): void;
  unobserveEvent(event: "change"): void;
  updateSettings(settings: Record<string, unknown>): void;
  destroy(): void;
}

export interface DesmosStatic {
  GraphingCalculator(el: HTMLElement, options?: Record<string, unknown>): DesmosCalculator;
}

declare global {
  interface Window {
    Desmos?: DesmosStatic;
  }
}
