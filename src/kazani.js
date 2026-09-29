/* Video kázání se načítá až na kliknutí.
   Do té doby na stránce není nic od Googlu – žádný přehrávač, žádné skripty.
   Bez JS zůstává odkaz odkazem a otevře YouTube v novém panelu. */
document.addEventListener('DOMContentLoaded', function () {
  var odkaz = document.querySelector('.kazani .prehrat');
  if (!odkaz) { return; }
  odkaz.addEventListener('click', function (udalost) {
    udalost.preventDefault();
    var ramec = document.createElement('iframe');
    ramec.src = 'https://www.youtube-nocookie.com/embed/' + odkaz.dataset.video
      + '?autoplay=1&rel=0&hl=cs';
    ramec.title = 'Kázání na YouTube';
    ramec.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
    ramec.allowFullscreen = true;
    odkaz.replaceWith(ramec);
  });
});
