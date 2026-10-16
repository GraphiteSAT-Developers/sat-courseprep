# 3. Technical how-to: platforms, recipe, serving, licenses

Research date: **2026-10-16**. Scope: check `docs/fine-tuning-plan.md` §2–4 and §6 and `data/traces/README.md` against current docs.

**How the sources were read:** direct page fetches were blocked in this sandbox (the egress proxy refused docs.together.ai, fireworks.ai, alibabacloud.com and huggingface.co). Every fact below comes from **web-search excerpts of the official pages** (linked in §6), plus a few third-party pages, which are marked as such. Treat every price as "as indexed, mid/late 2026". **[V]** means an official doc excerpt says so. **[3P]** means only a third-party source says so. **[UNVERIFIED]** means no source was found, or the sources conflict. Before spending money, open the live page for each [3P] or [UNVERIFIED] item.

---

## 0. The five findings that change the plan

1. **Together AI no longer fine-tunes Qwen3-8B or Qwen3-14B.** Its changelog and deprecations page list Qwen3-8B, Qwen3-14B and their Base variants as "no longer available for fine-tuning". The current supported-models table lists Qwen3.5 (for example 9B and 27B), Qwen3.6 and Qwen3.8-27B, plus gpt-oss-20b [V]. The plan's default ("Qwen3-14B on Together") therefore does not exist today. A few older Together pages still use `Qwen/Qwen3-8B` in their examples, so check the live table before deciding.
2. **Fireworks has no serverless per-token hosting for LoRA fine-tunes.** Its docs say LoRA models "can only be deployed to on-demand deployments" (dedicated GPUs, billed per GPU-second; the official pricing page shows about $4/h for an H100) [V]. Multi-LoRA lets one deployment carry up to about 100 adapters. Fireworks also retired serverless Qwen3-8B in May 2026 [V]. The plan calls Fireworks "multi-LoRA serverless, so a new adapter is near-free"; that is out of date. A model running around the clock on one H100 is about **$2.9k/month**. There is one conflicting snippet: a February 2026 Fireworks tutorial charges serverless LoRA add-ons at base-model rates on some bases [UNVERIFIED for Qwen3].
3. **On Together, Qwen3 counts as a reasoning model, which changes how multi-turn data is trained.** For reasoning models, "only the last assistant message is trained on by default". Each assistant turn in multi-turn data has to be its own example. Training a reasoning model without reasoning data "can degrade its reasoning ability; use an instruct model instead" [V]. Alibaba Model Studio has a similar rule: thinking-model SFT trains only the final assistant output [V]. **Recommendation:** expand each dialogue into one example per tutor turn. This also fixes the history-format mismatch the traces README flags (§3, step 1).
4. **Alibaba Model Studio does fine-tune the open Qwen3-14B** (`qwen3-14b`). In the Singapore/international region, only efficient (LoRA) SFT is offered, at **$0.0016 per 1K tokens ($1.60/M)**; one other page shows $4.126/M. DPO, continued pre-training and LoRA import from OSS are **Beijing-only** [V]. The tuned LoRA model serves per token at **$0.35/M input and $1.40/M output in non-thinking mode** ($4.20/M output in thinking mode) [V]. That is the cheapest serving path found. No documented way to **download** the trained weights was found [UNVERIFIED], so plan on serving there only (lock-in). Qwen3.7-Plus (the interim tutor) is proprietary and has no fine-tuning option that I could find [3P/UNVERIFIED].
5. **Two of the plan's tools are effectively dead.** **Hugging Face AutoTrain** says on its docs: "no longer maintained… no new features… bugs will not be fixed", and points users to Axolotl, TRL or `transformers.Trainer` [V]. **torchtune**'s README says it is no longer actively maintained (issue #2883, 2025) [V]. Neither should be used.

---

## 1. Platform comparison (as of 2026-10-16)

| Platform | Qwen3 8B/14B (orig.) | Newer Qwen | gpt-oss-20b | Phi-4-reasoning | LoRA / full | DPO | Data format, loss masking | Train price (≤16B, per 1M tokens × epochs) | Serving a LoRA | Export weights |
|---|---|---|---|---|---|---|---|---|---|---|
| **Together AI** | **Deprecated for FT** [V] | Qwen3.5-9B, Qwen3.5-27B (default LoRA rank 64, 131k SFT ctx), Qwen3.6, Qwen3.8-27B [V] | Yes, LoRA; max rank 128; SFT ctx 131k, DPO ctx 65k in the current table (16k/8k in the 2025 blog) [V] | Not seen in the table [UNVERIFIED] | LoRA default; full on a subset [V] | Yes. `dpo_beta` defaults to 0.1; the recipe LR is 5e-6 cosine [V] | JSONL/Parquet. `messages` must start with system or user and then alternate. Mask user/prompt tokens with `train_on_inputs` (bool or "auto"); per-message `weight` is also supported. Extra keys (e.g. `metadata`) are ignored per the older docs. Mixing two formats in one file is rejected. Reasoning models train only the last assistant turn [V] | LoRA SFT $0.48, LoRA DPO $1.20 [3P CostBench, mid-2026]. A separate "specialized" tier for long context costs $10–100+/M with a $20–60 job minimum [3P] | Serverless LoRA on "select base models" at the base price [V]; otherwise a dedicated endpoint billed per minute [V] | **Yes**: `download` of a merged model, or an adapter only. The adapter is in **SGLang multi-LoRA layout, not PEFT** [V, verify]. The merged model loads in any engine |
| **Fireworks AI** | Dense Qwen3 listed as tunable [V]. Check the "Tunable" filter for 14B [UNVERIFIED] | Qwen3.8-27B used in the serverless-training quickstart [V] | SFT yes, but "single-turn without thinking traces" for now [V changelog] | Phi 3/4 listed as tunable [V] | LoRA and full [V] | Yes, **single-turn only**: the preferred/rejected answer must be the final assistant message [V] | OpenAI chat JSONL; OpenAI-format files work unchanged [V]. Per-message `weight` not confirmed [UNVERIFIED] | $0.50 base for ≤16B; $3.00 for 16.1–80B [V]. Splits of $0.50 LoRA SFT / $1.00 LoRA DPO / $1.00 full SFT / $2.00 full DPO [3P] | **On-demand deployment only** [V], ~$4/h per H100, billed per second [V pricing; a dev mirror shows $7.79]. Up to ~100 LoRA add-ons per deployment at no extra cost [V] | Not documented [UNVERIFIED] |
| **Alibaba Model Studio** (QwenCloud) | `qwen3-14b`: efficient SFT in Singapore; more models and methods in Beijing [V] | Qwen3.x Plus/Max are hosted-only; no FT found [UNVERIFIED] | No | No | Singapore: LoRA (efficient_sft) only for 14B. Beijing: full or LoRA SFT and DPO [V] | **Beijing region only** [V] | ChatML `messages` JSONL, multi-turn allowed. "All assistant outputs are trained". OpenAI `name`/`weight` keys **not supported** (one example still shows `loss_weight`, so the docs conflict). For thinking models only the final turn trains [V] | $1.60/M (Singapore; another page says $4.126/M) [V, conflicting] | Per token for LoRA models: $0.35 in, $1.40 out (non-thinking) [V]; or provisioned Model Units [V] | **Not documented** [UNVERIFIED]. The reverse works: import your own PEFT LoRA (rank 8/16/32/64, `adapter_model.safetensors` + `adapter_config.json`), but only in Beijing [V] |
| **AWS Bedrock** | `qwen.qwen3-32b` only | – | `openai.gpt-oss-20b` | – | Managed | **RFT only** (reward = rule grader, LLM judge or Lambda). SFT for these models is not documented [V] | OpenAI-compatible Files and fine-tuning API, us-west-2 (`bedrock-mantle` endpoint) [V] | Not found [UNVERIFIED] | On-demand through the OpenAI-compatible Chat Completions/Responses API, "no additional deployment step" [V] | No [UNVERIFIED] |
| **HF AutoTrain** | – | – | – | – | – | – | **Unmaintained** [V] | – | – | – |
| **Modal** (DIY) | Any HF model | Any | Any | Any | Whatever you run (Unsloth/TRL/Axolotl) | Yes (TRL) | Yours | GPU time: H100 $0.001097/s ≈ $3.95/h; A100-80GB ≈ $2.50/h; L40S ≈ $1.95/h. Pinning a region adds 1.5–1.75×; non-preemptible adds 3× [3P, Jul 2026] | You run vLLM; scales to zero; cold starts are on you | Yes (you own it) |
| **RunPod** (DIY) | Any | Any | Any | Any | Yours | Yes | Yours | H100 80GB ~$2.49/h, A100 80GB ~$1.60/h on-demand [3P, Sep 2026] | Serverless `worker-vllm`, OpenAI-compatible, billed by usage [V]. LoRA support in the worker not confirmed [UNVERIFIED] | Yes |

**What a run costs** (correcting the plan's figure; see §5): 1,000 dialogues × ~2.5k tokens × 3 epochs ≈ **7.5M tokens**, which is about **$4–12** at $0.48–1.60/M. After per-turn expansion (about 2.5× the tokens), it is about **$10–30**. The smoke run costs a few dollars on any platform. The money is in **serving**, not training.

---

## 2. Base-model notes that affect the recipe

| Model | Thinking behavior | What it means for a non-thinking tutor |
|---|---|---|
| **Qwen3-8B / 14B / 32B** (hybrid, Apr 2025) | Thinks by default. `enable_thinking=False` makes the chat template insert an empty `<think>\n\n</think>\n\n` at the start of the reply; `/no_think` in a user or system turn works per turn. The template **strips think blocks from earlier assistant turns** [V Qwen3 report; HF template deep-dive] | Train on non-thinking renders (empty think block), and **serve with thinking off**. Our provider (`openai-compatible.ts`) sends no flag today, so a Qwen3 endpoint would *think by default* inside the 1,024-token `max_tokens` budget. Add `chat_template_kwargs: {enable_thinking: false}` for vLLM/Together, or `enable_thinking: false` for DashScope/Model Studio [V for vLLM ≥0.9; DashScope flag from memory, UNVERIFIED]. Note that there is **no 8B/14B Instruct-2507** non-thinking variant; only 4B, 30B-A3B and 235B have one |
| **Qwen3.5-9B / 27B** (Mar 2026) | Hybrid Gated-DeltaNet + attention architecture, natively multimodal, 262k context [3P]. Whether thinking is on by default is disputed: the model card mirror says on, Unsloth says off for ≤9B [conflict] | Unsloth: **do not QLoRA Qwen3.5**. Use bf16 LoRA (9B ≈ 22 GB, 27B ≈ 56 GB) and transformers v5 [V]. TRL refuses `assistant_only_loss` on VLM-registered Qwen3.5 checkpoints [3P forum]. License reported as Apache-2.0 [3P]; check the repo |
| **gpt-oss-20b** (MoE, 21B/3.6B active) | Harmony format with `analysis` and `final` channels; reasoning effort set in the system/developer message [V cookbook/Unsloth] | Training data must be in harmony format. TRL, PEFT and transformers render it from `messages` (cookbook: trl 0.20, peft 0.17, transformers ≥4.55, one H100 80GB; MXFP4 dequantized to bf16) [V]. bf16 LoRA needs ~44 GB [V Unsloth]. Fireworks SFT is single-turn without thinking traces [V]; Together supports it [V] |
| **Phi-4-reasoning** (14B dense) | Always reasons. The card requires ChatML plus a fixed system prompt that produces `<think>…</think>` then the answer; 32k context [V Azure card] | Poor fit for a short, non-thinking tutor: our production system prompt would replace the one the card requires. Training out the thinking is possible but fights the model. Suggest dropping it from the bake-off, or using the non-reasoning **Phi-4** instead (MIT; not verified this session) |

---

## 3. Recommended recipe

Strategy: **own the adapter.** Train with TRL or Unsloth on rented GPUs (Modal or RunPod; about $10–30 a run), so the artifact is a standard PEFT adapter that works with vLLM and can be uploaded to Together, Fireworks or Model Studio. Use a hosted platform's built-in fine-tuning only where it is clearly simpler and the base model is still offered. The fastest hosted, per-token-served path for **Qwen3-14B specifically** is now Model Studio (Singapore, SFT only, not exportable). Fireworks needs a dedicated GPU. Together needs a switch to Qwen3.5-9B or 27B.

### Step 1: Data prep (`sft.jsonl` → per-turn training files)

Expand each dialogue so that every tutor turn becomes its own example. The context is built **exactly as `buildMessages` sends it in production**: earlier turns as history, the current turn's full `describeTurn` block, and the loss on that final assistant message only. This (a) matches what the server sees at serve time, (b) satisfies Together and Model Studio's last-turn-only rule for reasoning models, and (c) avoids Qwen3's history think-stripping mismatch.

```python
# scripts/expand_turns.py (sketch). Run as: python -I expand_turns.py sft.jsonl train.jsonl
import json, sys
src, dst = sys.argv[1], sys.argv[2]
with open(src) as f, open(dst, "w") as out:
    for line in f:
        d = json.loads(line); msgs = d["messages"]
        assert msgs[0]["role"] == "system"
        for i, m in enumerate(msgs):
            if m["role"] != "assistant": continue
            hist = msgs[1:i-1]                       # earlier turns
            # mirror production: earlier user turns as the provider sends them (trim to "Student says" line if the provider keeps doing that)
            ex = {"messages": [msgs[0], *hist, msgs[i-1], m]}
            out.write(json.dumps(ex, ensure_ascii=False) + "\n")   # drop meta/metadata
```

- Remove `meta`/`metadata` from training uploads. Together ignores extra keys, but Model Studio does not support extra message keys. The export should write a clean file next to the annotated one.
- Optional, to reduce forgetting: mix in **5–10% general instruction data** in the same non-thinking format (for example a slice of a permissively licensed chat SFT set). LoRA already "learns less and forgets less" (Biderman et al., TMLR 2024), so this is cheap insurance, not a requirement.
- Hold out by item (as the plan says), and keep a **validation file** of held-out-item turns so the platform reports eval loss.

### Step 2: Train (SFT, LoRA)

TRL (current docs): `assistant_only_loss=True` needs `{% generation %}` markers. TRL **auto-patches known families including Qwen3** (bundled `qwen3_training.jinja`) [V]. With a conversational prompt–completion layout, `completion_only_loss` also works. Because Step 1 already puts the loss on the last turn, use prompt–completion:

```python
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer
ds = load_dataset("json", data_files={"train":"train.jsonl","eval":"heldout.jsonl"})
to_pc = lambda ex: {"prompt": ex["messages"][:-1], "completion": [ex["messages"][-1]]}
ds = ds.map(to_pc, remove_columns=["messages"])
cfg = SFTConfig(
  output_dir="out/qwen3-14b-tutor", num_train_epochs=2, learning_rate=1e-4,
  lr_scheduler_type="cosine", warmup_ratio=0.05, per_device_train_batch_size=2,
  gradient_accumulation_steps=4,            # effective 8; LoRA prefers small batches
  max_length=4096, packing=False, bf16=True, gradient_checkpointing=True,
  eval_strategy="steps", eval_steps=25, save_steps=25, load_best_model_at_end=True,
  chat_template_kwargs={"enable_thinking": False},   # render empty <think></think> (UNVERIFIED key name; else pre-render)
)
peft = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear", task_type="CAUSAL_LM")
SFTTrainer(model="Qwen/Qwen3-14B", args=cfg, train_dataset=ds["train"], eval_dataset=ds["eval"], peft_config=peft).train()
```

If the `chat_template_kwargs` key name is not supported in the installed TRL version, pre-render each example with `tokenizer.apply_chat_template(..., enable_thinking=False)` and train on text with a completion mask. **Check one rendered example by eye** before any run: the prompt should end with `<|im_start|>assistant\n<think>\n\n</think>\n\n`, and the loss span should be the tutor text plus `<|im_end|>`.

Unsloth equivalent: `FastLanguageModel.from_pretrained("unsloth/Qwen3-14B", load_in_4bit=False)`, then `get_peft_model(r=16, lora_alpha=32, target_modules=[q,k,v,o,gate,up,down])`, then `train_on_responses_only(trainer, instruction_part="<|im_start|>user\n", response_part="<|im_start|>assistant\n")`. On Qwen3.5, do not set `load_in_4bit` [V].

Axolotl equivalent (official Qwen3 example YAML; dataset in OpenAI messages format) [V Qwen docs]:
```yaml
base_model: Qwen/Qwen3-14B
chat_template: tokenizer_default
datasets: [{path: train.jsonl, type: chat_template, field_messages: messages, roles_to_train: [assistant]}]
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_linear: true
sequence_len: 4096
sample_packing: false
num_epochs: 2
learning_rate: 1e-4
lr_scheduler: cosine
warmup_ratio: 0.05
bf16: true
```
(`roles_to_train` comes from a community Qwen3 config [3P]; check the Axolotl docs. Thinking handling in Axolotl was not verified.)

Hosted alternatives (CLI flags as recalled from the docs, **verify before use**):
```bash
# Together (pick a base model that is still listed, e.g. Qwen/Qwen3.5-9B)
together files check train.jsonl && together files upload train.jsonl
together fine-tuning create --training-file file-… --validation-file file-… \
  --model Qwen/Qwen3.5-9B --lora --lora-r 16 --lora-alpha 32 --n-epochs 2 \
  --learning-rate 1e-4 --train-on-inputs false --n-evals 10
together fine-tuning download ft-… --checkpoint-type merged        # or adapter (SGLang layout)
# Fireworks
firectl create dataset tutor-v1 train.jsonl
firectl create sftj --base-model accounts/fireworks/models/qwen3-14b --dataset tutor-v1 \
  --output-model tutor-v1 --epochs 2 --learning-rate 1e-4 --lora-rank 16
firectl create deployment accounts/<acct>/models/tutor-v1   # on-demand; live-merge
```

### Hyperparameters (small-data, multi-turn SFT)

| Setting | Use | Source / reason |
|---|---|---|
| Target modules | **all linear** (attention + MLP) | LoRA Without Regret: attention-only underperforms even with the parameter count matched [V] |
| Rank / alpha | r=16, α=32 (r=32 if format still breaks). On Together, record its default (64 on 27B) | Unsloth: 16 or 32; α = r or 2r [V] |
| LR | **1e-4 to 2e-4** for LoRA; about 10× what full FT would use | Unsloth: 2e-4 start [V]; TM: LoRA LR ≈10× FullFT, roughly rank-independent [V] |
| Epochs | 1–3. Use eval loss and the per-25-step eval to choose; >3 gives diminishing returns and overfits | Unsloth [V] |
| Batch | effective 8–16; **keep it small** | TM: LoRA pays more for large batches than full FT does [V] |
| Packing | off (examples are 1.5–4k tokens; per-turn masking is simpler without packing) | – |
| Max length | 4,096 (8,192 if the longest expanded example exceeds that; measure) | – |
| Dropout / warmup | 0.05 / 3–5% | Unsloth suggests 5–10% warmup [V] |
| Eval during training | held-out-item eval loss every ~25 steps, keep the best checkpoint, **plus** a 20-dialogue generation spot check (leak check + format lint) per checkpoint | loss alone does not catch early reveal |

**DPO (phase B):** start from the SFT adapter. β=0.1 (Together default [V]; TRL default 0.1 [3P]), LR **5e-6** cosine (Together recipe [V]; Unsloth suggests 5e-6 for DPO/GRPO [V]), 1 epoch. On Fireworks and Together, preference data is **single-turn**: `{"input":{"messages":[…context…]},"preferred_output":[{"role":"assistant","content":…}],"non_preferred_output":[…]}` with exactly one assistant message each [V]. Our pairs ("one item, one student turn, 2–4 sampled replies") already fit this, with the context being the dialogue prefix. Together notes DPO helps less when there is only one target per prompt [V]. Model Studio DPO is Beijing-only [V]. TRL: `DPOConfig(beta=0.1, learning_rate=5e-6, num_train_epochs=1, max_length=4096)` with the same LoRA config. If a separate adapter is trained, set `ref_model=None` and the PEFT base acts as the reference.

### Step 3: Eval

The plan's §5 gate is unchanged. Add **thinking-leak checks**: zero `<think>` text in `content`, and zero non-empty `reasoning_content`. Measure p50/p95 latency **on the actual serving config**. No published batch-1 vLLM TTFT figures for Qwen3-14B were found. Qwen's Transformers speed table gives ~41 tok/s single-stream BF16 for 14B [V]; vLLM on an H100 should do clearly better. Measure with `vllm bench serve` at concurrency 1 and 8.

### Step 4: Serve

**Self-hosted vLLM (multi-LoRA, OpenAI-compatible)** [V vLLM docs v0.20]:
```bash
vllm serve Qwen/Qwen3-14B --enable-lora --max-lora-rank 32 --max-loras 4 \
  --lora-modules '{"name":"tutor-v1","path":"/adapters/tutor-v1","base_model_name":"Qwen/Qwen3-14B"}' \
  --reasoning-parser qwen3 --max-model-len 8192
# request: {"model":"tutor-v1", "messages":[…], "chat_template_kwargs":{"enable_thinking":false}}
```
- Each adapter is its own `model` name, which maps to `TUTOR_ENDPOINT_MODEL`. A new fine-tune is a new name, never retrained in place (as the plan says).
- Runtime loading: set `VLLM_ALLOW_RUNTIME_LORA_UPDATING=1` and use the `lora_filesystem_resolver` plugin [V].
- Structured output: the `response_format: {type:"json_schema", …}` API; the old `guided_json` fields were **removed in v0.12** in favor of `structured_outputs` [V]. With a reasoning parser enabled, the reasoning is returned separately [V].
- Hardware: 14B bf16 needs ~28 GB of weights, so use an L40S/A100-80GB/H100. 8B fits in 24 GB with a short context. FP8 halves memory.

**Provider-seam change needed** (`web/lib/tutor/openai-compatible.ts`): the request body has no thinking switch. Add an optional `TUTOR_ENDPOINT_EXTRA_BODY` (JSON) so the request can carry `chat_template_kwargs` (vLLM, Together) or `enable_thinking: false` (DashScope) without code changes per host. As defense in depth, strip any `<think>…</think>` from `content` before display.

---

## 4. Licenses (exact repos)

| Repo | License | Status |
|---|---|---|
| `Qwen/Qwen3-14B` | **apache-2.0** (card metadata plus a LICENSE file in the repo) | [V, HF card excerpt] |
| `Qwen/Qwen3-8B`, `Qwen/Qwen3-32B` | Apache-2.0 per the Qwen3 launch coverage ("all … Apache 2.0") | [3P]; card not seen; open LICENSE before download |
| `openai/gpt-oss-20b` | **apache-2.0**, plus a separate `USAGE_POLICY` file in the repo (updated in late 2025). Azure lists it as "Custom"; NVIDIA NIM hosting adds its own license | [V HF tree + OpenAI docs]; read USAGE_POLICY |
| `microsoft/Phi-4-reasoning` | **MIT** | [3P, consistent across sources]; HF card not seen |
| `Qwen/Qwen3.5-9B`, `Qwen/Qwen3.6-27B`, `Qwen/Qwen3.8-27B` | Apache-2.0 reported for each | [3P]; the plan's "conflicting reports" note on 3.8-27B is now settled as Apache-2.0 by post-release reports (eWeek) |

---

## 5. Corrections to `docs/fine-tuning-plan.md` and `data/traces/README.md`

| # | Where | Plan says | Sources say | Fix |
|---|---|---|---|---|
| 1 | §2 Hosting, Together row; §2 Recommendation | "Hosted LoRA/full SFT and DPO on Qwen3"; recommends Qwen3-14B on Together or Fireworks | Together deprecated Qwen3-8B/14B for fine-tuning (changelog, deprecations page) [V] | Choose one: Qwen3.5-9B/27B on Together; Qwen3-14B on Fireworks, Model Studio or DIY. The "does the platform list the exact size" check in the plan has already failed for Together |
| 2 | §2 Fireworks row | "Multi-LoRA serverless, so a new adapter is near-free to deploy"; "Similar order to Together" | LoRA fine-tunes need an on-demand deployment (~$4/h H100, per second) [V]; Qwen3-8B serverless retired May 2026 [V] | Budget about $2.9k/mo for one always-on GPU, or use multi-LoRA on one deployment for all experiments |
| 3 | §2 Hosting table | Model Studio not listed | Model Studio fine-tunes `qwen3-14b` (Singapore LoRA SFT at $1.60/M) and serves it per token at $0.35/$1.40 per M [V]; no export documented; DPO Beijing-only | Add it as a row: cheapest serving, same vendor as the interim tutor, but lock-in and no DPO outside China |
| 4 | §2 AWS Bedrock row | "fine-tuning / RFT for supported open models" | Only **RFT** documented, only for `qwen3-32b` and `gpt-oss-20b`, us-west-2; serving is on-demand per token (no provisioned throughput needed for these) [V] | Correct the row: Bedrock is an option for phase B (RFT with the leak check as reward), not SFT |
| 5 | §2 Together cost | "~2–4M tokens over 3 epochs" for 1,000 dialogues | 1,000 × 1.5–3k tokens × 3 = **4.5–9M**; per-turn expansion multiplies by ~2.5 | Still under $50; fix the arithmetic. Together ≤16B LoRA SFT ≈ $0.48/M [3P] |
| 6 | §3 Format | Format shown as `"meta"`; the README says `"metadata"` | Together ignores extra keys [V older docs]; Model Studio does not support extra message keys | Make the two docs agree on one key name, and strip it in the platform export |
| 7 | §3 Format / §4 Loss | "Platforms train on `messages`… loss on assistant turns only" | Together and Model Studio train **only the last assistant turn** for reasoning (Qwen3) models and need one example per turn [V]. Model Studio trains *all* assistant turns for non-thinking models and has no masking knobs [V] | Add the per-turn expansion step (§3 Step 1 here). It also settles the README's open question about history formatting: build each prefix exactly as `buildMessages` sends it |
| 8 | §4 Phase A | Nothing about thinking mode | Qwen3 thinks by default. Training should render empty think blocks; serving must send `enable_thinking:false` [V] | Add a "thinking off" row to the hyperparameter table and the provider change in §6 |
| 9 | §4 Phase A | rank 8 for the 8B control | LoRA Without Regret: rank matters less than all-layer targeting and LR; low ranks lose capacity only at larger data sizes | Use r=16 for both, so the 8B-vs-14B comparison changes only one variable |
| 10 | §4 Phase A | LR 1e-4, eff. batch 16, 3 epochs | Fine. Unsloth starts at 2e-4; LoRA tolerates small batches better; >3 epochs overfits | Keep 1e-4; try eff. batch 8; choose the epoch count by held-out eval; save checkpoints every ~25 steps |
| 11 | §4 Phase B | "beta 0.1, LR 5e-6, 1 epoch"; "DPO on Together/Fireworks" | Matches the Together defaults [V]. But Fireworks/Together DPO is **single-turn** (last message), Model Studio DPO is Beijing-only, and Fireworks gpt-oss SFT is single-turn | Note the single-turn layout (context = prefix) in §4 |
| 12 | §2 Candidates | Phi-4-reasoning as a bake-off model (per the task brief) | Always-reasoning model; the card requires a fixed system prompt and ChatML [V] | Swap for Phi-4 (non-reasoning), or accept that its thinking has to be trained out |
| 13 | §2 Self-host row | "Train with Axolotl / TRL / Unsloth" | Correct; also avoid AutoTrain (unmaintained) and torchtune (unmaintained) [V] | Add one line |
| 14 | §6 Deployment | "three env vars + restart" | A Qwen3 endpoint will think unless the request disables it; the provider sends no such field | Add `TUTOR_ENDPOINT_EXTRA_BODY` (or a hard-coded `chat_template_kwargs`) and strip `<think>` from `content` |
| 15 | §2 Qwen3 license row | 3.8-27B "conflicting license reports" | Post-release reports (eWeek, Aug 2026) say Apache-2.0 | Update the note; still check the LICENSE file |

---

## 6. Sources

| Topic | Link | What it supports |
|---|---|---|
| Together supported models | https://docs.together.ai/docs/fine-tuning-models | Qwen3.5/3.6/3.8 and gpt-oss-20b, context lengths, LoRA ranks |
| Together changelog | https://docs.together.ai/docs/changelog | Qwen3-8B/14B no longer available for FT |
| Together deprecations | https://docs.together.ai/docs/deprecations | FT deprecations and replacements |
| Together data prep | https://docs.together.ai/docs/fine-tuning/data-preparation | formats, alternation, extra keys, `train_on_inputs` |
| Together reasoning FT | https://docs.together.ai/docs/fine-tuning/reasoning | last-turn-only training, one example per turn, use reasoning data |
| Together DPO | https://docs.together.ai/docs/fine-tuning/preference-tuning ; https://docs.together.ai/docs/post-training/dpo | `dpo_beta` 0.1, LR 5e-6, preference format |
| Together LoRA inference | https://docs.together.ai/docs/lora-inference | serverless LoRA on select bases |
| Together download | https://docs.together.ai/reference/get-finetune-download ; https://docs.together.ai/docs/post-training/checkpoints | merged/adapter download; SGLang adapter layout |
| Together gpt-oss blog | https://www.together.ai/blog/fine-tune-gpt-oss-models-into-domain-experts-together-ai | gpt-oss LoRA SFT/DPO |
| Together pricing (3P) | https://www.costbench.com/software/fine-tuning-apis/together-ai-fine-tuning/ | $0.48 SFT / $1.20 DPO ≤16B |
| Fireworks SFT | https://docs.fireworks.ai/fine-tuning/supervised-fine-tuning | tunable families incl. Qwen3 dense, Phi 3/4 |
| Fireworks LoRA deploy | https://docs.fireworks.ai/fine-tuning/deploying-loras | on-demand only, multi-LoRA, live merge |
| Fireworks DPO | https://docs.fireworks.ai/fine-tuning/dpo-fine-tuning | single-turn DPO format |
| Fireworks changelog | https://docs.fireworks.ai/updates/changelog | gpt-oss SFT single-turn; Qwen3-8B serverless retired |
| Fireworks pricing | https://fireworks.ai/pricing | $0.50/$3.00 per M tiers; H100 $4/h; tuned model at base inference price |
| Fireworks pricing (3P) | https://www.morphllm.com/fireworks-ai-pricing | LoRA/full SFT/DPO split |
| Model Studio FT overview | https://www.alibabacloud.com/help/en/model-studio/model-training-overview | SFT/DPO/CPT; regions; methods |
| Model Studio billing | https://www.alibabacloud.com/help/en/model-studio/model-training-and-deployment-billing | $0.0016/1K training; LoRA serving $0.35/$1.40 |
| Model Studio qwen3-14b | https://www.alibabacloud.com/help/en/model-studio/qwen3-14b | per-token prices for the tuned model |
| Model Studio API / data rules | https://help.aliyun.com/en/model-studio/fine-tuning-api-guide ; https://help.aliyun.com/en/model-studio/text-generation-tuning-data-upload-rules | ChatML, all assistant turns trained, no `weight`, thinking last-turn |
| Model Studio LoRA import | https://www.alibabacloud.com/help/en/model-studio/my-model-center | PEFT import, rank 8–64, Beijing |
| Bedrock OpenAI-compatible FT | https://docs.aws.amazon.com/bedrock/latest/userguide/fine-tuning-openai-apis.html ; https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-reinforcement-fine-tuning-openai | RFT for qwen3-32b, gpt-oss-20b |
| AutoTrain status | https://huggingface.co/docs/autotrain/en/index | unmaintained |
| torchtune status | https://raw.githubusercontent.com/meta-pytorch/torchtune/main/README.md | not actively maintained |
| Modal prices (3P) | https://usagepricing.com/tools/pricing-calculator/modal | per-second GPU rates |
| RunPod vLLM worker | https://docs.runpod.io/serverless/workers/vllm/overview | OpenAI-compatible serverless vLLM |
| TRL SFT | https://huggingface.co/docs/trl/main/en/sft_trainer ; https://huggingface.co/docs/trl/main/en/chat_templates | `assistant_only_loss`, generation markers, Qwen3 auto-patch |
| TRL LoRA Without Regret | https://huggingface.co/docs/trl/main/en/lora_without_regret ; https://thinkingmachines.ai/blog/lora/ | all-layer LoRA, ~10× LR, small batch |
| Unsloth Qwen3 | https://docs.unsloth.ai/basics/qwen3-how-to-run-and-finetune | `enable_thinking`, fine-tune notebook |
| Unsloth Qwen3.5 | https://unsloth.ai/docs/models/qwen3.5/fine-tune | no QLoRA; VRAM table |
| Unsloth hyperparams | https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide | LR 2e-4 / 5e-6, epochs, rank |
| Unsloth gpt-oss | https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/tutorial-how-to-fine-tune-gpt-oss | 44 GB bf16 LoRA |
| OpenAI cookbook gpt-oss FT | https://developers.openai.com/cookbook/articles/gpt-oss/fine-tune-transfomers | harmony/TRL recipe, versions |
| Qwen3 template | https://huggingface.co/blog/qwen-3-chat-template-deep-dive ; https://arxiv.org/pdf/2505.09388 | empty think block; history stripping |
| Qwen multi-turn SFT discussion | https://github.com/QwenLM/Qwen3/discussions/1398 | removing earlier think blocks |
| Qwen Axolotl guide | https://qwen.readthedocs.io/en/stable/training/axolotl.html | Qwen3 YAML, messages format |
| vLLM LoRA | https://docs.vllm.ai/en/v0.20.2/features/lora/ | `--enable-lora`, JSON `--lora-modules`, resolver |
| vLLM structured outputs | https://docs.vllm.ai/en/latest/features/structured_outputs/ | `json_schema`; `guided_*` removed in v0.12 |
| Qwen speed benchmark | https://qwen.readthedocs.io/en/latest/getting_started/speed_benchmark.html | 14B ≈41 tok/s BF16 (Transformers) |
| LoRA forgetting | https://arxiv.org/html/2405.09673v2 | LoRA learns less, forgets less |
| Qwen3-14B license | https://huggingface.co/Qwen/Qwen3-14B | apache-2.0 |
| gpt-oss-20b license | https://huggingface.co/openai/gpt-oss-20b ; https://developers.openai.com/api/docs/models/gpt-oss-20b.md | Apache-2.0 + USAGE_POLICY |
| Phi-4-reasoning | https://ai.azure.com/catalog/models/microsoft-phi-4-reasoning ; https://huggingface.co/microsoft/Phi-4-reasoning | system prompt, 32k; MIT (3P) |
| Qwen3.8-27B license | https://www.eweek.com/news/alibaba-qwen3-8-27b-license-apac-china/ | Apache-2.0 at release |
| Qwen3.5 small (3P) | https://tokencost.app/blog/qwen-3-5-small-benchmarks-pricing | sizes, Apache-2.0, architecture |
