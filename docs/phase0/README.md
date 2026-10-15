# Phase 0: materials for clearing the launch blockers

These files prepare the owner (who builds the courses and the site, and is not a lawyer) to resolve the four blockers listed in `HANDOFF.md` under "Open blockers": the Gemini under-18 terms, the Desmos API license, College Board content, and minors' privacy. Nothing here is legal advice; every legal point is phrased as a question for counsel or a vendor, with the source URL from the research notes. The notes themselves were built from search-result summaries because the research session couldn't open collegeboard.org, desmos.com or ai.google.dev, so facts are flagged as unverified wherever the notes said so. Nothing student-facing ships until these gates clear.

**`desmos-licensing-email.md`** is a ready-to-send email to partnerships@desmos.com. It asks for current Starter pricing and tiers and how a "user" is counted, whether a server-side headless calculator used only for AI verification is covered by Starter or needs something else, whether the College Board testing configuration is available to API customers, and what attribution is required. Fill in the bracketed fields and send it; the reply decides the Desmos plan tier and the design of the headless verification service.

**`counsel-questions.md`** is a grouped list of questions for a lawyer, with a one-paragraph background you can paste. Group 1 covers the Gemini and Google Cloud under-18 terms and the three paths (written exception, another vendor, 18+ only). Group 2 covers College Board content (original items only) and the "SAT" trademark footnote. Group 3 is the amended COPPA Rule (compliance date April 22, 2026). Group 4 lists the state laws the notes did not cover at all: age-appropriate design codes, Utah and Texas age verification, and state chatbot-for-minors laws. Group 5 is contracts and policies. Group 6 is the school channel (FERPA, SOPIPA) and only matters if you sell to schools.

**`bluebook-desmos-audit.md`** is a hands-on checklist for sitting with Bluebook practice mode, desmos.com/testing/collegeboard/graphing and our own embed open side by side. Part A checks each option in `web/lib/desmos/config.ts` and the features the notes say Bluebook has (tables, `~` regression including nonlinear with Log Mode, sliders, lists, stats functions, angle mode default, points of interest, any one-click regression button, resize). Part B lists the ten moves the technique notes could not source, which must be confirmed in Bluebook before they are taught. Part C collects what the headless verification service needs to know.

**`age-gate-plan.md`** is a product plan for a neutral date-of-birth screen, under-13 handling with verifiable parental consent, a parent-paid Stripe checkout, data minimization, vendor settings and what to log. It marks each item that can't be finalized until counsel answers a numbered question, and notes that an 18+-only vendor decision would collapse the plan to the adult path.

## Do you need a lawyer?

Not to keep building. The one blocker that bites immediately is the AI vendor's terms, and that is settled by choosing a vendor, not by hiring counsel. A quick check on 2026-10-15 of the vendors' own pages found:

- **Gemini (Google):** still barred. The terms effective March 2026 prohibit apps "directed towards or likely to be accessed by" under-18s, with no education exception ([terms](https://ai.google.dev/gemini-api/terms)).
- **OpenAI:** allowed for users 13+ with safeguards (age-appropriate filters, AI disclosure, escalation path, zero data retention for under-13s) ([under-18 API guidance](https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance)).
- **Anthropic:** allowed in products for minors if the developer adds age verification, content moderation and monitoring and follows child privacy law; their policy names tutoring and test prep as intended uses ([policy](https://www.anthropic.com/policy), [usage policy update](https://www.anthropic.com/news/updating-our-usage-policy)).

So the working plan is: **build on OpenAI or Anthropic** (the site's `TutorProvider` seam makes either a drop-in), and keep Gemini out unless Google gives a written exception. The safeguards both vendors ask for are the same ones in `age-gate-plan.md`.

`counsel-questions.md` is a "when you're ready" document: worth a one-time consult before you take parents' money, store minors' chat logs, or sell to schools. It is not a gate on building and testing.

## Order of work

1. **Send the Desmos email today.** It needs no legal input and the reply may take time.
2. **Do the Bluebook audit this week.** It needs only a Bluebook install, the public College Board configuration, a Desmos trial key and a few hours. Its results change `config.ts`, the technique library and the verification service, so it unblocks engineering regardless of how the legal questions come out.
3. **Pick the AI vendor** (OpenAI or Anthropic; see above) and record it in `HANDOFF.md`. Group 1 of `counsel-questions.md` then only matters if you still want Gemini.
4. **Before launch, not before building:** send counsel groups 2–4 of `counsel-questions.md` with the background paragraph and the age-gate plan attached.
5. **Revise `age-gate-plan.md`** once counsel answers groups 3 and 4, then build the gate, consent record and parent checkout.
6. **Record each outcome** in `HANDOFF.md` ("Open blockers") and the decisions table in `reports/AI Desmos SAT math course plan.md`. Phase 0 exits when there is a written vendor decision, a chosen Desmos tier and an approved budget.
