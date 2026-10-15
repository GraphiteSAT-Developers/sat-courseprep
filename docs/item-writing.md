# Item-writing checklist

Rules for anyone adding items to `web/content/items.ts`. The schema is in
`web/content/types.ts`; the first batch (ids `alg-*`, `adv-*`, `psda-*`, `geo-*`)
shows every field filled in. Run `python3 web/scripts/verify_items.py` before
you hand an item over.

## 1. Originality (non-negotiable)

- [ ] Every item is written from scratch. Do not copy, paraphrase, re-number or
      "lightly change" a College Board, Khan Academy, Bluebook, Question Bank,
      or other published question. College Board content cannot be used
      commercially or with generative AI (see `HANDOFF.md`).
- [ ] Choose your own numbers, context and structure. Matching a *skill* is
      fine; matching a specific published question's setup is not.
- [ ] If you looked at a published item for the skill description, close it
      before writing. Do not write "inspired by" items.
- [ ] Contexts (print shop, seedlings, survey) are invented, not real
      organizations or people.

## 2. Provenance

- [ ] `provenance.author` is your name or agent id, `created` is an ISO date.
- [ ] `provenance.notes` records how the key was checked (for example
      `"key verified with SymPy"`) and anything a reviewer should know.
- [ ] The id is a short slug `domain-topic-detail` (`alg-no-solution-k`) and is
      never reused after an item is deleted.

## 3. Keys are verified, never assumed

- [ ] Add a SymPy computation for the item to `CHECKS` in
      `web/scripts/verify_items.py`. The computation must derive the answer
      from the stem's givens, not restate the key.
- [ ] Run the script. It fails if the key disagrees, if an MC distractor is
      also correct, if an SPR key doesn't fit Bluebook's entry box, or if an
      item has no check at all.
- [ ] Leave `desmos.verified: false`. Only the headless Desmos service sets it
      to true, after running the lines with the College Board options.

## 4. Format and difficulty tags

- [ ] `domain` is one of `algebra`, `advanced-math`, `psda`, `geometry-trig`;
      `skill` is one of the College Board skill names listed in
      `research_notes/AI Desmos SAT math course plan/sat_math_format.md`.
- [ ] Target mix for a batch: roughly 3 MC to 1 SPR; domains weighted
      35/35/15/15 like the test; lean `hard`, since the course targets
      700–800 scorers. Use `medium` for one-step items with one trap;
      `hard` for items with unknown constants, a structural insight, or two
      ideas combined. `easy` is for warm-ups only.
- [ ] Stems use `$...$` for math (KaTeX). Never put a literal dollar sign in
      prose; write "23.00 dollars". Keep choices free of `]` (the verifier's
      parser stops at the first one).

## 5. SPR (student-produced response) rules

- [ ] Keys are `Rational` objects (`{ num, den }`, `den > 0`), one per
      acceptable answer. Multiple keys only when the stem genuinely allows
      several answers and says so ("one possible value").
- [ ] The answer must be enterable under Bluebook rules: at most 5 characters
      for a positive answer, 6 for a negative one including the minus sign.
      Prefer keys whose reduced fraction fits (`36/7`, `-5/3`); avoid keys
      that only fit as a truncated decimal.
- [ ] Non-terminating decimals must fill the box (`1.666` / `1.667` for 5/3;
      `0.67` is wrong). Say so in `desmos.read` when the Desmos display shows
      a rounded value, and point to the fraction toggle (T11).
- [ ] No answers that need symbols, units, mixed numbers, or more than one
      value.

## 6. Multiple-choice distractors

- [ ] Four choices, exactly one correct. The verifier checks that no
      distractor equals the key.
- [ ] Each distractor is the result of a specific, plausible mistake: sign
      error, other root, halved or doubled, forgot the constant or fee,
      solved for the wrong variable, swapped conditional probability,
      used `x + y` instead of `x - y`, etc. Name the mistake in `byHand`.
- [ ] No "none of the above", no throwaway choices, no two choices that are
      the same value in different forms.
- [ ] Order choices numerically (ascending) unless the item is about words.
      Don't let the key land in the same position across a batch.

## 7. Desmos route and by-hand route

- [ ] `route` says which method the course teaches first:
      `desmos-primary` when typing the lines and reading the screen beats
      the algebra; `hand-primary` when the hand method takes under about
      15 seconds or Desmos can't express the step (perpendicular slopes,
      5-12-13 triangles, table reading, symmetric identities);
      `either` when both are reasonable and the choice is a judgment call.
      Every batch needs several `hand-primary` items so the Desmos-vs-hand
      boundary is taught, not just Desmos.
- [ ] `techniques` lists every T1–T13 id the Desmos route uses (from
      `research_notes/.../desmos_techniques.md`). Empty is allowed only if
      `desmos` is omitted.
- [ ] `desmos.lines` are the exact LaTeX strings the student types, one per
      expression line: `y_1\sim mx_1+b`, `x_1=[1,2,3]`, `\frac{a}{b}`,
      `\le`, `\operatorname{mean}(L)`. Remember the TS string needs `\\`.
      Include the setup line (`x_1=[...]`) for every tilde regression.
- [ ] `desmos.read` says what to click or read afterwards, which value to
      take, and any mode or zoom warning (degrees for T12, zoom out for T1).
      For `hand-primary` items, say honestly that Desmos is slower.
- [ ] `byHand` is a complete, checkable solution a strong student could
      follow, ending in the key. For MC, add the distractor rationale here.

## 8. Before handing over

- [ ] `python3 web/scripts/verify_items.py` passes with your item listed.
- [ ] `cd web && npm test && npm run typecheck` pass.
- [ ] Read the stem once more as a student would: is anything ambiguous
      (which root, which coordinate, integer or real, degrees or radians)?
      Fix the stem, not the key.
