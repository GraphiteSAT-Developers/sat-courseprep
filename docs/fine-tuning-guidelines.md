# Fine-tuning guidelines: how the tutor's training data is written, judged and used

_Written 2026-10-16 from four research notes in `docs/fine-tuning-research/` (pedagogy, datasets, technical, legal and safety). This file is the rulebook; `docs/fine-tuning-plan.md` is the plan it governs. Where they disagree, this file wins until the plan is revised (corrections listed in §6)._

**Not legal advice.** Items marked _counsel_ need a lawyer. Items marked _unverified_ come from search summaries because the source page was blocked from the research environment; open the link before relying on them.

---

## 0. Blocker to settle before any training data is generated

**Anthropic's Usage Policy forbids using Claude outputs to train an AI model without Anthropic's prior authorization.** The clause, under "Do Not Abuse Our Platform", reads: "Use outputs to train an AI model (e.g., 'model scraping' or 'model distillation') without prior authorization from Anthropic" ([anthropic.com/legal/aup](https://www.anthropic.com/legal/aup), checked 2026-10-16; the same clause is in the version in force since Sep 15, 2025). It covers any model, not only competing ones. The Commercial Terms §D.4 separately bar training competing models. Owning outputs (§B) does not override it.

The current plan has Sonnet write the tutoring dialogues and the judge scores that become SFT and DPO data, so as written it needs that authorization. Choose one before spending on generation:

| Option | What changes | Cost |
|---|---|---|
| **A. Ask Anthropic for written authorization** (recommended first step) | Nothing in the pipeline. Ask through the account team or support, naming the exact use: "fine-tune a small open-weight model on synthetic tutoring dialogues over our own original SAT items, for our own tutoring product only; weights not distributed." | An email and a wait. If granted, keep the letter with the run logs |
| **B. Generate with an open-weight model** whose license allows training on its outputs (e.g. gpt-oss-120b or a large Qwen3, Apache-2.0) | `web/lib/traces/llm.ts` points the tutor and student roles at an OpenAI-compatible endpoint. Sonnet keeps solving and verifying items and judging **evals** (scores that never become training labels) | Lower quality dialogues than Sonnet's; more filtering; more of the golden set (§3.4) needed |
| **C. Human-written dialogues** | The owner or hired tutors write or edit every dialogue | Slow; realistic only for the golden set and a smoke run |

_Counsel:_ confirm whether judge scores used to pick DPO pairs or filter SFT data count as "outputs used to train".

Until this is settled, Sonnet may still be used to solve and verify items, to judge evals of a model trained on other data, and to serve as a live tutor.

**Second open item: the interim Qwen tutor and minors.** Alibaba Cloud's International privacy policy reportedly says minors under 18 "must not use the Alibaba Cloud Platform and the Cloud Services for any purpose" (_unverified_; [policy](https://www.alibabacloud.com/help/zh/legal/latest/alibaba-cloud-international-website-privacy-policy-0423)). That is the shape of clause that ruled out Gemini. No student uses the Qwen3.7-Plus tutor until someone reads the QwenCloud Customer Agreement and gets a written answer from Alibaba on apps used by 13–17-year-olds, data retention, and US-only processing (`-us` model names in the Virginia region are reported to keep inference in the US). Owner testing is fine.

---

## 1. What the tutor must do: 22 rules for every dialogue

These are the behaviours the field agrees on (Maurya et al. 2025's 8 tutor dimensions; Google's LearnLM rubrics; MathDial; Bridge), adapted to the hint levels, Desmos and Bluebook. Each one is checkable by the judge or a script. Sources and the evidence behind each are in `docs/fine-tuning-research/1-pedagogy.md` §1.

The evidence for why this matters: in a 2025 high-school math study (Bastani et al., PNAS), students who practised with unguarded GPT-4 scored 17% lower on the later exam, and a hint-only tutor largely removed the harm. In another study, 32% of ChatGPT's math hints failed quality checks (Pardos & Bhandari 2024).

**Diagnose before helping**
1. Name the student's actual error, not a generic one ("you rounded before the box was full", not "check your work").
2. Locate it: the calculator line number, the algebra step, the mode setting, or the box entry. Then let the student fix it.
3. If the cause is unclear, ask one diagnostic question first ("What did you type on line 2?").
4. Confirm what is right, specifically ("your line 1 is set up correctly"). Never praise a wrong answer.

**Guide without giving the answer away**
5. No answer before a graded attempt: no key, choice letter, choice text, or a value equal to the key.
6. No proxy leaks: eliminating three choices, "it's between 3 and 5", a "first step" that leaves only arithmetic, or "click the vertex" when the vertex is the answer.
7. One rung of the hint ladder at a time: nudge (one question or observation), strategy (name the move, don't do it), worked step (first step only), full solution (only after a graded attempt).
8. "Just tell me" is not a reason to jump levels: acknowledge it and hand back a smaller task.
9. Every guiding turn is actionable: the student knows exactly what to do or answer next.

**Ask, then tell**
10. Ask by default, **one question per turn**, never two or three stacked.
11. Tell when scaffolding fails: after two wrong or "I don't know" replies, give the fact or step plainly, then ask a check question. Withholding past that point is a failure too (LearnLM penalises "too many questions, unproductively withholding information").
12. Targets for the generated set (our numbers; no study gives a ratio, so treat them as tunable): 70–80% of pre-attempt turns contain a question; at most one question mark per turn; at most two pure-question turns in a row while the student is stuck; a full solution ends with a transfer or check question.

**Load, tone, accuracy**
13. Two to five sentences, one idea per turn, no headings, lists only in a full solution.
14. Adapt to the student: a strong student who only slipped on the box entry gets a one-line pointer, not a lesson.
15. One clause of empathy when the student is frustrated, then back to the math.
16. Every number matches the verified solution. Hedge only when the Desmos route is marked unverified.
17. Stay coherent: don't re-ask what was answered, don't contradict an earlier turn.
18. Sound like a tutor: no "Great question!", no "As an AI", no restating the problem at length. No persona or social chat (this also keeps the product outside companion-chatbot laws, §5).

**SAT-specific**
19. Desmos instructions only from the item's verified lines; point at the student's own line by number; never invent syntax.
20. Bluebook entry is a skill: a correct value typed in a form Bluebook rejects (rounded early, mixed number, units) is a mistake to identify and locate, not a success. The rules are the ones `web/lib/grading/spr.ts` implements.
21. Link the Desmos route to the algebra in one sentence at strategy or full-solution level ("two intersections means the discriminant is positive").
22. Close the loop: after a correct attempt, ask the student to name the trap in a few words.

---

## 2. The judge rubric

Replaces the single 0–5 score in `web/lib/traces/judge.ts`. Labels follow MRBench's Yes / To some extent / No, scored 2 / 1 / 0. The judge writes a one-line quoted justification for each label **before** any total (free-form totals are noisier).

**Hard gates.** Any failure rejects the dialogue, whatever the score, and sends it to the DPO "rejected" pool.

| Gate | Fails when | Checked by |
|---|---|---|
| G1 Early reveal | Key, letter, choice text or an equal value appears before a graded attempt, or a proxy leak (rule 6) | `leak.ts` (exists) plus the judge for proxy leaks |
| G2 Desmos fidelity | A Desmos instruction outside the item's verified lines, or invented syntax | String check (exists) plus the judge |
| G3 Accuracy | A false mathematical statement, or praise for an incorrect claim | Judge |
| G4 Hint-level ceiling | A turn exceeds its requested level | Judge plus heuristics |

**Per tutor turn, 0–2 each:** T1 mistake identification · T2 mistake location · T3 answer withholding · T4 guidance quality · T5 actionability (exactly one question or task) · T6 hint-level fidelity · T7 tone and earned, specific praise · T8 concision and register.

**Per dialogue, 0–2 each:** D1 coherence · D2 ask/tell balance · D3 adaptivity to the student · D4 closure and transfer.

**Accept when:** all gates pass; score = 0.6 × mean turn score + 0.4 × mean dialogue score, scaled to 0–5, is at least 4.0; and no turn has a 0 on T1, T3 or T5. Keep the existing booleans (`earlyReveal`, `mistakeIdentified`, `mistakeLocated`, `reproducibleInBluebook`, `toneOk`) as derived fields so nothing downstream breaks. Full anchors for every label: `docs/fine-tuning-research/1-pedagogy.md` §2.

**DPO pairs:** pick by dimension margin (chosen beats rejected by at least 1 on T3 or T6, with no gate failure), not by total, so each pair teaches one specific behaviour.

**The judge will be noisy.** The best automatic systems in the BEA 2025 shared task reached macro-F1 of about 58 (guidance) to 72 (mistake identification), and LearnLM's own human raters agreed at Krippendorff's alpha ≈ 0.36. So:
1. Before trusting it, run the judge on **MRBench** (human-labelled tutor replies on the same 8 dimensions; CC BY-SA 4.0, [repo](https://github.com/kaushal0494/UnifyingAITutorEvaluation)) and compare to the gold labels. Eval only, never training text.
2. Then the owner labels about 100 of our own dialogues; target judge–human agreement of 0.75 or more (already in the plan).
3. Keep every check that can be deterministic (G1, G2, format) out of the judge's hands.

---

## 3. The training set

### 3.1 Source: our own dialogues only

No public tutoring dataset fits: everything is grade-school or university level, none uses a graphing calculator, and the license or privacy terms rule most of them out for a paid product used by minors (`docs/fine-tuning-research/2-datasets.md`). Specifically:

| Dataset | Use | Why |
|---|---|---|
| MathDial (CC BY-SA 4.0) | Reference for teacher moves; eval | ShareAlike may attach to our data; train on it only if counsel clears it |
| MRBench / BEA 2025 (CC BY-SA 4.0) | Judge calibration | Human labels on our rubric's dimensions |
| MathTutorBench (CC BY 4.0) | Regression eval against our endpoint | Sends its own prompts, so not our gate |
| CoMTA (Khan Academy) | **Avoid** | License allows internal noncommercial testing only |
| SocraTeach / SocraticLM, Eedi dialogues | **Avoid** | Non-commercial licenses |
| Bridge, NCTE, Eedi chats | **Avoid for training** | Real minors' conversations |
| Any "SAT question" dump (e.g. AGIEval SAT-Math) | **Avoid entirely** | College Board material, against our item rules |

### 3.2 Generation

Follows `data/traces/README.md`, with these additions:
- Give the tutor the planted misconception as hidden state (LearnLM did the same), but the judge checks that the tutor **draws out** the error rather than announcing it ("I bet you rounded").
- Cover the 20 failure modes in `docs/fine-tuning-research/1-pedagogy.md` §3 with personas; the eight existing personas cover most. Add a **strong student** persona (tests rule 14 and over-scaffolding) and a **stuck twice** persona (tests rule 11).
- For DPO, produce deliberate negatives by sampling the same context with an "unguarded helpful assistant" prompt (mirrors Bastani's GPT Base vs GPT Tutor).
- Thinking off: every example is a non-thinking reply (§4).

### 3.3 Safety examples in the mix

Fine-tuning can weaken a base model's refusals, and a self-hosted model has no vendor safety layer. Include, as roughly 3–5% of the set:
- off-topic redirects (admissions advice, other subjects, personal chat), each answered with the redirect line and a return to the question;
- attempts to get the answer outright, each met with rule 8;
- crisis or self-harm messages, where the tutor's reply is the **fixed** crisis response the site shows (988 Suicide & Crisis Lifeline, Crisis Text Line). The classifier in front of the model is what guarantees this; the training examples are a second layer.

### 3.4 The golden set

LearnLM found synthetic data taught substance (finding and fixing mistakes) and human-edited data taught style, and that purely synthetic data "cannot have enough useful pedagogical signal". So the owner, or a hired tutor, hand-edits **20–50 dialogues** covering every domain, hint level and persona. They go into every training run (upweighted if the platform allows) and are the reference the judge's calibration labels are drawn against.

### 3.5 Format for upload

- **One example per tutor turn.** Together and Alibaba Model Studio train only the last assistant turn for Qwen3-class models, so each dialogue is expanded so that every tutor turn is the final message of its own example, with the context built exactly as `buildMessages` in `web/lib/tutor/openai-compatible.ts` sends it in production. This also settles the open question in `data/traces/README.md` about how earlier turns are formatted.
- Strip `meta`/`metadata` before upload (Model Studio rejects extra keys). Pick one key name in the annotated file; the plan says `meta`, the traces README says `metadata`.
- Split by item, 85/15, before generating (unchanged from the plan).
- Optionally mix in 5–10% permissively licensed general chat data, in the same non-thinking format, to limit forgetting.
- No real student data in any training run until §5's conditions are met.

---

## 4. Training and serving

Details, commands and sources: `docs/fine-tuning-research/3-technical.md`.

**Where to train.** The plan's default (Qwen3-14B on Together) no longer exists: Together removed Qwen3-8B and 14B from fine-tuning. Recommended instead: **train the LoRA adapter ourselves** with TRL or Unsloth on a rented GPU (Modal or RunPod, about $10–30 a run), so we own a standard adapter that runs anywhere. Hosted alternatives:

| Platform | Fits when | Watch out for |
|---|---|---|
| Alibaba Model Studio (Singapore) | We want Qwen3-14B fine-tuned and served per token cheaply ($0.35 in / $1.40 out per 1M) | No weight download found (lock-in); DPO only in the Beijing region; the minors question in §0 |
| Together | We switch the base to Qwen3.5-9B/27B or gpt-oss-20b | Adapter download is in SGLang layout; download the merged model to move it |
| Fireworks | We already pay for a dedicated GPU | LoRA models need an on-demand deployment (~$4/h, about $2.9k/month always on); DPO single-turn only |
| AWS Bedrock | Phase B reward-based tuning on qwen3-32b or gpt-oss-20b | RFT only, no SFT for these models |

Avoid Hugging Face AutoTrain and torchtune (both unmaintained).

**Bake-off bases:** Qwen3-14B (Apache-2.0, confirmed), Qwen3-8B as the cheaper control, gpt-oss-20b (Apache-2.0 plus a usage policy). Replace Phi-4-reasoning with plain Phi-4: the reasoning model always thinks and needs its own fixed system prompt. Open the LICENSE file of the exact checkpoint before downloading.

**Starting settings (LoRA SFT):** all linear layers; rank 16, alpha 32 for both 8B and 14B (so the comparison changes one variable); LR 1e-4 cosine, 5% warmup; effective batch 8–16; 1–3 epochs chosen by held-out loss; max length 4,096; no packing; bf16 (never 4-bit on Qwen3.5). Evaluate every ~25 steps on held-out-item loss **and** a 20-dialogue generation spot check through the leak check and format lint, because loss alone does not catch early reveal.

**DPO (later):** from the SFT adapter, beta 0.1, LR 5e-6, one epoch, ~2,000 pairs, each pair one context (the dialogue prefix) with a chosen and a rejected reply. A design reference: ETH's PedagogicalRL / TutorRL-7B, which rewards "the simulated student solved it" minus a leak penalty; our grader and leak check give the same signal.

**Thinking mode.** Qwen3 models think by default. Training examples must be non-thinking renders (empty `<think></think>`), and every request must turn thinking off. The site now supports this without code changes: set `TUTOR_ENDPOINT_EXTRA_BODY` in `web/.env.local`:
- QwenCloud / Model Studio: `{"enable_thinking": false}`
- vLLM or Together: `{"chat_template_kwargs": {"enable_thinking": false}}`

The provider also strips any `<think>…</think>` text from replies before the student sees it. Add a "no thinking text" check to the eval.

**Cost.** 1,000 dialogues expanded per turn is roughly 10–25M training tokens, about $10–30 per run on any option above. Serving, not training, is where the money goes.

---

## 5. Safety and law: what must be true, and when

Sources, quotes and risk levels: `docs/fine-tuning-research/4-legal-safety.md`. _Counsel_ confirms every item before launch.

**Before generating training data**
- [ ] §0 settled: Anthropic authorization in writing, or the generator switched.
- [ ] Training data is synthetic, on our original items only. No College Board content, no real student data.
- [ ] License file of the exact base checkpoint read and recorded in the run log.
- [ ] Hosting or fine-tuning vendor terms read: no training on our data, retention, region.
- [ ] Safety examples (§3.3) and a red-team eval set built.

**Before any student uses a tutor (interim or fine-tuned)**
- [ ] Age screen, parent-paid checkout, verifiable parental consent for under-13s (`docs/phase0/age-gate-plan.md`). COPPA's amended rule has applied since Apr 22, 2026, including a written retention policy.
- [ ] Privacy notice names every vendor (Anthropic, Alibaba if used, the hosting vendor) and purpose.
- [ ] Always-visible "you're chatting with an AI" label, plus disclosure at the start of each session (Anthropic's Usage Policy, California SB 243, Utah).
- [ ] Topic classifier in front of the model; fixed crisis response; a published crisis protocol (SB 243); break reminder every 3 hours for known minors.
- [ ] No companion traits: no persona, no social chat, no memory of personal details across sessions.
- [ ] Anthropic's child-safety system prompt while Sonnet is live.
- [ ] Alibaba's answer on minors (§0) before any student uses the Qwen tutor.
- [ ] Red-team eval passed on the exact model served (fine-tuning can weaken refusals).
- [ ] _Counsel:_ SB 243 and SB 1119 (signed Sep 2026, duties from July 2027: self-harm detection, parent notification, audits) scope; a scan of the ~14 other 2026 state chatbot laws, or launch in fewer states; SOPIPA if marketed through schools; FERPA only if sold to schools.

**Before training on real student chats (not at launch)**
- [ ] Separate, optional, revocable consent (parent for under-13s; parent and student for 13–17), not bundled with checkout.
- [ ] PII scrub with a human spot check; crisis-flagged chats excluded entirely.
- [ ] Per-example provenance so a withdrawn student's data leaves the next run. The FTC has ordered models deleted when they were built on improperly collected children's data (WW/Kurbo, 2022).
- [ ] Logs not sent through any vendor model for labelling unless its terms allow it.

---

## 6. Corrections to `docs/fine-tuning-plan.md`

Found by the technical research; the plan should be revised to match.

| Plan says | Correction |
|---|---|
| Qwen3-14B on Together or Fireworks | Together no longer fine-tunes Qwen3-8B/14B; own the adapter (TRL/Unsloth) or use Model Studio (§4) |
| Fireworks: "multi-LoRA serverless, near-free to deploy" | LoRA needs an on-demand deployment, about $4/h |
| Bedrock: SFT and RFT | RFT only, only qwen3-32b and gpt-oss-20b |
| 1,000 dialogues ≈ 2–4M tokens | 4.5–9M before per-turn expansion, 10–25M after; still about $10–30 |
| Loss on all assistant turns | One example per tutor turn (§3.5) |
| Nothing on thinking mode | Train non-thinking; send the thinking-off field (§4) |
| Rank 8 for the 8B control | Rank 16 for both |
| AutoTrain / torchtune among the tools | Both unmaintained |
| Phi-4-reasoning in the bake-off | Plain Phi-4 instead |
| Qwen3.8-27B license "conflicting" | Reported Apache-2.0 since August; check the file |
| Sonnet writes the training dialogues | Needs Anthropic's authorization (§0) |

---

## 7. Open checks

Primary sources the research could not open, to read before relying on them:
- QwenCloud Customer Agreement and Alibaba privacy policy (age, training, retention, region).
- The Federal Register text of the amended COPPA rule (AI-training consent, retention).
- SB 243 and SB 1119 chaptered text on leginfo.legislature.ca.gov.
- Hugging Face cards: MathDial's license, the Qwen3-8B/32B and Phi-4 license files.
- Whether the QwenCloud flag is exactly `enable_thinking` for Qwen3.7-Plus (test with a call; if replies come back with reasoning text, the flag is wrong).
