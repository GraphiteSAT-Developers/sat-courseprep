---
name: sat-question-writer
description: Write original Digital SAT practice questions (Math and Reading and Writing) for the Graphite SAT question bank, in the bank's exact items.jsonl format, with every answer key checked before it's saved. Use this whenever the user wants to write, generate, draft, add, expand or fix SAT questions, practice items, question-bank entries, distractors, explanations, passages or Desmos/Topline solutions, even if they just say "make 20 hard quadratics", "we need more transitions questions" or "fill the geometry gaps".
---

# SAT question writer

You are writing questions for a course that aims students at an 800 (Math) and a high Reading and Writing score. A wrong answer key, an ambiguous question or a broken Desmos step teaches a student the wrong thing, and they trust the bank completely. So the job is not "write questions"; it is **write questions and prove each one is right before it is saved**. Expect to throw some away.

## Where things are (Graphite SAT repo)

| What | Path |
|---|---|
| The live bank (1,000 Math then 500 Reading and Writing, in that order) | `backend/app/content/bank/items.jsonl` |
| Math domains and skills, with College Board testing points | `backend/app/content/bank/skills.json` |
| Reading and Writing skills, testing points, tips and traps | `backend/app/content/bank/rw_skills.json` |
| Desmos techniques T1–T13 (ids used in `techniques`) | `backend/app/content/bank/techniques.json` |
| The calculator engine the checker runs Math lines through | `topline/index.html` |
| **Where you write** | `question-drafts/<batch-name>.jsonl` (create it) |

Read the relevant skills file before writing, and match `skill` names to it exactly.

**Never edit `items.jsonl` directly.** The backend tests pin it at exactly 1,000 Math then 500 Reading and Writing questions, and the site numbers questions by file position, so a stray line breaks tests and students' progress. New questions go to a drafts file; moving approved drafts into the bank is a separate step the owner asks for (append at the end of the right section's run and update the counts in `backend/tests/test_rw.py`).

## Workflow for each batch

1. **Plan the batch.** Agree with the user on count, section, domains/skills and difficulty mix. If they don't say, fill gaps: count what the bank already has per skill and difficulty (a quick script over `items.jsonl`) and favour thin areas. Keep the right answers spread evenly over A–D across the batch.
2. **Write each question** following the section reference:
   - Math: [references/math.md](references/math.md)
   - Reading and Writing: [references/reading-writing.md](references/reading-writing.md)
3. **Add a `check` block** to every draft (format below). It is draft-only and is stripped on export.
4. **Blind-solve.** Have a separate agent (a subagent with no access to your notes or the key) answer the questions from only what a student sees: passage, stem and choices, with SPR questions marked "enter a number". One solver can take the whole batch. Ask it to say if any question has more than one defensible answer. Record its answers in `check.blind`. If it disagrees with your key, the question is wrong or ambiguous: fix it or drop it, and don't argue the solver round to your answer. If you have no way to start a separate agent, stop and ask the user how they want this done; never fill `check.blind` from the key yourself.
5. **Run the checker** from the repo root, and fix everything it reports:
   ```bash
   python .claude/skills/sat-question-writer/scripts/check_drafts.py question-drafts/<batch>.jsonl
   ```
   (If the skill is installed elsewhere, use that path to `scripts/check_drafts.py`; it finds the repo from your working directory, or pass `--repo`.)
6. **Export** the clean batch once everything passes:
   ```bash
   python .../check_drafts.py question-drafts/<batch>.jsonl --export question-drafts/<batch>.ready.jsonl
   ```
   Export strips `check` and sets `desmos.verified: true` only on questions whose own `desmos.lines` produced the key in Topline (helper lines don't count, see below).
7. **Report** to the user: how many written, how many dropped and why, the skill/difficulty/answer-letter spread, and anything a human should look at (borderline wording, figures that need drawing). Commit the drafts on a `claude/...` branch if they want, but don't merge into the bank unless asked.

## The rules that matter most

**Original only.** Never reproduce, closely paraphrase or "lightly edit" a College Board question, an official practice test item, or a question from any prep book or site. College Board content can't be used commercially or with AI. Write from the skill's testing points, not from memory of a real item. The checker flags near-duplicates of the existing bank; it can't detect copies of outside material, so this one is on you.

**One right answer.** Exactly one choice is defensibly correct; each wrong choice is clearly wrong for a specific reason a student could be taught. No "trick" wording, no reliance on obscure facts, no answer that depends on rounding the student can't see.

**Distractors come from real mistakes.** Each wrong choice should be what a student gets from a specific error (sign slip, wrong formula, answering a different quantity, misreading "not", a plausible-but-imprecise word). Name the mistake for each one in the explanation's `Distractors:` part; the site uses it to tell students what went wrong.

**No tells.** The right answer shouldn't be the longest, the most hedged, the only one with a number in a certain form, or the "middle" value. Spread right answers across A–D.

**Difficulty is honest.** Easy: one step, a skill used directly. Medium: two or three steps, or a context to translate. Hard: the kind of item that separates 750 from 800: several steps, a constraint to notice, unknown constants, or interpretation that needs care. Don't make "hard" by making numbers ugly.

**Student-facing text** is plain and short, on one line (no line breaks in stems, choices or explanations; write systems inline, the bank's way: "In the system of equations $5x - ky = 8$ and $15x + 12y = 2$, ..."). Math is always LaTeX in `$...$` (the bank tests fail on bare `x^2`, `sqrt(`, `<=`, `π` or `3 + 4` outside `$`). Money is written in words ("45.00 dollars"), never with a `$` sign. No emoji, no slang, no names or topics that could upset a teenager, and keep contexts neutral and fair across backgrounds.

## The `check` block (draft-only)

```json
"check": {
  "sympy": "x = symbols('x'); sols = solve(6*x**2 - x - 2, x); answer = max(sols)",
  "topline": {"expect": {"line": 1, "value": 0.6667, "how": "positive x-intercept"}},
  "value": "2/3",
  "blind": "2/3",
  "notes": "anything a reviewer should know"
}
```

- `sympy` (Math, required): Python that **computes** the answer from the problem's math, with `from sympy import *` already done. Set `answer` (SPR, or the value of the right MC choice) and, for MC, `answer_index` by testing each choice. Don't hard-code the key; the point is an independent route.
- `topline` (Math, when the item has `desmos.lines`): what the lines should produce. `expect.line` (1-based) checks that line's value; `expect.param` checks a regression parameter (like `"b"`). The checker compares against the key (SPR) or `check.value` (MC). Points of interest (intersections, intercepts) can't be read by the engine. For those, either omit `expect` (the checker still makes sure every student line runs) or give `topline.lines`: the student's lines plus a helper line that computes the clicked value from the same math, never the key typed in. Helper lines mean the student's route isn't proven, so the item exports with `verified: false` and a human should try the clicks.
- `value`: the numeric value of the correct answer when there is one (MC or SPR), as a number or `"p/q"`.
- `blind` (required): the blind solver's answer: an index 0–3 for MC; for SPR a number or a `"p/q"` string.
- Reading and Writing questions need only `blind` (and `notes` if useful).

## Before you finish

Re-read three random questions as a strict student would: could you argue for a second choice? Is anything in the passage or stem doing nothing? Would the explanation actually teach the mistake behind each wrong choice? Fix what you find, rerun the checker, then report.
