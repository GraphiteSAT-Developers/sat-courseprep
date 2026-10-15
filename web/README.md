# web — the course site

Next.js (App Router, TypeScript) app for practice items with the student-operated Desmos calculator beside each question. See `../docs/desmos-integration.md` for the design.

## Run it

```bash
cd web
npm install
cp .env.example .env.local   # then set NEXT_PUBLIC_DESMOS_API_KEY
npm run dev                  # http://localhost:3000
npm test                     # grading + guardrail tests
npm run typecheck
```

Without a Desmos key the page still works; the calculator pane shows a setup message instead.

## Layout

| Path | What | Owner |
|---|---|---|
| `content/types.ts` | Item schema: MC / SPR, domain, techniques (T1–T13), route (Desmos-primary / hand-primary / either), Desmos lines, by-hand route, provenance | Course |
| `content/items.ts` | The item bank (3 original placeholders for now). Server-only, so keys never reach the browser | Course |
| `lib/grading/` | Deterministic grader. `spr.ts` implements Bluebook's typed-answer rules (5/6 characters, fractions, full-width truncated or rounded decimals) | Site |
| `lib/desmos/config.ts` | College Board–style calculator options. **Unverified until the Phase 0 Bluebook audit** | Site |
| `lib/desmos/snapshot.ts` | Compact, serializable view of the student's calculator that the tutor reads | Contract |
| `lib/tutor/types.ts` | `TutorProvider` interface: the seam between site and AI. No vendor names | Contract |
| `lib/tutor/guardrails.ts` | Site-enforced rules: no full solution or "show me" before a graded attempt | Site |
| `lib/tutor/provider.ts` | Stub provider that answers from the item's stored routes. Replace with the real one | AI |
| `app/api/grade`, `app/api/tutor` | Server routes. The browser only ever sees `PublicItem` | Site |
| `components/` | `DesmosCalculator`, `PracticeView`, `MathText` (KaTeX), `SatFootnote` | Site |

## For the AI side

Implement `TutorProvider` (`lib/tutor/types.ts`) and return it from `getTutorProvider()` in `lib/tutor/provider.ts`. You receive the full item (keys, `byHand`, `desmos.lines`), the student's `CalculatorSnapshot`, the requested hint level, chat history and the last graded attempt. The route clamps the request and reply with `guardrails.ts` either way.

Item `desmos.verified` starts `false`. The headless verification service should set it once it has run the lines with `COLLEGE_BOARD_OPTIONS` and confirmed the answer; the stub only loads verified lines into the student's calculator.

## Not built yet

Accounts and progress (Supabase), age screen and parental consent, billing, the item pipeline, Elo/IRT item selection, spaced review, streaming tutor replies.

## Tested so far

Unit tests cover the SPR rules (including the official 8/9 table) and the guardrails. An end-to-end browser run covered the practice flow against a **mocked** Desmos script, because desmos.com was blocked from the build environment. The first run against the real Desmos API still needs doing locally with a key.
