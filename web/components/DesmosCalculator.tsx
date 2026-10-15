"use client";

import { useEffect, useRef, useState } from "react";
import { COLLEGE_BOARD_OPTIONS, desmosScriptUrl, loadDesmos } from "@/lib/desmos/config";
import { buildSnapshot, type CalculatorSnapshot } from "@/lib/desmos/snapshot";
import type { DesmosCalculator as Calc } from "@/lib/desmos/types";

interface Props {
  /** Called (debounced) whenever the student's expressions or their evaluation change. */
  onSnapshot?: (snapshot: CalculatorSnapshot) => void;
  /** Gives the parent the calculator instance, e.g. to clear it or load show-me lines. */
  onReady?: (calculator: Calc) => void;
}

const SNAPSHOT_DEBOUNCE_MS = 300;

export function DesmosCalculator({ onSnapshot, onReady }: Props) {
  const el = useRef<HTMLDivElement>(null);
  const callbacks = useRef({ onSnapshot, onReady });
  callbacks.current = { onSnapshot, onReady };
  const src = desmosScriptUrl();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!src || !el.current) return;
    let calc: Calc | undefined;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let cancelled = false;

    loadDesmos(src)
      .then(() => {
        if (cancelled || !el.current || !window.Desmos) return;
        calc = window.Desmos.GraphingCalculator(el.current, { ...COLLEGE_BOARD_OPTIONS });
        const c = calc;
        const emit = () => {
          clearTimeout(timer);
          timer = setTimeout(() => {
            callbacks.current.onSnapshot?.(
              buildSnapshot(c.getExpressions(), c.expressionAnalysis, Boolean(c.getState().graph.degreeMode)),
            );
          }, SNAPSHOT_DEBOUNCE_MS);
        };
        c.observeEvent("change", emit);
        c.observe("expressionAnalysis", emit);
        callbacks.current.onReady?.(c);
      })
      .catch((e: Error) => setError(e.message));

    return () => {
      cancelled = true;
      clearTimeout(timer);
      calc?.destroy();
    };
  }, [src]);

  if (!src) {
    return (
      <div className="calc-placeholder">
        Set <code>NEXT_PUBLIC_DESMOS_API_KEY</code> in <code>web/.env.local</code> to load the calculator.
      </div>
    );
  }
  if (error) return <div className="calc-placeholder">{error}</div>;
  return <div ref={el} className="calc" aria-label="Desmos graphing calculator" />;
}
