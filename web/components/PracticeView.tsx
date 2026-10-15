"use client";

import { useRef, useState } from "react";
import type { PublicItem } from "@/content/types";
import type { CalculatorSnapshot } from "@/lib/desmos/snapshot";
import type { DesmosCalculator as Calc } from "@/lib/desmos/types";
import type { GradeResult } from "@/lib/grading/grade";
import { HINT_LEVELS, type HintLevel, type TutorReply, type TutorTurn } from "@/lib/tutor/types";
import { DesmosCalculator } from "./DesmosCalculator";
import { MathText } from "./MathText";

type Reveal = { answerIndex: number } | { acceptedEntries: string[] };

const EMPTY_SNAPSHOT: CalculatorSnapshot = { degreeMode: false, expressions: [] };
const LETTERS = ["A", "B", "C", "D"];

export function PracticeView({ item }: { item: PublicItem }) {
  const calc = useRef<Calc | null>(null);
  const [snapshot, setSnapshot] = useState(EMPTY_SNAPSHOT);
  const [choice, setChoice] = useState<number | null>(null);
  const [entry, setEntry] = useState("");
  // The latest graded attempt. Invalid entries (wrong format) show feedback but don't count as attempts.
  const [lastAttempt, setLastAttempt] = useState<{ response: string | number; result: GradeResult }>();
  const [feedback, setFeedback] = useState<GradeResult>();
  const [reveal, setReveal] = useState<Reveal>();
  const [history, setHistory] = useState<TutorTurn[]>([]);
  const [hintIndex, setHintIndex] = useState(0);
  const [showMeLoaded, setShowMeLoaded] = useState(false);
  const [busy, setBusy] = useState(false);

  const attempted = lastAttempt !== undefined;

  async function submit() {
    const response = item.format === "mc" ? choice : entry;
    if (response === null) return;
    const res = await fetch("/api/grade", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ itemId: item.id, response }),
    });
    const data = (await res.json()) as { result: GradeResult; reveal?: Reveal };
    setFeedback(data.result);
    if (data.result.status !== "invalid") setLastAttempt({ response, result: data.result });
    if (data.reveal) setReveal(data.reveal);
  }

  async function askTutor(level: HintLevel, showMe = false) {
    setBusy(true);
    const message = showMe ? "Show me in the calculator." : `Give me a ${level} hint.`;
    try {
      const res = await fetch("/api/tutor", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ itemId: item.id, message, hintLevel: level, calculator: snapshot, history, lastAttempt, showMe }),
      });
      const reply = (await res.json()) as TutorReply;
      setHistory((h) => [...h, { role: "student", text: message }, { role: "tutor", text: reply.text }]);
      if (reply.showMe && calc.current) {
        calc.current.setExpressions(reply.showMe.map((e, i) => ({ id: `showme-${i}`, latex: e.latex })));
        setShowMeLoaded(true);
      }
      if (!showMe) setHintIndex((i) => Math.min(i + 1, HINT_LEVELS.length - 1));
    } finally {
      setBusy(false);
    }
  }

  const nextHint = HINT_LEVELS[hintIndex];
  const hintLocked = nextHint === "full-solution" && !attempted;

  return (
    <div className="practice">
      <section className="calc-pane">
        <DesmosCalculator onSnapshot={setSnapshot} onReady={(c) => (calc.current = c)} />
      </section>

      <section className="question-pane">
        <p className="meta">
          {item.domain} · {item.skill} · {item.difficulty}
        </p>
        <MathText className="stem" text={item.stem} />

        {item.format === "mc" ? (
          <ol className="choices">
            {item.choices.map((c, i) => {
              const state =
                reveal && "answerIndex" in reveal
                  ? i === reveal.answerIndex
                    ? "right"
                    : i === lastAttempt?.response
                      ? "wrong"
                      : ""
                  : "";
              return (
                <li key={i}>
                  <button className={`choice ${choice === i ? "selected" : ""} ${state}`} onClick={() => setChoice(i)}>
                    <span className="letter">{LETTERS[i]}</span> <MathText text={c} />
                  </button>
                </li>
              );
            })}
          </ol>
        ) : (
          <label className="spr">
            Your answer
            <input value={entry} onChange={(e) => setEntry(e.target.value)} maxLength={6} inputMode="decimal" />
          </label>
        )}

        <button className="primary" onClick={submit} disabled={item.format === "mc" ? choice === null : !entry.trim()}>
          Check
        </button>

        {feedback && <Feedback result={feedback} reveal={reveal} />}

        <div className="tutor">
          <h2>Tutor</h2>
          {history.map((t, i) => (
            <p key={i} className={`turn ${t.role}`}>
              {t.text}
            </p>
          ))}
          <div className="tutor-actions">
            <button onClick={() => askTutor(nextHint)} disabled={busy || hintLocked}>
              {hintLocked ? "Try the question first to unlock the full solution" : `Hint: ${nextHint}`}
            </button>
            {attempted && (
              <button onClick={() => askTutor("full-solution", true)} disabled={busy}>
                Show me in Desmos
              </button>
            )}
          </div>
          {showMeLoaded && (
            <p className="note">
              Now clear it and type the steps yourself — that&apos;s what you&apos;ll do in Bluebook.{" "}
              <button
                onClick={() => {
                  calc.current?.setBlank();
                  setShowMeLoaded(false);
                }}
              >
                Clear and retype
              </button>
            </p>
          )}
        </div>
      </section>
    </div>
  );
}

function Feedback({ result, reveal }: { result: GradeResult; reveal?: Reveal }) {
  if (result.status === "invalid") return <p className="feedback invalid">{result.reason}</p>;
  return (
    <div className={`feedback ${result.status}`}>
      <p>
        {result.status === "correct" ? "Correct." : "Not quite."}
        {result.status === "incorrect" && result.hint === "rounded-too-early" &&
          " That's close, but you rounded too early. Bluebook needs a fraction or a decimal that fills the box."}
      </p>
      {reveal && "acceptedEntries" in reveal && <p>Accepted entries: {reveal.acceptedEntries.join(", ")}</p>}
    </div>
  );
}
