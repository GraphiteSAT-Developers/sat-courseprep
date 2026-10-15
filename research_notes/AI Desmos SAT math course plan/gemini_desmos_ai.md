# Building a Gemini-based SAT Math Tutor that is reliably good at Desmos

Research date: 2026-10-15. **Method caveat:** direct fetches of ai.google.dev and desmos.com were blocked from this research environment (proxy refused the connection), so every fact below comes from web-search result summaries of those pages and of third-party pages. Before you commit to any number (prices, rate limits, shutdown dates), check it against the official pages: https://ai.google.dev/gemini-api/docs/pricing, /models, /rate-limits, /deprecations, /terms and https://www.desmos.com/api.

## 1. Gemini API (as of Oct 2026): models, pricing, features, limits, terms, tuning

### Takeaway
The Gemini 3.x line is current. Gemini 3.1 Pro (preview) costs $2/$12 per 1M tokens (≤200K context) and has a 1M-token context window with function calling, structured output and code execution. The Flash and Flash-Lite tiers are much cheaper, but their names and prices change often. Two constraints matter most for an SAT product. First, the Gemini API terms require users to be 18+ and bar apps "directed towards or likely to be accessed by" under-18s. Second, supervised fine-tuning is not offered on the Gemini Developer API and is not yet available for Gemini 3.x on Vertex AI (renamed "Gemini Enterprise Agent Platform").

### Cited Findings
**Model lineup and status**
- Gemini 3.1 Pro: 1M-token input window. One aggregator gives the exact figure as 1,048,576 tokens in and 65,536 out. Function calling, code execution and structured output are listed as supported. — [Google Cloud docs: Gemini 3.1 Pro](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-pro); [DeepMind model card](https://deepmind.google/models/model-cards/gemini-3-1-pro/); [llm-stats](https://llm-stats.com/blog/research/gemini-3.1-pro-launch)
- Gemini 3.1 Pro supports "thinking levels". Third-party sources disagree on the set: Low/Medium/High in one, minimal/low/medium/high in another. Not confirmed officially. — [Verdent guide](https://www.verdent.ai/guides/what-is-gemini-3-1-pro); [OpenRouter](https://openrouter.ai/google/gemini-3.1-pro-preview)
- JSON-schema structured outputs on 3.1 Pro (third-party claim). — [OpenRouter](https://openrouter.ai/google/gemini-3.1-pro-preview)
- Deprecations page: Gemini 2.5 Pro preview versions (03/05/06-2025) were shut down Dec 2, 2025, and the listed replacement is `gemini-3.1-pro-preview`. Gemini 2.5 Flash-Lite preview 09-2025 was shut down Mar 31, 2026, with `gemini-3.1-flash-lite-preview` as the replacement. Stable 2.5 Flash and Flash-Lite have no shutdown date announced on the Developer API. On the Agent Platform/Vertex route they shut down on **Oct 20, 2026**. — [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations); [Firebase AI Logic models](https://firebase.google.com/docs/ai-logic/models); [Release notes](https://ai.google.dev/gemini-api/docs/changelog)
- Conflicting third-party claims: Gemini 3 Pro Preview was "aliased (2026-05)" to 3.1 Pro Preview, or discontinued 03/2026. — [benchlm deprecations](https://benchlm.ai/deprecations/google); [apiyi](https://docs.apiyi.com/en/api-capabilities/deprecated-models)
- GitHub Copilot deprecated Gemini 2.5 Pro and Gemini 3 Flash on Jul 31, 2026. This applies to Copilot only, not the API, but it shows how fast models turn over. — [GitHub changelog](https://github.blog/changelog/2026-07-31-gemini-2-5-pro-and-gemini-3-flash-deprecated/)
- Live API: `gemini-3.1-flash-live-preview` is the current native-audio real-time model. It is in preview via AI Studio and the Gemini Developer API, does audio, video and screen-share with tool use, and launched around Mar 26, 2026. Firebase says it is not available on the Agent Platform API. Google Cloud lists `gemini-live-2.5-flash-native-audio` as GA. — [Google blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-live/); [Google dev blog](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-3-1-flash-live/); [Firebase models](https://firebase.google.com/docs/ai-logic/models); [Cloud Live API overview](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api); [MarkTechPost](https://www.marktechpost.com/2026/03/26/google-releases-gemini-3-1-flash-live-a-real-time-multimodal-voice-model-for-low-latency-audio-video-and-tool-use-for-ai-agents/)
- Vertex AI was reportedly renamed "Gemini Enterprise Agent Platform" in 2026, and the Cloud docs URLs now use that path. A third party says the legacy `vertexai` SDK modules (including `vertexai.tuning`) were deprecated Jun 24, 2025 and set for removal Jun 24, 2026, with the Google Gen AI SDK as the replacement. — [Cloud docs URL](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-1-pro); [TheRouter.ai](https://therouter.ai/news/vertex-ai-sdk-migration-gemini-enterprise-agent-platform/)

**Pricing (per 1M tokens; sources dated Jan–Oct 2026; all third-party unless noted)**
- Gemini 3.1 Pro Preview: $2 input / $12 output for prompts ≤200K tokens, $4 / $18 above 200K. This is the most consistent figure across sources. — [CloudZero](https://www.cloudzero.com/blog/gemini-pricing/); [benchlm Oct 2026](https://benchlm.ai/google/api-pricing); [aifreeapi](https://www.aifreeapi.com/en/posts/gemini-api-pricing-2026)
- Gemini 3.1 Flash-Lite: $0.25 / $1.50. Batch is $0.125 / $0.75, i.e. Batch runs at about 50% of standard. — [Puter, Sep 2026](https://developer.puter.com/tutorials/gemini-api-pricing/); [mem0](https://mem0.ai/library/llms-and-models/gemini-api-pricing)
- Gemini 2.5 Flash-Lite: $0.10 / $0.40, the cheapest text model listed. — [geotoolbox](https://geotoolbox.ai/blog/gemini-api-pricing)
- Flash tier figures **conflict and are unverified**. Sources list "Gemini 3.5 Flash" at $1.50/$9.00, "3.5 Flash-Lite" at $0.30/$2.50, and "3.6/3.7/3.8 Flash" at $0.75/$3.75. One says that last rate is a promo through Dec 31, 2026, rising to $1.50/$7.50 after. One page says these newer versions were "not officially published" as of Sep 2026, and I could not confirm them. — [benchlm](https://benchlm.ai/google/api-pricing); [creditforstartups](https://creditforstartups.com/pricing/gemini-api-pricing); [memetik](https://www.memetik.ai/guides/gemini-api-free-tier-limits)

**Rate limits / free tier (all secondary; conflicting)**
- Google shows per-project limits (RPM, input TPM, RPD) in AI Studio instead of publishing fixed free-tier tables. The one fixed figure cited is 500 RPD each for Search and Maps grounding on 2.5 Flash and Flash-Lite. — [memetik, Sep 2026](https://www.memetik.ai/guides/gemini-api-free-tier-limits)
- Free-tier Flash is variously cited at 10–15 RPM and 500–1,500 RPD. Some sources say Pro was removed from the free API tier on Apr 1, 2026, and others contradict that. Paid tiers: Tier 1 needs billing on, Tier 2 needs $250 spend, Tier 3 needs $1,000 plus 30 days (June 2026 source). — [tinkerllm](https://tinkerllm.com/blog/gemini-api-free-tier-limits-rate-quotas/); [aipromptshub](https://aipromptshub.co/limits/gemini-rate-limits-2026); [pecollective](https://pecollective.com/tools/gemini-free-tier-guide/)

**Terms: data use and age**
- "You must be 18 years of age or older to use the APIs." Developers also may not use the Services in an app "directed towards or is likely to be accessed by individuals under the age of 18." — [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms); [Simon Willison summary](https://simonwillison.net/2024/Oct/17/gemini-terms-of-service/)
- Unpaid Services (AI Studio, free API quota): human reviewers may read, annotate and process inputs and outputs to improve products, and you should not submit sensitive or personal info. Paid Services: Google does not use prompts (including system instructions, cached content and files) or responses to improve products. In the EEA, Switzerland and the UK, the paid-service terms apply to all services. — [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms)

**Fine-tuning**
- Gemini Developer API tuning has been unavailable since Gemini 1.5 Flash-001, the last API-tunable model, was deprecated in May 2025. Tuning remains on Vertex AI. — [Google AI dev forum](https://discuss.ai.google.dev/t/gemini-api-fine-tuning-disabled/92763)
- Vertex AI SFT supports gemini-2.5-pro, 2.5-flash and 2.5-flash-lite (source dated Dec 2025). No Gemini 3.x model supports SFT yet. One claim says Gemini 3 tuning is limited to enterprise customers with existing contracts, and no timeline is announced. — [aifreeapi guide](https://www.aifreeapi.com/en/posts/how-to-fine-tune-gemini-custom-model); [Google Dev forum on 3.x SFT](https://discuss.google.dev/t/when-will-supervised-fine-tuning-be-available-for-gemini-3-x-models-on-vertex-ai/346487)
- Forum users report conflicting gemini-2.5-pro shutdown dates (Oct 17, 2026 vs Jun 17, 2026). It is also unclear whether tuned 2.5 endpoints stop serving when the base model does. — [Google AI dev forum](https://discuss.ai.google.dev/t/supervised-fine-tuned-gemini-2-5-pro-endpoints-what-happens-after-oct-17-2026-shutdown/137946)

### Inferences
- **Age is the biggest launch blocker.** SAT test-takers are mostly 16–17, so the Gemini Developer API terms appear to prohibit this use case outright. Legal review is needed before launch. Options to evaluate: Google Cloud / Agent Platform terms (Workspace for Education or enterprise agreements may differ), a different provider, or an 18+-only product. Use paid tier only, so student data is not used for training.
- **Fine-tuning is a weak lever here.** It is unavailable on the Developer API. On Vertex it is limited to 2.5-series models, which are being retired on that platform on Oct 20, 2026. So plan on prompting, few-shot examples, retrieval (RAG) and tool loops with a 3.x model. Keep SFT traces in a provider-agnostic format so you can tune later if 3.x SFT opens up, or so you can distill into an open model.
- **Suggested model split:** use 3.1 Pro (or the newest Pro) for offline generation of solution traces and as an eval judge. Use a Flash or Flash-Lite tier for the live tutor, with Batch at about 50% off for bulk data generation and evals. Use context caching for the long static system prompt plus technique library. Treat the Live API (3.1 Flash Live, with screen-share and tool use) as a phase-2 voice tutor.
- Pin explicit model versions and build a model-swap regression eval. Preview models alias or retire on roughly 3–9 month cycles.

### Gaps
- I could not read the official pricing, models or rate-limit pages directly, so the exact current Flash model IDs and prices (3 Flash vs 3.5 Flash vs "3.x Flash") are unverified. Claims of a "Gemini 4" are unverified.
- Not found: context-caching prices, storage fees and minimum token counts for 3.x; Live API session limits; whether code execution can be combined with function calling and structured output in a single call on 3.x.
- Whether Google offers a minors-compliant path (for example, Gemini for Education / Workspace terms) that an EdTech developer can build on.

## 2. Desmos API: capabilities, licensing, headless use

### Takeaway
The Desmos API (latest is v1.12) exposes everything a verification tool needs. You set expressions, and HelperExpressions report `numericValue` and `listValue`. `expressionAnalysis` reports per-expression errors, and `asyncScreenshot` waits for full evaluation. Production use needs a paid Commercial tier: Starter from $100/month for up to 1,000 users (Desmos-hosted only), or Enterprise at custom pricing with a self-hosting option. Open-source projects already run Desmos headless in Playwright for LLMs.

### Cited Findings
- The current docs page at desmos.com/api is titled "Desmos API v1.12". The v1.11.0 changelog added regression options and keyboard shortcuts. — [Desmos API](https://www.desmos.com/api); [Desmos API changelog](https://www.desmos.com/api/changelog)
- HelperExpression: evaluated like a normal expression but not shown in the expression list. It has observable `numericValue` (number results) and `listValue` (list results, present since at least v1.6). Example: `const a = calculator.HelperExpression({latex:'a'}); a.observe('numericValue', ()=>...)`. — [Desmos API v1.12](https://www.desmos.com/api); [v1.6 docs](https://www.desmos.com/api/v1.6/docs/index.html)
- `expressionAnalysis` (introduced in v1.0) is an observable object keyed by expression id. It reports whether each expression is graphable, whether it errored, and a localized error message. — [Desmos API v1.0](https://www.desmos.com/api/v1.0/docs/index.html)
- `asyncScreenshot` passes an image URI (PNG) or an SVG string to a callback, and guarantees the graph is fully evaluated before capture. — [Desmos API v1.11](https://www.desmos.com/api/v1.11/docs/index.html)
- Regressions: after a regression runs in Desmos, the fitted parameters are stored as variables usable elsewhere. The UI shows r (linear) or R² (nonlinear). I found no documented API route to R² or to the regression statistics panel. — [Desmos Help: Regressions](https://help.desmos.com/hc/en-us/articles/4406972958733-Regressions)
- Licensing: the free Trial Tier is limited to personal non-commercial use or a 90-day internal evaluation. "Commercial use includes any use of the API in an Application that is accessed by End Users in production, or any internal use of the API for a business purpose." Going beyond trial limits requires a self-service paid plan or a written Commercial Addendum (partnerships@desmos.com). — [Desmos API Terms](https://www.desmos.com/api-terms)
- Plans: free personal key; Starter from $100/month for up to 1,000 users, Desmos-hosted only; Enterprise custom-priced, Desmos-hosted or self-hosted. — [Desmos Help: API Plans for Commercial Use](https://help.desmos.com/hc/en-us/articles/49078363315725); [Desmos my-api](https://www.desmos.com/my-api)
- Headless precedent: MCP-Desmos (TypeScript, MIT) runs headless Chromium via Playwright, loads the official Desmos API, and exposes tools to plot (returns PNG), screenshot a shared graph URL, and extract expressions from a URL. — [GitHub: AndresMuelas2004/MCP-Desmos](https://github.com/AndresMuelas2004/MCP-Desmos)
- Desmos-MCP (TheGrSun) uses sympy for formula validation and analysis, with optional Desmos API integration and local fallback rendering. — [GitHub: TheGrSun/Desmos-MCP](https://github.com/thegrsun/desmos-mcp)
- Microsoft's Playwright MCP supports `--headless` for general browser-agent control. — [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
- The Digital SAT (Bluebook) has had built-in Desmos on all math questions since about March 2024, alongside a scientific calculator and a reference sheet. These are third-party guides; College Board pages were not retrieved. — [UWorld](https://collegeprep.uworld.com/blog/digital-sat-built-in-calculator-usage-and-tips/); [MEK Review](https://mekreview.com/?p=17093); [Acely Desmos cheat sheet](https://acely.com/sat/desmos-cheat-sheet)

### Inferences
- **Suggested tool design (headless Chromium in Node/Playwright with the API script loaded):**
  - `desmos_run({expressions:[{id, latex}], queries:[latex]})` → `setExpressions`. Then await settle with `observeEvent('change')`, `asyncScreenshot` or a timeout. For each expression, read `expressionAnalysis` (isError / errorMessage / isGraphable). For each query, create a HelperExpression and return `numericValue` / `listValue`. Optionally return an SVG or PNG screenshot.
  - Return structured JSON (errors are first-class) so the model can self-correct.
  - For regressions, write `y_1 \sim m x_1 + b` and then query helpers `m` and `b`. This is inferred from Desmos regression behavior and not confirmed in the API docs, so test it.
  - For intersections and zeros, Desmos shows points of interest in the UI. The API source I found did not confirm whether these are exposed. A safer approach is to have the model also emit a numeric query (for example, a helper on a root-finding construct) or to check candidates by substitution in helpers.
- Use the free trial key for the internal 90-day evaluation and harness build. Budget for a Commercial plan before any student sees it. Ask Desmos directly whether server-side automated, headless use for verification (no end-user display) is covered, and at what tier. Self-hosting needs Enterprise.
- Because the SAT uses Desmos natively, the tutor should teach student-reproducible Desmos keystrokes (graph both sides and click the intersection, sliders, regression with `~`). It should not teach only API-optimal constructs.

### Gaps
- Could not read the full v1.12 reference, so these are unconfirmed: the exact `expressionAnalysis` field names in v1.12, any API access to points of interest (intersections, extrema), access to regression statistics (R², residuals), and whether an API key is required in the script URL (older versions used `?apiKey=`; the trial key is presumably that).
- Desmos terms on automated or server-side rendering and on caching screenshots were not found.
- Common LaTeX errors LLMs make in Desmos: I found no published study. The candidate list in Section 3 comes from inference and needs empirical logging.

## 3. Making the LLM good at Desmos: tool loop, prompting, RAG, fine-tuning, synthetic data; prior research and tutoring pedagogy

### Takeaway
The proven pattern is tool-integrated reasoning (PAL → ToRA → ToRL/CoRT). The model interleaves natural-language reasoning with calls to an executor, and you improve it by keeping only trajectories whose executed result matches ground truth (rejection sampling / "output space shaping"), then imitation learning or RL. Apply it with Desmos as the executor. For tutoring, research shows a trade-off between solving ability and pedagogy, so solving and tutoring should be separate, evaluated stages. Google's LearnLM pedagogy is now built into Gemini (2.5+) and is reached through prompting.

### Cited Findings
- PAL: the LLM writes programs as intermediate reasoning steps, and the interpreter computes, which avoids arithmetic errors in chain-of-thought. — summarized in [ToRA paper](https://arxiv.org/pdf/2309.17452)
- ToRA (ICLR 2024): interleaves rationale with tool execution. Training is (1) imitation on GPT-4-generated tool-use trajectories, then (2) "output space shaping": sample diverse trajectories, keep the valid ones, have a teacher correct the invalid ones, and retrain. — [arXiv 2309.17452](https://arxiv.org/pdf/2309.17452)
- ToRL scales tool-integrated reasoning with RL, letting the model learn when and how to call tools beyond predefined patterns. — [arXiv 2503.23383](https://arxiv.org/pdf/2503.23383)
- CoRT uses rejection sampling plus RL to refine code/thinking interleaving, reporting +4% (32B) and +8% (1.5B) across five math datasets. — [arXiv 2510.20342](https://arxiv.org/html/2510.20342v1)
- No research was found using GeoGebra or Desmos specifically as an LLM reasoning tool. The existing Desmos+LLM work is MCP plotting servers (Section 2).
- LearnLM: no longer a separate model. Its capabilities were integrated into Gemini starting with the 2.5 series. Google publishes a LearnLM prompt guide for tutoring apps that references Gemini 3.1. — [Gemini API LearnLM page](https://ai.google.dev/gemini-api/docs/learnlm); [LearnLM prompt guide PDF](https://services.google.com/fh/files/misc/learnlm_prompt_guide.pdf); [LearnLM paper arXiv 2412.16429](https://arxiv.org/html/2412.16429v1)
- Guided Learning is a consumer Gemini-app mode that uses questions and step-by-step scaffolding. It is not confirmed as an API feature. Google cites a May 2026 report: students using Guided Learning for ≥12 hours over 8 weeks improved in math. A Sierra Leone study found LearnLM tutoring raised novel-problem solving by 5.5 percentage points vs human tutors alone. — [Google blog: Guided Learning](https://blog.google/products-and-platforms/products/education/guided-learning/); [Google Cloud LearnLM](https://cloud.google.com/solutions/learnlm)

### Inferences (recommended "training" approach without weight updates)
1. **Two-stage agent: Solver, then Tutor.**
   - The Solver privately solves the problem with Desmos tool calls until a verified answer exists, meaning the tool result agrees with an independent computation (code execution or sympy).
   - The Tutor then gets the verified solution plus the Desmos steps as hidden context and runs Socratic dialogue. It gives the student Desmos steps to try and checks the student's screenshot or expression via vision or the tool.
   - This addresses the solving-vs-pedagogy trade-off (Section 4).
2. **System prompt plus cached technique library (RAG).** Build about 30–60 SAT Desmos "moves", each with canonical LaTeX, when to use it, and pitfalls. Examples: intersect two curves; graph f(x)−g(x) and find zeros; sliders for unknown constants with "for what value of k…" via a table or regression `~`; regressions `y_1\sim ax_1^2+bx_1+c`; systems with no or infinite solutions (parallel or coincident); vertex and max/min; `\sqrt{}` and absolute value; `\left\{\right\}` restrictions; mean and median via `mean([...])`, `median([...])`; percent problems. Retrieve the top-k moves by problem type. Ship 3–8 worked few-shot traces in the cached prompt.
3. **Defensive LaTeX normalization layer.** A pre-processor and validator catches likely LLM errors before they reach Desmos. The list below is inferred and should be confirmed empirically from logs: `\frac` without braces; `*` vs `\cdot`; `^` exponents without braces (`x^10`); bare `sqrt`/`abs`; `\left(`/`\right)` mismatches; `y=` used where a regression needs `~`; reserved or multi-letter variable names (Desmos treats `ab` as a*b, so subscripts like `a_1` are required); degrees vs radians for trig; `e`/`\pi` conventions; markdown `$` delimiters left in the string. Feed `expressionAnalysis.errorMessage` back to the model for up to N retries, and log every error class.
4. **Self-verification.** Require the model to (a) substitute the answer back via a HelperExpression, (b) check that it matches a multiple-choice option, and (c) for SPR (grid-in) answers, check SAT formatting. Disagreement triggers a retry or escalation to the Pro model.
5. **Synthetic data via rejection sampling (ToRA-style).** For each problem with known ground truth:
   - Sample K Desmos trajectories with Pro.
   - Execute them in headless Desmos and keep those whose final answer matches and that have zero tool errors. Prefer shorter, student-reproducible ones.
   - Use these as few-shot examples, RAG entries and an SFT corpus. SFT applies only if a tunable model is available: Vertex 2.5 now, 3.x later, or an open model.
   - This also produces the error taxonomy for item 3.
6. **Vision.** Gemini multimodal input lets the tutor read photos of problems and screenshots of a student's Desmos. Verify by re-running extracted expressions in the tool rather than trusting pixel reading. This is an inference; graph-reading accuracy was not measured in sources.

### Gaps
- No published benchmarks on LLM accuracy at writing Desmos LaTeX, and no research on graphing-calculator-as-tool. This is novel territory, so plan internal measurement.
- Not found: the LearnLM prompt guide's specific pedagogical instructions (the PDF was not read in full); Khanmigo's published design specifics (not searched within budget).

## 4. Eval harness design

### Takeaway
Separate the metrics into three layers:
- (a) **Solver correctness:** exact match against ground truth.
- (b) **Tool hygiene:** Desmos expression validity rate, retries per problem, and whether the answer was verified by the tool.
- (c) **Tutoring quality:** rubric-based, with LLM-as-judge calibrated against human labels.

Published tutoring benchmarks show LLM judges are noisy (accuracy <0.7 in MathTutorBench) and that pedagogy and solving ability trade off.

### Cited Findings
- MathTutorBench (EMNLP 2025) evaluates Expertise, Student Understanding and Pedagogical Abilities. It uses a fine-tuned reward model ("Scaffolding Score") that beat LLM-as-judge baselines. LLM judges were prompt- and position-sensitive (order was randomized), with accuracy below 0.7. — [arXiv 2502.18940](https://arxiv.org/abs/2502.18940); [ACL Anthology](https://aclanthology.org/2025.emnlp-main.11/)
- The rubric dimensions used for human annotation include answer reveal, guidance, actionability, mistake identification, mistake location, coherence, tone and humanness. — [MathTutorBench](https://arxiv.org/html/2502.18940v2)
- Key finding: "Specializing an LLM for pedagogy comes at the cost of solving ability and, conversely, a high solving accuracy often means that the LLM lacks pedagogy." — [MathTutorBench](https://arxiv.org/html/2502.18940v2)
- AITutor-EvalKit uses LLM judges (GPT-5, Prometheus-7B-v2.0) on four pedagogical dimensions. MMTutorBench is a multimodal math-tutoring benchmark with a validated LLM-as-judge framework, relevant to screenshot and photo input. — [arXiv 2512.03688](https://arxiv.org/pdf/2512.03688); [arXiv 2510.23477](https://arxiv.org/pdf/2510.23477)

### Inferences (proposed harness)
- **Benchmark set:** about 300–500 SAT-style items stratified by College Board domain (Algebra, Advanced Math, Problem-Solving & Data Analysis, Geometry & Trig) and by difficulty. Mix MCQ and SPR. Tag each item "Desmos-advantaged" vs "Desmos-neutral". Store the ground-truth answer plus at least one reference Desmos solution verified in headless Desmos. Use original or licensed items; do not copy College Board material without checking rights. Hold out a contamination-safe test split.
- **Metrics:**
  - Solver: answer accuracy (pass@1, and self-consistency@k); tool-verified rate; expression error rate per call; retries per item; latency; cost per item.
  - Pedagogy, via simulated-student dialogues (an LLM student with scripted misconceptions): answer-reveal rate (must be about 0 before the student attempts); mistake identification and location; actionability of the Desmos instruction (can a student reproduce it in Bluebook?); tone.
  - Score pedagogy with an LLM judge (a different model family or Pro, with randomized order and pairwise comparisons). Calibrate on about 100 human-labeled dialogues, and report judge–human agreement before trusting it.
- Run the full suite on every prompt, model or tool change (regression gating), using Batch API pricing for cost.

### Gaps
- No public SAT-Desmos benchmark found. No figures found on Gemini 3.x accuracy on SAT math specifically.
- MRBench and other answer-leakage-specific evals were not located.
