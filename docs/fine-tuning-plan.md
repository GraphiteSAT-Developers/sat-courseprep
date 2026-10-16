# Fine-tuning plan: an open-weight tutor trained on verified dialogues

_Written 2026-10-15 for the owner and the AI collaborator. Decision it implements: Sonnet (Anthropic SDK) stays the solver, dialogue generator and judge; the live tutor becomes an open-weight model (Qwen/Llama class) fine-tuned on verified tutoring dialogues and served from an OpenAI-compatible endpoint. Until that model passes the eval gate, Sonnet serves live through the same `TutorProvider` seam._

> **2026-10-16: read `docs/fine-tuning-guidelines.md` first.** Research since this plan was written found (1) Anthropic's Usage Policy forbids training a model on Claude outputs without Anthropic's prior authorization, which affects Sonnet-generated dialogues and judge labels (guidelines §0); (2) Together no longer fine-tunes Qwen3-8B/14B, Fireworks needs a dedicated GPU for LoRA serving, and Qwen3 must be trained and served with thinking off (guidelines §4, §6). Where this plan and the guidelines disagree, the guidelines win until this plan is revised.

Figures below are **estimates** unless a source is named. Prices move monthly; check before budgeting.

## 1. Why open-weight

- **No closed model offers fine-tuning in 2026.** Gemini 3.x has no SFT (the report, "Model and feature choices"); Anthropic and OpenAI frontier models are prompt-only for us. The only way to put the verified dialogues into weights is an open model.
- **We own the weights.** The tutor's behaviour stops depending on a vendor's model deprecation calendar (the report records Gemini 2.5 variants shutting down within months). A LoRA adapter plus the base checkpoint is a file we keep.
- **Vendor-terms risk goes away for the live tutor.** The Gemini under-18 clause was the original blocker (`HANDOFF.md`). A self-hosted model has no usage policy that can change under us. Sonnet is still used offline (solver, generator, judge), where no minor's data is involved beyond item text.
- **Cost at scale.** A 8B–14B model served on a shared endpoint costs well under a frontier model per token (estimate: 10–30x cheaper per output token). Not the main reason, but it matters once there are thousands of daily tutor turns.

**What does not change.** The product's safeguards for minors apply regardless of model, and with a self-hosted model there is **no vendor policy backstop at all**: no vendor-side refusal training we can rely on, no vendor abuse filter. So the items in `docs/phase0/age-gate-plan.md` are load-bearing, not optional:

- the neutral age screen and parent-paid checkout;
- the always-visible "this tutor is an AI" disclosure;
- the topic classifier and self-harm/crisis protocol **in front of** the model (a fine-tuned 14B model will follow "stay on SAT math" most of the time; the classifier is what makes it every time);
- the site-side guardrails in `web/lib/tutor/guardrails.ts` (no full solution or show-me before a graded attempt) and the show-me rule in `web/lib/tutor/prompt.ts` (calculator lines come only from verified items, never from the model);
- daily message quotas and short chat-log retention.

The hosting vendor (Together, Fireworks, AWS) still sees the request text, so the DPA / no-training / short-retention settings in the age-gate plan apply to **them** now, and the privacy policy names them.

## 2. Base model, hosting, recommendation

### Candidate base models

All in the 8B–32B range: small enough to fine-tune on one or two GPUs and serve cheaply, large enough to hold a Socratic register and do light algebra without the solver's help. Reasoning is not the tutor's job (Sonnet solves; the tutor sees the verified solution in its prompt), so we are buying **instruction following, tone and format**, not raw math ability.

| Family | Sizes to try | License | What to verify before committing |
|---|---|---|---|
| **Qwen3** (Alibaba) | 8B, 14B, 32B (dense) | Apache-2.0 for the Qwen3 line per the model cards; one later release (Qwen3.8-27B, reported Aug 2026) had conflicting license reports at the time of writing | Open the LICENSE file in the exact Hugging Face repo you download. Some Qwen models have shipped under the Tongyi Qianwen license (commercial use only under 100M MAU), so do not assume Apache-2.0 from the family name. Sources: [eWeek on Qwen3.8-27B](https://www.eweek.com/news/alibaba-qwen3-8-27b-license-apac-china/), [orcarouter analysis](https://www.orcarouter.ai/blog/qwen-3-8-27b-license) |
| **Llama 3.1 / 3.3** (Meta) | 8B, 70B (too big for us) | Llama Community License | Free commercial use under 700M monthly active users; "Built with Llama" attribution required in product materials; cannot use Meta/Llama names to imply endorsement. Sources: [Llama 4 Maverick license text on Hugging Face](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Original), [Redress Compliance guide](https://www.redresscompliance.com/meta-llama-enterprise-licensing-costs-guide.html) |
| **Llama 4** (Meta) | Scout (17B active, MoE) | Llama 4 Community License | Same 700M MAU and attribution terms, plus the **EU restriction on the multimodal models** (an EU-domiciled entity cannot use them under the agreement; EU users may use services built on them by non-EU providers, per [llama.com FAQ](https://www.llama.com/faq/) and [commentary](https://blog.kilocode.ai/p/llama-4-one-week-after)). MoE models are also harder to LoRA-tune on hosted platforms; check the platform's supported-model list |

Others worth a look if the above disappoint on the eval: Gemma 3 (Google, 12B/27B, Gemma Terms of Use, which carry a use policy), Mistral Small (Apache-2.0 for some releases). Both need the same license check.

### Hosting options

Cost ranges are **estimates** from public price lists in 2025–26; confirm the current page before budgeting.

| Option | Fine-tuning | Serving | Rough cost | Ops burden |
|---|---|---|---|---|
| **Together AI** | Hosted LoRA/full SFT and DPO on Qwen3 and Llama; upload JSONL, get a model ID | Serverless LoRA inference on the base model's price, or dedicated endpoint | SFT: single-digit dollars per million training tokens (a 1,000-dialogue run is ~2–4M tokens over 3 epochs, so under $50). Serving 8B–14B LoRA: roughly $0.20–0.60 per million tokens. Dedicated endpoint: a few dollars per GPU-hour | Low |
| **Fireworks AI** | Hosted SFT and RFT (reward-based) on Qwen3 and Llama | Multi-LoRA serverless, so a new adapter is near-free to deploy | Similar order to Together | Low |
| **AWS Bedrock** | Custom model import plus fine-tuning / RFT for supported open models; OpenAI-compatible endpoint available | Provisioned or on-demand custom model units | Higher floor (provisioned throughput bills by the hour whether used or not; estimate hundreds to low thousands of dollars/month at steady state) | Medium; better if the rest of the stack is already on AWS (it is not: Firebase was chosen) |
| **Self-hosted vLLM** on a rented GPU (RunPod, Lambda, Vast) | Train with Axolotl / TRL / Unsloth on the same box | vLLM serves the OpenAI-compatible API natively | Training: one A100/H100 for a few hours ≈ $10–30 per run. Serving: a 24–48 GB GPU at ~$0.30–1.00/hour ≈ $200–700/month if always on; autoscaling to zero is DIY | High: uptime, patching, scaling, model loading, the on-call is us |

### Recommendation

**Qwen3-14B as the base, LoRA SFT, trained and served on Together or Fireworks, with an 8B run as the control.** Reasons:

1. Apache-2.0 (verify in the repo) removes the attribution and MAU clauses entirely, and there is no EU issue.
2. 14B is the sweet spot: an 8B model is cheaper but in informal experience drops format rules (hint levels, "no lists") more often; 32B costs 2–3x to serve for a gain the eval may not show. Run 8B alongside, because if 8B matches 14B on the pairwise eval we take the cheaper model.
3. A hosted fine-tune-and-serve platform means the whole loop (export JSONL → train → deploy → point `TUTOR_ENDPOINT_MODEL` at it) is a day's work, not a week's. Self-hosting vLLM is the fallback if a platform drops Qwen3, raises prices, or we need a custom serving feature; the provider seam makes that move a URL change.
4. Both Together and Fireworks speak the OpenAI chat-completions API that `web/lib/tutor/openai-compatible.ts` targets, as does vLLM and Bedrock's compatible route. Nothing in the site changes between them.

Pick between Together and Fireworks on three concrete checks the day we start: does the platform list the exact Qwen3 size we want for LoRA; what is the current serverless LoRA price; does it offer DPO/RFT for the phase-2 step.

## 3. Dataset

### What a training example is

One **dialogue** is a full chat on one item: the shared system prompt (rules + item block, exactly `SYSTEM_RULES` and `describeItem` from `web/lib/tutor/prompt.ts`), then alternating user turns (`describeTurn`: calculator state, last graded attempt, hint level, student message) and tutor turns. A dialogue has 2–8 tutor turns. Dialogues are generated by Sonnet playing both tutor and a scripted student with a persona and a planted misconception, over items whose solutions were verified by the solver (SymPy plus headless Desmos). `web/lib/traces/` and `web/scripts/generate-traces.ts` own generation and export; their output is `data/traces/sft.jsonl`.

### Format

`data/traces/sft.jsonl`: one JSON object per line, in the standard chat format every platform accepts:

```json
{"messages": [
  {"role": "system", "content": "<SYSTEM_RULES>\n\n<describeItem(item)>"},
  {"role": "user", "content": "<describeTurn: calculator, attempt, hint level, student message>"},
  {"role": "assistant", "content": "<tutor turn>"},
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."}
 ],
 "meta": {"item_id": "...", "domain": "...", "difficulty": "...", "hint_levels": ["nudge","strategy"], "persona": "...", "judge_score": 4.5, "split": "train"}}
```

Platforms train on `messages` and ignore `meta`; our scripts use `meta` for the mix report and the split. The `system` message is the one `buildMessages` in `openai-compatible.ts` sends at serve time, so train and serve prompts match byte for byte. Any change to `prompt.ts` therefore invalidates the dataset: regenerate, retrain, re-eval.

### Target sizes

| Run | Accepted dialogues | Items needed | Purpose |
|---|---|---|---|
| Smoke | ~200 | ~60 (today's 55 are nearly there) | Prove the pipeline: export → train → serve → eval. Expect it to lose to Sonnet |
| **First real SFT** | **~1,000** | **~300** at 3–4 accepted dialogues per item | The first candidate that could pass the gate |
| Solid | **3,000–5,000** | 500 items × 6–10 dialogues (or 300 items × ~12) | Where we expect format and tone to be stable across domains and personas |

Dialogues per item are capped (proposed: 12) so the model learns tutoring, not the item bank. The bank size is the binding constraint: see section 7.

### Mix

Stratify generation so the accepted set holds, within a few points:

- **By domain**, matching the test's distribution in `web/content/skills.ts` (Table A31): Algebra 35%, Advanced Math 35%, PSDA 15%, Geometry and Trig 15%. Over-weight hard items slightly (the course targets 800).
- **By hint level**: every dialogue climbs at least two levels; across the set, tutor turns should be roughly 30% nudge, 30% strategy, 25% worked-step, 15% full-solution. Full-solution turns only appear after a graded attempt in the transcript, because that is the only time the guardrails allow them in production.
- **By persona** (the scripted student): confident-and-wrong, stuck-at-the-start, right-answer-wrong-form (Bluebook typing rules), calculator-syntax-error (so the tutor learns to point at a line number), and off-topic-probe (tries to get the answer or changes the subject; the tutor must redirect). Roughly equal fifths, with off-topic a bit lower.
- **By route**: Desmos-primary, hand-primary and either, in the bank's proportions; and MC vs SPR in the test's proportions (about 75/25).

### Acceptance rules

A generated dialogue enters `sft.jsonl` only if all hold:

1. **Judge score ≥ 4 of 5** from the Sonnet judge on the tutoring rubric (hint-level fidelity, mistake identification, tone, brevity). The judge prompt is the same one the eval uses.
2. **No early reveal**: an automatic check, not the judge. No tutor turn before a correct graded attempt may contain the key (numeric match for SPR including equivalent fractions/decimals; choice letter or choice text for MC).
3. **Bluebook-reproducible**: every Desmos instruction in a tutor turn refers only to the item's verified `desmos.lines` (string containment after LaTeX normalization) and the item is `verified: true`. Nothing a student could not type into the Bluebook calculator.
4. **Format**: two to five sentences per turn, no markdown headings, lists only inside a full-solution turn.
5. **No College Board text** anywhere (every item is original; the lint in `docs/item-writing.md` already enforces this on items, and dialogues inherit it).

Log the rejection reason per dialogue; the rejection histogram is the first thing to look at when a run underperforms.

### Held-out split: by item, not by dialogue

Split **items** 85/15 before generating, with the split stratified by domain and difficulty, and keep the held-out item IDs in a committed file (`data/traces/heldout-items.json`, owned by the traces scripts). Every dialogue inherits its item's split. Splitting by dialogue would leak: two dialogues on the same item share the whole system prompt and the solution, so a held-out dialogue would be near-memorized. The held-out items are also the ones the launch eval runs on (section 5), and they are never used for few-shot examples in the Sonnet baseline prompt either.

## 4. Training recipe

### Phase A: SFT with LoRA

Start here. It is cheap, reversible (an adapter is a file) and enough to teach format and register.

Starting hyperparameters (estimates from common practice; tune on the smoke run):

| Setting | Start | Note |
|---|---|---|
| Method | LoRA, rank 16, alpha 32, dropout 0.05, on all linear projection layers | Rank 8 for the 8B control; try 32 if the model still breaks format |
| Epochs | 3 | Watch held-out loss; 2 may be enough at 3k+ dialogues |
| Learning rate | 1e-4 (LoRA), cosine decay, 3% warmup | Lower to 5e-5 if the loss curve is noisy |
| Batch | effective 16 sequences (grad accumulation as needed) | |
| Sequence length | 4,096 tokens | Our dialogues are 1.5–3k tokens with the item block |
| Loss | assistant turns only | Never train on the system or user text; the model must not learn to generate calculator state |
| Precision | bf16 | |

Hosted platforms expose most of these as fields; use their defaults where a field is missing and record what was used.

### Phase B: preference tuning (DPO or RFT), later

Only after SFT passes the gate or gets close. Build pairs from the generation step we already run: for one item and one student turn, sample 2–4 tutor replies, have the judge rank them pairwise with randomized order, and keep (chosen, rejected) pairs with a clear margin (≥ 1 point). This targets the failure modes the eval reports (early reveal, too long, wrong hint level) without new human labels. DPO on Together/Fireworks, or RFT on Fireworks/Bedrock with the leak check and the judge as the reward. Start with beta 0.1, LR 5e-6, 1 epoch over ~2,000 pairs. Expect modest gains; the point is to close a specific gap the SFT model shows, not to replace SFT.

### What to log per run

A committed `runs/<date>-<base>-<n>.md` (owned by the AI collaborator) with: base model and revision hash, dataset file hash and line count, the mix table, the rejection histogram, every hyperparameter, train and held-out loss curves, wall-clock and cost, the platform's model ID, and the full eval table from section 5 against the Sonnet baseline. No run without this file goes live.

## 5. Eval gate before the model goes live

The report's three-layer eval, assigned:

| Layer | Who it tests | Owner | Where |
|---|---|---|---|
| Solver correctness (pass@1, self-consistency, SymPy + headless Desmos agreement) | Sonnet as solver | AI side | Not the tutor's problem: the tutor only ever sees verified solutions |
| Tool hygiene (expression error rate, retries, verified share, latency, cost) | The solver and the verification service | AI side | Same |
| **Tutoring quality** | **The fine-tuned tutor vs. the Sonnet prompt-only baseline** | AI side builds, owner signs off | **This is the gate** |

### The tutoring gate

Run on the **held-out items** (never trained on) with the same scripted-student personas, generating fresh dialogues from both tutors on identical seeds (same item, persona, misconception, hint sequence). Then:

1. **Pairwise judging, randomized order.** The Sonnet judge sees the two dialogues as A and B with the order flipped per pair, scores on the rubric, and picks a winner. Report win rate with a 95% interval. The judge is noisy (MathTutorBench reports LLM-judge accuracy below 0.7 and position sensitivity), hence the order randomization and the calibration step below. A judge from a second model family as a tiebreaker is cheap insurance.
2. **Judge calibration.** Before trusting the win rate, the owner (or a hired tutor) labels ~100 dialogue pairs; judge-human agreement should be ≥ 0.75. If it is lower, fix the rubric before fixing the model.
3. **Leak rate ≈ 0.** The automatic early-reveal check from section 3 on every generated dialogue, both tutors. Target: 0 leaks in the held-out run; a single leak blocks launch and goes into the DPO pair set.
4. **Desmos-reproducibility rate.** The share of tutor turns whose Desmos instructions are entirely within the item's verified lines. Target ≥ 98% (the remainder are paraphrases the normalizer did not match, inspected by hand).
5. **Hint-level fidelity.** Per-turn automatic check (full-solution text at a nudge turn is a failure). Target ≥ 95%.
6. **Off-topic redirect rate** on the off-topic persona: ≥ 99% of turns redirect to the math.
7. **Latency and cost** at p50/p95 for a 6-turn dialogue, both models.

**Rule: the fine-tuned tutor must match or beat the Sonnet baseline** (pairwise win rate ≥ 50% with the interval's lower bound not far below it, and no worse on every automatic metric) **before `TUTOR_PROVIDER` is set to `endpoint` in production.** "Nearly as good but ten times cheaper" is a reason to keep training, not a reason to ship.

The full suite reruns on every change to `prompt.ts`, the dataset, the base model, or the endpoint.

## 6. Deployment through the provider seam

Nothing in the site knows which model is live. `web/lib/tutor/provider.ts` picks:

1. `TUTOR_PROVIDER` if set: `endpoint` | `anthropic` | `stub`;
2. else `TUTOR_ENDPOINT_URL` + `TUTOR_ENDPOINT_MODEL` set → the OpenAI-compatible provider;
3. else `ANTHROPIC_API_KEY` → Sonnet;
4. else the stub.

Going live with the fine-tuned model is three env vars on the host (`TUTOR_ENDPOINT_URL`, `TUTOR_ENDPOINT_KEY`, `TUTOR_ENDPOINT_MODEL`) plus a restart. The endpoint provider enforces a 30 s timeout and turns any non-200, timeout or empty reply into a neutral line, so a dead endpoint degrades to "Let's look at this together" rather than an error.

**Rollback is one env change: `TUTOR_PROVIDER=anthropic`.** Keep `ANTHROPIC_API_KEY` configured in production for exactly this reason. A new fine-tune is a new `TUTOR_ENDPOINT_MODEL` value; never retrain in place under an ID that is live.

Suggested rollout: a week at `TUTOR_PROVIDER=anthropic` with the endpoint shadow-called on a sample of turns (log both replies, judge offline), then flip for a cohort, then all.

## 7. Timeline (phased, gated on the item bank)

The item bank is the critical path: roughly **300 items → ~1,000 accepted dialogues** at 3–4 per item, so the first real training run cannot happen before the bank reaches ~300 verified items (55 today). Durations are estimates and assume part-time effort from both collaborators.

| Phase | Depends on | Work | Exit |
|---|---|---|---|
| **0. Pipeline smoke** (now; 1–2 weeks) | 55 items, headless verifier running | Generate ~200 dialogues, export `sft.jsonl`, LoRA-tune Qwen3-8B on a hosted platform, point a dev `TUTOR_ENDPOINT_URL` at it, run the eval end to end | The loop works; a first (losing) eval table exists; the judge calibration set is started |
| **1. Bank to 300** (parallel; 4–8 weeks) | Item writing per `docs/item-writing.md`, verification service | Owner writes items; AI side verifies and keeps the generation scripts producing accepted dialogues as items land | 300 verified items, 85/15 held-out split committed |
| **2. First real SFT** (1–2 weeks after phase 1) | ~1,000 accepted dialogues | Qwen3-14B and 8B LoRA runs, logged; full eval vs. Sonnet; judge calibrated on 100 human-labelled pairs | A run file; a decision: ship, iterate, or wait for more data |
| **3. Bank to 500 and solid SFT** (6–10 weeks) | 3,000–5,000 dialogues | Retrain; DPO on judge pairs targeting the gaps phase 2 showed | Passes the gate in section 5 |
| **4. Go live** | Phase 3, counsel sign-off on the age-gate plan, hosting DPA | Shadow week, cohort flip, full flip with `TUTOR_PROVIDER=endpoint`; Sonnet stays configured for rollback | Live on the fine-tuned tutor; the eval suite in CI on every prompt or data change |

If phase 2 already passes the gate, phase 3 still runs before the flip: the first pass on ~1,000 dialogues is as likely to be judge noise as a real result, and 300 held-out dialogues give a wide interval.

## 8. Open questions for the owner

- Budget ceiling for hosting at launch (the estimates above range from ~$50/month serverless to ~$700/month always-on dedicated).
- Who labels the ~100 judge-calibration pairs: the owner, or a paid tutor at a few hours' work.
- Whether under-13 accounts launch at all (age-gate plan open item), which decides how strict the content filter in front of the model must be at launch.
- Whether to publish the held-out benchmark results (the report suggests a head-to-head on original hard items as marketing); publishing means freezing the held-out set and never training on it.
