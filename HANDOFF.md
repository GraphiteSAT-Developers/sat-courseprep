# Handoff: SAT Math 800 course (Desmos-first, AI tutor)

_Last updated 2026-10-15. Status: research done; the site is scaffolded in `web/` (see `web/README.md`)._

## Project goal
Build an AI-powered SAT Math course site aimed at an 800. It teaches **Desmos first** and **by-hand methods second**. The planned tutor AI is the **Google Gemini API**. The owner wants the AI trained to be reliably good at Desmos **before** launch.

## Who does what
This is a collaborative project.
- **Owner (site and courses):** the course content, the item bank, the site in `web/`, grading, the calculator embed, and the tutoring guardrails.
- **AI collaborator:** everything behind the `TutorProvider` interface (`web/lib/tutor/types.ts`): model vendor, prompts, technique retrieval, the Solver/Tutor split, the headless Desmos verification service, and evals.
- **Shared contract:** the item schema (`web/content/types.ts`), the calculator snapshot (`web/lib/desmos/snapshot.ts`), and the College Board calculator options (`web/lib/desmos/config.ts`), which both instances must use.

## Decisions made so far
1. **Calculator UX follows OnePrep/Bluebook.** A Desmos graphing calculator is embedded next to each question through the official Desmos API (`Desmos.GraphingCalculator`), configured to match the College Board version. The **student** uses it.
   - The AI **reads** the student's calculator (`getState`, `observeEvent('change')`, `expressionAnalysis`) to coach.
   - An optional "show me" mode can fill in expressions after the student has tried. The student then retypes them.
   - Details: `docs/desmos-integration.md`.
2. **The AI is trained without fine-tuning.** Gemini 3.x can't be fine-tuned at present. Instead:
   - a Solver agent works each problem in a **headless Desmos instance (Playwright) on the server** and checks the answer with SymPy;
   - a separate Socratic Tutor works only from verified solutions;
   - a retrieved library of Desmos techniques;
   - a layer that cleans up the model's Desmos LaTeX;
   - rejection-sampled worked examples;
   - a three-layer eval (solver accuracy, expression validity, tutoring quality).

## Open blockers (resolve first, as Phase 0)
- **Gemini under-18 terms.** The Gemini API Additional Terms and Google Cloud terms §17(d) reportedly bar apps "directed towards or likely to be accessed by" anyone under 18. Options: a written exception from Google, a different LLM vendor, or an 18+-only product. **Needs a lawyer.** Keep the LLM layer provider-agnostic.
- **Desmos API license.** The free key covers personal use or 90-day internal evaluation only. Production needs a paid plan: Starter is reported at about $100/month for 1,000 users. Ask Desmos whether a server-side headless instance is covered.
- **College Board content.** Official questions can't be used commercially or with generative AI. **All items must be original**, including the eval benchmark. Every use of "SAT" needs College Board's trademark footnote.
- **COPPA and minors' privacy.** The amended rule's compliance date was April 22, 2026. Plan for a neutral age screen, parental consent for under-13s, and a parent-paid checkout.

## Owner decisions still pending
These are listed in the report's decisions table:
- LLM vendor and legal path
- audience and channel
- Desmos plan tier
- launch quality thresholds
- pricing
- human review budget

## Recommended next steps
1. Phase 0 gating: counsel and Google on the age clause; email Desmos about licensing; audit Bluebook's Desmos features by hand.
2. ~~Scaffold the repo~~ Done for the site: Next.js app with the Desmos embed, KaTeX, the SPR grader and the tutor seam (`web/`). Still open:
   - first run against the real Desmos API with a key (only a mock was tested)
   - the headless Desmos verification service (Playwright) and SymPy verifier (AI collaborator)
3. Build the technique library: 30–60 Desmos moves, each with a by-hand route.
4. Build an original benchmark of 300–500 items with a held-out split.

## Where things are
| Path | What |
|---|---|
| `web/` | Course site (Next.js). Start with `web/README.md` |
| `reports/AI Desmos SAT math course plan.md` | Full planning report: architecture, 5-phase roadmap, decision table, verification list |
| `docs/desmos-integration.md` | Calculator design decision (OnePrep-style embed) |
| `research_notes/AI Desmos SAT math course plan/sat_math_format.md` | Test format, scoring, Bluebook Desmos, typed-answer rules |
| `research_notes/.../desmos_techniques.md` | Technique library T1–T13 with syntax, pitfalls, by-hand alternatives, and competitor resources |
| `research_notes/.../gemini_desmos_ai.md` | Gemini models and pricing, Desmos API, Solver/Tutor design, evals |
| `research_notes/.../competitive_landscape.md` | Competitors, pricing, gap (no competitor's AI operates Desmos) |
| `research_notes/.../architecture_legal_pedagogy.md` | Stack, legal and compliance, learning-science evidence, item generation |

## Caveats
- Research tools couldn't open collegeboard.org, desmos.com or ai.google.dev directly. Facts come from search-result summaries. Check the report's verification table before relying on prices, terms or API details.
- OnePrep's actual calculator implementation is unverified.
