/* Lessons page: shows one lesson at a time (the one in the URL hash) and grades the quick checks.
   Without this script every lesson is shown in a row and the explanations still open. */
(function () {
  var page = document.querySelector('.lessons-page');
  if (!page) return;
  var index = page.querySelector('.ls-index');
  var intro = page.querySelector('.pr-lede');
  var lessons = Array.prototype.slice.call(page.querySelectorAll('[data-lesson]'));
  document.documentElement.classList.add('ls-js');

  function show() {
    var id = decodeURIComponent(location.hash.slice(1));
    var current = lessons.filter(function (l) { return l.id === id; })[0];
    lessons.forEach(function (l) { l.hidden = l !== current; });
    index.hidden = intro.hidden = !!current;
    if (current) {
      window.scrollTo(0, 0);
      var h = current.querySelector('h2');
      h.setAttribute('tabindex', '-1');
      h.focus({ preventScroll: true });
      document.title = h.textContent + ' | Graphite SAT Tutoring';
    } else {
      document.title = 'Reading and Writing Lessons | Graphite SAT Tutoring';
    }
  }
  window.addEventListener('hashchange', show);
  show();

  page.addEventListener('click', function (e) {
    var btn = e.target.closest('.ls-check .choice');
    if (!btn || btn.disabled) return;
    var group = btn.parentNode;
    var answer = Number(group.getAttribute('data-answer'));
    var picked = Number(btn.getAttribute('data-choice'));
    var right = picked === answer;
    var buttons = group.querySelectorAll('.choice');
    btn.classList.add(right ? 'is-right' : 'is-wrong');
    btn.setAttribute('aria-pressed', 'true');
    if (right) {
      Array.prototype.forEach.call(buttons, function (b) { b.disabled = true; });
    } else {
      btn.disabled = true;
    }
    var fb = group.nextElementSibling;
    var verdict = fb.querySelector('.ls-verdict');
    verdict.textContent = right ? 'Right! ' + 'ABCD'[answer] + ' is the answer.' : 'Not quite. Try another choice, or open the explanation.';
    verdict.className = 'ls-verdict ' + (right ? 'is-right' : 'is-wrong');
    if (right) fb.querySelector('details').open = true;
  });
})();
