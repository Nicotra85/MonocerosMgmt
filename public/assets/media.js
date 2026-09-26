(() => {
  function initializeMedia() {
    document.querySelectorAll('video').forEach(video => {
      video.muted = true;
      video.defaultMuted = true;
      video.autoplay = true;
      video.loop = true;
      video.playsInline = true;
      video.controls = false;
      ['muted','autoplay','loop','playsinline'].forEach(attribute => video.setAttribute(attribute, ''));
      const play = () => { const attempt = video.play(); if (attempt) attempt.catch(() => {}); };
      video.addEventListener('loadeddata', play);
      video.addEventListener('canplay', play);
      window.addEventListener('pageshow', play);
      document.addEventListener('visibilitychange', () => { if (!document.hidden) play(); });
      document.addEventListener('pointerdown', play, {once: true});
      play();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initializeMedia, {once: true});
  else initializeMedia();
})();
