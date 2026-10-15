# Digital SAT Math: Format, Content, Desmos, and Official Resources (as of October 2026)

**Method note:** Direct page fetches were blocked in this research session. The egress proxy refused satsuite.collegeboard.org, desmos.com, and oneprep.co. All findings come from web-search result summaries of the cited pages. Official College Board URLs are cited where search surfaced them, but their exact wording was not read directly. Before publishing, a course designer should open the College Board pages in a browser and confirm the details. Facts that come only from background knowledge are kept out of the cited findings and marked "unverified" under Inferences or Gaps.

**Outdated-info flag:** Any source that refers to "calculator vs. no-calculator" math sections, 58 math questions, 80 minutes, or the 0.5-point "grid-in" bubble sheet describes the paper SAT used through 2023 in the US and is out of date. The digital SAT has one Math section, and a calculator is allowed on every question.

## 1. Section structure, adaptivity, scoring, and how many misses still allow 800

### Takeaway
- **Format:** The Math section has 44 questions in 70 minutes, split into two 35-minute modules of 22 questions each. In each module, 20 questions are scored and 2 are unscored pretest questions.
- **Adaptivity:** How a student does in Module 1 decides whether Module 2 is the easier or the harder version. Only the harder Module 2 can lead to 800.
- **Misses at 800:** Third-party estimates say 800 typically allows 0–2 misses on the harder path, depending on the form. College Board publishes no conversion table for the adaptive test.

### Cited Findings
- The Math section has 44 questions in 70 minutes: two separately timed 35-minute modules of 22 questions each. Each module has 20 operational (scored) questions and 2 unscored pretest questions. That works out to about 1.59 minutes per question. — [College Board: How the SAT Is Structured](https://satsuite.collegeboard.org/sat/whats-on-the-test/structure); [Digital SAT Test Spec Overview](https://satsuite.collegeboard.org/media/pdf/digital-sat-test-spec-overview.pdf); [College Board Blog: How Long Does the SAT Take](https://blog.collegeboard.org/how-long-does-the-sat-take)
- The test uses a multistage adaptive design. Each section has two stages, and each stage is one module holding half of the section's items. Students are sent to a lower- or higher-difficulty second module based on how they did on the first module. — [Assessment Framework for the Digital SAT Suite](https://satsuite.collegeboard.org/media/pdf/assessment-framework-for-digital-sat-suite.pdf)
- Pretest items are embedded among the operational items, and students cannot tell them apart. — [Assessment Framework](https://satsuite.collegeboard.org/media/pdf/assessment-framework-for-digital-sat-suite.pdf); [Digital SAT Suite Technical Manual](https://research.collegeboard.org/media/pdf/Digital%20SAT%20Suite%20of%20Assessments%20Technical%20Manual-FINAL.pdf)
- Scores are produced with an item response theory (IRT) model, not a simple raw-score count. Third-party guides say a 3-parameter model is used, with a difficulty, discrimination, and guessing parameter for each item. — [Assessment Framework](https://satsuite.collegeboard.org/media/pdf/assessment-framework-for-digital-sat-suite.pdf); [Edison OS scoring algorithm guide](https://www.edisonos.com/digital-sat/scoring-algorithm). The 3PL detail is third-party only.
- The easier Module 2 limits the score a student can reach, but sources disagree on the cap:
  - Typically about 600–650 — [PrepScholar](https://blog.prepscholar.com/how-many-can-you-miss-for-a-perfect-score-on-the-sat)
  - 560–600 — reported by another guide in the search results
  - About 620–630 — [Lumist](https://www.lumist.ai/blog/digital-sat-scoring-adaptive-testing-explained); [IvyStrides](https://www.ivystrides.com/blog/how-the-digital-sat-is-scored/)
  - None of these caps is confirmed by College Board.
- Third-party estimates of how many misses still allow 800:
  - Usually 0–2 misses on the harder Module 2, varying by form — [PrepScholar](https://blog.prepscholar.com/how-many-can-you-miss-for-a-perfect-score-on-the-sat)
  - Normally 0–1 misses; the guide advises planning for zero — [Sigma Prep](https://www.sigmaprep.io/sat-math-how-many-can-you-miss)
  - 0 misses ≈ 800, 1 miss ≈ 790, 2 misses ≈ 780, though on harder forms 1–2 misses may still give 800; up to 4 misses ≈ 750 and up to 9 misses ≈ 700 on the hard path — [satcalculator.co](https://satcalculator.co/how-many-questions-can-you-miss-on-the-sat); [Sigma Prep score calculator](https://www.sigmaprep.io/sat-math-score-calculator)
- College Board does not publish a raw-to-scaled conversion table for the adaptive test, so all "curve" figures are third-party estimates. — [PrepScholar](https://blog.prepscholar.com/how-many-can-you-miss-for-a-perfect-score-on-the-sat); [Caddell Prep](https://caddellprep.com/sat/scores/800-math/)

### Inferences
- Because 2 of the 22 questions in each module are unscored and students cannot identify them, a "miss" may cost nothing if it lands on a pretest item. This is one reason anecdotal reports of "missed 2, still got 800" vary. Under IRT, missing a hard item costs less than missing an easy one, so careless errors on easy questions are the biggest risk to 800.
- Syllabus implications:
  - Treat getting every question right as the goal, with at most one miss allowed.
  - Train accuracy on easy and medium questions as hard as hard-question content. Module 1 errors also risk routing a student to the easier Module 2, which caps the score.
  - Pacing practice should target about 1.5 minutes per question, leaving buffer time for checking with Desmos.
- Score scale: each section is 200–800 and the total is 400–1600. This is from background knowledge and was not re-sourced in this session.

### Gaps
- No official or College Board-endorsed raw-to-scaled table exists. Reddit r/Sat anecdotal curve data could not be retrieved in this session.
- The exact IRT model and equating details in the Technical Manual could not be read directly because the fetch was blocked.

## 2. Content domains: weighting, question counts, and official skill taxonomy

### Takeaway
- **Domains:** There are four domains: Algebra (~35%), Advanced Math (~35%), Problem-Solving & Data Analysis (~15%), and Geometry & Trigonometry (~15%).
- **Skills:** The Educator Question Bank tags each item with one of about 19 skills under these domains.
- **Mixing:** Every module includes questions from all four domains.

### Cited Findings
- Domain weights on the College Board's Math specifications page: Algebra ≈35%, Advanced Math ≈35%, Problem-Solving & Data Analysis ≈15%, Geometry & Trigonometry ≈15%. An older or other-test version of the figures (≈42.5/20/25/12.5) also appears in the search results. — [College Board Math Specifications](https://satsuite.collegeboard.org/k12-educators/about/alignment/math)
- Algebra has 13–15 questions per test (this figure is from the PSAT 10 guide). Questions from all 4 domains appear in each module. — [PSAT 10 Student Guide](https://satsuite.collegeboard.org/media/pdf/official-student-guide-psat-10.pdf)
- Algebra covers linear equations in one and two variables, linear functions, systems, and inequalities. Advanced Math covers equivalent expressions, nonlinear equations, and nonlinear functions such as quadratics and exponentials. — [PrepMaven](https://prepmaven.com/blog/test-prep/sat-math/)
- Official Question Bank skill tags seen on exported items include:
  - "Linear equations in one variable"
  - "Nonlinear functions"
  - "Equivalent expressions"
  - "Nonlinear equations in one variable and systems of equations in two variables"
  - Sources: [CliffsNotes-hosted QB export](https://www.cliffsnotes.com/study-notes/23753554); [Studocu QB export](https://www.studocu.com/en-us/document/alliance-academy-for-innovation/advanced-math/sat-suite-question-bank-advanced-math-hard-no-answers/107665411)
- The Problem-Solving & Data Analysis skills on College Board's page include:
  - Ratios, rates, proportional relationships, and units
  - Percentages
  - One-variable data
  - Two-variable data
  - Probability and conditional probability
  - Inference from sample statistics and margin of error
  - Evaluating statistical claims: observational studies and experiments
  - Source: [College Board PSDA page](https://satsuite.collegeboard.org/sat/whats-on-the-test/math/types/problem-solving)
- Margin-of-error items test interpretation, such as the inverse relationship between sample size and margin of error, not calculation. — [OnePrep](https://www.oneprep.com/blog/relationship-sample-size-margin-error-sat)
- A third-party bank (Cooksat) that organizes official items by skill lists 112 questions under "linear equations in one variable" and 259 under "nonlinear functions." — [Cooksat](https://cooksat.com/sat-training-bank)

### Inferences
- **Full skill list (unverified this session).** Background knowledge of the College Board Question Bank filters gives the complete taxonomy below. It is consistent with the partial lists cited above, but the full list was not fetched directly, so verify it in the Question Bank before use.
  - **Algebra (13–15 questions)**
    - Linear equations in one variable
    - Linear functions
    - Linear equations in two variables
    - Systems of two linear equations in two variables
    - Linear inequalities in one or two variables
  - **Advanced Math (13–15 questions)**
    - Nonlinear functions
    - Nonlinear equations in one variable and systems of equations in two variables
    - Equivalent expressions
  - **Problem-Solving & Data Analysis (5–7 questions)**
    - Ratios, rates, proportional relationships, and units
    - Percentages
    - One-variable data: distributions and measures of center and spread
    - Two-variable data: models and scatterplots
    - Probability and conditional probability
    - Inference from sample statistics and margin of error
    - Evaluating statistical claims: observational studies and experiments
  - **Geometry & Trigonometry (5–7 questions)**
    - Area and volume
    - Lines, angles, and triangles
    - Right triangles and trigonometry
    - Circles
- The question counts are out of 40 scored questions. 35% of 40 is 14, which matches the cited Algebra count of 13–15.
- The ≈42.5/20/25/12.5 weighting is most likely the PSAT 8/9 distribution, which puts more weight on Algebra. Do not use it for SAT planning.
- Syllabus implication: Algebra and Advanced Math together make up about 70% of scored items (about 26–30 questions). They should take up most of the course time. Still, a single miss in the small PSDA or Geometry domains can cost the 800.

### Gaps
- The official Question Bank skill filter list and per-skill item counts could not be fetched directly.
- No official per-skill question count per test exists. College Board gives counts by domain only.

## 3. Question types: multiple choice vs. student-produced response (SPR) entry rules

### Takeaway
- **Question types:** Most questions are 4-option multiple choice, and the rest are student-produced responses (SPR), where the student types the answer.
- **SPR length limits:** Positive answers allow up to 5 characters. Negative answers allow up to 6 characters, with the minus sign counted.
- **SPR formats:** Fractions and decimals are both accepted, but a decimal must not be rounded more coarsely than the space allows.

### Cited Findings
- The section is mostly multiple choice, with some SPR questions where students enter their own answer. — [College Board Math Specifications](https://satsuite.collegeboard.org/k12-educators/about/alignment/math)
- Official Bluebook SPR directions, which match the Spring 2026 paper directions:
  - Up to 5 characters for a positive answer and 6 for a negative answer, including the minus sign.
  - If a fraction is too long, enter its decimal equivalent.
  - If a decimal is too long, truncate it or round at the fourth digit.
  - Enter mixed numbers as an improper fraction or a decimal.
  - Leave out symbols such as %, commas, and $.
  - Sources: [Fall 2026 SAT School Day Bluebook Test Directions](https://satsuite.collegeboard.org/media/pdf/english-sat-test-directions-bb.pdf); [Spring 2026 Paper Test Directions](https://satsuite.collegeboard.org/media/pdf/english-sat-test-directions.pdf)
- Rounding too coarsely earns no credit. For example, entering 0.67 for 2/3 is marked wrong. — [Target Test Prep](https://sat.blog.targettestprep.com/fractions-to-decimals/)
- For 8/9, the accepted entries are 8/9, .8888, .8889, 0.888, and 0.889. The entry .88 is rejected. This is from an unofficial reproduction of a practice-test answer table. — [Scribd practice test answer table](https://www.scribd.com/document/870706292/Test-3-Math)
- Further entry-rule tips are in [OnePrep grid-in rules](https://www.oneprep.com/blog/sat-grid-in-student-produced-response-questions) and [Satified](https://satified.org/sat-math/student-produced-responses/).

### Inferences
- Some SPR questions have more than one correct answer, and the student enters just one. This is background knowledge, standard in the official directions, but the wording was not fetched.
- The MC/SPR split is about 75%/25% (roughly 11 SPR questions out of 44). This is background knowledge and is not cited here.
- Desmos helps with SPR because typing an expression shows the exact decimal. Students still need the 5- and 6-character rules drilled so they don't lose correct work to formatting.

### Gaps
- An official statement of the MC/SPR percentage was not retrieved this session.

## 4. The embedded Desmos calculator in Bluebook, the reference sheet, and personal calculators

### Takeaway
- **Calculator:** Bluebook includes a College Board-configured Desmos graphing calculator and a Desmos scientific calculator on every Math question. Its main features work: tables, regression with "~", sliders, lists, and statistics functions. A few features are disabled.
- **Own calculator:** Students may also bring an approved handheld calculator.
- **Reference sheet:** A formula reference sheet is built into Bluebook.
- **2026–27 change:** Students can now resize the calculator.

### Cited Findings
- Desmos says both its Graphing and Scientific calculators are available on the digital SAT in Bluebook. Content does not carry over from one to the other. — [Desmos Help: Assessment Resources & FAQ](https://help.desmos.com/hc/en-us/articles/30913914831757)
- Desmos testing configurations may differ from the free desmos.com calculator. For example, a state configuration that includes the SAT program disables images, folders, notes, and "zoom fit." — [Desmos CT state testing PDF](https://www.desmos.com/state-pdfs/CT_Desmos_Calculators.pdf). This is a state configuration and may not exactly match Bluebook.
- An older (2022) Pennsylvania PSSA configuration disabled sliders, actions, advanced trig functions, and function definitions. This is NOT a Bluebook configuration and should not be applied to the SAT. — [PA Desmos PDF](https://www.education.pa.gov:443/Documents/K-12/Assessment%20and%20Accountability/PSSA/PA%20Desmos%20Calculators.pdf)
- A third-party guide says the College Board version disables images, folders, and notes, and fits exponential, logarithmic, and power regressions in Log mode. This could not be confirmed against an official source. — [The Test Advantage](https://thetestadvantage.com/blog/sat-regression-with-desmos-may-2026-data-tables-to-equations); [The Test Advantage: College Board version guide](https://thetestadvantage.com/blog/how-to-use-desmos-on-the-sat-complete-may-2026-guide)
- Features prep guides report as working in Bluebook:
  - Tables, with regression using `y1 ~ m x1 + b`
  - Sliders, created automatically for undefined parameters, which can be used to solve for unknown constants
  - Lists
  - The statistics functions in the Functions menu: mean, median, mode, range, max, min, standard deviation, and variance
  - Sources: [EdisonOS Desmos guide](https://www.edisonos.com/digital-sat/desmos-guide); [PrepMaven Desmos skills](https://prepmaven.com/blog/test-prep/desmos-on-the-digital-sat/); [Pursu Desmos cheat sheet](https://pursu.io/blog/how-to-use-desmos-on-the-sat); [Vibrant Publishers](https://www.vibrantpublishers.com/blogs/blogs-on-act-sat/how-to-use-the-desmos-calculator-on-the-digital-sat)
- SuperTutorTV shows a button next to a table that runs a linear regression in one click. This comes from a single older (~2024) video, and its availability in the current Bluebook build is unverified. — [SuperTutorTV](https://supertutortv.com/videos/mind-blowing-new-desmos-feature-to-crush-the-sat/)
- The calculator is available on every Math question, requires no account, and students can switch between graphing and scientific modes. — [EdisonOS](https://www.edisonos.com/digital-sat/desmos-guide); [The Test Advantage: Is Desmos allowed](https://thetestadvantage.com/blog/is-desmos-allowed-on-the-sat)
- The official Bluebook Testing Tools page lists Desmos as available on the SAT. It also says a reference sheet with commonly used formulas appears on all tests with math questions. — [Bluebook Testing Tools](https://bluebook.collegeboard.org/students/tools)
- Students may bring their own approved handheld calculator in addition to, or instead of, Desmos. Calculators with CAS features are reported to be banned. — [LarryLearns calculator policy](https://www.larrylearns.com/blog/sat-calculator-policy-allowed-not-allowed); [Galvanize Test Prep](https://galvanizetestprep.com/blogs/desmos-sat-calculator-how-to-use-it/). Phones, smartwatches, tablets, and any communication-capable device are prohibited as calculators. — [OnePrep 2026 calculator policy](https://www.oneprep.co/blog/sat-calculator-policy-2026-bluebook-desmos-prohibited-features)
- 2026–27 change: students can now resize the embedded Desmos calculator in the Math section. — [College Board: Changes for 2026-27 Testing](https://satsuite.collegeboard.org/k12-educators/educator-experience/in-school/start/changes); [College Board testing-staff changes](https://satsuite.collegeboard.org/sat/testing-staff/changes)

### Inferences
- Course practice should use the College Board version of Desmos, which prep sites link to as a direct "College Board version," rather than the regular desmos.com calculator. That way students do not rely on disabled features such as notes and folders.
- The reference sheet covers basic area, volume, triangle, and circle facts. It does not include things like the vertex form, the discriminant, or circle equations, so students still need to memorize those. Its exact contents could not be fetched; The Test Advantage lists "54 formulas to memorize" ([source](https://thetestadvantage.com/blog/sat-math-formulas)).
- The CAS ban comes from third-party sources. College Board's official approved-calculator list was not retrieved directly.

### Gaps
- No official College Board or Desmos document listing the exact Bluebook feature set was retrieved. Confirm directly on desmos.com/testing or in Bluebook's practice mode whether these work: the one-click regression button, `~` regression on non-linear models, sliders, piecewise functions, and lists.
- The official calculator-policy page (satsuite.collegeboard.org/digital/what-students-can-expect/calculator-policy) was blocked, so the approved-calculator list could not be checked.

## 5. Official free practice resources and content-use rights

### Takeaway
- **Bluebook practice tests:** Bluebook has 8 full-length adaptive SAT practice tests, numbered Tests 4–11. Test 11, released early 2026, is the newest.
- **Question Bank:** The free Educator Question Bank holds about 1,900–2,000 SAT-suite Math items, each tagged by domain, skill, and difficulty.
- **Khan Academy:** Official SAT Prep with Khan Academy is free.
- **Usage rights:** All of this content is College Board copyright. Terms for reusing it commercially were not found.

### Cited Findings
- Bluebook practice tests:
  - Bluebook holds 8 full-length digital SAT practice tests, numbered 4–11. Tests 1–3 have been retired, and no Test 12 had been announced as of early October 2026. — [The Test Advantage: How many practice tests](https://thetestadvantage.com/blog/how-many-practice-tests-does-bluebook-have); [LarryLearns: hardest tests ranked](https://www.larrylearns.com/blog/hardest-sat-practice-test)
  - One 2026 guide says there are 10 tests (1–10). It appears to be out of date. — [mycollegebook.org](https://mycollegebook.org/bluebook-sat-practice-tests)
  - Test 11 was released in early 2026 and is described as closest to recent real SATs. — [IvyTutors Network](https://ivytutorsnetwork.com/blog/march-2026-sat-changes-bluebook-test-11); [LearnQ](https://blogs.learnq.ai/are-bluebook-practice-tests-accurate/)
  - New full-length Bluebook practice tests for the PSAT/NMSQT, PSAT 10, and PSAT 8/9 were slated for late summer 2026. No new SAT test was listed. — [College Board: Changes for 2026-27](https://satsuite.collegeboard.org/k12-educators/educator-experience/in-school/start/changes)
- Educator Question Bank size:
  - A 2023 state document said the bank had over 3,500 questions across the SAT, PSAT/NMSQT, PSAT 10, and PSAT 8/9. This figure is outdated. — [RIDE: Understanding SAT Suite Results (May 2023)](https://ride.ri.gov/media/26061/download)
  - Sigma Prep counted 1,876 official Math questions with rationales as of September 2026. — [Sigma Prep](https://www.sigmaprep.io/sat-question-bank)
  - Aniko counts about 2,000 Math questions. — [Aniko](https://www.aniko.ai/free-resources/sat/question-bank)
- In August 2026, College Board added 196 new math questions to the bank without a public announcement. This is Sigma Prep's own comparison against a March snapshot. — [Sigma Prep Aug 2026 update](https://www.sigmaprep.io/blog/sat-question-bank-august-2026-new-questions); see also [PanoPrep](https://www.panoprep.com/blog/sat-question-bank-update-2026-new-questions-difficulty-key-changes/)
- The bank is free with no login. Users can filter by assessment, section, domain, skill, and difficulty (Easy/Medium/Hard), and can export questions and rationales to PDF. — [The Test Advantage: What is the SAT Question Bank](https://thetestadvantage.com/blog/what-is-the-sat-question-bank); [RIDE](https://ride.ri.gov/media/26061/download). Note: RIDE's mention of a "calculator/no-calculator" tag is OUTDATED, from the paper era.
- College Board's free official prep is delivered through Khan Academy. — [The Test Advantage](https://thetestadvantage.com/blog/what-is-the-sat-question-bank)
- Some third-party sites publish "question banks" reconstructed from specific live 2026 test administrations, such as the August, September, and October 2026 forms. — [The Test Advantage October 2026](https://thetestadvantage.com/test/dsat-math-october-2026-question-bank). **Flag:** content recalled from live tests probably breaks College Board test-security and copyright terms. A legitimate course should not use or link to it.

### Inferences
- An 800-target course has 8 official full-length tests to work with. A sensible plan holds back 2–3 of them, including Test 11, for final diagnostics.
- Each Bluebook test contains both Module 2 versions, but a student only sees one per sitting. Retaking a test after a deliberately weak Module 1 can expose the easier Module 2. For an 800 target, though, the harder Module 2 is what matters.
- For hard-item drilling, the main official source is the Question Bank filtered to Hard. Its exact count of Hard math items is unknown.
- Copyright: the Question Bank, Bluebook tests, and Khan Academy official SAT content are College Board (or Khan) intellectual property. Linking to them and using them for students' own practice is clearly fine. Reproducing items in a paid course likely needs permission. This is an inference; the terms were not retrieved.

### Gaps
- No official count of Question Bank math items by difficulty. The filter counts in the live bank would answer this.
- Terms of use and copyright statements for the Question Bank, Bluebook tests, and Khan Academy content were not retrieved. Check the College Board terms of use and the Question Bank's own terms page.
- No 2026 information was found on what Khan Academy's official SAT course currently contains, such as unit structure or number of practice items.

## 6. What share of SAT math questions Desmos can solve faster or outright

### Takeaway
- **Estimates:** Prep-company estimates range from about one-third to 90%. The most defensible figure, and the only one based on counting questions, is that about a third to a half of questions can be solved outright or much faster with Desmos.
- **Source quality:** None of these figures comes from College Board.

### Cited Findings
- Roughly a third of all math questions can be solved with Desmos, based on reviewing the digital practice tests. This is the only estimate based on counting questions. — [Method Learning](https://www.methodlearning.com/blog/the-power-of-desmos-on-the-digital-sat-math-section)
- About 40% of questions, including very difficult ones, "can be easily solved using Desmos." This is secondhand, attributed to "colleagues." — [Chariot Learning](https://www.chariotlearning.com/the-power-of-desmos-on-the-sat/)
- About half, citing "multiple SAT prep sources" without naming them (Sept 2026). — [Miyagi Labs](https://miyagilabs.ai/blog/desmos-sat-tips-guide)
- About 90%. This is a marketing claim and an outlier. — [SATmaxxing](https://www.satmaxxing.com/desmos)
- Cooksat provides Desmos solutions for nearly every official Question Bank math item. — [Cooksat](https://cooksat.com/sat-training-bank)

### Inferences
- The differences between estimates come mostly from definitions. "Solves entirely" (for example, graph and read an intersection, a root, or a vertex) gives about 30–50%. "Desmos helps at all" (checking arithmetic, testing answer choices, evaluating expressions) gives more.
- Question types where Desmos does well:
  - Systems of equations (intersections)
  - Quadratic roots and vertex
  - Solving for constants with sliders, regression, or tables
  - Equivalent-expression checks (graph both sides)
  - Number of solutions
  - Statistics with lists
- Conceptual PSDA questions (study design, margin-of-error interpretation) and many geometry questions benefit little from Desmos.
- An 800 course should teach Desmos as a parallel method and a way to check answers, not as a replacement for algebra.

### Gaps
- No systematic, published, question-by-question classification of official tests by "Desmos-solvable" status was found.

## 7. Changes announced for the 2026–27 SAT

### Takeaway
- **Content:** No change to Math content, length, or scoring has been announced for 2026–27.
- **Bluebook and logistics:** The changes are logistical and technical: a resizable Desmos calculator, Chromebook verified mode, Windows 11 required, a US waitlist, and new PSAT-family practice tests.

### Cited Findings
- College Board's official "Changes for 2026-27 Testing" pages list:
  - Students can resize the embedded Desmos calculator
  - Bluebook on Chromebooks requires verified mode (bluebook.org/verified-mode)
  - A US waitlist for full test dates or centers
  - On-time ordering deadlines for schools: Sept 30, 2026 (fall) and Feb 28, 2027 (spring)
  - New full-length PSAT/NMSQT, PSAT 10, and PSAT 8/9 practice tests in late summer 2026
  - Sources: [College Board: Changes for 2026-27 (educators)](https://satsuite.collegeboard.org/k12-educators/educator-experience/in-school/start/changes); [College Board: Changes for 2026-27 (testing staff)](https://satsuite.collegeboard.org/sat/testing-staff/changes)
- Bluebook requires Windows 11 for 2026–27, and Windows 10 support is being phased out in fall 2026. This comes from a third-party summary. — [satscorerelease.com](https://satscorerelease.com/digital-sat-updates/)
- Spring 2026 Bluebook updates added new practice content and device requirements. — [Freedom For All Americans summary](https://freedomforallamericans.org/sat-bluebook-device-requirements/); [Score At The Top: CB briefing notes](https://www.scoreatthetop.com/blog/digital-sat-updates-for-2026-what-the-college-board-told-a-room-full-of-test-prep-experts)
- Some third-party sites make claims such as "dynamic capacity models," "40% of seats reserved," or score-scale changes. They are unverified and some look AI-generated, so do not rely on them. — [practicetestgeeks.com](https://practicetestgeeks.com/sat/sat-news); [EdisonOS SAT trends](https://www.edisonos.com/digital-sat/sat-trends)

### Inferences
- Commentators reading Bluebook Test 11 ([IvyTutors](https://ivytutorsnetwork.com/blog/march-2026-sat-changes-bluebook-test-11)) suggest recent real tests have hard Module 2s that are harder than earlier practice tests. A course aiming at 800 should rely on Test 11 and Hard Question Bank items to calibrate difficulty.

### Gaps
- The full text of the official College Board changes pages could not be read directly because the fetch was blocked. Other Math-specific changes may be listed there.
- No official announcement of changes to Math content or scoring for 2027 was found.
