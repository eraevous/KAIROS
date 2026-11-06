/* Theme toggle and collapsible nav. No requests, no cookies.
   The theme choice is kept in localStorage only when the browser allows it. */
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');

  var KEY = 'kairos-theme';
  var order = ['auto', 'dark', 'light'];
  var labels = { auto: 'Theme: auto', dark: 'Theme: dark', light: 'Theme: light' };

  function read() {
    try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* storage blocked; the page still works */ }
  }
  function apply(v) {
    if (v === 'auto') { root.removeAttribute('data-theme'); }
    else { root.setAttribute('data-theme', v); }
    var b = document.querySelector('.theme-toggle');
    if (b) { b.textContent = labels[v]; }
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
  }
})();
