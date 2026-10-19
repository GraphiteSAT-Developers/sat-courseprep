# Reading and Writing question sources

Original Reading and Writing questions written for Graphite SAT in the style of the digital SAT
(not College Board content). People, studies, places, novels and poems in the passages are
fictional unless the passage says otherwise.

Each `.txt` file holds one skill. `python3 backend/compile_rw.py` checks every question and writes
`../rw_items.jsonl`, which the site serves. Run it after any edit; the tests fail if the two disagree.

## Format

A question starts with a `##` line naming the skill code and difficulty, then tagged lines:

```
## cid easy
I: The following text is adapted from a short story.      (optional intro, shown in italics)
P: The passage. A line that starts without a tag continues the tag above it.
   A blank line starts a new paragraph.
P1: / P2:   Text 1 and Text 2, for cross-text questions
N: one bullet of a student's notes (rhetorical synthesis)
T: Table caption
| Header | Header |
| cell   | cell   |
G: Bar graph title | label for the values
| Category | Series A | Series B |
| 2019     | 12       | 15       |
Q: The question.
A: a wrong choice
*A: the right choice (exactly one star)
A: ...
X: The explanation: why the answer is right and why each other choice is wrong.
```

Inline: `[u]underlined[/u]`, `[i]italics[/i]`, and `______` for the blank.

## Skill codes

| Code | Domain | Skill |
| --- | --- | --- |
| cid | Information and Ideas | Central ideas and details |
| coet | Information and Ideas | Command of evidence: textual |
| coeq | Information and Ideas | Command of evidence: quantitative |
| inf | Information and Ideas | Inferences |
| wic | Craft and Structure | Words in context |
| tsp | Craft and Structure | Text structure and purpose |
| ctc | Craft and Structure | Cross-text connections |
| rs | Expression of Ideas | Rhetorical synthesis |
| tr | Expression of Ideas | Transitions |
| bnd | Standard English Conventions | Boundaries |
| fss | Standard English Conventions | Form, structure, and sense |
