# Email to Desmos partnerships (ready to send)

**Why this email:** the free Desmos API key covers personal use or a 90-day internal evaluation only, so the production embed needs a paid plan. The notes report Starter at about $100–$300/month tiered by 1,000 / 2,500 / 5,000 users, hosted by Desmos only, with Enterprise custom-priced and self-hosted. None of that was read from the live Desmos pages (the proxy blocked them), and nothing in the notes says whether a server-side headless instance that no end user sees is covered. This email asks Desmos directly. Sources: [Desmos API Terms](https://www.desmos.com/api-terms), [Desmos Help: API Plans for Commercial Use](https://help.desmos.com/hc/en-us/articles/49078363315725), [Desmos my-api](https://www.desmos.com/my-api).

**Before sending:** fill in the bracketed fields, and check desmos.com/my-api once yourself so the email doesn't quote a price that the page no longer shows (the figures below are hedged for that reason).

---

**To:** partnerships@desmos.com
**Subject:** Commercial API plan for an SAT math prep site: embed plus server-side verification

Hello Desmos team,

I'm building a Digital SAT math prep website, [SITE NAME], at [URL or "not yet public"]. Each practice question has a Desmos graphing calculator next to it, embedded through the official API (`Desmos.GraphingCalculator`), configured to match the College Board version as closely as possible so students practice on the tool they'll have in Bluebook. I'm currently on the free key for internal evaluation and want to move to the right paid plan before anything is public. I have four questions.

**1. Starter pricing and tiers.** Your API plans page appears to list a Starter plan starting around $100/month for up to 1,000 users, with higher tiers at 2,500 and 5,000 users. Could you confirm the current prices and tiers, and how a "user" is counted (monthly active students, registered accounts, or something else)? I expect to start under 1,000 students.

**2. A server-side instance that no student sees.** In addition to the student-facing embed, I plan to run the same calculator in a headless browser (Playwright) on my server. Its only job is to check, before a hint is shown, that the calculator steps my site's AI tutor suggests actually work in Desmos. No end user ever sees that instance, and it runs on the same expressions a student would type. Is that use covered by Starter, or does it need a different plan or an addendum? If it matters for your answer: I'd expect low volume (on the order of hundreds to a few thousand calculator sessions a day during content generation, and far fewer in steady state).

**3. College Board test configuration.** Is the College Board testing configuration (the one at desmos.com/testing/collegeboard/graphing, with images, folders and notes disabled and Log Mode automatically on for the applicable regressions) available to API customers as a configuration or preset? If not, is there a documented list of the options that build uses so I can set them myself?

**4. Attribution.** What attribution, logo or "powered by Desmos" requirements apply to a commercial embed, and is there a brand page I should follow?

If a short call is easier, I'm glad to do that. Thank you for making the calculator available this way; it's central to what I'm building.

Best regards,
[NAME]
[ROLE, SITE NAME]
[EMAIL] · [PHONE, optional]

---

**After the reply, record the answers in `HANDOFF.md` under "Desmos API license"** and in the decisions table in `reports/AI Desmos SAT math course plan.md` (row "Desmos plan"). The headless verification service design (owned by the AI collaborator) depends on the answer to question 2.
