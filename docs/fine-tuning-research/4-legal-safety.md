# 4. Rules that constrain fine-tuning and deployment (legal and safety)

_Researched 2026-10-16 for the SAT Math tutor plan (`docs/fine-tuning-plan.md` §1, `HANDOFF.md`, `docs/phase0/`). **Not legal advice.** I am not a lawyer; every "counsel" tag below means a lawyer must confirm before we rely on it._

**How sources were checked.** "Opened" means I fetched the page itself on 2026-10-16 and the quote is from it. "Search summary" means the network proxy blocked the page (ftc.gov, federalregister.gov, alibabacloud.com, help.aliyun.com, qwencloud docs, leginfo, openai.com, most law-firm sites all returned 403/DNS errors) and the wording comes from a search engine's summary of that page: treat it as **unverified** until someone opens the link.

Risk levels: **BLOCKER** (plan as written cannot proceed), **MUST-DO** (required before the named milestone), **NICE-TO-HAVE**.

---

## Q1. Anthropic: may Sonnet outputs train our open-weight tutor? Minors?

**Answer: No, not without Anthropic's prior written authorization.** This is the single biggest finding. Anthropic's Usage Policy bans using outputs to train any AI model without prior authorization; it is not limited to "competing" models. The Commercial Terms separately bar using the Services "to train competing AI models". A narrow SAT tutor is arguably not "competing", but the Usage Policy clause applies regardless, and Commercial Terms incorporate the Usage Policy.

| Source | Quote | Status |
|---|---|---|
| [Usage Policy](https://www.anthropic.com/legal/aup) (version effective Nov 12, 2026), "Do Not Abuse Our Platform" | "Use outputs to train an AI model (e.g., "model scraping" or "model distillation") without prior authorization from Anthropic" | Opened 2026-10-16 |
| [Usage Policy, prior version](https://www.anthropic.com/legal/archive/22742366-2ef0-4c7a-a833-6523f10d3944) (effective Sep 15, 2025; the version in force today) | "Utilization of inputs and outputs to train an AI model (e.g., "model scraping" or "model distillation")" (without prior authorization) | Opened 2026-10-16 |
| [Commercial Terms](https://www.anthropic.com/legal/commercial-terms) §D.4 (effective June 17, 2025) | "Customer may not and must not attempt to (a) access the Services to build a competing product or service, including to train competing AI models or resell the Services except as expressly approved by Anthropic" | Opened 2026-10-16 |
| Commercial Terms §B | Customer "owns its Outputs" (subject to compliance with the Terms) | Opened |
| [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) §2–3 (effective Oct 8, 2025) | 18+ only; may not use the Services to "develop or train any artificial intelligence or machine learning algorithms or models" | Opened. Not our contract (we use the API), listed only so nobody uses a claude.ai subscription for generation |

What this means for the pipeline:
- **Sonnet-written tutoring dialogues used as SFT data = BLOCKER** unless Anthropic authorizes it in writing. Owning outputs (§B) does not override the use restriction.
- **Sonnet judge scores / preference labels used for DPO/RFT** are also "outputs" used to train: same problem (counsel to confirm; I read it as covered).
- **Allowed without authorization (my reading):** Sonnet as solver/verifier for item keys, as the eval judge for a model trained on non-Anthropic data, and as an interim live tutor.
- Options: (a) ask Anthropic (account team / support) for written authorization naming the use: "fine-tune a small open-weight model, for our own SAT tutoring product only, weights not distributed"; (b) generate training dialogues with a model whose license permits it (self-hosted Qwen3 / gpt-oss-120b, Apache-2.0) and use Sonnet only to verify math and to evaluate; (c) owner-written / human-edited dialogues. Pick before any generation spend.

**Minors (Anthropic).** Allowed with safeguards. Minor = under 18.
- [Usage Policy](https://www.anthropic.com/legal/aup): "Products serving minors, including organizations providing minors with the ability to directly interact with [our] API-based products, must comply with the additional guidelines outlined in our Support article and all applicable laws"; "We define a minor or child to be any individual under the age of 18 years old, regardless of jurisdiction." Also: consumer-facing chatbots must disclose they are AI, "at a minimum at the beginning of each chat session or in the product interface". Opened.
- [Guidelines for Organizations Serving Minors](https://support.claude.com/en/articles/9307344-responsible-use-of-anthropic-s-models-guidelines-for-organizations-serving-minors) (updated Mar 16, 2026): should implement "Age verification systems", "Content moderation and filtering", "Monitoring and reporting mechanisms", "Educational resources and guidance for minors"; organizations serving minors "should implement" Anthropic's child-safety system prompt; "Organizations must disclose to their users that they are interacting with an AI system rather than a human"; must comply with COPPA; "Anthropic will periodically audit organizations for compliance". Opened. No pre-approval needed.

**Risk:** training on Sonnet outputs **BLOCKER**; minors safeguards while Sonnet serves live **MUST-DO before launch**. Counsel: confirm reading of "outputs" (does a judge score count?) and whether the written authorization we get is sufficient.

---

## Q2. Alibaba Cloud / QwenCloud / Model Studio (interim live tutor Qwen3.7-Plus)

**Could not open any Alibaba page** (all blocked). Everything here is **unverified search-summary** content. Must be read by a human before minors touch it.

- **Minimum age / minors: likely a problem.** The Alibaba Cloud International privacy policy reportedly says: "The Alibaba Cloud Platform and the Cloud Services are not intended for minors (persons under the age of 18). Minors must not use the Alibaba Cloud Platform and the Cloud Services for any purpose." ([privacy policy](https://www.alibabacloud.com/help/zh/legal/latest/alibaba-cloud-international-website-privacy-policy-0423), [FAQ 42425](https://www.alibabacloud.com/help/doc-detail/42425.htm); search summary). Whether "use the Cloud Services" reaches **end users of our app** (vs. the account holder) is unresolved; it is the same shape of clause that blocked Gemini. QwenCloud has its own [Customer Agreement](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260319165752650/20260319165752650.html) (dated Apr 2, 2026, contracting entity Alibaba Cloud (Singapore) Pte Ltd for most customers); its age clause was not retrievable. Model Studio [service-specific terms](https://help.aliyun.com/en/model-studio/bailian-service-notes) put liability for generated content on the customer. No minors-in-apps guidance (like Anthropic's) was found.
- **Training on prompts:** Model Studio FAQ reportedly says customer data "is never used for model training" ([FAQ](https://www.alibabacloud.com/help/doc-detail/2587658.html)); QwenCloud security docs reportedly say API inputs/outputs are not used to train ([data security](https://docs.platform.qianwenai.com/developer-guides/security-compliance/data-security)). Search summary only.
- **Retention:** no retention period in days found; a "Zero data retention" doc section is referenced but not retrieved; one third-party tracker says no ZDR toggle is documented. Unverified.
- **Region:** per the [regions page](https://help.aliyun.com/en/model-studio/regions/), region sets where static data (inputs and outputs) is stored; deployment scope sets where inference runs. US (Virginia) offers "Global" (any node, including inside China) or "US" scope; localized pages say a `-us` model suffix (e.g. `qwen-plus-us`) keeps inference in the US. Singapore is the default international region. Search summary.
- **Using Qwen-Plus outputs to train our model:** no clause found either way. Unverified.

**Risk: MUST-DO before any student uses the Qwen interim tutor, possible BLOCKER.** Actions: open the Customer Agreement, privacy policy and service terms and search "minor", "18", "age", "train", "retain"; email Alibaba Cloud sales for a written answer on (1) apps used by 13–17 (and under-13 with parental consent), (2) retention/ZDR, (3) US-only processing; pick US scope/`-us` model if available. Counsel: Chinese-parent vendor processing US minors' data may also raise state-law and parent-trust issues; name it in the privacy notice. Keep `TUTOR_PROVIDER=anthropic` as the launch default until this is answered.

---

## Q3. Open-weight licenses (the fine-tuned tutor)

| Model | License / policy | Minors / education restrictions | Status |
|---|---|---|---|
| Qwen3 (open weights) | [QwenLM/Qwen3](https://github.com/QwenLM/Qwen3): "All our open-weight models are licensed under Apache 2.0." | None in Apache-2.0. Alibaba's [AI governance page](https://www.alibabagroup.com/en-US/ai-governance/governance) bans using Qwen to target/exploit minors (policy, not license) | Opened 2026-10-16. Check the **specific checkpoint's** LICENSE on its model page: some past Qwen sizes shipped under a separate "Qwen License" (huggingface.co was blocked, unverified for the chosen size) |
| gpt-oss-20b / 120b | Apache-2.0 + [USAGE_POLICY](https://github.com/openai/gpt-oss/blob/main/USAGE_POLICY): "We aim for our tools to be used safely, responsibly, and democratically, while maximizing your control over how you use them. By using OpenAI gpt-oss-120b and gpt-oss-20b, you agree to comply with all applicable law." | None beyond "comply with all applicable law" (which pulls in COPPA etc.) | Opened |
| Phi-4 | MIT per [model card](https://huggingface.co/microsoft/phi-4) (search summary; HF blocked). Card asks developers to evaluate accuracy/safety before high-risk use and follow privacy law | None | Unverified; NVIDIA NGC mirror lists a different license, so take weights from Microsoft's own repo |

**Risk: NICE-TO-HAVE (record license + version in the model card).** Licenses are not the constraint; the constraint is that a self-hosted model has no vendor safety backstop (already noted in `fine-tuning-plan.md` §1). Hosting vendor (Together/Fireworks/AWS) terms still apply and were not researched here.

---

## Q4. US law for an AI tutor used by minors

**COPPA (under 13). MUST-DO before launch if any under-13 can get in.**
- Amended rule: published Apr 22, 2025 ([Federal Register 2025-05904](https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule), [PDF](https://www.govinfo.gov/content/pkg/FR-2025-04-22/pdf/2025-05904.pdf)); effective June 23, 2025; compliance date **Apr 22, 2026** (passed). Search summary; page blocked.
- Separate consent for third-party disclosure (§312.5(a)(2)) and the AI point, preamble: "Disclosures of a child's personal information to third parties for monetary or other consideration, for advertising purposes, or to train or otherwise develop artificial intelligence technologies, are not integral to the website or online service" and so need **separate verifiable parental consent**; disclosures "necessary to provide the product or service the consumer is asking for are integral". Search summary of the Federal Register text; see also [Data Protection Report](https://www.dataprotectionreport.com/2025/06/ftcs-coppa-rule-changes-include-ai-training-consent-requirement/).
- Notice must name third-party recipients (by name or category) and purposes; written data-retention policy; no indefinite retention ([Commissioner Bedoya statement](https://www.ftc.gov/system/files/ftc_gov/pdf/bedoya-coppa-statement-2025-01-16.pdf) ties this to AI training-data hoarding). Search summary.
- Enforcement precedent: [WW/Kurbo (2022)](https://www.ftc.gov/news-events/news/press-releases/2022/03/ftc-takes-action-against-company-formerly-known-weight-watchers-illegally-collecting-kids-sensitive): $1.5M penalty, delete children's data **and destroy "any algorithms or work product derived from"** it. A model fine-tuned on improperly collected under-13 chats can be ordered deleted.
- FTC [EdTech policy statement (2022)](https://www.ftc.gov/system/files/ftc_gov/pdf/Policy%20Statement%20of%20the%20Federal%20Trade%20Commission%20on%20Education%20Technology.pdf): edtech may not use children's data collected for education for unrelated purposes, and must not retain it longer than needed. Search summary.

**FERPA. NICE-TO-HAVE now; MUST-DO only if we sell to schools/districts.** FERPA binds schools; a vendor gets records only under the "school official" exception (direct control, legitimate educational interest). DTC sales to parents are outside it. Not re-verified today (ed.gov blocked); see counsel group 6.

**SOPIPA (Cal. Bus. & Prof. Code §22584).** Applies to operators whose service is "used primarily for K-12 school purposes and was designed and marketed for K-12 school purposes"; "Operators do not need to have a contract with a school" ([FPF SOPIPA guide](https://fpf.org/blog/fpf-guide-student-data-protections-sopipa-k-12-school-administrators-ed-tech-vendors/), search summary). A DTC SAT-prep site is probably outside, but marketing through schools could pull it in. If it applies: no targeted ads, no profiling for non-school purposes, no sale; (counsel: whether training our own model on student data is a permitted "K-12 school purpose"). **MUST-DO counsel question.**

**California SB 243 (companion chatbots), in force Jan 1, 2026.** Covers AI that gives "adaptive, human-like responses", "is capable of meeting a user's social needs" and can "sustain a relationship across multiple interactions". Exclusion is for "A bot that is used only for customer service, a business' operational purposes, productivity and analysis related to source information, internal research, or technical assistance" ([Sidley PDF of text](https://www.sidley.com/en/-/media/resource-pages/ai-monitor/laws-and-regulations/cal-sb243-companion-chatbots.pdf?la=en), [LegiScan](https://legiscan.com/CA/text/SB243/2025); search summary). Education is **not** an explicit exclusion. Duties: AI disclosure; for known minors, AI disclosure plus a break reminder every 3 hours; published suicide/self-harm protocol with crisis referrals; annual reporting to the Office of Suicide Prevention from July 1, 2027; private right of action.
**California SB 1119 "Adam's Law", signed Sep 10, 2026, core duties reportedly operative July 1, 2027.** Keeps SB 243's definition (a system "need not be designed specifically for the purpose of companionship", ZwillGen summary); adds suicidal-ideation detection with parent notification for minors, independent child-safety audits (frequency disputed), reported daily usage caps and memory off by default for minors; adds an exclusion for colleges' educational chatbots, **not** K-12 tutoring ([Fenwick](https://www.fenwick.com/insights/publications/california-enacts-comprehensive-child-safety-laws-targeting-ai-chatbots), [Orrick, Oct 2026](https://www.orrick.com/en/Insights/2026/10/Examining-Californias-New-AI-Chatbot-Bill-SB-1119), [ZwillGen](https://www.zwillgen.com/artificial-intelligence/adams-law-california-raises-the-bar-for-child-chatbot-protections/); all search summaries, unverified).
A topic-locked SAT math tutor with no persona and no cross-session "relationship" is plausibly outside "companion chatbot", but not safely so. **MUST-DO: design to be clearly outside (no persona, no social chat, no memory of personal details across sessions) AND meet SB 243 duties anyway (cheap). Counsel to confirm scope for SB 243 and SB 1119.**

**California AB 1064 (LEAD for Kids Act):** passed the Legislature, **vetoed** Oct 2025 ([PolicyRisk tracker](https://policyrisk.com/state-bill/CA-AB1064-20252026)). Successor ballot measure (Common Sense + OpenAI, "Parents & Kids Safe AI Act", announced Jan 9, 2026, [CalMatters](https://calmatters.org/economy/technology/2026/01/california-chatbot-initiatives-merged/)) reportedly put on hold in favour of legislation; SB 1119 appears to be the result. Status unverified. **NICE-TO-HAVE: monitor.**

**Utah AI Policy Act as amended by SB 226 (eff. May 7, 2025; sunset July 2027):** must disclose AI use when a consumer makes a "clear and unambiguous request"; safe harbor if the AI discloses "at the outset of any interaction... and throughout" and "in writing before the start of a written interaction" ([Perkins Coie](https://perkinscoie.com/insights/update/new-utah-ai-laws-change-disclosure-requirements-and-identity-protections-target), [Knobbe chart](https://www.knobbe.com/wp-content/uploads/2025/10/Utah-SB-226-Compliance-Chart.pdf); search summary). Our always-visible AI label satisfies it.

**Other states (2026 wave).** One tracker counts 14 new chatbot-safety laws in 2026 ([Transparency Coalition](https://www.transparencycoalition.ai/news/watershed-year-for-chatbot-safety-measures-14-new-state-laws-enacted-so-far-in-2026)); named states include New York (AI companion crisis protocol + recurring disclosure), Washington HB 2225 (eff. Jan 1, 2027), Colorado, Georgia, Iowa, Idaho, Nebraska, Hawaii, Rhode Island, Oregon ([Bloomberg Law](https://news.bloomberglaw.com/bloomberg-law-analysis/ai-chatbot-laws-are-emerging-as-a-hot-ticket-item-for-states), [MultiState](https://www.multistate.us/insider/2026/4/30/state-childrens-online-safety-laws-expand-beyond-social-media-in-2026)). Common duties: AI disclosure, crisis referral protocol, no sexual content with minors, no emotional manipulation. **Unverified; MUST-DO counsel 50-state scan before launch** (or geo-limit launch).

**FTC 6(b) inquiry (Sep 11, 2025).** Orders to Alphabet, Character Technologies, Instagram, Meta, OpenAI, Snap, xAI on how they "measure, test, and monitor" harms to children and teens, limit minors' use, and comply with COPPA ([FTC release](https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions), [order template](https://www.ftc.gov/system/files/ftc_gov/pdf/AICompanionChatbot6(b)Order.pdf); search summary). Not aimed at us, but it is the FTC's checklist: pre-deployment testing, age limits, monitoring, monetization. **NICE-TO-HAVE: keep evidence of the same (eval reports, red-team logs).**

---

## Q5. Can live student chat logs become fine-tuning data?

**Answer: only with a deliberate consent and data design; default should be "no" at launch.**
- **Under-13:** sending their chats to a third party to train (e.g. a hosted fine-tuning vendor, or Anthropic/Alibaba if they trained) needs **separate verifiable parental consent** (COPPA preamble above). Training **our own** model in-house is not squarely addressed; the "integral to the service" test and the retention rule (keep only as long as necessary for the purpose collected) argue for consent anyway, and Kurbo shows the remedy is model deletion. Counsel must confirm. Treat as separate, optional, revocable parental consent, not bundled with checkout.
- **13–17:** COPPA doesn't apply, but FTC Act §5 (deception: privacy notice must say it), state privacy laws with teen opt-in rules (e.g. CCPA under-16 opt-in for "sale/sharing" if thresholds met), SOPIPA if it applies, and the new chatbot laws (memory/data limits for minors in SB 1119) do. Disclose in the privacy notice before collection; get opt-in from parent (and student assent).
- **Revocation:** if a parent withdraws consent or deletes the account, we must be able to drop that student's data from future training sets; keep a per-example provenance ID so this is possible. Retraining/"unlearning" obligations for an already-trained adapter: counsel.
- **De-identification:** chat logs carry names, schools, emails, self-disclosures. Before any training use: automated PII scrub + human spot check, drop all crisis/self-harm-flagged conversations entirely, strip calculator state of free text, keep only the math dialogue. De-identified data is outside COPPA's "personal information" only if it cannot reasonably identify the child; counsel to confirm the standard. Also the Anthropic clause bars feeding these logs through Sonnet to produce training labels unless authorized (Q1).
- **Retention conflict:** the age-gate plan proposes 90-day chat retention. Training use means keeping data longer → must be stated in the written retention policy.

**Risk: MUST-DO before any production log is used; not needed for the first fine-tune (which uses synthetic dialogues on original items).**

---

## Q6. Content safety for minors: what providers and guidance expect

- **AI disclosure:** required by Anthropic ([AUP](https://www.anthropic.com/legal/aup), at least at start of each session or in the UI), CA SB 243, Utah SB 226 safe harbor. **MUST-DO.**
- **Crisis / self-harm:** SB 243 requires a published protocol that refers users to crisis services (988 Suicide & Crisis Lifeline, Crisis Text Line); SB 1119 adds detection and parent notification for minors (from 2027). OpenAI's [Teen Safety Blueprint](https://openai.com/index/introducing-the-teen-safety-blueprint) (Nov 6, 2025; search summary) expects: identify teens and default to the under-18 experience when unsure, block self-harm depictions, sexual content and graphic violence for minors, parental controls. OpenAI's [under-18 API guidance](https://developers.openai.com/api/docs/guides/safety-checks/under-18-api-guidance) (cited in repo, not re-opened) asks for age-appropriate filters, AI disclosure, escalation path. **MUST-DO:** classifier in front of the model, fixed crisis response (not model-generated), flag to a human reviewer, publish the protocol, parent-notification policy decided with counsel.
- **Anthropic minors guidelines:** age verification, moderation/filtering, monitoring and reporting, child-safety system prompt (while Sonnet is live). **MUST-DO.**
- **Common Sense Media:** rated social AI companions "Unacceptable" for under-18s (Apr 30, 2025, [release](https://commonsensemedia.org/press-releases/ai-companions-decoded-common-sense-media-recommends-ai-companion-safety-standards)); AI teacher assistants "Moderate Risk" (Aug 6, 2025, [release](https://www.commonsensemedia.org/press-releases/ai-teacher-assistants-need-better-safety-measures-common-sense-media-report-finds)). No rating of AI tutors found. Lesson: avoid companion-like traits (persona, flattery, "I missed you", relationship talk). **NICE-TO-HAVE** but cheap; also keeps us outside SB 243/1119 scope.
- **ED toolkit:** [Empowering Education Leaders](https://thejournal.com/articles/2024/10/25/ed-releases-toolkit-for-intentional-use-of-ai-in-education.aspx) (Oct 2024, 74 pp, non-regulatory): transparency, human oversight, privacy, evaluate for bias and accuracy. ed.gov blocked; current status under the 2025+ administration unverified. **NICE-TO-HAVE.**
- **Fine-tune-specific safety:** fine-tuning can erode a base model's refusal behaviour. Include refusal/redirect and crisis-handoff examples in SFT data, and gate release on a red-team eval (self-harm, sexual content, PII solicitation, off-topic social chat, jailbreaks) run on the fine-tuned model, not just the base. **MUST-DO before the fine-tuned model serves minors.**

---

## Checklist: before fine-tuning

- [ ] **Resolve the Anthropic training restriction (BLOCKER).** Either written authorization from Anthropic covering Sonnet-generated dialogues and judge labels as training data for our self-hosted tutor, or switch the generator (and any label source) to a model whose license allows it, keeping Sonnet for verification and evaluation only. Record the decision in `HANDOFF.md`.
- [ ] Counsel confirms our reading of the Usage Policy "outputs" clause and the Commercial Terms §D.4.
- [ ] Training data contains no real student data (synthetic only, on original items); College Board content excluded (already a rule).
- [ ] Base checkpoint's license file read and recorded (Apache-2.0 / MIT / gpt-oss usage policy), plus the model card for the exact size.
- [ ] If a hosted fine-tuning vendor is used: its terms read (no training on our data, retention, region).
- [ ] SFT mix includes refusal, off-topic redirect and crisis-handoff examples; red-team eval set built.

## Checklist: before launch to minors

- [ ] Age gate, parent-paid checkout, under-13 verifiable parental consent per `docs/phase0/age-gate-plan.md`; counsel signs off on the consent method (counsel Q3.3).
- [ ] Privacy notice names every recipient (Anthropic and/or Alibaba/QwenCloud, hosting vendor, Firebase, Stripe, email), purposes, and a written retention policy (COPPA).
- [ ] **Alibaba/QwenCloud:** terms read by a human; written answer on minors, retention/ZDR, US-only scope. Until then, no minors on the Qwen interim tutor (use Sonnet with Anthropic's minors safeguards).
- [ ] Vendor settings: no training on our data, shortest retention, DPA, for every model/hosting vendor.
- [ ] Always-visible "You are chatting with an AI" label, plus disclosure at the start of each session.
- [ ] Topic classifier + fixed crisis response (988 / Crisis Text Line), human flag, published protocol (SB 243); decision on parent notification (SB 1119, from July 2027).
- [ ] No companion traits: no persona, no social chat, no cross-session personal memory; SB 243 3-hour break reminder for known minors.
- [ ] Red-team and tutoring eval passed on the exact model served (fine-tuned or interim), with reports kept.
- [ ] Anthropic child-safety system prompt in use while Sonnet is live.
- [ ] Counsel: SB 243 / SB 1119 scope, 50-state chatbot law scan (or geo-limit), SOPIPA applicability, CCPA teen rules.
- [ ] Chat logs: 90-day (or counsel-set) retention, deletion job working, **not** used for training.

## Checklist: before using live chat logs for training (later)

- [ ] Separate, optional, revocable consent (parent for under-13; parent + student for 13–17), not bundled with checkout; privacy notice and retention policy updated first.
- [ ] Per-example provenance so withdrawn students' data can be excluded from the next training run.
- [ ] PII scrub + human spot check; crisis-flagged conversations excluded; counsel confirms de-identification standard.
- [ ] Logs not passed through any vendor model for labelling unless that vendor's terms allow it (Anthropic: see Q1).
- [ ] Counsel confirms first-party training under COPPA, SOPIPA and SB 1119.

## Open items needing a primary-source read (blocked during this research)

Federal Register COPPA text (§312.5(a)(2), §312.10, preamble on AI); Alibaba Cloud International privacy policy, membership agreement and QwenCloud Customer Agreement (age, training, retention); SB 243 and SB 1119 chaptered text (leginfo.legislature.ca.gov); Phi-4 and chosen Qwen3 checkpoint license on Hugging Face; OpenAI Teen Safety Blueprint PDF; 2026 state chatbot statutes.
