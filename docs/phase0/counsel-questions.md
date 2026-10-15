# Questions for counsel: launch blockers for a Desmos-first SAT math site with an AI tutor

_Prepared 2026-10-15 from the project research notes. This document is a question list, not legal analysis. Every "fact" below came from web-search summaries, because the research session could not open ai.google.dev, cloud.google.com/terms, collegeboard.org or desmos.com directly. Counsel should read the live primary pages; the URLs are given so they can._

## How to use this

Send the "Background for counsel" section plus the question groups you care about. Groups 1 and 2 are the existential ones (whether the planned AI vendor can be used at all, and what content is allowed). Groups 3–5 shape the product design. Group 6 only matters if you sell to schools.

## Background for counsel (one paragraph you can paste)

> I'm building a paid, direct-to-consumer website that teaches Digital SAT math with an emphasis on the Desmos graphing calculator built into the test. Students (mostly 15–17, with some younger PSAT students and some adults) work practice questions, use an embedded Desmos calculator, and chat with an AI tutor that gives staged hints. All questions will be written by me, not copied from College Board. A parent is expected to pay. The AI tutor was planned on Google's Gemini API, but Google's terms appear to bar services for under-18s. I need to know (1) which AI vendor paths are open, (2) what I may say and use regarding "SAT" and College Board materials, (3) what COPPA and state minors' laws require of the signup, consent and data flows, and (4) whether any of this changes if I later sell to schools.

Facts the research marked **unverified** are flagged inline. Items marked **[not researched]** had no source at all; counsel is being asked to cover them from scratch.

---

## 1. Gemini / Google under-18 API terms

**Context:** The Gemini API Additional Terms reportedly say "You must be 18 years of age or older to use the APIs" and prohibit an "API Client directed towards or likely to be accessed by individuals under the age of 18." Google Cloud Service Specific Terms §17(d) reportedly apply the same restriction to generative AI on the Gemini Enterprise Agent Platform (formerly Vertex AI). A Google forum reply says the restriction applies regardless of access route, and Google declined to say whether routing minors away from Gemini would comply. Google serves teens Gemini through Workspace for Education, which is a first-party product, not a developer carve-out. _All quotes are from search-result excerpts; the terms page was reported as last modified April 2026._
Sources: [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms) · [Google Cloud Service Specific Terms](https://cloud.google.com/terms/service-terms) · [Google Dev forum reply](https://discuss.google.dev/t/question-regarding-age-restrictions-for-the-gemini-api/188060/2) · [AI Dev forum: routing minors](https://discuss.ai.google.dev/t/age-restriction-under-18-is-routing-minors-away-from-gemini-api-acceptable/188423) · [Workspace for Education teen access](https://workspaceupdates.googleblog.com/2024/10/gemini-app-access-for-teen-students-workspace-education.html) · [Example of a project switching vendor over this](https://github.com/AI-X-16-1/BOOKIT/issues/54)

1.1. Reading the live text of both documents, does an SAT prep site fall within "directed towards or likely to be accessed by individuals under the age of 18"? Is there any education or enterprise carve-out the notes missed? _(The notes found no confirmed exception for education apps.)_

1.2. **Option A, written exception.** If I ask a Google Cloud account team for a written exception or an enterprise agreement, what form would that need to take to actually override the Service Specific Terms? What should I ask for in writing, and who at Google can grant it?

1.3. **Option B, another vendor.** The notes did **not research** the minimum-age and minors terms of OpenAI, Anthropic or any other provider **[not researched]**. Can you review the current terms of two or three alternatives and tell me which permit a 13–17 audience, with what conditions (parental consent, safety settings, data-use terms)?

1.4. **Option C, 18+ only.** If I verify that users are 18+, does an SAT product still fail the "likely to be accessed by" test given who takes the SAT? What age-verification standard would be needed to make this defensible, if any?

1.5. **Paid vs free tier.** The notes say that under Gemini "Unpaid Services" Google may use prompts and outputs to improve products and human reviewers may read them, while under "Paid Services" it does not. Does using only Paid Services change the analysis for minors' data, and what does the data-logging policy allow Google to keep? Source: [Gemini API logs policy](https://ai.google.dev/gemini-api/docs/logs-policy)

1.6. If the vendor is unsettled, is there a legal reason to delay signing anything (beta terms, DPAs) until it is, or can I proceed on a trial basis with no minors in the system?

## 2. College Board content and trademark use

**Context:** College Board's permission pages reportedly say official SAT materials may not be reproduced in test prep or commercial settings, and that it does not grant permission for its copyrighted content, including practice questions, to be used with generative AI. Its trademark guidelines reportedly require a footnote stating the mark belongs to College Board and that College Board "is not affiliated with, and does not endorse, this [product/site]," on the same page as the mark, which on websites means the home page and every internal page that uses it. The plan is **original items only**: nothing from Bluebook, the Question Bank or released tests goes into the site, the AI prompts, the retrieval library or the evaluation set. The site would link out to official practice rather than embed it.
Sources: [CB permission request instructions](https://privacy.collegeboard.org/copyright-trademark/request-instructions) · [CB trademark guidelines](https://privacy.collegeboard.org/copyright-trademark/guidelines) · [Question Bank overview](https://satsuite.collegeboard.org/k12-educators/tools-resources/question-bank/overview)

2.1. Is descriptive use of "SAT" and "Digital SAT" in a name such as "[Brand] — Digital SAT Math Prep" acceptable as nominative use, with the footnote? Is "SAT [Brand]" or "SAT 800" as a product name a problem? _(The only source on this was an informal Q&A, not authority.)_

2.2. Please supply the exact footnote wording and placement you'd want: every page that says "SAT", the home page, marketing emails, ads, app-store listings?

2.3. Writing original questions "aligned to College Board's published content domains and skill descriptions" (Algebra, Advanced Math, Problem-Solving & Data Analysis, Geometry & Trigonometry): is aligning to published test specifications safe, and where is the line between an original item and one "inspired by" an official item? What provenance records should I keep for each item in case of a claim?

2.4. The notes found **no explicit terms of use for the Question Bank** and no reuse license for Bluebook tests **[gap]**. Does that change anything, and should I avoid even having staff study official items while writing originals?

2.5. Who owns AI-assisted original items, and do any vendor terms restrict commercial use of model outputs as course content? **[flagged LAWYER in the notes]**

2.6. Khan Academy content is CC BY-NC-SA and its ToS reportedly limits the service to personal, non-commercial use. Linking to Khan from a paid site: fine? Embedding or quoting: not fine? Source: [Khan Academy help](https://support.khanacademy.org/hc/en-us/articles/202262954-Can-I-use-Khan-Academy-s-videos-name-materials-links-) · [Khan trademark policy](https://support.khanacademy.org/hc/en-us/articles/202263034-Trademark-and-Brand-Usage-Policy)

## 3. COPPA (amended rule, compliance date April 22, 2026)

**Context:** The amended COPPA Rule took effect June 23, 2025, with general compliance required by **April 22, 2026**, which has passed. It adds biometric identifiers (including voiceprints) to "personal information" and requires privacy notices to identify the third parties that receive data. COPPA covers under-13s; a teen SAT product will still reach some 12-year-olds (PSAT 8/9 students) unless it screens. A February 25, 2026 FTC policy statement reportedly limits enforcement when children's data is collected only for age verification before consent is obtained _(via a law-firm summary, not the FTC page)_.
Sources: [Federal Register 2025-05904](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule) · [BBB Programs summary](https://bbbprograms.org/media/insights/blog/coppa-amended) · [Cullen LLP summary](https://www.cullenllp.com/blog/ftc-publishes-coppa-rule-amendments/) · [Davis Polk update](https://www.davispolk.com/index%2ephp/print/pdf/node/116375)

3.1. Is this site a "general audience" service or one "directed to children"? Does a product aimed at 15–17-year-olds with some PSAT 8/9 users get treated as directed to children in part?

3.2. For a neutral date-of-birth screen: what counts as "neutral" (no hint of the eligible age, no retry with a different date)? What may I collect and store from an under-13 attempt before parental consent, and how long may I keep it? _(See `age-gate-plan.md` for the proposed flow.)_

3.3. Which verifiable parental consent methods are acceptable for a paid product? Does a parent completing a card payment at checkout count ("credit card plus transaction")? Does it count if the student, not the parent, started the signup?

3.4. For 13–17 users, is parental notice needed at all under federal law, and is a parent-paid checkout sufficient as notice?

3.5. Treating AI tutor chat logs as the student's personal information: what retention period, deletion rights and third-party disclosure (LLM vendor, analytics, error logging, email provider) must the privacy notice name? What vendor contract terms (training off, limited retention) do you want to see?

3.6. Voice, camera or screenshot features are planned as **later options only**. Confirm that a student uploading a screenshot of their calculator is not biometric data, and what adding voice would require.

## 4. State laws the notes flagged as not covered

**Context:** The research covered only California's CCPA opt-in for under-16s (which applies only above the CCPA thresholds, e.g. $25M revenue or 100,000 consumers) and SOPIPA. It explicitly **did not research** state age-appropriate design codes, the Utah and Texas app-store age-verification laws, state AI-companion/chatbot laws for minors, or the CPPA's minors regulations. These are listed here as questions with no answer in the notes. **[not researched]**
Sources (for what was covered): [CA AB 801 analysis](https://apcp.assembly.ca.gov/sites/privacycp.assembly.ca.gov/files/AB%20801%20(Joe%20Patterson)%20APCP%20analysis.pdf) · [CCPA thresholds, secondary](https://www.cybernut.com/blog/what-to-know-about-the-california-consumer-privacy-act-ccpa-for-schools)

4.1. **Age-appropriate design codes** (California's and any other states' now in force): do they apply to a small DTC prep site, and what would they require of defaults (data minimization, no profiling, no dark patterns, high-privacy defaults for minors)?

4.2. **Utah and Texas age-verification laws:** my product is a website, not an app-store app. Do these laws reach a web product, and would a future mobile app change that?

4.3. **State chatbot-for-minors laws:** several states reportedly regulate AI chatbots or "companions" used by minors (disclosure that the user is talking to an AI, self-harm protocols, usage limits, audit duties). Which apply to a math tutoring chat, and what disclosures or protocols must the tutor implement at launch?

4.4. **California CCPA/CPRA:** below the thresholds now, but when does the under-16 opt-in for selling or sharing data apply, and does ordinary analytics or ad-pixel use count as "sharing"? What do the CPPA's minors regulations require?

4.5. Any other state student-privacy or minors' data law that reaches a DTC product (not only school vendors)? Please list the states where I should not sell until something is in place, if any.

## 5. Product and contract items that follow from the above

5.1. Please draft or review: Terms of Service (with the parent as the contracting party), Privacy Policy naming every third-party recipient, a short student-facing notice, and the consent language at checkout.

5.2. Stripe and minors: a parent must be the payer and account holder for billing. Is anything needed beyond that in the ToS? _(The notes did not research Stripe's handling of minors.)_

5.3. Desmos API commercial terms: once Desmos replies to `desmos-licensing-email.md`, please review the Commercial Addendum or self-service plan terms, especially whether the server-side verification use is covered and any attribution duties.

5.4. Marketing claims: the notes say figures such as "an 800 allows 0–2 misses" and "Desmos solves a third to half of questions" are third-party estimates with no official source. Any constraints on stating these as estimates?

## 6. School channel (only if I later sell to schools or districts)

**Context:** A school channel adds FERPA's "school official" exception (the vendor must serve a legitimate educational interest, perform a service the school would otherwise perform, and be under the school's direct control) and SOPIPA (Cal. Bus. & Prof. Code §§22584–22585), which bars targeted advertising on student data, profiling for non-K-12 purposes and selling student information. Whether SOPIPA reaches a purely DTC product marketed to students was **not verified** and turns on "K-12 school purposes".
Sources: [FPF SOPIPA guide](https://fpf.org/wp-content/uploads/2016/11/SOPIPA-Guide_Nov-4-2016.pdf) · [Edlink: student privacy laws for developers](https://ed.link/community/student-privacy-laws-edtech-developers-need-to-know/) · [FERPA vs COPPA guide](https://privacylawmap.com/blog/ferpa-vs-coppa-compliance-student-data-privacy-guide)

6.1. Does SOPIPA apply to my DTC product today, even without school contracts, because students use it for school-related test prep?

6.2. If a school buys seats: what must the data-processing agreement contain, what does "direct control" require of my architecture, and can school-authorized consent replace parental consent under COPPA for educational use only?

6.3. Which state student-data-privacy laws and standard DPAs (e.g., the national student privacy DPA templates) should I expect to sign, and is it reasonable to defer the school channel until I have that capacity?

---

## Decisions these answers unlock (from the project's decisions table)

| Decision | Depends on |
|---|---|
| LLM vendor and legal path (Gemini exception / other vendor / 18+ only) | Group 1 |
| Audience and channel (DTC with parent payer / schools / adults only) | Groups 1, 3, 4, 6 |
| Age-gate and consent flow (`age-gate-plan.md`) | Groups 3, 4 |
| Content sourcing (original only, provenance logs) and naming | Group 2 |
| Desmos plan tier | Desmos reply + 5.3 |
