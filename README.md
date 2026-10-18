# sat-courseprep

Planning for an AI-powered SAT Math course aimed at an 800. It teaches Desmos first and by-hand methods second, with an AI tutor that uses Desmos itself.

Start here: [`HANDOFF.md`](HANDOFF.md)

To run the Graphite SAT website on your computer: open this folder in VS Code and press F5, or run `python start.py`. Details are in [`backend/README.md`](backend/README.md).

## Contents

- [`reports/AI Desmos SAT math course plan.md`](reports/AI%20Desmos%20SAT%20math%20course%20plan.md): the full planning report, with the recommended architecture, a phased roadmap, the decisions the owner needs to make, and a list of facts still to verify.
- [`website/`](website/): Graphite SAT, the website for the AI SAT tutor: marketing pages, sign-in, the student dashboard and the math practice test. Built pages are in `website/site/`.
- [`backend/`](backend/): the Flask server that runs the site, with student accounts, test grading, the dashboard API and the database. Start with [`backend/README.md`](backend/README.md).
- [`topline/`](topline/): Topline, a standalone browser graphing calculator with a live math editor. Open `topline/index.html` in a browser.
- [`docs/desmos-integration.md`](docs/desmos-integration.md): calculator design decision (student-operated embed, OnePrep-style) and how the AI reads it
- `research_notes/AI Desmos SAT math course plan/`: the notes behind the report, with sources:
  - `sat_math_format.md`: Digital SAT Math format, scoring, and the Desmos calculator in Bluebook
  - `desmos_techniques.md`: Desmos technique library (T1–T13) and existing resources
  - `gemini_desmos_ai.md`: Gemini API features, the Desmos API, and how to make an AI reliably good at Desmos
  - `competitive_landscape.md`: competing AI SAT tutors and Desmos courses
  - `architecture_legal_pedagogy.md`: tech stack, legal and compliance (Gemini age terms, College Board, Desmos licensing, COPPA), and learning science

> Note: the research environment could not open official pages (collegeboard.org, desmos.com, ai.google.dev) directly. The findings come from search-result summaries, so check the items in the report's verification table before relying on them.
