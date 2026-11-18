/* Theme toggle and collapsible nav. No requests, no cookies.
   The active theme is held in memory for this page; it is also saved to localStorage when the
   browser allows it, so it survives navigation. When storage is blocked every click still cycles
   auto -> dark -> light, it just isn't remembered on the next page.
   Without JavaScript the site follows the system theme and the nav is always open. */
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

  function load() {
    try {
      var v = localStorage.getItem(KEY);
      return order.indexOf(v) >= 0 ? v : 'auto';
    } catch (e) { return 'auto'; }
  }
  function save(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* storage blocked; the in-memory value still works */ }
  }

  // The single source of truth while the page is open.
  var current = load();

  function apply() {
    if (current === 'auto') { root.removeAttribute('data-theme'); }
    else { root.setAttribute('data-theme', current); }
    var b = document.querySelector('.theme-toggle');
    if (!b) { return; }
    var next = order[(order.indexOf(current) + 1) % order.length];
    var label = 'Theme: ' + current + ' (switch to ' + next + ')';
    b.setAttribute('aria-label', label);
    b.title = label;
    b.innerHTML = '';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    svg.innerHTML = icons[current];
    b.appendChild(svg);
  }

  apply();

  var themeBtn = document.querySelector('.theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      current = order[(order.indexOf(current) + 1) % order.length];
      save(current);
      apply();
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
