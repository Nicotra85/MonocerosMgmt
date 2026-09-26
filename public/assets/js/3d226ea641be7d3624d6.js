/* Initialize text motion after the page content. */
(() => {
  'use strict';

  function initialize() {
    const page = document.documentElement;
    if (page.dataset.longmerTextMotion === 'ready') return;
    page.dataset.longmerTextMotion = 'ready';
    if (!('IntersectionObserver' in window) || !window.matchMedia) return;

    const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (preference.matches) return;

    let observer;
    const active = new Set();
    const clear = (element) => {
      element.classList.remove('lm-text-enter');
      active.delete(element);
    };

    try {
      observer = new IntersectionObserver((entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const element = entry.target;
          observer.unobserve(element);
          if (preference.matches) continue;
          active.add(element);
          element.classList.add('lm-text-enter');
          element.addEventListener('animationend', () => clear(element), { once: true });
          // Also restore the ordinary style if another stylesheet cancels animation.
          window.setTimeout(() => clear(element), 800);
        }
      }, { threshold: 0, rootMargin: '0px 0px 24px 0px' });

      const candidates = document.querySelectorAll(
        'main h1, main h2, main h3, #longmer-signature h2, #longmer-signature h3, ' +
        '.overline, .eyebrow, .lead, .article-meta'
      );
      for (const element of candidates) {
        // The approved logo hero already animates its own text. Leave it intact.
        if (element.closest('#lm-drawn, [aria-live], [hidden]')) continue;
        if (window.getComputedStyle(element).animationName !== 'none') continue;
        observer.observe(element);
      }

      const reduceMotion = () => {
        if (!preference.matches) return;
        observer.disconnect();
        active.forEach(clear);
      };
      if (preference.addEventListener) preference.addEventListener('change', reduceMotion);
      else if (preference.addListener) preference.addListener(reduceMotion);
      window.addEventListener('pagehide', () => {
        observer.disconnect();
        active.forEach(clear);
      }, { once: true });
    } catch (_) {
      if (observer) observer.disconnect();
      active.forEach(clear);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }
})();
