# What the College Board framework says that should shape practice generation

_Source: College Board, "Assessment Framework for the Digital SAT Suite" (the 2026 update of the 2022 document). Page numbers below are the **printed** page numbers; in the PDF file the printed page N is PDF page N+9. Ranges read: chapter 2 (printed pp. 3–41) and the Math parts of chapter 5 (printed pp. 139–163: 5.2.2 Math, 5.3.2 calculator, 5.3.3 below-grade-level content). Chapter 4 (the Math test specification with domain weights and skill lists) was not in scope and is not cited here._

Everything in this note is either a direct reading of the framework or is marked as an inference. Quotes are kept to the sentences whose wording matters.

## 1. The two-module adaptive design (pp. 10–13, 37–38)

What the framework says:

- Each section is a two-stage multistage adaptive test (MST). Module 1 is the routing module: "a broad mix of easy, medium-difficulty, and hard questions" that gives "an accurate if provisional measure" of achievement (p. 11). Bluebook then picks one of two Module 2s: one is "on average, of higher difficulty than those in the first module," the other lower, "although both options include easy, medium-difficulty, and hard questions, albeit in differing proportions" (p. 11).
- The section score is "calculated based on student performance across all the questions given in the section" (p. 11), not Module 2 alone.
- Questions from all four Math content domains appear in both the routing module and the second-stage modules (p. 11).
- The routing "break point" is "set around the median" section score, so roughly half of test takers go to the harder module (p. 12). "For students who perform particularly well or poorly on the first module's questions, little chance of routing error exists" (p. 12). Simulation studies found routing accuracy over 93 percent and routing consistency over 90 percent (p. 12).
- "Many midlevel section scores are, by design, obtainable from either path" (p. 13). The framework does not state a score ceiling for the lower-difficulty path; that the top of the scale is reachable only on the harder path is an inference from this sentence, not a quoted fact.
- Deliberately tanking Module 1 to get the easier Module 2 lowers the final score in simulation (p. 13).
- Students can navigate freely within a module, mark questions for review, and return to them, but cannot return to Module 1 after moving on (pp. 11–12, 37).
- Each Math module is 22 questions: 20 operational plus 2 unscored pretest questions that are indistinguishable from scored ones (p. 13, 38). The same second-stage pretest questions appear in both Module 2 versions (p. 38).

What it implies for a practice site aimed at 700+ students:

1. **A "hard Module 2" is not all hard.** A faithful simulated Module 2 is a 22-item set whose *average* difficulty is above Module 1 but that still contains easy and medium items. A bank that is almost entirely `hard` (as `docs/item-writing.md` currently asks for) cannot assemble a realistic module of either kind. Keep a floor of easy and medium items in every domain and sequence practice modules with a mixed difficulty profile skewed hard, not uniformly hard.
2. **Routing is not the risk for this audience.** A student scoring 700+ is far above the median break point, and the framework says routing error is negligible for strong performers. A missed Module 1 item costs score points through the IRT model (section 2), not through routing. The course should drop "a Module 1 slip can send you to the capped path" as a motivational line for 700+ students and replace it with "every item, including easy ones, counts toward the IRT estimate."
3. **Simulate the mechanics, not just the difficulty.** The things that are actually module-shaped in Bluebook are: 22 items in 35 minutes, free navigation within the module, mark-for-review, a timer that can be hidden until five minutes remain (pp. 9, 23), and no return to Module 1. A practice module should reproduce these.
4. **Mix all four domains in every simulated module** (p. 11); do not run single-domain "modules" and call them module simulations. Single-domain sets are fine as drills.
5. **Pretest items are a design feature, not a curiosity.** Two of 22 items in each module are unscored. A simulated module can include two unscored items and report the score on the 20 that count, both to mirror the test and to make the "a miss on a pretest item costs nothing" point concrete.

## 2. Scoring and the "roughly one miss for 800" claim (pp. 28–30)

What the framework says:

- Section scores are 200–800 in 10-point intervals; total 400–1600 (Table 2, p. 28).
- Each MC response is scored 1 or 0 against the key. Each SPR response is "cleansed" (for example, double fractional slashes or decimals removed) and compared to the keyed response(s); a match scores 1 (p. 29).
- Scoring uses item response theory. Under it "scoring is a function of three main factors: (1) whether a student answers questions correctly or incorrectly, (2) attributes of the questions, such as difficulty level, that a student answers correctly or incorrectly, and (3) whether a student's response pattern across questions suggests guessing" (p. 29). The next sentence is the one that matters for the 800 claim: **"Therefore, two students may obtain the same number of correct responses on two different test forms but still have different reported scale scores"** (p. 29).
- There is no guessing penalty. The IRT model "evaluates test taker response patterns to estimate the likelihood that a student answered a given question correctly merely by guessing" (sidebar, p. 29). College Board advises answering every question.
- The framework publishes no raw-to-scale conversion and no statement about how many misses an 800 tolerates.
- The Math College and Career Readiness benchmark is 530 (Table 3, p. 30). Skills Insight describes what students in each score band typically can do (pp. 30–31); it is the only official description of what the top band looks like, and it was not in the ranges read here.

Bearing on HANDOFF.md and the report:

- "An 800 tolerates roughly one miss" is a third-party estimate. The framework neither confirms nor refutes it, and its own statement that the same raw count can map to different scale scores on different forms means no fixed miss count can be correct for every form. The course should present it as "plan for zero misses; on some forms one miss still scores 800."
- The report's claim that under IRT "a careless miss on an easy Module 1 item ... costs more than a hard miss" is **not stated in the framework**. The framework says item difficulty is a factor in scoring; it does not say which direction. Treat the "easy misses cost more" claim as third-party or as an inference, not as sourced to the framework.
- The guessing-pattern factor is real and official. A student who answers inconsistently with their ability (missing easy items while getting hard ones right) is exactly the pattern the model reads as guessing. That is a defensible official reason to drill accuracy on easy items, and a better one than the unsourced "easy misses cost more" line.
- For the site's own scoring, do not try to reproduce an IRT scale score. Report raw correct out of 20 operational items per module, flag which items were easy, and keep "projected score" out of the product unless it carries a clear "estimate, not College Board's method" label.

## 3. Calculator policy and its rationale (pp. 23, 26, 161–162)

Policy:

- Universal tools list (p. 23): **"Calculator. A built-in Desmos® calculator is available for the entire Math section. Students can toggle between scientific and graphing options."** A reference sheet of common formulas is also available (p. 23).
- Section 5.3.2 (p. 161): **"In the digital SAT Suite Math section, students are allowed to use a calculator—either the Desmos graphing or scientific calculator built directly into Bluebook, the digital testing app, or their own approved handheld device—on all Math questions."** This "ended a paper-era policy of having separately timed calculator-allowed and no-calculator portions of the Math section" (p. 161).
- A four-function calculator is listed as an accommodation (p. 26), which only matters if the site ever serves accommodated students.

Rationale (p. 161–162). These are the sentences to quote as the official basis for a Desmos-first course:

- The policy "is consistent with both how and how often students use calculators as tools in their schoolwork and daily lives and with extant and emerging evidence about the value of calculator use in educational settings" (p. 161).
- Barton's 2000 meta-analysis "suggested positive impacts of calculator use on overall achievement and conceptual understanding, while most studies showed no effect on students' procedural knowledge" (p. 161).
- Ellington (2003): "when calculators were part of *both* testing and instruction, the operational skills, computational skills, skills necessary to understand mathematical concepts, and problem-solving skills improved for participating students" (p. 161, emphasis in original).
- **"Finally, because strategic calculator use is embedded in the math achievement construct being measured by the digital SAT Suite, there is no risk that students' use of the tool will in any way compromise the validity of the assessments or the data yielded by them."** (p. 162)
- "Having the choice is important because student comfort with the tools they will use during testing is vital to obtaining an accurate assessment of their achievement in math" (p. 162).

The sentences that limit Desmos-first, which the course should also honor:

- **"these test developers carefully examine each question to ensure that calculator use does not trivialize or otherwise short-circuit the intended rigor of the questions; moreover, in furtherance of the goal of supporting strategic (rather than indiscriminate) use of the calculator as a tool, College Board test developers also create some questions for which a calculator is either not needed or its use is not particularly beneficial to solving the problem."** (p. 162)

Design consequences:

- "Strategic calculator use" is College Board's own phrase for the construct. The course's `route` field (`desmos-primary` / `hand-primary` / `either`) is the operational form of that phrase, and the framework explicitly says some items are written so that a calculator does not help. The bank must keep a meaningful share of `hand-primary` items, and the tutor must be able to say "Desmos won't help here" as a taught skill, not a fallback.
- The framework names both the graphing and the scientific calculator. The site embeds only the graphing calculator; that matches what matters, but the tutor should know the scientific view exists and that content does not carry over (reported in the research notes, not the framework).
- The reference sheet is a universal tool. Items that need a formula on the sheet should not be treated as requiring memorization; the practice UI should expose the same sheet.

## 4. Below-grade-level content and procedural versus reasoning items (pp. 13–14, 139–146, 162–163)

Below-grade-level content (5.3.3, pp. 162–163):

- The Math section covers "some topics, such as ratios, rates, and proportions as well as area, perimeter, and volume, that, by a strict reading of many state academic standards documents, should have been mastered by students at grades earlier" than the test-taking population (p. 162).
- Two reasons given. First, these skills "are not merely precursors to advanced mathematics; they are also integral components of mathematical proficiency," and "the scenarios and applications in which such topics are tested may well be more complex than those encountered in middle school" (p. 163). Second, including them "supports the psychometric quality of the assessment by improving score scale coverage and measurement precision across a wide range of achievement levels" (p. 163).
- "the inclusion or exclusion of specific content is governed not by its nominal grade placement but by its relevance to the construct being measured" (p. 163).

Procedural versus reasoning:

- Pretesting "has consistently demonstrated that digital-suite questions are capable of spanning the full range of difficulty required by the specifications and emphasize higher-order thinking skills over low-level recognition, recall, and rote application of rules and algorithms" (p. 14).
- Algebra: questions "require students to demonstrate skill in generalization, abstraction, and symbolization, with a strong emphasis on equivalence and using structure. Many of the test questions are constructed to allow for more than one solving strategy" (p. 140).
- Advanced Math: "Many of the test questions represent challenging, authentic problems in context for which students can draw on strategies developed during their coursework to solve" (p. 142).
- Problem-Solving and Data Analysis: proportional reasoning "is assessed, at appropriately challenging levels, throughout the digital SAT Suite" (p. 144); questions "test a wide range of reasoning skills" (p. 144) and are "not aligned to those covered in a specific secondary-level course" (p. 144).
- Geometry and Trigonometry: questions "vary in difficulty from easy to very hard and allow students to demonstrate problem-solving skills and knowledge using a variety of solving strategies" (p. 146). Geometric objects are also "woven into questions in the Algebra and Advanced Math domains ... as contexts for building functions or modeling real-world scenarios" (p. 145). Trigonometry is tested only on the SAT, PSAT/NMSQT and PSAT 10 (p. 145); radians, unit circle and circle theorems are SAT-only (p. 146).
- The framework does not give a numeric procedural/reasoning split. What it gives is a direction: the hard end of the scale is reached through structure, equivalence, multi-strategy problems and unfamiliar contexts, not through harder arithmetic.

Design consequences:

- A 700+ bank still needs ratio, rate, percent, area and volume items, written at the "more complex scenario" level the framework describes, not as middle-school drills. The current difficulty guidance in `docs/item-writing.md` ("`hard` for items with unknown constants, a structural insight, or two ideas combined") matches the framework's description of what makes an item hard.
- "More than one solving strategy" is the official hook for teaching Desmos and by-hand routes to the same item. Items tagged `either` are the ones that best embody it; the bank should have plenty of them, and the tutor should be able to show the second route after the first succeeds.
- Hard geometry items may live inside Algebra or Advanced Math (a geometric context for a function). The `domain` tag should follow the skill being measured, not the presence of a figure.

## 5. Timing, question length and word count (pp. 9, 21–23, 37–40)

- Math: two modules of 35 minutes, 22 questions each (20 operational + 2 pretest), 44 questions in 70 minutes, "1.59 minutes" average per question (Table 7, p. 37; pp. 38). The average is uniform across difficulty; the framework assigns no per-item time by difficulty.
- The timer counts down per module and can be hidden until five minutes remain, after which it cannot be hidden (pp. 9, 23).
- Extended time accommodations are time-and-one-half, double time, and more than double (p. 25). A practice timer with 1.0x, 1.5x and 2.0x settings would cover the official options.
- Question formats: "Approximately 75 percent of questions in the Math section use the same four-option multiple-choice format, while the remainder use the student-produced response (SPR) format" (p. 39). SPR questions "assess students' ability to solve math problems with greater independence and with less structure and support than that provided in the multiple-choice format. SPR questions may have more than one correct response, although students are directed to supply only one answer" (p. 39).
- Bluebook validates SPR entries: it precludes "entry of too many digits; use of nonnumerical characters other than the negative sign and the slash for fractional answers" and shows a preview of the typed answer (p. 21). The site's SPR grader and input box should enforce the same character set and preview.
- Context and word count: "about 30 percent of test questions are set in academic (science or social studies) or real-world contexts, while the rest are 'pure' math questions set outside of context" (p. 39). "Math contexts are brief: sufficient in length to establish a scenario but clear, direct, and concise enough not to impose undue linguistic burdens on students" (p. 39). "In-context Math questions are typically fifty (six-character) words or fewer" (p. 40); Table 7 phrases it as "a majority of in-context questions have 50 (6-character) words or fewer" (p. 37). A "word" here is six characters including spaces and punctuation, so the limit is about 300 characters of stem.
- Math contexts are not rated for text complexity, but staff "review each context qualitatively to ensure that its linguistic load and demands are consistent with the requirements of the question being posed," applying linguistic-modification principles (p. 40; see also p. 22, which says this is "particularly important for the Math section").
- Topic-specific prior knowledge is never required; contexts "may assume that students have acquired the sorts of general subject area knowledge typically imparted by a rigorous secondary curriculum" (p. 39).
- Informational graphics in Math: "a wide range of data displays, geometric figures, and *xy*-plane graphs," including scatterplots (pp. 37, 40). Graphics have textual alternatives for accessibility (p. 22).

Design consequences for item generation:

- Add two checks to the item verifier: a context flag (target about 30 percent of a batch in context) and a six-character word count on in-context stems with a soft ceiling of 50 (300 characters). An item generator that writes long word problems is off-model.
- Item generation prompts should carry the linguistic-modification rule: plain words, direct sentences, no scenario detail that the question does not use.
- Timed practice should use 35 minutes per 22-item module as the only official pacing figure. The "1.5 minutes per item" line in the report is a rounding of 1.59.

## 6. What the Math section is designed to measure, mapped to item fields (pp. 4, 14, 19, 32–33, 139–146, 162)

Official statements about the construct:

- The suite measures "essential college and career readiness outcomes" (p. 3) and each test collects "evidence from student performance in support of a set of broad claims about what students know and can do" (p. 4).
- Questions emphasize "higher-order thinking skills over low-level recognition, recall, and rote application of rules and algorithms" (p. 14).
- "strategic calculator use is embedded in the math achievement construct being measured" (p. 162).
- The Math construct is "math achievement" with construct-irrelevant factors (language load, visual acuity, home region) deliberately removed (pp. 19, 22). This is why word count and plain language matter: linguistic difficulty is treated as noise, not signal.
- College Board's own three levels of practice (p. 32–33): platform familiarization, test wisdom ("acquaint students with the types of questions ... and offer insights into ways they can improve"), and skill/knowledge building ("durable academic abilities"). The framework warns that "overfocusing on repetitive test- or question-level practice risks narrowing students' attention ... to only those skills and knowledge elements directly measured" and "runs the risk of conflating a proxy of the desired skills and knowledge ... with the goal of developing students' durable skills" (p. 33).

Mapping to the item schema in `web/content/types.ts`:

| Framework idea | Item field | How to use it |
|---|---|---|
| "Strategic (rather than indiscriminate)" calculator use; some items where a calculator "is not particularly beneficial" (p. 162) | `route` | `desmos-primary`, `hand-primary`, `either` is the right vocabulary. Keep a real share of `hand-primary`. |
| "More than one solving strategy" (pp. 140, 146) | `route: "either"` plus both `desmos` and `byHand` | These items are the core of the Desmos-first / by-hand-second lesson. |
| Conceptual understanding improved by calculator use; procedural knowledge unaffected (Barton, p. 161) | `techniques` | Technique IDs should name a conceptual move (read an intersection, find constants by regression), not a keystroke sequence. The by-hand route carries the procedural half. |
| "Generalization, abstraction, and symbolization ... equivalence and using structure" (p. 140) | `skill`, `difficulty` | Use these as the criteria for `hard`: unknown constants, structural equivalence, combining two ideas. |
| Domain descriptions (pp. 140–146) | `domain`, `skill` | Tag by the skill measured; geometric contexts inside function items stay in `algebra` or `advanced-math`. |
| "Less structure and support" in SPR (p. 39) | `format: "spr"` | SPR is a deliberate independence check, about a quarter of items. Keep the ratio in simulated modules. |
| Context ~30 percent, ≤50 six-character words (pp. 37–40) | new: `context: boolean`, verifier word count | Not in the schema yet; recommended addition. |
| Three practice levels (pp. 32–33) | course structure, not an item field | Platform familiarization = the Bluebook-like embed and SPR entry box; test wisdom = the technique library and `route`; skill building = the by-hand routes and reasoning explanations. The framework's warning against pure question-drilling is a reason to keep the by-hand route and conceptual explanation in every item rather than only a keystroke recipe. |

## 7. Corrections to HANDOFF.md and the report

None of these require editing the framework claims that were cited correctly (the 44/70/20+2 structure, IRT scoring, Desmos on every question, 1.59 minutes). These are the places where the project documents go further than, or against, the framework.

1. **"Only the harder Module 2 can lead to 800" (report, research note line 11).** Not stated in the framework. The framework says midlevel scores are obtainable from either path (p. 13) and gives no ceiling for the lower path. Keep the claim, but label it an inference and drop the attribution to the Assessment Framework.
2. **"Under IRT, missing a hard item costs less than missing an easy one, so careless errors on easy questions are the biggest risk to 800" (research note line 31; report, scoring paragraph).** The framework says difficulty is a scoring factor (p. 29) but does not state the direction. The official and quotable reason to drill easy-item accuracy is the guessing-pattern factor (p. 29 sidebar), not item weighting.
3. **"Module 1 errors also risk routing a student to the easier Module 2, which caps the score" (research note line 34; report).** For the course's 700+ audience this is wrong in emphasis: the break point is near the median and "little chance of routing error exists" for strong performers (p. 12). Reframe as a point about the IRT estimate, not routing.
4. **"Roughly one miss for 800" (HANDOFF title framing; report section heading).** No official basis. The framework's statement that equal raw counts can yield different scale scores on different forms (p. 29) means a fixed miss count is form-dependent. Say "plan for zero; some forms tolerate one."
5. **`docs/item-writing.md`: "lean `hard` ... `easy` is for warm-ups only."** The harder Module 2 still contains easy and medium items (p. 11), and Module 1 is a broad mix. A bank with no easy or medium items cannot assemble a faithful simulated module. Keep a floor of easy and medium items per domain for module simulation; drills can still lean hard.
6. **The report's pedagogy section describes "timed 22-question mini-modules at about 1.5 minutes per item."** The official pacing unit is 35 minutes per 22-item module (p. 38), which the module simulation should use directly rather than a per-item timer; also mirror the hideable timer and the five-minute forced reveal (p. 23).
7. **The report's calculator paragraph treats Desmos only as a graphing calculator.** The framework names both a graphing and a scientific Desmos calculator in Bluebook, plus the student's own approved handheld (pp. 23, 161). Not a contradiction, but the tutor and the FAQ should say so.
8. **Research note line 18: "a 3-parameter model is used" is third-party.** The framework confirms only that the model accounts for correctness, item attributes such as difficulty, and guessing patterns (p. 29). Keep the 3PL claim marked third-party; do not attribute it to the framework.
9. **No word-count or context rule anywhere in the project docs.** Not a contradiction, but the framework's 30 percent in-context and 50 six-character-word figures (pp. 37, 39–40) are concrete enough to enforce in the verifier, and currently nothing does.
10. **SPR grader scope.** The framework describes Bluebook as rejecting nonnumeric characters other than the minus sign and slash and showing a preview (p. 21), and scoring as cleansing double slashes or decimals before matching (p. 29). The project's SPR rules (5/6 characters, fraction or decimal) are consistent, but the entry box should also reject the disallowed characters at input time, as Bluebook does.
11. **The report's "Desmos solves or verifies roughly a third to half of questions" is unsourced to College Board.** The framework gives no fraction but does say some questions are written so a calculator does not help (p. 162). The marketing line can stand, but the product must not imply Desmos is the primary route on most items.
