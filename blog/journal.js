/* The Journal — small, dependency-free interactions. */
(function () {
  // Category filtering on the index grid.
  var filters = document.querySelectorAll('[data-filter]');
  var cards = document.querySelectorAll('[data-cat]');
  if (filters.length && cards.length) {
    filters.forEach(function (f) {
      f.addEventListener('click', function () {
        var cat = f.getAttribute('data-filter');
        filters.forEach(function (x) { x.classList.toggle('on', x === f); });
        cards.forEach(function (c) {
          var show = cat === 'all' || c.getAttribute('data-cat') === cat;
          c.classList.toggle('hide', !show);
        });
      });
    });
  }

  // Scroll-reveal — mirrors the main site.
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }
})();
