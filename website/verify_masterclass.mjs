// Runs every Desmos masterclass lesson in a real browser against Topline, the calculator students use.
// For each step it checks that the step isn't already done, then puts in the step's "show" lines and
// checks that the step now passes. Reads with a "verify" line are checked against their answers.
//
//   node website/verify_masterclass.mjs        (needs Playwright: npm install playwright)
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); } catch {
  ({ chromium } = createRequire(path.join(process.execPath, "../../lib/node_modules/"))("playwright"));
}
const content = JSON.parse(readFileSync(path.join(here, "../backend/app/content/masterclass/lessons.json"), "utf8"));
// MERGE=path/to/pool.json adds draft quiz questions ({"lesson-id": [question, ...]}) before checking, without touching lessons.json.
if (process.env.MERGE) {
  const extra = JSON.parse(readFileSync(process.env.MERGE, "utf8"));
  for (const L of [...content.lessons, ...(content.topics || [])]) if (extra[L.id]) L.quiz = [...(L.quiz || []), ...extra[L.id]];
  const only = new Set(Object.keys(extra));
  content.lessons = content.lessons.filter(L => only.has(L.id));
  content.topics = (content.topics || []).filter(L => only.has(L.id));
}
const checks = readFileSync(path.join(here, "src/masterclass-checks.js"), "utf8");
const Checks = require(path.join(here, "src/masterclass-checks.js"));

const problems = [];
const fail = (where, msg) => problems.push(`${where}: ${msg}`);

// Content that doesn't need a browser.
const unitIds = new Set(content.units.map(u => u.id));
const ids = new Set();
const ALL = [...content.lessons, ...(content.topics || [])];
for (const L of ALL) {
  if (ids.has(L.id)) fail(L.id, "duplicate lesson id");
  ids.add(L.id);
  if (L.kind !== "topic" && !unitIds.has(L.unit)) fail(L.id, `unknown unit ${L.unit}`);
  const qs = [...(L.reads || []), ...(L.try ? [L.try] : []), ...(L.quiz || [])];
  if (L.kind !== "drill" && !(L.quiz && L.quiz.length)) fail(L.id, "no practice quiz");
  const stems = new Set();
  for (const q of L.quiz || []) { if (stems.has(q.stem)) fail(L.id, `duplicate quiz question: ${q.stem}`); stems.add(q.stem); }
  for (const q of qs) {
    if (q.choices) { if (!(Number.isInteger(q.answer) && q.answer >= 0 && q.answer < q.choices.length)) fail(L.id, `bad choice answer in "${q.prompt || q.stem}"`); }
    else if (!Checks.answerMatches(q.answer, q)) fail(L.id, `answer ${q.answer} doesn't match itself`);
  }
  if (L.kind === "drill") for (const it of L.items) if (!["desmos", "hand"].includes(it.answer)) fail(L.id, `drill answer ${it.answer}`);
}

const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const page = await browser.newPage();
page.on("pageerror", e => fail("calculator", e.message));
await page.goto(pathToFileURL(path.join(here, "../topline/index.html")).href);
await page.addScriptTag({ content: checks });
await page.waitForFunction(() => window.Topline && window.GraphiteMasterclassChecks);

for (const L of ALL) {
  if (L.kind === "drill") continue;
  const result = await page.evaluate(lesson => {
    const T = window.Topline, C = window.GraphiteMasterclassChecks, out = [];
    T.clear();
    lesson.steps.forEach((step, i) => {
      if (C.passes(step.check, T.lines(), T)) out.push(`step ${i + 1} passes before its lines are in`);
      C.applyShow(T, step);
      if (!C.passes(step.check, T.lines(), T)) {
        out.push(`step ${i + 1} fails after "show": ` + JSON.stringify(T.lines().map(l => [l.text, l.kind, l.error, l.value ?? l.fit ?? null])));
      }
    });
    if (lesson.try && lesson.try.check) {
      T.clear();
      if (C.passes(lesson.try.check, T.lines(), T)) out.push("the SAT-style question's calculator check passes on a blank calculator");
      C.applyShow(T, lesson.try);
      if (!C.passes(lesson.try.check, T.lines(), T)) out.push("the SAT-style question's calculator check fails after its lines: " + JSON.stringify(T.lines().map(l => [l.text, l.kind, l.error])));
      T.clear();
      lesson.steps.forEach(step => C.applyShow(T, step));
    }
    // Practice quiz: each question's work must not already be done by the lesson, and its lines must pass.
    (lesson.quiz || []).forEach((q, i) => {
      T.clear();
      lesson.steps.forEach(step => C.applyShow(T, step));
      if (lesson.try) C.applyShow(T, lesson.try);
      if (!q.check) return;
      if (C.passes(q.check, T.lines(), T)) out.push(`quiz ${i + 1}: its calculator check already passes from the lesson's work`);
      // Quizzes draw questions in any order, so no other question's work may unlock this one.
      lesson.quiz.forEach((other, j) => { if (j === i || !other.show) return; T.clear(); C.applyShow(T, other); if (C.passes(q.check, T.lines(), T)) out.push(`quiz ${i + 1}: unlocked by quiz ${j + 1}'s work`); });
      T.clear();
      C.applyShow(T, q);
      if (!C.passes(q.check, T.lines(), T)) out.push(`quiz ${i + 1}: check fails after its lines: ` + JSON.stringify(T.lines().map(l => [l.text, l.kind, l.error, l.value ?? l.fit ?? null])));
    });
    T.clear();
    lesson.steps.forEach(step => C.applyShow(T, step));
    (lesson.reads || []).forEach((q, i) => {
      if (!q.verify) return;
      T.add([q.verify]);
      const lines = T.lines(), v = lines[lines.length - 2].value;
      const want = "equals" in q ? q.equals : C.parseAnswer(q.answer);
      if (!(typeof v === "number" && Math.abs(v - want) <= (q.tol || 1e-9) * Math.max(1, Math.abs(want)))) out.push(`read ${i + 1}: ${q.verify} = ${v}, expected ${want}`);
    });
    return out;
  }, L);
  result.forEach(r => fail(L.id, r));
  console.log(`${result.length ? "FAIL" : "ok  "} ${L.id}`);
}
await browser.close();

if (problems.length) {
  console.error("\n" + problems.join("\n"));
  process.exit(1);
}
console.log(`\nAll ${ALL.length} lessons check out.`);
