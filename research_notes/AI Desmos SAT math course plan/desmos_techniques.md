# Desmos Techniques for Digital SAT Math: Technique Library and Existing Resources

Research method note: in this session, direct page fetches (WebFetch/curl) were blocked by the egress proxy for every site tried (acely.com, oneprep.co, help.desmos.com, desmos.com, reddit mirror). All findings below come from web-search result summaries of the cited pages. Treat quotes as summary-level and re-verify exact wording/prices before publishing. Nearly all sources are test-prep company blogs (commercial, self-interested); the only primary/official sources found are the Desmos/College Board testing PDF and the Desmos Help Center "Supported Functions" page.

## 1. Core techniques: technique → SAT question types → Desmos syntax → pitfalls → when by-hand is faster

### Takeaway
Roughly a dozen core moves cover most Desmos-solvable SAT items. They are: graph-and-intersect, zeros, clicking points of interest (vertex/extrema), sliders, tilde regression (data fitting and "find the constants" equivalence), tables, list statistics, inequality shading, circle reading, function definition/evaluation, and graphing answer choices. Sources broadly agree on syntax. They disagree on when to use Desmos for circles and parallel-line/no-solution systems.

### Cited Findings

**T1. Graph both sides / intersection (solve any one-variable equation)**
- Solve an equation by graphing each side and clicking the intersection, or rewrite it as "= 0" and read the x-intercepts. — [Acely cheat sheet (via search summary)](https://acely.com/sat-prep/desmos-cheat-sheet)
- Pitfall: an intersection can be off-screen, so zoom out before concluding "no solution." — [CheetahPrep systems walkthrough](https://www.cheetahprep.com/desmos/system-linear-equations-infinite); [OnePrep 12 moves](https://www.oneprep.co/blog/sat-math-tips-desmos-2026-12-calculator-moves) ("many SAT traps are just 'you didn't zoom'")
- Pitfall: zooming too far in loses context. — [Miyagi Labs](https://miyagilabs.ai/blog/desmos-sat-tips-guide)

**T2. Systems of equations (linear/nonlinear)**
- Type both equations and click the intersection point to read (x, y). — [The Test Advantage: systems on Desmos](https://thetestadvantage.com/blog/systems-of-equations-on-desmos-sat-math-shortcut-guide)
- Read the graph this way: overlapping lines mean infinitely many solutions, parallel non-touching lines mean no solution. — [CheetahPrep](https://www.cheetahprep.com/desmos/system-linear-equations-infinite)

**T3. Unknown constants that give infinitely many / no / exactly one solution (sliders + ratios)**
- Type the equation with the unknown letter (e.g., k). Desmos offers "add slider." Drag it until the graphs coincide, become parallel, or are tangent. — [The Test Advantage: infinite solutions guide](https://thetestadvantage.com/blog/sat-infinite-solutions-systems-on-desmos-may-2026-full-guide)
- Recommended hybrid: put both equations in Ax + By = C form and compare ratios. Example: ax + 4y = 12 and 6x + by = 18 have every ratio equal to 12/18 = 2/3, so a = 4 and b = 6. Then graph to confirm the overlap. — [The Test Advantage](https://thetestadvantage.com/blog/sat-infinite-solutions-systems-on-desmos-may-2026-full-guide)
- Counter-view: Say Hello College lists parallel-line systems among problems to avoid doing in Desmos. — [Say Hello College](https://sayhellocollege.com/blog/guide-to-using-the-desmos-sat-calculator/)
- Count solutions by counting intersections, with sliders for "how many solutions" questions. — [Aniko: how many solutions](https://www.aniko.ai/free-resources/sat/courses/desmos/how-many-solutions); [Edison OS guide](https://www.edisonos.com/digital-sat/desmos-guide)

**T4. Sliders (general)**
- Typing an unknown coefficient as a letter (y = mx + b) prompts a dynamic slider. — [Edison OS guide](https://www.edisonos.com/digital-sat/desmos-guide)

**T5. Regression with tables (line/curve of best fit, model from data/points)**
- Syntax: add a table with columns x₁, y₁, then type `y_1 ~ m x_1 + b`. The underscore makes the subscript and ~ is the regression operator. — [Edison OS guide](https://www.edisonos.com/digital-sat/desmos-guide)
- With only one point plus a slope, you cannot regress; type the formula manually. Regression needs at least 2 points. — [Edison OS guide (via search)](https://www.edisonos.com/digital-sat/desmos-guide)
- Exponential/power fits use forms such as `y_1 ~ a b^{x_1}`. Desmos shared graphs show this. — [Desmos shared graph](https://desmos.com/calculator/vrhmsznixn?lang=de)
- The College Board version automatically turns on Log Mode for applicable exponential, logarithmic, and power regressions. — [Official College Board Desmos PDF](https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator.pdf); echoed by [The Test Advantage](https://thetestadvantage.com/blog/how-to-use-desmos-on-the-sat-complete-may-2026-guide)
- Pursu has a dedicated guide, "5 Desmos tricks to find constraints & line of best fit." — [Pursu regression guide](https://pursu.io/guide/sat-regression-questions-solved-the-5-desmos-tricks-to-find-constraints-line-of-best-fit). LearnDesmos has an 8-chapter regression unit. — [LearnDesmos regression curriculum](https://learndesmos.com/curriculum/regression). A dedicated drill site also exists. — [SAT Regression Trainer](https://regressiontrainer.org/)

**T6. "Tilde trick" for equivalent expressions / finding coefficients**
- Replace "=" with "~" and x with x₁, then supply a list of test values for x₁ with at least as many values as unknown constants. — [Resolve Prep regression guide](https://resolveprep.com/blog/desmos-regression-sat-guide)
- Worked example: `(5x_1 − 17)(4x_1 − c) ~ a x_1^2 + b x_1 + 119` with `x_1 = [2, 3, 4]` gives c = 7, a = 20, b = −103. Expanding confirms 20x² − 103x + 119. — [Resolve Prep](https://resolveprep.com/blog/desmos-regression-sat-guide)
- Pitfalls: the x₁ list (setup line) is required and fails silently if omitted. Regression returns only one solution. Constants must actually be constant. Don't retype the rounded decimals shown, since Desmos stores more digits. — [Resolve Prep](https://resolveprep.com/blog/desmos-regression-sat-guide)
- Alternative check for "which expression is equivalent": graph both as y = …; exact overlap means equivalent. — [Resolve Prep key features](https://resolveprep.com/blog/key-desmos-features)

**T7. Lists and statistics (mean, median, SD, range)**
- Official functions: mean, median, min, max, quartile, quantile, stdev (sample SD), stdevp (population SD). Lists use square brackets, e.g. [1,5,5,10]. — [Desmos Help Center: Supported Functions](https://help.desmos.com/hc/en-us/articles/212235786-Supported-Functions); [Desmos User Guide PDF](https://desmos.s3.amazonaws.com/Desmos_User_Guide.pdf)
- Pitfall: curly braces mean a restriction, not a list, so `L_1 = {4, 7}` builds no list and stats come back blank. (Third-party claim, not confirmed on the Help Center.) — [Learner Labs stats-from-list](https://learnerlabs.app/sat-prep/desmos/stats-from-list)

**T8. Inequalities (shading, systems of inequalities, "which point satisfies")**
- Desmos shades each inequality. Strict (<, >) inequalities get a dashed line and inclusive (≤, ≥) a solid one, and the darker overlap is the solution set. Typing <= / >= auto-converts. Confirm the region with a test point instead of trusting overlapping colors. — [Effortless Math 12 moves](https://www.effortlessmath.com/blog/desmos-sat-math-cheat-sheet-12-moves/); [BWS Education Consulting Ten Tips PDF](https://bwseducationconsulting.com/wp-content/uploads/2024/07/Desmos_SAT_Tips_and_Tricks.pdf)

**T9. Function definition and evaluation**
- Define `f(x) = 2x + 5`, then type `f(3)` to evaluate. — [Edison OS guide](https://www.edisonos.com/digital-sat/desmos-guide)

**T10. Circles (center/radius from expanded form)**
- Desmos graphs expanded forms directly. Example: x² + y² − 6x + 4y − 3 = 0 has center (3, −2) and radius 4, with no completing the square. — [Pursu circles guide](https://pursu.io/guide/sat-circles-made-easy-7-ways-to-solve-geometry-problems-using-desmos-with-examples)
- Clicking the curve shows gray dots at the top and bottom. The center is their midpoint and the radius is half the distance between them. Desmos does not reliably mark the leftmost/rightmost points. — [Learner Labs circles](https://learnerlabs.app/sat-prep/desmos/circles); [Aniko circle equations](https://www.aniko.ai/free-resources/sat/courses/desmos/circle-equations-in-the-graph)
- Diameter endpoints: name the points A=(−2,1) and B=(4,9), then use `midpoint(A,B)` for the center and `distance(A,B)/2` for the radius. — [Learner Labs circles](https://learnerlabs.app/sat-prep/desmos/circles)
- Conflict: Say Hello College lists center/radius of circles among problems to avoid with Desmos. — [Say Hello College](https://sayhellocollege.com/blog/guide-to-using-the-desmos-sat-calculator/)

**T11. Exact vs. decimal answers (fraction conversion)**
- Use the fraction toggle to convert a decimal to an exact value (example: 5.125 becomes 41/8). Store exact values in variables to avoid rounding errors. — [LearnQ blog](https://blogs.learnq.ai/math-calcutor-desmos-digital-sat/)
- For free-response items, one source recommends solving by hand to get an exact answer. — [Sherpa/aggregated search summary: Sherpalai cheat sheet](https://sherpalai.com/sat-r-desmos-calculator-tips/sat-math-desmos-cheat-sheet)

**T12. Trig**
- The most common and costly trig error is wrong angle mode (radians vs. degrees). Check settings first. — [Miyagi Labs](https://miyagilabs.ai/blog/desmos-sat-tips-guide); [Acely cheat sheet](https://acely.com/sat-prep/desmos-cheat-sheet)

**T13. Checking / back-solving answer choices**
- Graph or plug each answer choice in and eliminate. This works best for multiple choice. — [Strategic Test Prep 6 hacks](https://www.strategictestprep.com/post/6-desmos-hacks-to-boost-your-sat-math-score); [Sherpalai](https://sherpalai.com/sat-r-desmos-calculator-tips/sat-math-desmos-cheat-sheet)

**General entry errors**
- The most common entry mistakes are missing parentheses, sign errors, using the wrong variable, and reading an approximate value as exact. — [LearnQ](https://blogs.learnq.ai/math-calcutor-desmos-digital-sat/); [Miyagi Labs](https://miyagilabs.ai/blog/desmos-sat-tips-guide)

### Inferences
- Below are Desmos behaviors from my background knowledge of Desmos. I could not verify them with a source this session, so test them in desmos.com/testing/collegeboard/graphing before putting them in the curriculum:
  - Vertex/max/min: clicking a parabola shows gray "points of interest" (vertex, zeros, y-intercept). Hovering or clicking shows the coordinates. This covers vertex-form, max height, and zero questions.
  - Sum/product: type `sum` or `prod` to get Σ/Π templates, or use `total([list])`. Ranges like `[1...10]` generate lists.
  - Absolute value: `|` or `abs()`. Questions like "how many solutions does |x−3| = k have" become T1/T3 (graph y = |x−3| and y = k, then slide k).
  - Percent: Desmos accepts `%` (e.g., `20% of 50` is supported in newer versions). Plain decimal arithmetic is the safer teaching default.
  - Domain restriction: append `{0 < x < 5}` to an expression. This is the restriction meaning of {} that T7 warns about.
  - Implicit multiplication: `ab` is parsed as a·b, but multi-letter function names (e.g., `mean`, `sin`) are auto-recognized. A user-defined parameter list like `ax^2+bx+c` works. Typing `x1` without an underscore may auto-subscript in Desmos, but `x_1` is the safe form.
  - Exponential growth/decay: graph `y = a(1+r)^x` with sliders, or regress `y_1 ~ a b^{x_1}` on given points.
- The two "find constants" methods (T3 sliders, T6 tilde regression) are the biggest differentiators between basic and advanced Desmos instruction. For an AI tutor, T6 is highly algorithmic and well suited to automated step generation.
- The conflicting advice on circles and parallel-line systems suggests the curriculum should teach the hand method (ratios, completing the square) as primary for those, with Desmos as verification.

### Gaps
- No official Desmos Help Center regression article content was retrieved; the page fetch was blocked. Exact official wording on subscripts and regression restrictions is unverified.
- No sourced worked examples were found for sum/product notation, percent syntax, absolute-value solution counting, or vertex clicking specifically for the SAT.
- No sourced discussion of implicit-multiplication quirks was found.

## 2. Syntax quirks and common errors (consolidated)

### Takeaway
The recurring errors are: not zooming out, wrong angle mode, missing parentheses/signs, confusing {} (restriction) with [] (list), omitting subscripts or the x₁ list in regression, retyping rounded decimals, and accepting a decimal when an exact value is needed. The College Board version disables some features and forces Log Mode for some regressions.

### Cited Findings
- College Board version: images, folders, and notes are disabled. Log Mode is auto-checked for applicable exponential/log/power regressions. Bluebook lets students toggle between scientific and graphing calculators. — [Official CB Desmos PDF](https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator.pdf)
- A practice version is at desmos.com/testing/collegeboard/graphing. — [The Test Advantage](https://thetestadvantage.com/blog/how-to-use-desmos-on-the-sat-complete-may-2026-guide)
- Conflict: one guide claims the test version is not stripped down, which the official PDF contradicts. — [The Test Advantage: Is Desmos allowed](https://thetestadvantage.com/blog/is-desmos-allowed-on-the-sat) vs [Official PDF](https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator.pdf)
- Desmos is available across the entire Math section (both modules). — [Achievable](https://achievable.me/exams/act/resources/how-to-use-the-desmos-sat-calculator/)
- The regression setup list is required (fails silently). Don't retype rounded decimals. — [Resolve Prep](https://resolveprep.com/blog/desmos-regression-sat-guide)
- Curly braces are a restriction, not a list. — [Learner Labs](https://learnerlabs.app/sat-prep/desmos/stats-from-list)
- Angle mode, zoom, parentheses, and approximate-vs-exact. — see T1, T11, T12 sources above.

### Inferences
- An AI tutor should run a pre-flight checklist before trusting a Desmos answer: angle mode → zoom-to-fit → parentheses → [] vs {} → is an exact form required?

### Gaps
- No source documented Desmos's exact parsing rules for implicit multiplication or auto-subscripting.

## 3. Where Desmos does NOT help or is slower

### Takeaway
Prep sources agree that Desmos is weak or slower on geometry and trig reasoning, word-problem setup, definitions and structure questions, and some of the hardest Module 2 items. The common heuristic: if it can be done by hand in under ~15 seconds, skip Desmos.

### Cited Findings
- Heuristic: if you can solve it without a calculator in under 15 seconds, skip Desmos. Use Desmos when graphing or numerics beat the algebra. — [Miyagi Labs](https://miyagilabs.ai/blog/desmos-sat-tips-guide); [Sherpalai](https://sherpalai.com/sat-r-desmos-calculator-tips/sat-math-desmos-cheat-sheet)
- Consider algebraic structure, geometry, special triangles, and definitions before graphing. Switch to Desmos only if the hand route stays unclear after a short attempt. — [Aniko: When not to use Desmos](https://www.aniko.ai/free-resources/sat/courses/desmos/when-not-to-use-desmos)
- Problems to avoid in Desmos: parallel-line systems, circle center/radius, and the last 4 problems of Module 2 unless Desmos obviously applies. — [Say Hello College](https://sayhellocollege.com/blog/guide-to-using-the-desmos-sat-calculator/)
- "There are now plenty of questions where Desmos doesn't just fail to help—it actively slows you down." Messy decimals can mislead. One blog claims College Board made questions "Desmos-proof" using unknown constants (prep-company opinion, not official). — [Strategic Test Prep: Is Desmos dead in 2026?](https://www.strategictestprep.com/post/is-desmos-dead-on-the-sat-in-2026)
- The hardest items lean on abstraction and multi-step reasoning, mostly in Advanced Math, and are rarely computation-heavy. — [AlphaTest AI hardest questions 2026](https://www.alphatestai.com/blog/148-what-are-the-hardest-questions-on-the-digital-sat-math-section-2026-guide)
- Algebra and Advanced Math are each about 35% of the test and are where Desmos does the most work. — [PrepDrills cheat sheet 2026 (via search summary)](https://prepdrills.com/blog/desmos-sat-cheat-sheet-2026/)
- Free response: one source recommends by-hand for exact answers. MCQ: Desmos helps with elimination. — [Sherpalai](https://sherpalai.com/sat-r-desmos-calculator-tips/sat-math-desmos-cheat-sheet)

### Inferences
- By-hand-first units: word-problem translation, geometry/trig (area, volume, similar triangles, special right triangles, unit circle), Problem Solving & Data Analysis interpretation (reading graphs/tables, study design, margin of error), and abstract "which must be true" structure questions. The "Desmos-proof" claim is unverified, but it is consistent with T3/T6 still working on unknown-constant questions, so the claim may be overstated.

### Gaps
- No rigorous per-question-type timing study (Desmos vs. hand) was found.

## 4. Existing Desmos-for-SAT resources

### Takeaway
The market is crowded with free blog cheat sheets and YouTube content. Structured courses are mostly free (LearnDesmos, Aniko, CheetahPrep free tier) or cheap (1600.io membership, SATDesmos subscription, Temple Edge $10 PDF). No source offered an adaptive, technique-tagged, AI-driven drill system that maps each question type to a Desmos-or-hand decision, though Aniko and Miyagi Labs are AI-branded.

### Cited Findings
**Courses / sites**
- LearnDesmos: free, independent, 27 chapters in 3 sections, with an 8-chapter regression unit. The FAQ says there is no paid tier. — [LearnDesmos curriculum](https://learndesmos.com/curriculum); [FAQ](https://learndesmos.com/faq)
- SATDesmos.com: $25/month, $60/3 months, $192/year. — [SATDesmos](https://www.satdesmos.com/pages/home)
- 1600.io "Mastering Desmos for the Digital SAT": part of a membership, with the page showing a $6.99/week tier. 1600.io also sells the 2-volume SAT Math "Orange Book." — [1600.io course](https://1600.io/p/mastering-desmos-for-the-digital-sat); [AbeBooks listing](https://www.abebooks.com/9798703045787/1600.io-SAT-Math-Orange-Book/plp)
- CheetahPrep Desmos course: free to start, with a live calculator in every lesson that maps each question type to a Desmos move. Paid pricing was not found. — [CheetahPrep](https://www.cheetahprep.com/desmos)
- Aniko.ai: free guide with 30+ lessons and practice, plus a 4-stage learning roadmap. — [Aniko course](https://www.aniko.ai/free-resources/sat/courses/desmos); [roadmap](https://www.aniko.ai/blog/how-to-learn-desmos-for-the-sat)
- Test Prep Wizards (Teachable): course lectures on Desmos. Pricing not found. — [Teachable](https://test-prep-wizards.teachable.com/courses/2130816/lectures/64153379)
- Upwork freelance course: $30, 9 hours, Desmos on the toughest Educator Question Bank items. Seller is unverified. — [Upwork](https://www.upwork.com/services/product/writing-translation-a-course-to-master-digital-sat-math-in-9-hours-1847982453367265900)
- SAT Regression Trainer: a single-skill drill site. — [regressiontrainer.org](https://regressiontrainer.org/)
- Schoolhouse.world: free peer-tutoring series "SAT Advanced Math + Desmos Tips" from an 800 scorer. — [Schoolhouse](https://schoolhouse.world/series/74215)

**PDFs / books / cheat sheets**
- Temple Edge Learning, "Desmos and the PSAT/SAT": $10, 224 pages, no refunds. A companion to the Dr. Test Prep YouTube channel, aimed at students scoring under 690 in Math. — [Gumroad](https://templeedgelearning.gumroad.com/l/Desmos-and-the-PSAT-SAT)
- BWS Education Consulting, "Ten Tips for Desmos on the Digital SAT": free PDF (2024). — [PDF](https://bwseducationconsulting.com/wp-content/uploads/2024/07/Desmos_SAT_Tips_and_Tricks.pdf)
- Official College Board Desmos reference PDF. — [PDF](https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator.pdf)
- Free blog cheat sheets: [Acely](https://acely.com/sat-prep/desmos-cheat-sheet), [Pursu](https://pursu.io/blog/how-to-use-desmos-on-the-sat), [OnePrep 12 moves](https://www.oneprep.co/blog/sat-math-tips-desmos-2026-12-calculator-moves), [PrepMaven 7 skills](https://prepmaven.com/blog/test-prep/desmos-on-the-digital-sat/), [Effortless Math 12 moves](https://www.effortlessmath.com/blog/desmos-sat-math-cheat-sheet-12-moves/), [SAT Monster](https://satmonster.com/desmos-guide), [SATmaxxing](https://www.satmaxxing.com/desmos), [MathChops 5-minute intro](https://mathchops.substack.com/p/a-five-minute-dsat-desmos-intro), [Sigma Prep 8 tricks](https://www.sigmaprep.io/blog/how-to-use-desmos-on-sat), [Progress Learning](https://progresslearning.com/news-blog/desmos-tips-for-the-sat/), [Say Hello College](https://sayhellocollege.com/blog/guide-to-using-the-desmos-sat-calculator/), [Edison OS](https://www.edisonos.com/digital-sat/desmos-guide)

**YouTube**
- Ammasat's ranked watch order: (1) LearnSATMath, the clearest intro, covering tables, regression, and inequalities, and noting when Desmos isn't the right tool; (2) Tutorllini Test Prep, short one-skill lessons; (3) James Lu SAT, with a strong table-regression segment; (4) Scalar Learning, broad and fast. — [Ammasat](https://www.ammasat.com/blog/sat-desmos-youtube-guide)
- Reddit r/Sat (anecdotal, a single 2025 user): recommends "Adiar's Desmos Guide," JW Math Tutoring's advanced playlist, and Tutorlini's DSAT Math Desmos playlist as in-depth. It calls LearnSATMath and Rishab's guides decent but not in-depth, and says one popular 7-minute video covers "only about 20%" of Desmos's capability. — [r/Sat mirror](https://nyc1.lr.ggtyler.dev/r/Sat/comments/1if34ny/best_desmos_guide_tailored_to_the_sat)
- Full-course videos: "Every SAT Desmos Trick in One Video (FULL COURSE)" — [YouTube](https://www.youtube.com/watch?v=ihELOUeXIlQ); "The Ultimate Guide to DESMOS on the SAT in 2026" — [YouTube](https://www.youtube.com/watch?v=1e_8zv6Q3r8); "Digital SAT Math Desmos Course" playlist — [YouTube](https://www.youtube.com/playlist?list=PLf3ypEs9Kobgascv5bwpOadB0UiVI5IQS)

### Inferences
- Coverage pattern: almost every free resource covers intersections, sliders, basic regression, inequalities, circles, and stats. Fewer cover the tilde-equivalence trick in depth (Resolve Prep, LearnDesmos, Pursu do). Almost none provide a systematic "Desmos vs. by-hand decision" taxonomy per College Board skill/domain with timing data, or adaptive practice. That is the likely gap for an AI-tutor product.
- Pricing anchors: free is the norm. Paid offerings run about $10 (PDF) to $25/month (subscription), and 1600.io is about $6.99/week.

### Gaps
- Pricing and Desmos-specific content for Princeton Review, PrepScholar, and Khan Academy were not found in searches. Khan Academy's Desmos content (if any) is unverified.
- Channel names/URLs for JW Math Tutoring, Adiar, Rishab, and Dr. Test Prep could not be verified directly; subscriber counts are unknown.
- Quality judgments are from Ammasat (itself a prep company) and one Reddit user; there are no independent reviews.

## 5. Estimates of % of SAT math solvable with Desmos and time saved

### Takeaway
Estimates range from about one-third to about one-half. One outlier claims 90%. None are official, methodologies differ, and no credible time-saved figures were found.

### Cited Findings
- About 1/3 of questions, from a review of the digital practice tests. — [Method Learning](https://www.methodlearning.com/blog/the-power-of-desmos-on-the-digital-sat-math-section)
- About 40%, from colleagues' estimate in an article about 3 years old. — [Chariot Learning](https://www.chariotlearning.com/the-power-of-desmos-on-the-sat/)
- About half (≈22 of 44), varying by form. — [Miyagi Labs, Sept 2026](https://miyagilabs.ai/blog/desmos-sat-tips-guide); [PrepMaven](https://prepmaven.com/blog/test-prep/desmos-on-the-digital-sat/)
- About 90% (outlier, marketing-style claim). — [SATmaxxing](https://www.satmaxxing.com/desmos)
- Counterpoint: there is a trend toward questions where Desmos slows students down. — [Strategic Test Prep](https://www.strategictestprep.com/post/is-desmos-dead-on-the-sat-in-2026)

### Inferences
- A defensible course claim: "Desmos can solve or verify roughly a third to half of Digital SAT math questions." Present this as a range, citing the disagreement.

### Gaps
- No source quantified time saved per question or score impact with data. No College Board statement on Desmos-solvable share exists in the results.

## 6. Extra hacks in the answer explanations (H1–H14, researched October 2026)

### Takeaway
Fourteen smaller Desmos moves now sit in `backend/app/content/bank/hacks.json`. They go beyond the main route (T1–T13). Each explanation shows up to two that fit the question, under "More Desmos hacks", typed out with that question's own numbers where possible. 311 of the 1,000 bank items get at least one, including 31 of the hand-only items. All 14 are `"verified": false` until someone tries them in desmos.com/testing/collegeboard/graphing.

### Cited Findings
| Hack | What the student types | Source |
|---|---|---|
| H1 Type the equation as written | `6x^2-x-2=0`: Desmos draws a vertical line at each real solution | [Edison OS 2026 guide](https://www.edisonos.com/digital-sat/desmos-guide); [Math Chops comments](https://mathchops.substack.com/p/a-five-minute-dsat-desmos-intro/comments) |
| H2 Test every choice in a table | `f(x)=` left − right, choices under `x_1`, header `f(x_1)`, find the 0 | [OnePrep 2026](https://www.oneprep.com/blog/sat-math-tips-desmos-2026-12-calculator-moves) |
| H3 Shade the inequality as written | `3(2-x)>12`; dashed edge = strict | [Desmos help: Inequalities and Restrictions](https://help.desmos.com/hc/en-us/articles/4407885334285-Inequalities-and-Restrictions) |
| H4 Restrict with braces | `y=x^2{0<=x<=5}` | [Desmos help](https://help.desmos.com/hc/en-us/articles/4407885334285-Inequalities-and-Restrictions); [Learner Labs](https://learnerlabs.app/sat-prep/desmos/stats-from-list) |
| H5 Built-in distance and midpoint | `distance((1,2),(4,6))`, `midpoint(...)` | [Achievable](https://achievable.me/exams/sat/resources/how-to-use-the-desmos-sat-calculator/); [1600.io](https://1600.io/courses/1698988/lectures/38541808) |
| H6 Line through points, by regression | table, then `y_1~mx_1+b` | [Acely guide library](https://acely.com/desmos-guide-library/linear-functions-table-points-to-find-function); [r/Sat Desmos thread](https://reddit.birdcat.cafe/r/Sat/comments/1c8at7a/official_desmos_thread/l1uz7uo/?context=3) |
| H7 Graph without solving for y | `4x-6y=5`, `x^2+y^2-10x+6y+18=0` as written | [Edison OS 2026 guide](https://www.edisonos.com/digital-sat/desmos-guide) |
| H8 Formula with x as the unknown | `pi x^2=49pi` | [Edison OS 2026 guide](https://www.edisonos.com/digital-sat/desmos-guide) (rename-to-x idea applied to geometry) |
| H9 Sum or product of the solutions | click each intercept; check with −b/a and c/a | [OnePrep 2026](https://www.oneprep.com/blog/sat-math-tips-desmos-2026-12-calculator-moves) |
| H10 Statistics functions | `mean([...])`, `median`, `stdev`, `stdevp`; `mean([5,9,x])=11` | [Math Chops comments](https://mathchops.substack.com/p/a-five-minute-dsat-desmos-intro/comments); [Yonkers Desmos stats sheet](https://www.yonkerspublicschools.org/cms/lib/NY01814060/Centricity/Domain/1790/Desmos%20Stats%20Functions.pdf) |
| H11 Percents with % | `35% of 80`; `x% of 160=40` | [Math Chops comments](https://mathchops.substack.com/p/a-five-minute-dsat-desmos-intro/comments) |
| H12 Rename the letter to x | solve for t, p or n by typing x | [Edison OS 2026 guide](https://www.edisonos.com/digital-sat/desmos-guide); [PrepDrills cheat sheet 2026](https://prepdrills.com/blog/desmos-sat-cheat-sheet-2026/) |
| H13 Click the curve for its key points | gray dots on vertex, intercepts, crossings | [Acely cheat sheet](https://acely.com/sat-prep/desmos-cheat-sheet); [OnePrep 2026](https://www.oneprep.com/blog/sat-math-tips-desmos-2026-12-calculator-moves) |
| H14 Decimal to fraction | the fraction button beside a computed value; name values to keep them exact | [Acely cheat sheet](https://acely.com/sat-prep/desmos-cheat-sheet); [Progress Learning](https://progresslearning.com/news-blog/desmos-tips-for-the-sat/) |

### Inferences
- `x% of 160=40` solving for x, and a vertical line's x-intercept showing as a gray dot, come from Desmos behavior I expect but couldn't open Desmos to confirm. Check them first.
- `midpoint()` isn't in Desmos's own documentation (per 1600.io), so the hack's watch-out gives the formula as a fallback.
- The 22-question mock test (`pt4-math-m1.json`) got calculator tips on seven more questions, using the same moves.

### Gaps
- The research environment again couldn't open the prep sites or desmos.com directly, so these come from search-result summaries.
- No source covered summing solutions in Desmos specifically; H9 combines clicking intercepts with Vieta's formulas.
