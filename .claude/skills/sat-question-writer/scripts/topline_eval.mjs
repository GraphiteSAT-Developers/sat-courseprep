// Runs calculator lines through Topline's math engine (the code between the ENGINE markers in topline/index.html).
// Usage: node topline_eval.mjs <path/to/topline/index.html>   with JSON on stdin: [{"lines": [...], "degrees": false}, ...]
// Prints one result per job: {"rows": [{"kind", "value", "error", "params"}]} (value is plain JSON; params for regressions).
import { readFileSync } from 'node:fs';

const html = readFileSync(process.argv[2], 'utf8');
const m = /\/\/ == ENGINE START ==([\s\S]*)\/\/ == ENGINE END ==/.exec(html);
if (!m) { console.error('No ENGINE START/END markers in ' + process.argv[2]); process.exit(2); }
const E = new Function(`${m[1]}; return { analyzeAll, setDeg: d => { DEG = d; }, Pt: typeof Pt === 'undefined' ? null : Pt };`)();

const plain = v => {
  if (typeof v === 'number') return Number.isFinite(v) ? v : null;
  if (typeof v === 'boolean' || typeof v === 'string') return v;
  if (Array.isArray(v)) return v.map(plain);
  if (v && typeof v === 'object' && 'x' in v && 'y' in v) return { x: plain(v.x), y: plain(v.y) };
  if (v && typeof v === 'object' && 're' in v && 'im' in v) return { re: plain(v.re), im: plain(v.im) };
  return null;
};

const jobs = JSON.parse(readFileSync(0, 'utf8'));
const out = jobs.map(job => {
  try {
    E.setDeg(!!job.degrees);
    const res = E.analyzeAll(job.lines.map((text, i) => ({ text, seed: i + 1 })));
    return {
      rows: res.map(R => {
        const row = { kind: R.kind, value: null, error: R.kind === 'err' ? R.error : null, params: null };
        if ('value' in R) row.value = plain(R.value);
        if (R.kind === 'reg' && R.res && R.params) row.params = Object.fromEntries(R.params.map((p, i) => [p, plain(R.res.p[i])]));
        return row;
      }),
    };
  } catch (e) { return { error: String(e && e.message || e) }; }
});
process.stdout.write(JSON.stringify(out));
