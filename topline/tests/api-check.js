// Checks Topline's tutor API (window.topline and the postMessage bridge) in headless Chromium.
// Usage: node topline/tests/api-check.js
const fs = require('fs');
const os = require('os');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('/opt/node-tools/node_modules/playwright');

const PAGE = pathToFileURL(path.join(__dirname, '..', 'index.html')).href;
let fail = 0, total = 0;
function check(name, ok, detail) {
  total++; if (!ok) fail++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : `: ${detail === undefined ? '' : JSON.stringify(detail)}`}`);
}
const near = (a, b, tol = 1e-6) => typeof a === 'number' && Math.abs(a - b) < tol * Math.max(1, Math.abs(b));
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function openPage(browser, url = PAGE) {
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(url);
  await page.waitForFunction(() => window.topline && document.querySelector('#list .row'));
  return { page, errors };
}

(async () => {
  const browser = await chromium.launch();
  try {
    // ---- direct API ----
    const { page, errors } = await openPage(browser);
    check('version is a string', typeof await page.evaluate(() => topline.version) === 'string');

    const ids = await page.evaluate(() => topline.setExpressions([
      'f(x)=x^2-5x+6', 'f(3)', 'x_1=[1,2,3,4,5]', 'y_1=[2.1,3.9,6.2,7.8,10.1]', 'y_1\\sim mx_1+b', 'A=(-2,1)', 'k+1', { latex: '"a note' },
    ]));
    check('setExpressions returns ids', Array.isArray(ids) && ids.length === 8, ids);
    const exprs = await page.evaluate(() => topline.getExpressions());
    check('getExpressions lists the rows', exprs.length === 8 && exprs[0].latex === 'f(x)=x^2-5x+6' && exprs[0].type === 'expression' && exprs[7].type === 'note', exprs);
    check('the UI shows the new rows', await page.evaluate(() => document.querySelectorAll('#list .row').length) === 9);

    const an = await page.evaluate(() => topline.analyze());
    const byLatex = t => an.find(r => r.latex === t) || {};
    check('analyze: f(3) = 0', byLatex('f(3)').kind === 'val' && byLatex('f(3)').value === 0, byLatex('f(3)'));
    check('analyze: f is a function definition', byLatex('f(x)=x^2-5x+6').kind === 'fdef' && byLatex('f(x)=x^2-5x+6').name === 'f', byLatex('f(x)=x^2-5x+6'));
    check('analyze: list value', JSON.stringify(byLatex('x_1=[1,2,3,4,5]').value) === '[1,2,3,4,5]', byLatex('x_1=[1,2,3,4,5]'));
    const reg = byLatex('y_1\\sim mx_1+b').regression;
    check('analyze: regression params', reg && near(reg.params.m, 1.99) && near(reg.params.b, 0.05, 1e-4) && reg.n === 5 && reg.r2 > 0.99 && typeof reg.rmse === 'number', reg);
    check('analyze: point as {x,y}', JSON.stringify(byLatex('A=(-2,1)').value) === '{"x":-2,"y":1}', byLatex('A=(-2,1)'));
    const k = byLatex('k+1');
    check('analyze: error and missing names', k.kind === 'err' && /k/.test(k.error) && JSON.stringify(k.missing) === '["k"]', k);
    check('analyze is JSON-safe', await page.evaluate(() => { const a = topline.analyze(); return JSON.stringify(JSON.parse(JSON.stringify(a))) === JSON.stringify(a); }));

    // ---- evaluate ----
    const ev = await page.evaluate(() => [topline.evaluate('f(2)+m'), topline.evaluate('\\operatorname{mean}(x_1)'), topline.evaluate('q^2'), topline.evaluate('y=2'), topline.getExpressions().length]);
    check('evaluate f(2)+m', near(ev[0].value, 1.99) && ev[0].error === null, ev[0]);
    check('evaluate mean(x_1)', ev[1].value === 3, ev[1]);
    check('evaluate reports missing names', ev[2].value === null && JSON.stringify(ev[2].missing) === '["q"]', ev[2]);
    check('evaluate rejects equations', ev[3].value === null && !!ev[3].error, ev[3]);
    check('evaluate adds no row', ev[4] === 8, ev[4]);

    // ---- setExpression / removeExpression ----
    const r = await page.evaluate(() => {
      const id = topline.setExpression({ latex: 'g(x)=2x' });
      const id2 = topline.setExpression({ latex: 'g(4)' });
      const v1 = topline.analyze().find(r => r.id === id2).value;
      topline.setExpression({ id, latex: 'g(x)=3x' });
      const v2 = topline.analyze().find(r => r.id === id2).value;
      topline.setExpression({ id, hidden: true });
      const kept = topline.getState().rows.find(r => r.text === 'g(x)=3x');
      const removed = topline.removeExpression(id2), gone = !topline.getExpressions().some(r => r.id === id2);
      return { v1, v2, hiddenKeptLatex: !!(kept && kept.hidden), removed, gone, missing: topline.removeExpression(99999) };
    });
    check('setExpression adds and updates by id', r.v1 === 8 && r.v2 === 12, r);
    check('setExpression merges fields', r.hiddenKeptLatex, r);
    check('removeExpression', r.removed && r.gone && r.missing === false, r);

    // ---- settings ----
    const st = await page.evaluate(() => { topline.setExpression({ latex: '\\sin(30)' }); const s = topline.setSettings({ degrees: true, theme: 'dark' }); const v = topline.analyze().find(r => r.latex === '\\sin(30)').value; return { s, v, theme: document.documentElement.dataset.theme, pressed: document.querySelector('#angDeg').getAttribute('aria-pressed') }; });
    check('setSettings degrees + theme', st.s.degrees === true && st.s.theme === 'dark' && near(st.v, 0.5) && st.theme === 'dark' && st.pressed === 'true', st);
    const badSet = await page.evaluate(() => { try { topline.setSettings({ theme: 'pink' }); return 'no error'; } catch (e) { return e.message; } });
    check('setSettings validates theme', badSet !== 'no error', badSet);

    // ---- onChange after the student types ----
    await page.evaluate(() => {
      topline.setExpressions(['a=4']);
      window.__changes = [];
      window.__unsub = topline.onChange(p => window.__changes.push(p));
    });
    await sleep(250); // let the setExpressions notification pass
    await page.evaluate(() => { window.__changes = []; });
    const lastId = await page.evaluate(() => document.querySelector('#list .row:last-child').dataset.id);
    await page.click(`#list .row[data-id="${lastId}"] .mf`);
    await page.keyboard.type('a*3', { delay: 20 });
    await page.waitForFunction(() => window.__changes.some(c => c.analysis.some(r => r.value === 12)), null, { timeout: 3000 }).catch(() => {});
    const ch = await page.evaluate(() => ({ n: window.__changes.length, last: window.__changes[window.__changes.length - 1] }));
    const typed = ch.last && ch.last.analysis.find(r => r.value === 12);
    check('onChange fires after typing', ch.n >= 1 && !!typed && ch.last.state && Array.isArray(ch.last.state.rows), ch);
    check('onChange is debounced', ch.n < 3, ch.n);
    await page.evaluate(() => { window.__unsub(); window.__changes = []; topline.setExpression({ latex: 'b=1' }); });
    await sleep(300);
    check('unsubscribe stops callbacks', await page.evaluate(() => window.__changes.length) === 0);

    // ---- getState / setState round trip ----
    const rt = await page.evaluate(() => {
      const s = { rows: [{ type: 'expr', text: 'p=7', color: 2, hidden: false, slider: { min: 0, max: 10 }, style: { dash: true } }, { type: 'table', table: { cols: [{ name: 'x_2', cells: ['1', '2'] }, { name: 'y_2', cells: ['3', '5'] }] } }, { type: 'expr', text: 'p\\cdot2' }], settings: { deg: false, complex: false, logX: false, logY: false, theme: 'light' }, view: { cx: 1, cy: 2, sx: 40, sy: 30 } };
      topline.setState(s);
      const a = topline.getState(); topline.setState(a); const b = topline.getState();
      const an = topline.analyze();
      let bad; try { topline.setState({ rows: 'nope' }); bad = 'no error'; } catch (e) { bad = e.message; }
      return { a, b, an, bad, after: topline.getState(), ui: document.querySelectorAll('#list .row').length };
    });
    check('setState then getState keeps rows', rt.a.rows.length === 4 && rt.a.rows[0].text === 'p=7' && rt.a.rows[0].style.dash === true && rt.a.rows[1].type === 'table' && rt.a.settings.theme === 'light' && rt.a.view.sx === 40, rt.a);
    check('getState/setState round trip is stable', JSON.stringify(rt.a) === JSON.stringify(rt.b), [rt.a, rt.b]);
    check('setState recomputes', rt.an.some(r => r.value === 14) && rt.an.some(r => r.kind === 'table' && JSON.stringify(r.columns[1].values) === '[3,5]'), rt.an);
    check('setState rejects bad input and keeps state', rt.bad !== 'no error' && JSON.stringify(rt.after) === JSON.stringify(rt.b), rt.bad);
    check('UI rows match state', rt.ui === 4, rt.ui);
    await sleep(400); // saves are debounced by 300 ms
    await page.reload();
    await page.waitForFunction(() => window.topline);
    check('state is saved to local storage', await page.evaluate(() => topline.getState().rows[0].text) === 'p=7');

    // ---- postMessage bridge, same window ----
    const pm = await page.evaluate(() => new Promise(res => {
      const got = {};
      addEventListener('message', e => {
        const d = e.data; if (!d || d.source !== 'topline' || d.id == null) return;
        got[d.id] = d;
        if (Object.keys(got).length === 3) res(got);
      });
      postMessage({ source: 'topline-host', id: 1, method: 'setExpressions', args: [['h(x)=x+1', 'h(4)']] }, '*');
      postMessage({ source: 'topline-host', id: 2, method: 'analyze' }, '*');
      postMessage({ source: 'topline-host', id: 3, method: 'nope' }, '*');
    }));
    check('bridge: setExpressions result', Array.isArray(pm[1].result) && pm[1].result.length === 2, pm[1]);
    check('bridge: analyze result', pm[2].result.some(r => r.value === 5), pm[2]);
    check('bridge: unknown method gives error', typeof pm[3].error === 'string' && !('result' in pm[3]), pm[3]);
    check('no console errors (direct page)', errors.length === 0, errors);
    await page.close();

    // ---- allowOrigin blocks other origins ----
    const { page: p2, errors: e2 } = await openPage(browser, PAGE + '?allowOrigin=https://example.com');
    const blocked = await p2.evaluate(() => new Promise(res => {
      let replied = false;
      addEventListener('message', e => { if (e.data && e.data.source === 'topline' && e.data.id === 9) replied = true; });
      postMessage({ source: 'topline-host', id: 9, method: 'getState' }, '*');
      setTimeout(() => res(replied), 400);
    }));
    check('allowOrigin ignores other origins', blocked === false);
    check('no console errors (allowOrigin page)', e2.length === 0, e2);
    await p2.close();

    // ---- postMessage bridge, real iframe host ----
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'topline-api-'));
    const host = path.join(dir, 'host.html');
    fs.writeFileSync(host, `<!doctype html><meta charset="utf-8"><iframe id="f" src="${PAGE}" style="width:900px;height:600px"></iframe>
<script>
window.log = []; let n = 0; const wait = {};
addEventListener('message', e => { const d = e.data; if (!d || d.source !== 'topline') return; if (d.event) log.push(d); else if (wait[d.id]) { wait[d.id](d); delete wait[d.id]; } });
window.call = (method, ...args) => new Promise(r => { const id = ++n; wait[id] = r; document.getElementById('f').contentWindow.postMessage({ source: 'topline-host', id, method, args }, '*'); });
</script>`);
    const hostPage = await browser.newPage(), he = [];
    hostPage.on('console', m => { if (m.type() === 'error') he.push(m.text()); });
    hostPage.on('pageerror', e => he.push(String(e)));
    await hostPage.goto(pathToFileURL(host).href);
    const frame = await (await hostPage.waitForSelector('#f')).contentFrame();
    await frame.waitForFunction(() => window.topline && document.querySelector('#list .row'));
    const ifr = await hostPage.evaluate(async () => {
      const s = await call('setExpressions', ['f(x)=x^2-5x+6', 'f(3)', 'x_1=[1,2,3]', 'y_1=[2,4,6]', 'y_1\\sim mx_1+b']);
      const a = await call('analyze');
      const ev = await call('evaluate', 'f(5)');
      const bad = await call('setState', { rows: 5 });
      await new Promise(r => setTimeout(r, 300));
      return { s, a, ev, bad, changes: log.length, lastChange: log[log.length - 1] };
    });
    check('iframe bridge: setExpressions', Array.isArray(ifr.s.result) && ifr.s.result.length === 5, ifr.s);
    check('iframe bridge: analyze', ifr.a.result.some(r => r.latex === 'f(3)' && r.value === 0) && ifr.a.result.some(r => r.regression && near(r.regression.params.m, 2)), ifr.a);
    check('iframe bridge: evaluate', ifr.ev.result && ifr.ev.result.value === 6, ifr.ev);
    check('iframe bridge: errors are returned', typeof ifr.bad.error === 'string', ifr.bad);
    check('iframe posts change events to the parent', ifr.changes >= 1 && ifr.lastChange.event === 'change' && Array.isArray(ifr.lastChange.analysis), { changes: ifr.changes });
    await hostPage.evaluate(() => { log.length = 0; });
    const fid = await frame.evaluate(() => document.querySelector('#list .row:last-child').dataset.id);
    await frame.click(`#list .row[data-id="${fid}"] .mf`);
    await hostPage.keyboard.type('f(4)', { delay: 20 });
    await hostPage.waitForFunction(() => log.some(c => c.analysis.some(r => r.value === 2)), null, { timeout: 3000 }).catch(() => {});
    check('iframe posts a change event when the student types', await hostPage.evaluate(() => log.some(c => c.analysis.some(r => r.value === 2))));
    check('no console errors (iframe host)', he.length === 0, he);
    fs.rmSync(dir, { recursive: true, force: true });
  } catch (e) {
    fail++; console.log('FAIL unexpected error:', e && e.stack || e);
  } finally {
    await browser.close();
  }
  console.log(`\n${Math.max(0, total - fail)}/${total} passed`);
  process.exit(fail ? 1 : 0);
})();
