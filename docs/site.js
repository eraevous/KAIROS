/* Theme toggle and collapsible nav. No requests, no cookies.
   The theme choice is kept in localStorage only when the browser allows it;
   without JavaScript the site follows the system theme and the nav is always open. */
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');

  var KEY = 'kairos-theme';
  var order = ['auto', 'dark', 'light'];
  var NS = 'http://www.w3.org/2000/svg';
  // One small line icon per state: half-filled circle (auto), crescent (dark), sun (light).
  var icons = {
    auto: '<circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/>',
    dark: '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>',
    light: '<circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
  };

  function read() {
    try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* storage blocked; the page still works */ }
  }
  function apply(v) {
    if (order.indexOf(v) < 0) { v = 'auto'; }
    if (v === 'auto') { root.removeAttribute('data-theme'); }
    else { root.setAttribute('data-theme', v); }
    var b = document.querySelector('.theme-toggle');
    if (!b) { return; }
    var next = order[(order.indexOf(v) + 1) % order.length];
    var label = 'Theme: ' + v + ' (switch to ' + next + ')';
    b.setAttribute('aria-label', label);
    b.title = label;
    b.innerHTML = '';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    svg.innerHTML = icons[v];
    b.appendChild(svg);
  }

  apply(read());

  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = order[(order.indexOf(read()) + 1) % order.length];
      write(next);
      apply(next);
    });
  }

  var navBtn = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  if (navBtn && nav) {
    navBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        navBtn.setAttribute('aria-expanded', 'false');
        navBtn.focus();
      }
    });
  }
})();
