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
const checks = readFileSync(path.join(here, "src/masterclass-checks.js"), "utf8");
const Checks = require(path.join(here, "src/masterclass-checks.js"));

const problems = [];
const fail = (where, msg) => problems.push(`${where}: ${msg}`);

// Content that doesn't need a browser.
const unitIds = new Set(content.units.map(u => u.id));
const ids = new Set();
for (const L of content.lessons) {
  if (ids.has(L.id)) fail(L.id, "duplicate lesson id");
  ids.add(L.id);
  if (!unitIds.has(L.unit)) fail(L.id, `unknown unit ${L.unit}`);
  const qs = [...(L.reads || []), ...(L.try ? [L.try] : [])];
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

for (const L of content.lessons) {
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
console.log(`\nAll ${content.lessons.length} lessons check out.`);
