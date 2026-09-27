/* Promítání: každá otázka je jeden snímek.
   Snímky se neskládají do HTML předem – čtou se z bloků na stránce, takže
   promítání ukazuje přesně to, co je na listu, a nemá se s čím rozejít.
   Ovládá se klikem, šipkami, mezerou a přejetím prstu; Esc zavírá. Celá
   obrazovka je bonus: kde ji prohlížeč nedá (iPhone), přeleze plátno přes
   okno a promítá se dál. */
document.addEventListener('DOMContentLoaded', function () {
  var spoust = document.querySelector('.promitat');
  var bloky = document.querySelectorAll('.block');
  if (!spoust || !bloky.length) { return; }

  var snimky = [];
  var dil = document.querySelector('.dil');
  var lead = document.querySelector('.lead');
  snimky.push({
    kde: dil ? dil.firstChild.textContent.trim() : 'otázky na tělo',
    text: lead ? lead.firstChild.textContent.trim() : '',
    kraj: true
  });
  Array.prototype.forEach.call(bloky, function (blok) {
    var nazev = blok.querySelector('h2').firstChild.textContent.trim();
    Array.prototype.forEach.call(blok.querySelectorAll('li'), function (otazka) {
      snimky.push({ kde: nazev, text: otazka.textContent.trim() });
    });
  });
  snimky.push({ kde: 'církev jako kráva', text: 'otazky.cirkevjakokrava.cz', kraj: true });

  var platno = document.createElement('div');
  platno.className = 'promitani';
  platno.hidden = true;
  platno.innerHTML = '<div class="snimek"><p class="kde"></p><p class="text"></p></div>'
    + '<button class="konec" type="button" aria-label="Zavřít promítání">✕</button>'
    + '<p class="napoveda">klikni nebo šipky · Esc zavře</p>'
    + '<div class="postup"><span></span></div>';
  document.body.appendChild(platno);

  var kde = platno.querySelector('.kde');
  var text = platno.querySelector('.text');
  var postup = platno.querySelector('.postup span');
  var konec = platno.querySelector('.konec');
  var kolikaty = 0;
  var otazek = snimky.length - 2;

  function vykresli() {
    var snimek = snimky[kolikaty];
    kde.textContent = snimek.kraj ? snimek.kde : snimek.kde + ' · ' + kolikaty + '/' + otazek;
    text.textContent = snimek.text;
    platno.classList.toggle('kraj', !!snimek.kraj);
    postup.style.width = (kolikaty / (snimky.length - 1) * 100) + '%';
  }

  function posun(kam) {
    var novy = kolikaty + kam;
    if (novy < 0 || novy >= snimky.length) { return; }
    kolikaty = novy;
    vykresli();
  }

  function otevri() {
    kolikaty = 0;
    vykresli();
    platno.hidden = false;
    document.body.classList.add('promita');
    if (platno.requestFullscreen) { platno.requestFullscreen().catch(function () {}); }
    konec.focus();
  }

  function zavri() {
    platno.hidden = true;
    document.body.classList.remove('promita');
    if (document.fullscreenElement && document.exitFullscreen) { document.exitFullscreen(); }
    spoust.focus();
  }

  spoust.addEventListener('click', otevri);
  konec.addEventListener('click', function (udalost) { udalost.stopPropagation(); zavri(); });
  platno.addEventListener('click', function (udalost) {
    posun(udalost.clientX < window.innerWidth / 3 ? -1 : 1);
  });
  document.addEventListener('keydown', function (udalost) {
    if (platno.hidden) { return; }
    if (udalost.key === 'Escape') { zavri(); return; }
    if (udalost.key === 'ArrowLeft' || udalost.key === 'PageUp') { posun(-1); return; }
    if (udalost.key === 'ArrowRight' || udalost.key === 'PageDown' || udalost.key === ' ') {
      udalost.preventDefault();
      posun(1);
    }
  });
  document.addEventListener('fullscreenchange', function () {
    if (!document.fullscreenElement && !platno.hidden) { zavri(); }
  });

  var odkud = null;
  platno.addEventListener('touchstart', function (udalost) { odkud = udalost.changedTouches[0].clientX; });
  platno.addEventListener('touchend', function (udalost) {
    if (odkud === null) { return; }
    var posunuto = udalost.changedTouches[0].clientX - odkud;
    if (Math.abs(posunuto) > 60) { posun(posunuto < 0 ? 1 : -1); }
    odkud = null;
  });
});
