# data/traces/ — verified tutoring dialogues (the fine-tuning raw material)

Decision 2026-10-15: the live tutor will be an open-weight model fine-tuned on
verified tutoring dialogues. Sonnet (`claude-sonnet-5-5`) is the solver, the
dialogue generator and the simulated student; a different model (default
`claude-opus-5-5`) is the judge. The item bank (`../items.jsonl`) is the raw
material; **the training set is dialogues, not questions.**

Generated files. Do not edit by hand; regenerate. Types and parsers:
`web/lib/traces/schema.ts`.

| File | One line per | What |
|---|---|---|
| `solutions.jsonl` | `SolutionTrace` | The solver's Desmos lines, read-off, reasoning summary and final answer for an item, with `agreesWithKey` from the deterministic grader (`web/lib/grading`), `verifiedInDesmos` (false until the headless Desmos service has run the lines), and `status` |
| `dialogues.jsonl` | `Dialogue` | A simulated tutoring session: `messages` in the neutral chat format, `turns` (per-message metadata: hint level before and after the site's clamp, calculator summary, whether a graded attempt preceded the turn, the attempt and its grade), `labels`, `status`, token usage |
| `sft.jsonl` | `SftLine` | **Accepted dialogues only.** `{"messages":[{"role","content"},...],"metadata":{...}}`: the common chat-format JSONL open-weight fine-tuning tools accept. Nothing but `role` and `content` inside `messages` |

## How a line is produced

1. **Solve.** Sonnet (adaptive thinking, effort high, structured JSON output) proposes `desmosLines` in Desmos LaTeX, a read-off, a short reasoning summary and a `finalAnswer` in the item's format (a letter for MC, a Bluebook entry for SPR). `gradeItem` grades it. The model is never asked whether it is right. On a miss the grader's feedback (never the key) goes back; up to 2 retries, then `status: "rejected"`.
2. **Simulate.** For an item with an accepted trace, Sonnet plays the tutor on the production prompt (`web/lib/tutor/prompt.ts`: `SYSTEM_RULES`, the item block with the trace standing in for the Desmos route, the per-turn state block). A second Sonnet call plays one of eight scripted students (`web/lib/traces/personas.ts`), each with a named misconception: rounds too early on SPR, `=` instead of `~` for regression, forgets to zoom, strict inequality read as inclusive, degree mode left on, sign slip when typing, wrong coordinate read, wants the answer handed over. The site's guardrails (`clampRequest`) run on every tutor turn exactly as in the API route, and every student attempt is graded deterministically. 2–4 exchanges, so 4–8 turns after the system message.
3. **Leak check (deterministic).** The key (every Bluebook-accepted SPR entry, or the correct choice's text or letter) must not appear in a tutor turn before the student has made a graded (correct or incorrect) attempt. Sets `labels.answerRevealedEarly`.
4. **Judge.** `TRACE_JUDGE_MODEL` scores 0–5 on the plan's rubric: no early reveal; the student's mistake identified; its location named (line, step, setting); every Desmos instruction typeable in Bluebook; tone and hint discipline. Structured output. `compareDialogues` does pairwise comparison with randomized position for calibration runs.

## Acceptance rules

| Record | Accepted when |
|---|---|
| Solution trace | `agreesWithKey` is true (grader, not model). `status` is `candidate` until the headless Desmos service sets `verifiedInDesmos` and `verified`; `rejected` after 2 failed retries. Dialogues are built on candidate or verified traces |
| Dialogue | `labels.answerRevealedEarly` false (deterministic check **or** judge; either flag rejects), `labels.reproducibleInBluebook` true, `labels.judgeScore >= 4` (`--min-score`). Otherwise `rejected` |
| SFT line | The dialogue is `accepted` |

The judge is a different model from the generator because LLM judges are noisy
and position-sensitive (MathTutorBench: accuracy below 0.7). Per the plan, its
scores should be calibrated against about 100 human-labeled dialogues before
the threshold is trusted.

## Command

```bash
cd web
npm run traces:generate -- --items all --dialogues-per-item 2 --out ../data/traces
# or a few items:
npm run traces:generate -- --items sample-positive-root,sample-tangent-system --dialogues-per-item 1 --out ../data/traces
```

Options: `--items <id,id|all>`, `--dialogues-per-item N`, `--out <dir>`,
`--force` (re-solve and re-simulate even when accepted records exist),
`--min-score N` (default 4), `--max-exchanges N` (default 4).

Idempotent: an item that already has an accepted trace keeps it; an item that
already has N accepted dialogues gets no new ones. Files are rewritten after
every item, so an interrupted run loses at most one item. The run ends with a
per-item summary table and token and cost totals per model from
`response.usage`.

Environment: `ANTHROPIC_API_KEY` (or an `ant auth login` profile),
`TRACE_SOLVER_MODEL` (solver and simulated student, default
`claude-sonnet-5-5`), `TRACE_STUDENT_MODEL` (optional override for the
student), `TUTOR_MODEL` (the tutor, same variable the site uses, default
`claude-sonnet-5-5`), `TRACE_JUDGE_MODEL` (default `claude-opus-5-5`).

Everything is testable without a key: `web/lib/traces/traces.test.ts` runs the
solver, the loop, the leak check, the judge and the export against a fake
client.

## Notes for the fine-tuning side

- The `user` turns in `messages` are the full per-turn block the production
  provider sends (calculator state, last graded attempt, hint level, then
  "Student says: ..."), so the trained model sees exactly the input format
  it will be served. The production provider currently sends earlier history
  turns as plain text; if that stays, trim earlier user turns to the
  "Student says" line before training, or change the provider to send the
  full block on every turn.
- `desmosLines` are unverified until the headless Desmos service has run them.
  The tutor's system rules already make it hedge on unverified lines; once the
  service marks a trace `verified`, regenerate its dialogues so the training
  data has no hedging where none is needed.
- Every item is original (see `docs/item-writing.md`). Nothing in this
  directory may contain College Board questions.
