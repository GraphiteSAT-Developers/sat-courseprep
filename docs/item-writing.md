# Item-writing checklist

The single checklist for adding items to `web/content/items.ts`. Style comes
from `docs/item-style-guide.md` (the College Board Assessment Framework,
chapter 4, turned into rules; cited below as "SG §n"); process rules live
here. Every rule that can be checked by code is checked by code: an item is
eligible for the database only when **both** scripts pass.

```sh
python3 web/scripts/verify_items.py   # keys recomputed with SymPy; exit 1 on any failure
python3 web/scripts/lint_items.py     # style rules below; exit 1 on any error-level rule
cd web && npm run items:check         # runs both, in that order
cd web && npm test && npm run typecheck
```

`lint_items.py --rules` prints the rule table; `--quiet` prints counts only.
Both scripts read `items.ts` through `web/scripts/itembank.py`, so a schema
change in `web/content/types.ts` is a change to that one parser.

## 1. Originality (SG §9) — rules OR01, OR02

- [ ] Every item is written from scratch. No College Board, Khan Academy,
      Bluebook, Question Bank or framework sample item is copied, paraphrased,
      re-numbered, re-skinned with a new context, or used as a structural
      template. Matching a *skill* and the *conventions* below is the goal;
      matching a published item's setup is a defect.
- [ ] If you read a published item to learn the skill, close it before
      writing and say so in `provenance.notes`.
- [ ] Contexts are invented and generic (a store, a club, a type of wood);
      no real organizations, no names of people.
- **OR01** (error, bank-level): no two stems share a 10-word window. The
  framework's own question frames ("which of the following is the best
  interpretation of", "what is the value of", "is a constant", ...) are
  excluded from the window; anything else that repeats across two stems is
  reported.
- **OR02** (error): the stem never contains "College Board" or "Khan".

## 2. Provenance and ids (SG §9) — ID01, PR01, PR02

- [ ] `id` is a unique slug `domain-topic-detail` (`alg-no-solution-k`), never
      reused after an item is deleted. **ID01** (error).
- [ ] `provenance.author` is your name or agent id. **PR01** (error).
- [ ] `provenance.created` is an ISO date `YYYY-MM-DD`. **PR02** (error).
- [ ] `provenance.notes` records how the key was checked ("key verified with
      SymPy") and anything a reviewer should know.

## 3. Keys are verified, never assumed (SG §5) — SP01, plus verify_items.py

- [ ] Add a SymPy computation to `CHECKS` in `web/scripts/verify_items.py`
      that derives the answer from the stem's givens (not a restatement of the
      key). The verifier fails if the key disagrees, if an MC distractor is
      also correct, if an SPR key doesn't fit the entry box, or if an item has
      no check.
- [ ] SPR keys are `Rational` objects `{ num, den }` with `den > 0`, one per
      acceptable value. Several keys only when the stem says "one possible
      value".
- [ ] **SP01** (error): each key fits Bluebook's box as a reduced fraction or
      a full-width decimal: 5 characters positive, 6 negative including the
      sign. Prefer keys that fit exactly (`36/7`, `-5/3`, `7.5`). Never key a
      percent, a dollar amount, a unit, a coordinate pair or an expression; if
      the item is about a percent, ask for "the value of p" where p% is defined
      in the stem.
- [ ] For a non-terminating decimal, `desmos.read` must tell the student to
      enter the fraction (fraction toggle, T11) or a full-width decimal
      (`1.666`/`1.667` for 5/3; `0.67` is wrong). See
      `docs/spr-directions-check.md` for the grader's exact behaviour.
- [ ] `desmos.verified` stays `false`. Only the headless Desmos service sets it
      to `true`.

## 4. Domain, skill, difficulty (SG §2, §6) — SK01, SK02, DF01

- [ ] `domain` is `algebra`, `advanced-math`, `psda` or `geometry-trig`.
- [ ] **SK01** (error): `skill` is one of the 19 exact names in
      `web/content/skills.ts` (framework Table A31). **SK02** (error): the
      skill belongs to the item's domain. Absolute value is Advanced Math;
      geometric contexts inside function items stay in Algebra/Advanced Math
      (tag by the skill measured, not by the presence of a figure).
- [ ] **DF01** (error): `difficulty` is `easy`, `medium` or `hard`; `route`
      and `format` are valid.
- [ ] Difficulty, per SG §6: `easy` = one step, one representation;
      `medium` = one idea with one trap or one translation; `hard` = a
      restricted constant, a structural insight, or two ideas chained, with
      every distractor a named mistake. The bank needs a floor of easy and
      medium items in every domain so module simulations can be assembled
      (design notes §1); drills may lean hard.

## 5. Stem conventions (SG §3) — ST01–ST09

- [ ] One equation goes on its own line and the prose calls it "the given
      equation"; do not restate it in the question sentence.
- [ ] **ST01** (warn): a single-letter constant (anything other than x, y or
      a function name) is declared. **ST02** (warn): declared in a trailing
      "where k is a (positive) constant" clause, with whatever restriction
      makes the key unique. "In the equation ..., k is a constant." is
      accepted but reported so a batch can be brought to the house form.
- [ ] Functions: "The function f is defined by f(x) = ...". Values: "what is
      the value of f(2)?"; products of constants: "What is the value of ab?".
- [ ] **ST03** (error): any mention of a graph, an x- or y-intercept, a slope,
      a parabola, a line with an equation, or an intersection of equations in
      y, carries "in the xy-plane" (written `$xy$-plane`). Arcs, transversals
      and triangles do not need it.
- [ ] Context items: one or two declarative sentences set the scenario and
      define every variable with its unit, then the question. Units and
      rounding sit inside the question sentence, set off by commas: "What is
      the height, in centimeters, of the block?"; "To the nearest tenth, ...".
      **ST09** (warn) flags "what is the <quantity>" questions with no
      ", in <unit>".
- [ ] **ST05** (warn): in-context stems are at most 50 standardized words
      (characters ÷ 6, about 300 characters). An item counts as in context
      when its stem names a unit, money, time, people or a scenario noun (the
      word list is `CONTEXT_WORDS` in the linter).
- [ ] **ST04** (error): "Which of the following" only when the choices are
      objects (expressions, equations, statements, points). Numeric choices
      use "What is the value of ...?" or "How many ...?".
- [ ] **ST06** (error): the stem ends with a question mark. A parenthetical
      note such as "(1 kilometer = 1,000 meters)" or an "I. ... II. ... III."
      list may follow the question.
- [ ] **ST07** (error): third person, present tense; no "you", "we", "I" and
      no names of people.
- [ ] **ST08** (error): dollar-sign rule, see section 6.
- [ ] Angles: "45°" with the degree sign (`^\circ` in math). Quantities with
      units in words: "353 kilograms per cubic meter".
- [ ] Figures: nothing the figure shows is repeated in the stem; items that
      words describe fully get no figure; "Note: Figure not drawn to scale."
      only in that wording (SG §7). (The schema has no figure field yet; an
      item that needs one is not ready.)

## 6. Dollar signs and math markup — ST08

House decision (2026-10-15). `web/components/MathText.tsx` splits text on
`/(\$[^$]+\$)/` and renders each span with KaTeX. It has **no escape for a
literal dollar sign**: `\$` is still a `$` to the splitter, so both "costs
$5.50" in prose and `\$5.50` inside a math span break the pairing and corrupt
every later span. The framework writes prices as "$5.50" (SG §3), but until
MathText honours `\$` the bank cannot.

- Prose: write the amount with the word, "23.00 dollars", "a fee of 11
  dollars". Keep two decimals when the context is money.
- Question sentence: "What is the cost, in dollars, of ...?".
- Choices: plain numbers (`$33.50$`), never a dollar sign; the unit is fixed
  by the stem. Percent choices do carry `\%`.
- SPR keys never carry a sign, a `%` or a unit.
- **ST08** (error) rejects an odd number of `$` delimiters, any `\$`, a math
  span that contains three or more consecutive words of prose, and `$<number> `
  followed by prose (a price written with a sign).

If MathText later gains an escape (`\$` → literal), relax ST08 to allow `\$`
inside spans and move to the framework's "$5.50" form in one batch. Until
then this file and the linter are the source of truth, not SG §3's example.

Other markup facts about MathText: inline `$...$` only (no `$$` display
math); `throwOnError: false`, so a KaTeX syntax slip renders red rather than
failing a test; the TS string needs `\\` for every LaTeX backslash. The old
"keep choices free of `]`" restriction is gone: `itembank.py` parses string
arrays properly.

## 7. Multiple-choice conventions (SG §4) — CH01–CH05, PR04

- [ ] **CH01** (error): exactly four choices, `answerIndex` 0–3.
- [ ] **CH02** (error): choices are parallel in form: all numeric, all
      equations/inequalities, all expressions, or all sentences (sentence
      choices all end with a period or none do). Count-of-solutions choices
      read "Zero / Exactly one / Exactly two / Infinitely many"; comparison
      choices form a template grid; variable-valued choices go in
      alphabetical variable order.
- [ ] **CH03** (error): numeric choices are strictly ascending or strictly
      descending. Ascending is the default; descending is legitimate SAT
      style; mixed is never allowed.
- [ ] **CH04** (error): no two choices are the same value or text, in any
      form. No "none of the above".
- [ ] **CH05** (warn, bank-level): no key position holds more than 40% of MC
      items. Spread the key across a batch.
- [ ] Each distractor is a specific, plausible mistake from the house list in
      SG §4 (wrong variable, intermediate result, grouping slip, wrong
      operation, wrong percent operation, neighbouring graph value,
      true-but-irrelevant fact, discarded root or sign error). **PR04**
      (warn): `byHand` names the mistake behind every distractor; the linter
      looks for each distractor's value or text in `byHand`.

## 8. Desmos route and by-hand route — DS01, DS02, PR03

- [ ] `route` says which method the course teaches first: `desmos-primary`
      when typing the lines beats the algebra; `hand-primary` when the hand
      method takes under about 15 seconds or Desmos cannot express the step;
      `either` when both are reasonable. The framework's "strategic
      calculator use" needs a real share of `hand-primary` and `either` items
      (design notes §3, §4).
- [ ] **DS01** (error): `desmos` is present exactly when `techniques` is
      non-empty. `techniques` lists every T-id the Desmos route uses (see
      `web/content/techniques.ts`).
- [ ] **DS02** (error): `desmos.lines` and `desmos.read` are present and
      `desmos.verified` is a boolean literal (`false` until the service flips
      it). `lines` are the exact strings the student types, one per expression
      line, including the `x_1=[...]` setup for every regression. `read` says
      what to click or read, which value to take, and any mode or zoom warning
      (degrees for T12, zoom out for T1). For `hand-primary` items, say
      honestly that Desmos is slower.
- [ ] **PR03** (error): `byHand` is non-empty. Write it in the framework's
      explanation voice (SG §8): "It's given that ...", "Substituting ...
      yields ...", "Therefore, ..."; add "Alternate approach:" when a second
      method is natural; end with the distractor paragraph for MC.

## 9. Bank-level distribution (SG §1, §10) — SP02, BK01–BK04

These are warnings; they describe the bank, not a single item. The linter
prints the current numbers at the end of every run.

- [ ] **BK01**: domains within 10 points of 35 / 35 / 15 / 15 (Algebra /
      Advanced Math / PSDA / Geometry and Trigonometry).
- [ ] **BK02**: SPR within 10 points of 25% (≈3 MC : 1 SPR).
- [ ] **BK03**: in-context items within 10 points of 30%.
- [ ] **BK04**: every difficulty level and every route is represented.
- [ ] **SP02**: SPR items exist in PSDA and in Geometry and Trigonometry, not
      only in Algebra and Advanced Math.

A 40-item "form-shaped" batch is 14 / 14 / 6 / 6 by domain, about 30 MC and
10 SPR, about 12 items in context, SPR in every domain, and all four domains
present in any module-sized subset.

## 10. Batch brief template

A generation agent is asked for items per skill, so the bank converges on
the official distribution. Every brief carries these fields; the agent
echoes them back in `provenance.notes` ("batch 3, brief: ...").

```
Batch:         <name or number>
Domain:        algebra | advanced-math | psda | geometry-trig
Skill:         <one of the 19 exact names in web/content/skills.ts>
Testing points: <which bullets from skills.ts the batch should cover>
Count:         <n items>
Difficulty:    easy <a> / medium <b> / hard <c>        (a + b + c = n)
Format:        mc <m> / spr <s>                        (m + s = n; ≈3:1)
Context share: <k of n in context; ≤ 50 standardized words each>
Route mix:     desmos-primary <d> / hand-primary <h> / either <e>
Techniques:    <T-ids expected on the Desmos routes, or "none">
Key positions: <spread; no position above 40% within the batch's MC items>
Choice order:  ascending unless noted
Figures:       none | <which items need one and what it shows>
Author:        <agent id>      Created: <YYYY-MM-DD>
Avoid:         <ids or setups already in the bank for this skill>
```

What the agent must do with the brief:

1. Write each item to the schema in `web/content/types.ts`, following
   sections 1–8 above.
2. Add a `CHECKS` entry per item in `verify_items.py`.
3. Run `python3 web/scripts/verify_items.py` and
   `python3 web/scripts/lint_items.py`; fix every error; list every warning in
   the hand-over note with a one-line reason for each one left standing.
4. Run `cd web && npm test && npm run typecheck`.
5. Read each stem once more as a student would: which root, which coordinate,
   integer or real, degrees or radians. Fix the stem, not the key.

## Rule index

| Rule | Severity | Scope | Section |
|---|---|---|---|
| ID01 | error | item | 2 |
| SK01, SK02 | error | item | 4 |
| DF01 | error | item | 4 |
| CH01, CH02, CH03, CH04 | error | item | 7 |
| CH05 | warn | bank | 7 |
| SP01 | error | item | 3 |
| SP02 | warn | bank | 9 |
| ST01, ST02 | warn | item | 5 |
| ST03, ST04, ST06, ST07, ST08 | error | item | 5, 6 |
| ST05, ST09 | warn | item | 5 |
| PR01, PR02, PR03 | error | item | 2, 8 |
| PR04 | warn | item | 7 |
| DS01, DS02 | error | item | 8 |
| OR01, OR02 | error | item / bank | 1 |
| BK01, BK02, BK03, BK04 | warn | bank | 9 |
