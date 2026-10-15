# Architecture, Legal/Compliance, and Learning-Science Design for an AI SAT Math Course (Gemini tutor + Desmos)

Research date: 2026-10-15. US jurisdiction. This is not legal advice; items marked "LAWYER" need counsel review.
Method note: direct page fetches to ai.google.dev, desmos.com, and collegeboard.org were blocked by the session's network proxy. Findings below come from web-search results that quote or summarize those primary pages. Re-read the live primary pages before relying on them, especially for terms of service.

## Legal/IP: College Board content, SAT trademark, Khan Academy, Desmos, and Gemini terms

### Takeaway
Do not reuse any official College Board SAT questions. That covers Bluebook tests, the Question Bank, and released tests. College Board says reproduction for test prep or commercial use is not allowed, and it specifically refuses permission for use with generative AI. You can say "SAT" in a descriptive, nominative way if you add the required non-affiliation footnote. Commercial use of Desmos needs a paid plan, starting at about $100–$300/month. **The biggest blocker is Gemini: both the Gemini API terms and the Google Cloud/Vertex AI Service Specific Terms bar services "directed towards or likely to be accessed by individuals under the age of 18."** A high-school SAT tutor falls inside that language on its face. This needs a lawyer and a Google account-team answer before you build on Gemini.

### Cited Findings
**College Board content and trademarks**
- College Board's permission instructions say official SAT test materials may not be reproduced in test prep or other commercial settings. — [College Board Copyright & Trademark Permission Request Instructions](https://privacy.collegeboard.org/copyright-trademark/request-instructions)
- College Board says it does not grant permission for its copyrighted content, including practice test questions, to be used with generative AI or similar technologies. — [College Board Guidelines for Using College Board Trademarks / permissions](https://privacy.collegeboard.org/copyright-trademark/guidelines)
- Third parties must use College Board marks in a way that "will minimize consumer confusion and avoid implying a relationship with the College Board." A footnote must state that the mark belongs to College Board and that College Board is "not affiliated with, and does not endorse, this [product/site]." The footnote goes on the same page as the mark, which on websites means the home page and every internal page that uses the marks. — [College Board Trademark Guidelines](https://privacy.collegeboard.org/copyright-trademark/guidelines)
- An informal legal Q&A says descriptive use such as "SAT Prep" is generally allowed under nominative fair use. This is an informal opinion, not authority. — [JustAnswer IP Q&A](https://www.justanswer.com/intellectual-property-law/bz290-small-tutoring-center-help-students-prepare.html)
- The SAT Suite Question Bank holds 3,500+ questions from the SAT, PSAT/NMSQT, PSAT 10, and PSAT 8/9, and educators use it to build custom sets. — [College Board Question Bank overview](https://satsuite.collegeboard.org/k12-educators/tools-resources/question-bank/overview). A 2020 Michigan DOE FAQ says it is publicly accessible without an account. — [Michigan DOE FAQ](https://www.michigan.gov/documents/mde/SAT_Suite_Question_Bank_FAQs_687827_7.pdf)
- Bluebook practice tests are promoted as free official practice. I found no reuse license. — [College Board free practice resources PDF](https://satsuite.collegeboard.org/media/pdf/sats-free-official-practice-resources.pdf)

**Khan Academy**
- Khan Academy content outside its site is governed by CC BY-NC-SA and its Terms of Service. Its own example says charging more because Khan materials are involved breaks the non-commercial clause. Linking to Khan Academy is generally fine. — [Khan Academy Help: Can I use Khan Academy's videos/name/materials](https://support.khanacademy.org/hc/en-us/articles/202262954-Can-I-use-Khan-Academy-s-videos-name-materials-links-)
- Attribution must not imply endorsement, and you may not combine your brand with Khan Academy's name. — [Khan Academy Trademark and Brand Usage Policy](https://support.khanacademy.org/hc/en-us/articles/202263034-Trademark-and-Brand-Usage-Policy)
- The ToS reportedly limits the services to personal, non-commercial use unless Khan gives written permission. This comes from a third-party excerpt. — [ConductAtlas excerpt](https://conductatlas.com/platform/khan-academy/khan-academy-terms-of-service/provision/CA-P-028120/no-commercial-use-of-services-without-written-permission/)

**Desmos (Desmos Studio)**
- The free trial tier covers only personal, non-commercial use or a 90-day internal testing period. "Commercial use" includes any production use by end users, or any internal business use. — [Desmos API Terms](https://www.desmos.com/api-terms)
- To use the API beyond the trial, you must upgrade through self-service or sign a written Commercial Addendum by emailing partnerships@desmos.com. The addendum sets fees, term, included Desmos Studio products, and the covered application. — [Desmos API Terms](https://www.desmos.com/api-terms); [Desmos Help: API Plans for Commercial Use](https://help.desmos.com/hc/en-us/articles/49078363315725)
- The published Starter plan costs about $100–$300/month, tiered by users (up to 1,000 / 2,500 / 5,000), and is Desmos-hosted only. Enterprise is custom-priced and adds self-hosting and premium support. — [Desmos API page / my-api](https://www.desmos.com/my-api). One third-party review says pricing is unpublished, which conflicts with Desmos's own page. — [itqlick](https://www.itqlick.com/desmos)
- Desmos describes its business model as paid partnerships with publishers, assessment companies, and institutions, all under the API ToS. — [desmosinc/policies FAQ (GitHub)](https://github.com/desmosinc/policies/blob/main/faqs.md)

**Gemini API / Google Cloud generative AI**
- Gemini API Additional Terms: "You must be 18 years of age or older to use the APIs." They also prohibit use in an "API Client directed towards or likely to be accessed by individuals under the age of 18." — [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms) (search result reports the page was last modified April 2026)
- Google Cloud Service Specific Terms §17(d) (Generative AI) say the Customer "will not, and will not allow End Users to, use a Generative AI Service as part of a website, Customer Application, or other online service that is directed towards or is likely to be accessed by individuals under the age of 18." The page now calls Vertex AI "Gemini Enterprise Agent Platform (formerly Vertex AI)." — [Google Cloud Service Specific Terms](https://cloud.google.com/terms/service-terms)
- A Google developer-forum reply says the Gemini API age restriction applies however you access it, including through Vertex AI. This is a forum post, not policy. — [Google Developer Forums](https://discuss.google.dev/t/question-regarding-age-restrictions-for-the-gemini-api/188060/2). Google declined to give legal guidance on whether routing minors away from Gemini would comply. — [AI Developers Forum thread](https://discuss.ai.google.dev/t/age-restriction-under-18-is-routing-minors-away-from-gemini-api-acceptable/188423)
- Other teams have treated this as a hard blocker that forces them to change LLM vendor. — [GitHub issue, BOOKIT project](https://github.com/AI-X-16-1/BOOKIT/issues/54)
- Google does give teens Gemini through Google Workspace for Education, as a first-party app with an age-restricted experience. That is a different product, not a developer API carve-out. The Google AI Pro for Education add-on is 18+ only. — [Workspace Updates blog](https://workspaceupdates.googleblog.com/2024/10/gemini-app-access-for-teen-students-workspace-education.html); [AI Pro for Education help](https://knowledge.workspace.google.com/admin/generative-ai/workspace-with-gemini/ai-pro-for-education)
- Data use: under "Unpaid Services" (free tier and AI Studio), Google may use prompts and outputs to improve products, human reviewers may read them after they are disconnected from the account, and the terms warn against submitting sensitive or personal information. Under Paid Services, Google says it does not use prompts or responses to improve products and keeps logs for a limited time for abuse detection and legal purposes. — [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms); [Gemini API data logging policy](https://ai.google.dev/gemini-api/docs/logs-policy)

### Inferences
- Build all question content from scratch: original, SAT-style items. You can align to College Board's *published content domains and skill descriptions*, since facts and test specifications are not copyrightable expression, but you may not copy items, passages, or figures. Do not feed official items into Gemini prompts, few-shot examples, or retrieval (RAG). College Board's explicit no-generative-AI statement makes that a high-risk move. LAWYER for any "inspired by" workflow.
- Use naming such as "[Brand] — Digital SAT Math Prep," never "SAT [Brand]" or College Board-style visual branding. Put the non-affiliation footnote on every page that says "SAT." Link out to Bluebook and the Question Bank instead of embedding them.
- Link to Khan Academy's free official SAT resources, but do not embed or copy their content in a paid product.
- Budget for the Desmos Starter tier. The 90-day trial covers development only.
- Gemini decision: as written, the Google terms make Gemini a poor fit for a product aimed at high schoolers, most of whom are 14–17. Options, all needing LAWYER review and/or written confirmation from Google:
  (a) Ask the Google Cloud account team for a written exception or enterprise agreement.
  (b) Use a different LLM provider whose terms allow 13–17 users with safeguards. Those terms were not researched here and need verification.
  (c) Restrict the product to 18+ verified users. This does not fit the market and may still fail "likely to be accessed by."
  If you use Gemini at all, use only Paid Services (billing on), never the free tier. Minors' data on the free tier could be human-reviewed and used for training, which is incompatible with COPPA and state student-privacy norms.

### Gaps
- I could not fetch the live text of the Gemini terms, the Desmos API terms, or the College Board pages because the proxy blocked them. Quotes come from search-result excerpts.
- I found no explicit Question Bank terms of use. I found no attribution or logo requirements for Desmos embeds; check the API terms.
- I did not research the minimum-age and minors terms of alternative LLM providers (OpenAI, Anthropic, etc.). This is critical for vendor choice.
- I found no confirmed exception for education apps in Google's terms.

## Privacy for minors: COPPA, state student-privacy laws, FERPA, and age gating

### Takeaway
The amended COPPA Rule took effect June 23, 2025, with general compliance required by **April 22, 2026**, which has passed. COPPA covers only under-13 users, but a teen SAT product will reach some 12-year-olds unless it age-gates. If you go direct-to-consumer, use a neutral age screen, block or route under-13s through verifiable parental consent, and plan for California's opt-in rules for selling or sharing data of under-16s. If you go through schools, add FERPA's "school official" contract requirements and SOPIPA's K-12 restrictions.

### Cited Findings
- Amended COPPA Rule: effective June 23, 2025. Regulated entities must comply by April 22, 2026, except §312.11(d)(1), (d)(4), and (g), which cover safe-harbor programs. — [Federal Register, 2025-05904](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule)
- Safe-harbor programs had an October 22, 2025 deadline. "Personal information" now includes biometric identifiers such as face templates, fingerprints, retina scans, and voiceprints. Privacy notices must give the identities and categories of third parties that receive data. — [BBB Programs](https://bbbprograms.org/media/insights/blog/coppa-amended); [Cullen LLP](https://www.cullenllp.com/blog/ftc-publishes-coppa-rule-amendments/)
- The FTC signaled active enforcement. A February 25, 2026 FTC Policy Statement limits enforcement when children's data is collected only for age verification before parental consent is obtained. — [Davis Polk client update (Apr 16, 2026)](https://www.davispolk.com/index%2ephp/print/pdf/node/116375) (via search summary)
- SOPIPA (Cal. Bus. & Prof. Code §§22584–22585) bars K-12 operators from targeted advertising based on student data, from building student profiles for non-K-12 purposes, and from selling student information. — [FPF SOPIPA Guide](https://fpf.org/wp-content/uploads/2016/11/SOPIPA-Guide_Nov-4-2016.pdf)
- CCPA: opt-out of sale for consumers, but opt-in for minors under 16. — [CA Assembly AB 801 analysis](https://apcp.assembly.ca.gov/sites/privacycp.assembly.ca.gov/files/AB%20801%20(Joe%20Patterson)%20APCP%20analysis.pdf). CCPA applies only above its thresholds, for example $25M+ revenue or 100,000+ consumers. — [Cybernut](https://www.cybernut.com/blog/what-to-know-about-the-california-consumer-privacy-act-ccpa-for-schools) (secondary)
- FERPA school-official exception: the vendor must serve a "legitimate educational interest," perform a service the school would otherwise perform, and be under the school's "direct control." School authorization under COPPA covers educational purposes only, never advertising or commercial profiling. — [Edlink: 5 student privacy laws](https://ed.link/community/student-privacy-laws-edtech-developers-need-to-know/); [privacylawmap FERPA vs COPPA](https://privacylawmap.com/blog/ferpa-vs-coppa-compliance-student-data-privacy-guide)

### Inferences
- Age gate: ask for date of birth neutrally at signup, without hinting at an "eligible" age, and don't let users retry with a different date. Under 13: block, or collect a parent's email for verifiable parental consent before creating an account. 13–17: create the account with parental notice. A parent-paid checkout is the natural place for consent and payment. Collect only what you need: first name, email, DOB year, and progress data.
- Treat tutor chat logs as student personal information. Don't use them for ads, don't sell them, set short retention, and offer deletion. Turn off training and data sharing on every vendor (LLM, analytics, error logging). Name every third-party recipient in the privacy policy, as the amended COPPA Rule requires.
- Avoid voice, camera, and face features, which are biometric under the amended COPPA definition.
- A school channel (district contracts) brings FERPA and SOPIPA data-processing agreements and state DPAs. Defer it until there is legal capacity. LAWYER: privacy policy, terms of service, and COPPA/CCPA/SOPIPA applicability to a direct-to-consumer teen product.

### Gaps
- I did not verify whether SOPIPA reaches a purely direct-to-consumer product marketed to students. That turns on "K-12 school purposes," so it needs counsel.
- I did not research newer state laws: age-appropriate design codes, app-store age-verification laws in UT and TX, or state AI-companion and chatbot laws for minors. Several of these may apply to a teen AI chat product in 2026.
- I did not confirm the exact text of the CPPA's minors regulations.

## Tech stack options for the AI tutoring web app (2026)

### Takeaway
The pragmatic stack is: Next.js/React frontend with the Desmos API embed and KaTeX for math; a server-side LLM orchestration layer that holds the system prompt, tool calls, safety filtering, and per-user rate limits; managed auth plus Postgres (Supabase) or Firebase (Auth + Firestore) for progress data; and Stripe for parent-paid subscriptions. Firebase AI Logic gives easy Gemini access, but it is tied to Gemini, which carries the under-18 terms problem. Keep the LLM layer provider-agnostic so you can switch vendors.

### Cited Findings
- Firebase AI Logic enforces a per-user quota on "Generate content requests," per user per region per minute. The default is 100 RPM per user, applied project-wide. You can't set different limits for specific users. The Gemini provider's own limits take precedence. — [Firebase AI Logic: Rate limits and quotas](https://firebase.google.com/docs/ai-logic/quotas?api=vertex)
- Community guides recommend Firebase App Check (reCAPTCHA v3 on web) to protect client-side AI Logic calls before production. This is a secondary source. — [vibeindex Firebase AI Logic skill](https://www.vibeindex.ai/skills/just-mpm/conformai/firebase-ai-logic)
- Desmos Starter is hosted by Desmos, so the calculator script loads from Desmos's CDN with an API key. Self-hosting requires Enterprise. — [Desmos API plans](https://www.desmos.com/my-api)

### Inferences
These are architecture recommendations, not sourced facts.
- **Frontend:** Next.js (App Router) + React + TypeScript. Embed Desmos via `Desmos.GraphingCalculator(el, options)` and use `getState`/`setState`/`setExpression` so the tutor can read the student's graph and put up scaffolds. Render math with KaTeX (faster for SSR and streaming) and use MathJax only if you need wider LaTeX coverage. Stream tutor responses with SSE, for example through the Vercel AI SDK, which has provider adapters and helps keep the LLM vendor swappable.
- **Orchestration:** server-only route handlers or a small Cloud Run/Node service. The client must never call the LLM with a raw key. Define tools such as `check_answer` (deterministic grader, never the LLM), `get_hint(level)`, `set_desmos_expression`, and `log_misconception`. Store canonical answers and solutions in the database. The LLM explains, and code grades.
- **Data:** Supabase (Postgres + Auth + row-level security) suits relational progress data: items, attempts, skill mastery, spaced-repetition schedule, error log. Firebase (Auth + Firestore + AI Logic) is the Google-native alternative. Either way, sign a DPA and turn off vendor analytics on minors' data.
- **Payments:** Stripe Checkout and Billing, with the parent as payer. That also gives a natural point for parental consent and notice.
- **Cost control:** cache static explanations per item, use context and prompt caching for the long shared system prompt, cap tokens per turn, set daily per-user message quotas, route easy tasks to a smaller model, and use an Elo/IRT engine (not the LLM) to pick the next item.
- **Safety:** use the provider's safety settings plus your own input/output moderation, keep the tutor on topic through the system prompt and a classifier, filter PII, escalate self-harm content to resources, and keep audit logs with short retention.
- **Hosting:** Vercel (frontend) + Supabase, or all-in on Firebase Hosting/App Hosting + Cloud Run on Google Cloud.

### Gaps
- I did not retrieve current docs for Genkit, Vercel AI SDK Google-provider streaming, Supabase pricing, Stripe's handling of minors, Gemini context-caching prices, or Desmos API embed/attribution specifics. These were out of tool-call budget.

## Learning-science design for test prep, and evidence on AI tutors

### Takeaway
Evidence supports retrieval practice, spacing, and interleaving, all of which fit SAT math practice well. The strongest warning comes from a high-school math RCT: an unguarded ChatGPT-style helper raised practice scores and then *lowered* unassisted exam scores by 17%. A hint-based "GPT Tutor" with guardrails removed that harm. Design the tutor to be Socratic and answer-withholding by default, and grade with code.

### Cited Findings
- **Bastani et al., PNAS (July 2025), ~1,000 Turkish high-school math students.** Practice performance rose 48% with GPT Base and 127% with GPT Tutor. On the unassisted exam, GPT Base students scored 17% lower than controls, and GPT Tutor students were no different from controls. GPT Base users believed they had learned as much as their peers. — [SSRN preprint](https://papers.ssrn.com/abstract=4895486); [Wharton Knowledge](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education); [PsyPost](https://www.psypost.org/unrestricted-generative-ai-harms-high-school-math-learning-by-acting-as-a-crutch/)
- **Kestin, Miller et al., Scientific Reports (June 2025), Harvard intro physics, N=194, crossover design.** A carefully prompted AI tutor at home produced about twice the learning gains of in-class active learning, in less time: median ~49 min vs 75 min. Limits: two topics, one institution, short-term outcomes only. — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- **World Bank Nigeria (Benin City), 6-week after-school GPT-4 (Microsoft Copilot) English tutoring RCT in 9 schools.** +0.31 SD on the combined assessment and +0.23 SD on English, the primary outcome. It is a working paper, and the "1.5–2 years of learning" framing is disputed. — [World Bank working paper 11125 (RePEc)](https://ideas.repec.org/p/wbk/wbrwps/11125.html); [World Bank blog](https://blogs.worldbank.org/en/education/people-centered-ai-in-education--five-lessons-from-the-global-so)
- **Tutor CoPilot (Stanford RCT, 700+ tutors, ~1,000 students).** Students whose tutors had AI assistance were 4 percentage points more likely to master math topics, and 9 points more for lower-rated tutors, at about $20 per tutor per year. — [NSSA Stanford](https://nssa.stanford.edu/studies/tutor-copilot-human-ai-approach-scaling-real-time-expertise)
- **Khanmigo.** The evidence is mixed and the reported numbers conflict. NBER WP 35620 (Oreopoulos & Low, 2026), a two-year school experiment, found low engagement: the median student messaged on only about a third of practice days, and engagement was the binding constraint. A 0.34 SD figure circulates unverified. A WestEd 0.15 SD figure is second-hand. — [NBER w35620](https://www.nber.org/papers/w35620); [summary](https://plainai.aguidetocloud.com/changes/khanmigo-classroom-results/)
- **Interleaving.** Several classroom RCTs show higher math test scores when practice problems are mixed. Only 9.7% of problems in six common math textbooks were interleaved. — [Rohrer et al., Educ Psychol Rev 2020](https://link.springer.com/doi/10.1007/s10648-020-09516-2). Spaced and interleaved math practice each produced benefits in randomized studies and need no teacher training. — [Rohrer & Hartwig chapter (UNH)](https://www.unh.edu/teaching-learning-resource-hub/sites/default/files/media/2023-06/itow-spaced-and-interleaved-mathematics-practice-rohrer-hartwig.pdf)

### Inferences
These are design recommendations.
- **Tutor policy:** attempt first, then graduated hints (nudge → strategy → worked step → full solution), shown only after a committed attempt or explicit give-up. Never reveal the answer before an attempt. Require the student to explain or redo a similar item after seeing a solution. This copies the guardrails that removed the harm in Bastani et al.
- **Session loop:** a short retrieval warm-up of spaced review items from past errors; new-skill instruction using a worked example followed by faded examples; mixed (interleaved) practice; and timed mixed mini-modules that mimic the adaptive digital SAT.
- **Mastery and knowledge tracing:** use per-skill Elo or a 1–2PL IRT to calibrate both item difficulty and student ability (simple to run online), or BKT per skill for mastery gates. Pick the next item with a target success rate of about 70–85%. The LLM never decides mastery.
- **Error log:** tag each wrong answer with a misconception (LLM-suggested, from a fixed taxonomy). Resurface errors on an SM-2/FSRS-style schedule.
- **Desmos:** the digital SAT includes a built-in Desmos calculator, so teach Desmos strategies explicitly (intersections, regressions, systems). Pair each with a "no-calculator first" mental estimate to guard against over-reliance. Measure over-reliance with an occasional calculator-off check item.
- **Engagement:** the Khanmigo NBER finding says use is the bottleneck. Build in streaks, short sessions, and parent progress emails, but keep them consistent with privacy rules.

### Gaps
- I did not verify Dunlosky et al. (2013) utility ratings from the primary source. I found no SAT-specific RCTs of AI tutors. I found no direct evidence on calculator over-reliance with Desmos on the digital SAT.

## Item generation: LLM-written original SAT-style questions with verified answers

### Takeaway
LLMs can draft original SAT-style math items, but they produce flawed questions often enough that you need a verification pipeline. Cross-model checking roughly doubles flaw detection compared with self-checking. Add programmatic checks and a human review before items reach students.

### Cited Findings
- Cross-LLM verification ("Cross-CoVe") flagged 63.6% of flawed MCQs vs 27.3% for self-verification (p = 0.002). — [IEEE Access 2025, PolyU CPCE](https://profile.cpce-polyu.edu.hk/en/publications/automatic-generation-of-high-quality-mcqs-with-llms-for-artificia-2/)
- ValiMath is a benchmark of 2,147 human-verified math questions annotated for whether the *question itself* is well-posed. Question validity is a separate failure mode from wrong answers. — [arXiv 2505.13903](https://arxiv.org/pdf/2505.13903v2)
- CompMath-MCQ validates items through cross-LLM disagreement followed by expert review, so no single model serves as the oracle. — [arXiv 2603.03334](https://www.alphaxiv.org/abs/2603.03334)

### Inferences
- **Pipeline:**
  1. Generate items from a skill spec plus a template, with parameterized numbers, using College Board's public skill taxonomy and not official items.
  2. The generator outputs the stem, the key, a worked solution, and one distractor per misconception.
  3. A deterministic check runs SymPy/Python on the key, confirms exactly one correct option, and validates grid-in (student-produced response) answer formats.
  4. A second, different model solves the item blind, and any disagreement is flagged.
  5. A uniqueness and plagiarism check uses embedding similarity against any known public items, to avoid near-copies.
  6. A human reviews items before release.
  7. After release, calibrate difficulty with Elo/IRT from real responses and retire items with odd statistics, such as negative discrimination.
- Prefer templated or parametric generation, where code computes the answer, for algebra and advanced math. Reserve free-form LLM generation for word problems and data-analysis contexts.
- Keep provenance logs showing each item is original. That helps if College Board ever raises a copyright claim. LAWYER on IP ownership of AI-generated items and any vendor-terms output restrictions.

### Gaps
- I found no published study specific to LLM-generated *SAT* math items or their psychometric equivalence to official items.
