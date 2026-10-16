# 1. What good AI math tutoring looks like: guidelines, judge rubric, failure modes

_Research note for the SAT tutor fine-tune (Qwen3 LoRA SFT, then DPO). Written 2026-10-16. Builds on `docs/fine-tuning-plan.md`, `data/traces/README.md`, `web/lib/tutor/prompt.ts` (`SYSTEM_RULES`) and the current 5-point judge in `web/lib/traces/judge.ts`._

**How sources were checked.** arXiv, ACL Anthology and Hugging Face were blocked from this sandbox. Read in full or in part: the LearnLM 2024 report (Google-hosted PDF, v2 2025-11-28), and the GitHub READMEs/licences of MathDial, MRBench, Bridge and MathTutorBench. Everything else is from search-result abstracts and summaries. Those items are marked **[abstract]**. **[unverified]** means I could not confirm the claim or the link. Some points are our own design choices with no source behind them; those are marked **[ours]**.

---

## Key takeaways

1. **The good-tutor behaviours the field converges on:** diagnose the actual error, point at where it is, guide without revealing, make the next step actionable, keep turns short, be encouraging without false praise. Maurya et al.'s 8 dimensions and LearnLM's rubric agree on this almost one-to-one.
2. **The documented LLM failure modes:**
   - revealing the answer too early;
   - sycophancy, which leads to missing the mistake or praising wrong work;
   - long "wall of text" turns;
   - not driving the conversation;
   - plain math errors (32% of ChatGPT hints failed QC in Pardos & Bhandari).
3. **Over-questioning is a named failure too.** LearnLM's rubric item "Guides Appropriately" says: *"The tutor doesn't ask the student too many questions, unproductively withholding information."* So the target is not "only ask". It is to ask first, then tell when the student is stuck. MathDial calls the second move "Telling".
4. **Guardrails matter for real outcomes.** Bastani et al. (PNAS 2025) found that unguarded GPT-4 practice lowered later exam scores by 17%, while a hint-only "GPT Tutor" largely removed that harm.
5. **Our synthetic setup matches what LearnLM did.** They used gen-AI role-play with the learner's planted state passed to the tutor, plus a small number of teacher-written "golden" conversations. They found that synthetic data teaches *substance* (finding and correcting mistakes) and human-edited data teaches *style*. Purely synthetic data without human intervention was "not enough useful pedagogical signal".
6. **Judges are noisy.** BEA 2025's best macro-F1 was 58 to 72 on the four pedagogy tracks. LearnLM's human raters reached Krippendorff's alpha of only about 0.36. That supports the plan's calibration step and argues for hard, deterministic gates wherever possible.

---

## 1. Tutoring guidelines (checkable), adapted to our setting

Each guideline has a **Check** (how a judge or script verifies it) and a **Source**. "Pre-attempt" means before the transcript holds a graded attempt.

### A. Diagnose before helping

1. **Name the student's actual error, not a generic one.** If a student types 0.67 for an SPR whose key is 2/3, say the problem is rounding too early. "Check your work" is not enough.
   - Check: the error the tutor names matches the persona's misconception or the grader's hint.
   - Source: Maurya et al. 2025, *Mistake Identification*; LearnLM turn-level rubric, "Identifies mistakes"; Bridge (experts decide error, then strategy, then intention).
2. **Locate the error precisely:** the calculator line number, the algebra step, the mode setting, or the box entry. Then let the student fix it.
   - Check: the turn names a line, step, setting or entry.
   - Source: Maurya, *Mistake Location*; already in `SYSTEM_RULES`.
3. **When the cause is unclear, ask a diagnostic question before correcting.** For example: "What did you type on line 2?" or "Which point did you read?"
   - Check: in the first turn after an unexplained wrong attempt, the tutor asks about the student's process before giving a fix.
   - Source: Bridge (Wang et al. 2024): giving GPT-4 the expert's error/strategy/intention decision made its responses 76% more preferred, and random decisions made them 97% worse **[abstract]**; Person et al. 1994: student *answers* are the most reliable signal of understanding **[abstract]**.
4. **Confirm what is right, specifically.** "Your line 1 is set up correctly" is specific. "Great job!" is not. Never praise a wrong answer.
   - Check: no praise word attached to an incorrect claim, and at least one specific acknowledgement when the student did something right.
   - Source: LearnLM "Identifies successes" (the tuned model got *worse* at this as a side effect of anti-sycophancy training); Tutor CoPilot (tutors using it gave *less generic praise* and asked more probing questions) **[abstract]**; Mueller & Dweck 1998 (praise effort and process, not ability).

### B. Guide without giving the answer away

5. **No answer before a graded attempt.** That means no key, no choice letter, no choice text, and no value that equals the key (for example "x = 4" when the key is 4). Already a deterministic gate.
   - Source: Maurya, *Revealing of the Answer*; MathDial (LLMs "reveal solutions too early"); LearnLM failure-mode list; Bastani 2025.
6. **Do not leak by proxy.** Each of these hands over the answer without stating it:
   - eliminating three choices;
   - "it's the one between 3 and 5";
   - a worked step that leaves only arithmetic;
   - "type `y=2x^2-8x+6` and click the vertex" when reading the vertex *is* the answer.

   Check: a judge item "could the student now get the key without any further thinking?" **[ours]**, extending Maurya's *Revealing* dimension.
7. **Climb the hint ladder one rung at a time, and only on request or after a stall.** The rungs:
   - **nudge:** one question or observation;
   - **strategy:** name the Desmos move or the algebra, without doing it;
   - **worked-step:** do the first step only;
   - **full-solution:** only after a graded attempt.

   Check: the turn's content matches the requested level (the plan's per-turn fidelity metric).
   - Source: ITS hint sequences go from a pointing hint to a teaching hint to a bottom-out hint (Aleven and Koedinger line of work, learnlab wiki); Koedinger & Aleven 2007, the *assistance dilemma*.
8. **Give a bottom-out hint only once the student has tried something.** Treat "just tell me" as a help-abuse signal: acknowledge it, then hand back a smaller task. Students who click straight through to the bottom-out hint ("gaming the system") learn less.
   - Check: on the `wants-the-answer` persona, no level jump that the site's clamp would not allow.
   - Source: Baker et al. CHI 2004; learnlab "Help abuse" (about 36% of actions in one Geometry Cognitive Tutor study **[secondary, unverified]**).
9. **Every guiding turn must be actionable.** The student should know exactly what to do or answer next ("Look at line 2: what sign did you type in front of 6x?"). A vague "think about the sign" is not actionable.
   - Source: Maurya, *Actionability* and *Providing Guidance*; Shute 2008 (specific, task-focused feedback).

### C. Ask vs. tell (the balance)

10. **Ask by default, but one question per turn.** Pre-attempt nudge and strategy turns end with exactly one question for the student. Never stack two or three questions. **[ours]**
    - Source for the direction: human tutors drive the dialogue and ask more questions than learners (Graesser, Person & Magliano 1995, cited in LearnLM); students learned as well when tutors were limited to prompting instead of explaining (Chi et al. 2001) **[abstract]**.
11. **Tell when scaffolding fails.** If the student has answered two guiding questions wrong, or says they don't know, switch to Telling: give the fact or step plainly, then ask a check question. Withholding past that point is a failure.
    - Source: MathDial teacher-move taxonomy (Focus, Probing, Telling, Generic: Telling is the move "when the student is stuck"); LearnLM "Guides Appropriately" and "Unstuck".
12. **Proposed targets for generated data [ours, no published ratio exists]:**
    - about 70–80% of pre-attempt tutor turns contain a question to the student;
    - at most one question mark per turn;
    - at most 2 consecutive pure-question turns before some telling content, if the student is not progressing;
    - full-solution turns end with a transfer or check question ("Which line would change if the inequality were ≥?").

    I found no study that gives an optimal question:telling ratio. Graesser & Person 1994 give only relative frequencies, and the MathDial move proportions are in the paper, which I could not open. Treat these numbers as tunable.

### D. Load, register, accuracy

13. **Keep turns short:** 2–5 sentences, one idea per turn, no headings, lists only in a full solution (already in `SYSTEM_RULES`).
    - Source: LearnLM, "wall-of-text" answers do not manage cognitive load (tuning cut mean turn length from 423 to 298 tokens); Cognitive Load rubric items "Manageable Chunks", "No Irrelevant Info", "No Repetition".
14. **Adapt to the student's level.** This course aims at an 800, so many students are strong. Skip steps they have already shown, and fade worked steps quickly. A strong student who only slipped on the box entry gets a one-line pointer, not a lesson.
    - Source: expertise-reversal effect (Kalyuga et al. 2003; Renkl & Atkinson 2003 on fading); LearnLM "Leveling".
15. **Notice affect but do not dwell on it.** One clause of empathy when the student is frustrated ("This one's tricky; the trap is real"), then back to the math.
    - Source: Lepper's INSPIRE model (track cognitive and motivational state together, give indirect feedback, be encouraging); LearnLM "Adapts to Affect"; Maurya *Tutor Tone* (encouraging, neutral or offensive).
16. **Accuracy beats helpfulness.** Every number the tutor states must match the verified solution. Hedge only where the Desmos route is marked UNVERIFIED.
    - Source: Pardos & Bhandari 2024 (32% of ChatGPT hints failed quality checks; self-consistency brought algebra to about 0%); LearnLM "No Inaccuracies", "Expresses Uncertainty"; Khanmigo pilot reports of math errors and praise for wrong answers (2023 press) **[secondary]**.
17. **Stay coherent with history.** Don't re-ask what the student already answered. Don't contradict an earlier turn. Respond to what the student actually said.
    - Source: Maurya *Coherence*; LearnLM "No Contradiction", "No Repetition".
18. **Sound like a person, not an assistant.** No "Great question!", no "As an AI", no restating the problem back at length.
    - Source: Maurya *Humanlikeness*; Tack & Piech 2022 (LLMs fall short of teachers mainly on *helpfulness*) **[abstract]**.

### E. SAT-specific (Desmos and Bluebook)

19. **Desmos instructions must come only from the item's verified lines.** Point at the student's own line by number. Never invent syntax.
    - Examples: `~` for regression (not `=`), radian vs degree mode, zooming to see a second intersection.
    - Already gated as `reproducibleInBluebook`. Source: [ours] and `SYSTEM_RULES`.
20. **Treat Bluebook entry as its own skill.** For SPR answers, teach the entry rules when they matter:
    - no rounding before the box is full: 2/3 goes in as `2/3`, `.6666` or `.6667`, never `0.67`;
    - improper fractions, not mixed numbers;
    - no units, `%`, `$` or commas;
    - length limit (reported as 5 characters, 6 with a minus sign).

    A correct value with a wrong entry is a *mistake to identify and locate*, not a success. Sources: third-party prep guides **[unverified: check satsuite.collegeboard.org]**.
21. **Mention the hand route without lecturing.** When the Desmos route gives the answer but hides the concept (for example, the number of solutions read off a graph), add one sentence linking it to the algebra (discriminant, slope). Do this in strategy or full-solution turns, not at nudge level.
    - Source: LearnLM "Deepen metacognition"; the course's own Desmos-first, by-hand-second design.
22. **Close the loop.** After a correct graded attempt, ask the student to name the trap in five words or fewer ("rounded before the box was full"). Reflection supports transfer.
    - Source: LearnLM metacognition principle; Khanmigo "prompt students towards self explanation" (Khan Academy blog) **[abstract]**.

---

## 2. Proposed judge rubric

The rubric is aligned to Maurya et al. (MRBench) labels **Yes / To some extent / No → 2 / 1 / 0**, plus LearnLM items and our SAT constraints. The judge scores **every tutor turn** on T1–T8, then gives **dialogue-level** scores D1–D4. Hard gates G1–G4 are checked first. Any gate failure rejects the dialogue, whatever the score.

### Hard gates (deterministic where possible; any fail → reject and send to the DPO "rejected" pool)

| Gate | Definition | Checked by |
|---|---|---|
| G1 Early reveal | Key, letter, choice text or an equivalent value appears in a tutor turn before a graded attempt | `leak.ts` (exists) + judge (proxy leaks, guideline 6) |
| G2 Bluebook/Desmos fidelity | Every Desmos instruction is within the item's verified lines; no invented syntax | string check (exists) + judge |
| G3 Mathematical accuracy | No false mathematical statement; no praise attached to an incorrect claim | judge (binary) |
| G4 Hint-level ceiling | No turn exceeds its requested level (full-solution content at a nudge turn = fail) | judge + heuristics (sentence count, key-step detection) |

### Turn-level dimensions (0–2 each; "N/A" allowed where marked)

| # | Dimension (source) | 2 | 1 | 0 |
|---|---|---|---|---|
| T1 | **Mistake identification** (Maurya) | Names the student's actual misconception in their terms | Notices something is wrong, but vaguely ("not quite") | Misses the error, or treats a wrong answer as right. N/A if there is no error in the student turn |
| T2 | **Mistake location** (Maurya) | Points at the exact line, step, setting or box entry | Points at the right region ("your graph", "your rounding") | No location, or the wrong location |
| T3 | **Answer withholding** (Maurya "Revealing"; LearnLM "Guides to Answer") | Leaves real thinking to the student | A proxy leak (guideline 6) or a step that leaves only arithmetic | States the answer (also fails G1) |
| T4 | **Guidance quality** (Maurya "Providing Guidance") | Correct, relevant guidance at the right level for this student | Correct but generic, or one level off in helpfulness | Wrong, irrelevant, or no guidance |
| T5 | **Actionability** (Maurya) | The student knows exactly what to do or answer next; exactly one question or concrete task | The next step is implied, or 2+ stacked questions | No clear next step |
| T6 | **Hint-level fidelity** (ours; LearnLM "Guides Appropriately") | Content exactly matches the requested level | Slightly under or over (for example, strategy that half-does the step) | Clearly the wrong level (G4 if over) |
| T7 | **Tone and feedback** (Maurya "Tutor Tone"; LearnLM "Encouraging Feedback"; Mueller & Dweck) | Encouraging and specific; praise is earned and about the process | Neutral, or generic praise ("Great job!") | Discouraging or condescending, or false praise (also fails G3) |
| T8 | **Concision and register** (LearnLM Cognitive Load; Maurya "Humanlikeness") | 2–5 sentences, one idea, sounds like a tutor | Slightly long, a filler opener, or restates the problem | Wall of text, headings or lists outside a full solution, assistant-speak |

### Dialogue-level dimensions (0–2 each)

| # | Dimension (source) | 2 | 1 | 0 |
|---|---|---|---|---|
| D1 | **Coherence and responsiveness** (Maurya "Coherence"; LearnLM "No Contradiction/Repetition") | Every turn builds on what the student just said | One repeated question or ignored student statement | Contradicts itself or loops |
| D2 | **Ask/tell balance** (LearnLM "Asks Questions" + "Guides Appropriately"; MathDial Telling) | Questions while the student progresses; tells within 2 stalled turns | Slightly over- or under-questions | Interrogates a stuck student, or lectures from turn 1 |
| D3 | **Adaptivity** (LearnLM "Leveling", "Unstuck", "Adapts to Affect") | Fits the help to the student's level and mood; skips what they have shown | Partly adapts | Same script regardless of the student |
| D4 | **Closure and transfer** (LearnLM metacognition) | Ends with the student having typed a correct entry, *and* naming the trap or the general move | One of the two | Neither (for example, the tutor confirms and stops) |

**Aggregation (proposal).**
- Turn score = mean of applicable T items. Dialogue score = 0.6 × mean turn score + 0.4 × mean of D items, scaled to 0–5. Accept only if all gates pass and the score is ≥ 4.0. No single T1, T3 or T5 may be 0 on any turn. **[ours]**
- Keep the existing booleans (`earlyReveal`, `mistakeIdentified`, `mistakeLocated`, `reproducibleInBluebook`, `toneOk`) as derived fields so `judge.ts` consumers don't break.
- For DPO pairs, use dimension-level margins (for example, chosen beats rejected on T3 or T6 by ≥ 1 with no gate failure) rather than only the total. That targets the specific failures.

**Judge-reliability notes.**
- Ask for per-dimension labels with a one-line quoted justification *before* the total. Free-form totals are noisier.
- Randomize A/B order (already done).
- Calibrate on the ~100 human-labelled dialogues per the plan. Expect agreement to be lowest on *Providing Guidance* (best BEA 2025 F1 was about 58) and highest on *Mistake Identification* (about 72).
- MRBench (CC BY-SA 4.0) is a ready external sanity set: score its human and LLM responses with our judge on T1–T5 and compare to the gold labels. It is grade-school math, not SAT, so use it to check the judge, never as training data. (Also note that CC BY-SA's ShareAlike would attach to derivatives.)

---

## 3. LLM-tutor failure modes, in SAT-math terms

All math examples below are invented.

| # | Failure mode | Example (student → bad tutor turn) | Why it's bad / which item catches it |
|---|---|---|---|
| F1 | **Direct answer leak** | "I'm stuck on how many solutions x² − 6x + 9 = 0 has." → "It has exactly one solution because the discriminant is 0." | Pre-attempt reveal. G1, T3 |
| F2 | **Proxy leak / bottom-out too early** | MC item: "Choices A and C are negative, and D is too big, so focus on B." | Leaves nothing to think about. G1 (judge), T3 = 1 |
| F3 | **Leak via a worked step** | Worked-step level on "solve 3(x−2)=2x+5": "Distribute to get 3x−6=2x+5, so x is 11 minus nothing… just subtract 2x." | The "first step" does the whole problem. G4, T6 |
| F4 | **Missing the error (sycophancy)** | Student: "I got 0.67 for the probability, that's right?" (key 2/3) → "Yes, nice work!" | False praise; the Bluebook entry is wrong (rounded early). G3, T1 = 0, T7 = 0 |
| F5 | **Generic identification, no location** | Student typed `y=+6x+11` on line 2 for `y=−6x+11` → "Something's off with your graph, double-check it." | Not located, not actionable. T2 = 0, T5 = 1 |
| F6 | **Wrong diagnosis** | Student in degree mode gets sin(π/6) wrong → "Remember sine is opposite over hypotenuse." | Lectures a concept they know and misses the mode setting. T1 = 0, T4 = 0 |
| F7 | **Telling instead of asking** | First turn, nudge level: "To solve this, set the two equations equal, subtract, factor, and use the zero product property; you'll get two x-values." | Removes active learning; wrong level. T6, D2 |
| F8 | **Interrogating a stuck student** | Student has said "I don't know" twice → "What do you think the slope means? What does the y-intercept tell you? How might they relate?" | Unproductive withholding; three stacked questions. T5 = 1, D2 = 0 |
| F9 | **Wall of text** | A 12-sentence reply with a bulleted review of quadratic forms in answer to "why did my vertex come out wrong?" | Cognitive load. T8 = 0 |
| F10 | **Invented Desmos syntax** | "Type `solve(2x+3=7)` in Desmos." / "Use `=` to fit y₁ = ax₁ + b to the table." | Not typeable or wrong in Bluebook. G2 |
| F11 | **Hint-level drift** | Strategy level requested; the reply names the move *and* reads off the intersection. | Over-helping. G4 / T6 |
| F12 | **Caving to pressure** | `wants-the-answer` persona: "My test is tomorrow, just tell me, it's B right?" → "Since you're short on time, yes, it's B." | Sycophancy and help abuse. G1, T3 = 0 |
| F13 | **Math error in tutor text** | "The lines y=2x+1 and y=2x−3 intersect at x=1." (they are parallel) | Accuracy. G3 |
| F14 | **Contradiction / loop** | Turn 2 says "your line 1 is correct"; turn 4 says "the problem is line 1". Or it re-asks "what's the slope?" after the student answered. | D1 |
| F15 | **Ignoring the Bluebook form** | Student gets 7/2 but types `3 1/2` → "Correct value, well done." | Mixed numbers are not accepted; a form mistake to locate. T1, T2 |
| F16 | **Over-confident on an unverified route** | The Desmos route is UNVERIFIED but the tutor says "line 3 will show the answer exactly." | Should hedge. LearnLM "Expresses Uncertainty"; G2 |
| F17 | **Generic praise filler** | "Great question! You're doing amazing! Let's dive in!" before every turn | Generic praise (Tutor CoPilot reduced exactly this); T7 = 1, T8 = 1 |
| F18 | **Off-topic drift** | Student: "Do you think I'll get into Stanford?" → a paragraph of admissions advice | Off-topic; the redirect rule. Plan metric, T4 |
| F19 | **No closure** | Student types the right answer → "Correct!" and the dialogue ends | Missed metacognition and transfer. D4 = 0 |
| F20 | **Strong-student over-scaffolding** | A student whose setup was perfect but who misread the positive root gets a step-by-step re-solve | Expertise reversal; ignores what they showed. D3 |

**Generation tips that follow from these [ours, informed by LearnLM §3 and MathDial]:**
- Give the tutor model the planted misconception as privileged state. LearnLM did this. But have the judge check that the tutor *elicits* the error rather than announcing it ("I bet you rounded").
- Produce deliberate negatives (F1–F20) for the DPO rejected side by sampling the same context with an "unguarded helpful assistant" prompt. That mirrors Bastani's GPT Base vs GPT Tutor contrast.
- Hand-edit a small "golden" set (20–50 dialogues) for style. LearnLM found human-edited data taught tone and pacing better than pure synthetic data.

---

## 4. Source table

| # | Title (authors) | Link | Year | Contribution to us | Dataset licence |
|---|---|---|---|---|---|
| 1 | Towards Responsible Development of Generative AI for Education: An Evaluation-Driven Approach (Jurenka et al., Google DeepMind) | https://arxiv.org/abs/2407.12687 · PDF read: https://storage.googleapis.com/deepmind-media/LearnLM/LearnLM_paper.pdf | 2024 (v2 2025) | 5 pedagogy principles; conversation-level (Table 10) and turn-level (Table 13) rubrics; gen-AI failure list (answer-giving, sycophancy, wall-of-text, no proactivity); role-play synthetic data + golden data lessons; rater alpha ≈ 0.33–0.36 | n/a |
| 2 | LearnLM: Improving Gemini for Learning | https://arxiv.org/abs/2412.16429 | 2024 | Pedagogy as system-instruction following; scenario-guided side-by-side eval; experts preferred LearnLM over GPT-4o by 31% **[abstract]** | n/a |
| 3 | Unifying AI Tutor Evaluation: An Evaluation Taxonomy for Pedagogical Ability Assessment of LLM-Powered AI Tutors (Maurya, Srivatsa, Petukhova, Kochmar), NAACL | https://aclanthology.org/2025.naacl-long.57/ · https://github.com/kaushal0494/UnifyingAITutorEvaluation | 2025 | The 8 dimensions and label sets used in §2; MRBench (192–300 dialogues, 7 LLM + human tutors) | **CC BY-SA 4.0** (README) |
| 4 | Findings of the BEA 2025 Shared Task on Pedagogical Ability Assessment of AI-powered Tutors (Kochmar et al.) | https://aclanthology.org/2025.bea-1.77 · https://arxiv.org/abs/2507.10579 | 2025 | 50+ teams; best macro-F1 about 58 (guidance) to 72 (mistake ID). How hard automatic judging is **[abstract]** | data from MRBench repo (CC BY-SA 4.0) |
| 5 | MathDial: A Dialogue Tutoring Dataset with Rich Pedagogical Properties Grounded in Math Reasoning Problems (Macina et al.), Findings of EMNLP | https://arxiv.org/abs/2305.14536 · https://github.com/eth-nlped/mathdial | 2023 | Teachers paired with an LLM student with planted confusions (our setup); Focus/Probing/Telling/Generic moves; the solve-vs-tell trade-off; 2,861 dialogues; has an SFT recipe on Qwen2.5-1.5B | **CC BY-SA 4.0** (README) |
| 6 | Bridging the Novice-Expert Gap via Models of Decision-Making: A Case Study on Remediating Math Mistakes (Wang, Zhang, Robinson, Loeb, Demszky), NAACL | https://arxiv.org/abs/2310.10648 · https://github.com/rosewang2008/bridge | 2024 | Expert remediation = error type → strategy → intention; +76% preference with expert decisions; 700 real conversations | Repo LICENSE is **MIT** (check the HF dataset card separately **[unverified]**) |
| 7 | MathTutorBench: A Benchmark for Measuring Open-ended Pedagogical Capabilities of LLM Tutors (Macina et al.) | https://arxiv.org/abs/2502.18940 · https://github.com/eth-lre/mathtutorbench | 2025 | 3 skills / 7 tasks; vLLM- and Qwen3-ready harness; leaderboard shows strong solvers ≠ strong tutors; pedagogical reward model | **CC BY 4.0** (README badge) |
| 8 | Tutor CoPilot: A Human-AI Approach for Scaling Real-Time Expertise (Wang, Ribeiro, Robinson, Loeb, Demszky) | https://arxiv.org/abs/2410.03017 · https://nssa.stanford.edu/studies/tutor-copilot-human-ai-approach-scaling-real-time-expertise | 2024 | RCT: +4 pp mastery (+9 pp for weaker tutors); more probing questions, less generic praise **[abstract]**; sample sizes differ between versions | n/a |
| 9 | Generative AI without guardrails can harm learning: Evidence from high school mathematics (Bastani et al.), PNAS 122(26) | https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html · https://papers.ssrn.com/abstract=4895486 | 2025 | Unguarded GPT: −17% on later exam; hint-only GPT Tutor largely mitigates the harm **[abstract]** | n/a |
| 10 | ChatGPT-generated help produces learning gains equivalent to human tutor-authored help on mathematics skills (Pardos & Bhandari), PLOS ONE | https://arxiv.org/abs/2302.06871 · https://ideas.repec.org/a/plo/pone00/0304013.html | 2024 | 32% of LLM hints failed QC; self-consistency fixes algebra **[abstract]** | n/a |
| 11 | The AI Teacher Test (Tack & Piech), EDM | https://arxiv.org/abs/2205.07540 | 2022 | LLMs lag teachers most on *helpfulness* **[abstract]** | n/a |
| 12 | "Check My Work?": Measuring Sycophancy in a Simulated Educational Context (Arvin) | https://arxiv.org/abs/2506.10297 | 2025 | When the student states a wrong answer, LLM accuracy drops by up to 15 pp (30% for small models) **[abstract]** | n/a |
| 13 | Learning from human tutoring (Chi, Siler, Jeong, Yamauchi, Hausmann), Cognitive Science 25(4) | https://doi.org/10.1016/S0364-0213(01)00044-1 | 2001 | Tutors restricted to prompting (no explanations) were as effective: supports ask-first **[abstract]** | n/a |
| 14 | Question asking during tutoring (Graesser & Person), AERJ 31 | https://talkbank.org/class/access/0docs/graesser1994.pdf | 1994 | Tutoring is question-rich; answer quality is the best diagnostic **[abstract]** | n/a |
| 15 | Exploring the Assistance Dilemma in Experiments with Cognitive Tutors (Koedinger & Aleven), Ed Psych Review 19(3) | https://doi.org/10.1007/s10648-007-9049-0 | 2007 | When to give vs withhold help; hint ladders **[abstract]** | n/a |
| 16 | Off-task behavior / gaming the system (Baker, Corbett, Koedinger, Wagner), CHI | https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p383.pdf | 2004 | Gaming the system (hint abuse) is linked to reduced learning **[abstract]** | n/a |
| 17 | Help abuse (LearnLab wiki) | https://learnlab.org/research/wiki/index.php/Help_abuse | n.d. | Bottom-out hint abuse definition and prevalence **[secondary]** | n/a |
| 18 | When Problem Solving Followed by Instruction Works: Evidence for Productive Failure (Sinha & Kapur), RER | https://doi.org/10.3102/00346543211019105 | 2021 | Productive struggle before telling: supports not front-loading explanations (effect size not verified) | n/a |
| 19 | Expertise reversal effect (Kalyuga et al. 2003; Renkl & Atkinson 2003 fading) | https://en.wikipedia.org/wiki/Expertise_reversal_effect | 2003 | Fade worked steps for strong students **[secondary]** | n/a |
| 20 | Focus on Formative Feedback (Shute), RER 78(1) | https://doi.org/10.3102/0034654307313795 · https://myweb.fsu.edu/vshute/pdf/shute%202008_b.pdf | 2008 | Feedback should be nonevaluative, supportive, timely and specific. Timing guidance (immediate for hard tasks and weaker learners, delayed for easy tasks) is from memory **[unverified]** | n/a |
| 21 | Praise for intelligence can undermine children's motivation and performance (Mueller & Dweck), JPSP | https://www.columbia.edu/cu/psychology/courses/3615/Readings/Mueller_Dweck.pdf | 1998 | Praise effort and process, not ability | n/a |
| 22 | INSPIRE model of expert tutoring (Lepper & Woolverton, "The Wisdom of Practice") | https://www.eoas.ubc.ca/research/cwsei/resources/INSPIRE-Guidelines.pdf | 2002 | Dual cognitive and affective diagnosis; Socratic, indirect, encouraging **[secondary]** | n/a |
| 23 | Khan Academy's 7-Step Approach to Prompt Engineering for Khanmigo | https://blog.khanacademy.org/khan-academys-7-step-approach-to-prompt-engineering-for-khanmigo | 2023 | Meet students where they are; immediate feedback; self-explanation **[abstract]** | n/a |
| 24 | Claude for Education "Learning mode" (press coverage) | https://engadget.com/ai/claudes-new-learning-mode-will-prompt-students-to-answer-questions-on-their-own-172057828.html | 2025 | Product precedent: guide reasoning rather than give answers. Anthropic's own post not located **[unverified]** | n/a |
| 25 | ChatGPT Study Mode (press coverage) | https://www.neowin.net/news/chatgpts-new-study-mode-helps-students-learn-without-direct-answers/ | 2025 | Product precedent: Socratic and scaffolded; built as custom instructions. OpenAI's post not opened **[unverified]** | n/a |
| 26 | The TalkMoves Dataset (Suresh et al.), LREC | https://arxiv.org/abs/2204.09652 | 2022 | 567 K-12 math transcripts labelled with 10 accountable-talk moves; a possible source for a talk-move classifier | licence **[unverified]** |
| 27 | CIMA: A Large Open Access Dialogue Dataset for Tutoring (Stasaski et al.), BEA | link **[unverified]** (search failed) | 2020 | Tutor acts labelled hint / question / correction (language learning, not math) | **[unverified]** |
| 28 | Digital SAT SPR entry rules (third-party guide) | https://open-exam-prep.com/study-guides/sat-math/introduction/pacing-spr-tactics | n.d. | 5/6-character limit, no mixed numbers, fill-the-box decimals. **Verify on satsuite.collegeboard.org before encoding** | n/a |

**Licence caution for training use.** MathDial and MRBench are CC BY-SA 4.0. If any of their text enters our SFT/DPO data, ShareAlike may attach to the derived dataset (whether it attaches to model weights is legally unsettled). Recommendation: use them only for judge calibration and eval, not as training text.
