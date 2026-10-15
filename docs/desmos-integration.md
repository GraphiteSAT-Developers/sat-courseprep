# Desmos integration: the OnePrep / Bluebook model

**Decision (owner):** Students get a Desmos graphing calculator embedded beside each question, the same way OnePrep and Bluebook do it. The student operates it. The AI does not take over the student's calculator.

This file adds to `reports/AI Desmos SAT math course plan.md`, which assumed an AI that drives Desmos.

## Two Desmos instances, two jobs

| | Student calculator (UI) | AI's verification calculator (backend) |
|---|---|---|
| Where | Browser, side panel next to the question | Headless browser (Playwright) on the server, or in CI |
| Who types | The student | The Solver agent |
| Purpose | Practice exactly what they will do in Bluebook | Make sure every Desmos step the AI teaches actually works |
| API | `Desmos.GraphingCalculator(el, opts)` | Same API, scripted with `setExpressions` + `HelperExpression` |

Both instances use the same configuration, chosen to look like the College Board build: images, folders and notes turned off, and degree/radian mode matching. Before any student uses it, a person compares it side by side with `desmos.com/testing/collegeboard/graphing` and with Bluebook.

## How the AI tutor uses the student's calculator

- **Read, don't write (default).** The tutor reads the student's work (`calculator.getState()` and `observeEvent('change')`) and sends a compact summary of their expressions to the LLM. That lets it say things like "line 3 uses `y=`; for regression you need `~` and subscripted variables". Per-expression errors come from `expressionAnalysis`, and values come from `HelperExpression`.
- **"Show me" mode (opt-in, after a failed attempt).** The tutor fills in its expressions with `setExpressions`, but only after the student has tried and asked for help. The student then has to retype the steps in a cleared calculator. This follows the guarded-tutor evidence in the report (Bastani et al.).
- **Every keystroke the AI suggests has already been run** in the backend instance and checked against the verified answer. The student never sees a Desmos instruction that hasn't been executed.

## What this changes and what it doesn't

- **Simpler:** the student-facing product doesn't need the AI to operate Desmos live. Graphing quality comes from the engine the student is already using.
- **Unchanged:** training and evaluating the AI on Desmos still happen through the headless backend instance. That is the work to finish before launch.
- **Unchanged:** a production embed needs a **paid Desmos API key**. The free key covers personal use or a 90-day internal evaluation only. Starter is reported at about $100/month for 1,000 users and is hosted by Desmos. Ask Desmos whether the server-side headless instance falls under the same plan. Embedding the public desmos.com page in an iframe is not a substitute: it is not the licensed route, and the tutor can't read its state.
- **Unchanged:** the Gemini under-18 terms problem.

## Unverified

How OnePrep actually implements its calculator (Desmos API embed or something else) could not be confirmed. Search results describe OnePrep only as a free question bank with more than 13,000 items. Check it by opening its practice interface and looking for `calculator.desmos.com/api/v1.x/calculator.js` in the network tab.
