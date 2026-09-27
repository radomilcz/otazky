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
    + '<p class="napoveda">Klik nebo šipky · Esc stránku zavře.</p>'
    + '<div class="postup"><span></span></div>';
  document.body.appendChild(platno);

  var snimek = platno.querySelector('.snimek');
  var kde = platno.querySelector('.kde');
  var text = platno.querySelector('.text');
  var postup = platno.querySelector('.postup span');
  var konec = platno.querySelector('.konec');
  var kolikaty = 0;
  var otazek = snimky.length - 2;

  /* Písmo se nastavuje měřením, ne pevnou velikostí: krátká otázka má vyplnit plátno
     stejně jako dlouhá. Šířku řádku drží max-width v em, takže se sazba zvětšuje
     do obou stran zároveň a stačí hledat jedno číslo. */
  function napasuj() {
    var styl = getComputedStyle(platno);
    var sirka = platno.clientWidth - parseFloat(styl.paddingLeft) - parseFloat(styl.paddingRight);
    var vyska = platno.clientHeight - parseFloat(styl.paddingTop) - parseFloat(styl.paddingBottom);
    if (sirka < 40 || vyska < 40) { return; }        // plátno ještě nemá míru (skryté)
    // sazba nemá dosedat na okraje plátna; šířka se nekrátí – tu drží max-width
    // samotného textu a snímek by pak vycházel jako přetečený vždycky
    vyska *= 0.85;
    var dole = 14;
    var nahore = vyska / 1.8;
    var kolo = 0;
    while (kolo++ < 18 && nahore - dole > 0.6) {     // půlení intervalu: pár kol a přesně
      var stred = (dole + nahore) / 2;
      text.style.fontSize = stred + 'px';
      // scrollWidth/Height jsou celá čísla, míra plátna zlomková – bez rezervy
      // by zaokrouhlení nahoru vypadalo jako přetečení a písmo by se nezvětšilo
      if (snimek.scrollHeight > vyska + 1 || snimek.scrollWidth > sirka + 1) { nahore = stred; }
      else { dole = stred; }
    }
    text.style.fontSize = dole + 'px';
  }

  function vykresli() {
    var tenhle = snimky[kolikaty];
    kde.textContent = tenhle.kraj ? tenhle.kde : tenhle.kde + ' · ' + kolikaty + '/' + otazek;
    text.textContent = tenhle.text;
    platno.classList.toggle('kraj', !!tenhle.kraj);
    postup.style.width = (kolikaty / (snimky.length - 1) * 100) + '%';
    napasuj();
  }

  function posun(kam) {
    var novy = kolikaty + kam;
    if (novy < 0 || novy >= snimky.length) { return; }
    kolikaty = novy;
    vykresli();
  }

  function otevri() {
    kolikaty = 0;
    platno.hidden = false;                 // až pak vykreslit: skryté plátno nemá míru
    document.body.classList.add('promita');
    if (platno.requestFullscreen) { platno.requestFullscreen().catch(function () {}); }
    vykresli();
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
    else if (!platno.hidden) { setTimeout(napasuj, 120); }   // celá obrazovka mění míru
  });
  window.addEventListener('resize', function () { if (!platno.hidden) { napasuj(); } });

  var odkud = null;
  platno.addEventListener('touchstart', function (udalost) { odkud = udalost.changedTouches[0].clientX; });
  platno.addEventListener('touchend', function (udalost) {
    if (odkud === null) { return; }
    var posunuto = udalost.changedTouches[0].clientX - odkud;
    if (Math.abs(posunuto) > 60) { posun(posunuto < 0 ? 1 : -1); }
    odkud = null;
  });
});
