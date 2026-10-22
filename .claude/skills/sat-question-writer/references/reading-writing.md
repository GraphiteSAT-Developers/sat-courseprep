# Reading and Writing questions

The Digital SAT Reading and Writing section is 54 questions in two 32-minute modules of 27. Every question has its own short text and is four-choice multiple choice. Read `rw_skills.json` first: it has the 11 skills with their College Board testing points, a `tip` (the strategy the site teaches) and a `trap` (the mistake it warns about). Good questions test exactly that tip and tempt exactly that trap.

## Format (one JSON object per line)

```json
{"id": "rw-wic-NNN", "section": "rw", "domain": "craft-structure", "skill": "Words in context", "difficulty": "medium",
 "format": "mc",
 "passage": [{"kind": "p", "paras": ["... ______ ..."]}],
 "stem": "Which choice completes the text with the most logical and precise word or phrase?",
 "byHand": "Why the answer is right, from the text. Distractors: why A is wrong; why C is wrong; why D is wrong.",
 "provenance": {"author": "claude-question-writer", "created": "2026-10-22", "notes": "batch rw-wic-1"},
 "status": "draft", "choices": ["...", "...", "...", "..."], "answerIndex": 1,
 "check": {"blind": 1, "notes": ""}}
```

| Field | Rule |
|---|---|
| `id` | `rw-<code>-NNN`, where `<code>` is the skill's `code` in `rw_skills.json` (`wic`, `tsp`, `ctc`, `cid`, `coet`, `coeq`, `inf`, `bnd`, `fss`, `tr`, `rs`) and NNN continues after the highest number for that code in the bank and in any existing `question-drafts/*.jsonl` (the checker fails on a reused id) |
| `section` | `"rw"` |
| `domain` | `craft-structure`, `information-ideas`, `conventions`, `expression-ideas` (must match the skill's domain) |
| `skill` | Exactly a `name` from `rw_skills.json` |
| `format` | `"mc"` |
| `passage` | A list of blocks (below) |
| `stem` | The question, in the official phrasing for the skill (examples below) |
| `choices` / `answerIndex` | Four distinct choices; the right one's index 0–3 |
| `byHand` | The explanation: why the right answer is right, quoting or pointing to the text, then `Distractors:` and a short reason for each wrong choice, naming the trap |
| No `tex`, `techniques`, `route` or `desmos` fields | |

### Passage blocks

| Block | Use |
|---|---|
| `{"kind": "intro", "text": "..."}` | One line of context for literary excerpts ("The following text is adapted from ...") or poems. Only when it's actually needed |
| `{"kind": "p", "paras": ["...", "..."]}` | The text. Use `______` for the blank in completion questions |
| `{"kind": "text1", "paras": [...]}`, `{"kind": "text2", "paras": [...]}` | Cross-text connections: two short texts on the same topic |
| `{"kind": "notes", "items": ["...", ...]}` | Rhetorical synthesis: 4–6 bullet notes, introduced by a `p` block ("While researching a topic, a student has taken the following notes:") |
| `{"kind": "table", "caption": "...", "header": [...], "rows": [[...]]}` | Quantitative evidence with a table |
| `{"kind": "graph", "title": "...", "label": "axis label", "header": [...], "rows": [[...]]}` | Quantitative evidence with a bar graph (the site draws it from the rows) |

Inline marks: `[u]underlined[/u]` (balanced; used for "the underlined sentence" questions) and `[i]italics[/i]` for titles and scientific names.

### Length

Real SAT texts run about 25–150 words. Conventions and transitions items can be short (one to three sentences); craft, information and inference items should usually be 60–150 words so there is something to read closely. The checker warns below 15 or above 170 words.

## Official stem phrasing by skill

- **Words in context:** "Which choice completes the text with the most logical and precise word or phrase?" / "As used in the text, what does the word "___" most nearly mean?"
- **Text structure and purpose:** "Which choice best states the main purpose of the text?" / "Which choice best describes the function of the underlined sentence in the text as a whole?" / "Which choice best describes the overall structure of the text?"
- **Cross-text connections:** "Based on the texts, how would the author of Text 2 most likely respond to the ... described in Text 1?"
- **Central ideas and details:** "Which choice best states the main idea of the text?" / "According to the text, ...?"
- **Command of evidence: textual:** "Which finding, if true, would most directly support the researcher's claim?" / "Which quotation from the poem most effectively illustrates the claim?"
- **Command of evidence: quantitative:** "Which choice most effectively uses data from the table/graph to complete the statement/example?"
- **Inferences:** "Which choice most logically completes the text?"
- **Boundaries** and **Form, structure, and sense:** "Which choice completes the text so that it conforms to the conventions of Standard English?"
- **Transitions:** "Which choice completes the text with the most logical transition?"
- **Rhetorical synthesis:** "The student wants to [goal]. Which choice most effectively uses relevant information from the notes to accomplish this goal?"

## What good questions look like

- **Topics** span the test's mix: science, social science, humanities (art, music, literature, history) and literary excerpts. Write original texts. For "adapted from" literary or historical excerpts, only use work that is public domain (published before 1929) and that you're quoting accurately; otherwise write an original passage and don't attribute it.
- **Facts** in informational texts should be accurate or clearly hypothetical. Don't invent studies by real named researchers; use generic researchers ("a team of ecologists") or clearly fictional names.
- **The right answer** is supported by the text alone, without outside knowledge.
- **Wrong answers are tempting for a reason:** true but irrelevant to the question, too broad or narrow, the opposite relationship, half right, a plausible word with the wrong precise meaning, a common punctuation error.
- **No length tell.** Across a batch the right answer should be the longest choice no more than about a quarter of the time. Make choices similar in length and form. (The bank's tests enforce this per skill.)
- **Conventions items** test one rule each (comma splice, colon after an independent clause, subject-verb agreement across an interrupting phrase, pronoun agreement, verb tense, possessives, modifier placement). The other three choices are each a specific wrong version of the same spot.
- **Transitions** need a passage whose logic forces exactly one relationship (contrast, cause, example, addition, sequence); avoid passages where two transitions both work.
- **Rhetorical synthesis** notes must contain the facts for every choice, with only one choice meeting the stated goal.
- **Quantitative evidence** data must be internally consistent, and exactly one choice must be both true of the data and relevant to the claim.
