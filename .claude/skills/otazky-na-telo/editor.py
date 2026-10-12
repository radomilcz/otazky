"""Z vysázené stránky dílu udělá editovatelný náhled pro artefakt.

Použití: python3 .claude/skills/otazky-na-telo/editor.py <slug> <cílová složka>
Spouštěj z korene repa; <slug> je jméno složky v docs/, cíl patří do scratchpadu.
"""
import re, shutil, sys, os, pathlib

slug, cil = sys.argv[1], sys.argv[2]
zdroj = f'/home/user/otazky/docs/{slug}'

pathlib.Path(cil).mkdir(parents=True, exist_ok=True)
shutil.copy(f'{zdroj}/index.html', f'{cil}/index.html')
shutil.copy(f'{zdroj}/otazky-na-telo.pdf', f'{cil}/otazky-na-telo.pdf')
if not os.path.isdir(f'{cil}/assets'):
    shutil.copytree('/home/user/otazky/docs/assets', f'{cil}/assets')

s = open(f'{cil}/index.html', encoding='utf-8').read()

# --- cesty na náhled ---
s = s.replace('"/assets/', '"assets/').replace('url(/assets/', 'url(assets/')
s = re.sub(r'href="/(?!/)', 'href="https://otazky.cirkevjakokrava.cz/', s)
s = s.replace(f'href="https://otazky.cirkevjakokrava.cz/{slug}/otazky-na-telo.pdf"',
              'href="otazky-na-telo.pdf"')

# --- klíče na položky: b<blok>q<poradi> ---
blok = [0]
def oznac_blok(m):
    blok[0] += 1
    return m.group(0)

casti = re.split(r'(<section class="block">)', s)
ven, b = [casti[0]], 0
for i in range(1, len(casti), 2):
    b += 1
    telo, q = casti[i + 1], [0]
    def oznac(m):
        q[0] += 1
        return f'<li data-k="b{b}q{q[0]}">{m.group(1)}</li>'
    telo = re.sub(r'<li>(.*?)</li>', oznac, telo, flags=re.S)
    ven.append(casti[i]); ven.append(telo)
s = ''.join(ven)

STYL = '''
<style id="editace">
  .psani { max-width: 48rem; margin: 0 auto 1.5rem; padding: .7rem .9rem;
    border: 1px solid currentColor; border-radius: .4rem; font-size: .85rem;
    line-height: 1.45; opacity: .85; }
  .psani b { font-weight: 600; }
  .psani .stav { opacity: .7; }
  li[contenteditable] { outline: none; border-radius: .2rem;
    transition: background-color .15s; }
  li[contenteditable]:hover { background: rgba(127,127,127,.09); }
  li[contenteditable]:focus { background: rgba(127,127,127,.14);
    box-shadow: 0 0 0 2px rgba(127,127,127,.35); }
  li.zmeneno { border-left: 3px solid currentColor; padding-left: .45rem;
    margin-left: -.48rem; }
  .zpet { display: none; margin-left: .4rem; font-size: .72rem;
    background: none; border: 1px solid currentColor; border-radius: .25rem;
    padding: 0 .3rem; cursor: pointer; opacity: .6; font-family: inherit; }
  li.zmeneno .zpet { display: inline-block; }
  .zpet:hover { opacity: 1; }
  .poznamka { max-width: 48rem; margin: 0 auto 2rem; }
  .poznamka label { display: block; font-size: .8rem; opacity: .7;
    margin-bottom: .3rem; }
  .poznamka textarea { width: 100%; min-height: 4.5rem; font: inherit;
    font-size: .9rem; padding: .5rem .6rem; border: 1px solid currentColor;
    border-radius: .4rem; background: transparent; color: inherit; }
  @media print {
    .psani, .poznamka, .zpet { display: none !important; }
    li.zmeneno { border-left: 0; padding-left: 0; margin-left: 0; }
  }
</style>
'''

SKRIPT = '''
<script>
(function () {
  var polozky = [].slice.call(document.querySelectorAll('li[data-k]'));
  var puvodni = {};
  polozky.forEach(function (li) { puvodni[li.dataset.k] = li.textContent.trim(); });

  var pas = document.createElement('div');
  pas.className = 'psani';
  pas.innerHTML = '<b>Načítám…</b>';
  var cols = document.querySelector('.cols');
  cols.parentNode.insertBefore(pas, cols);

  function hlaska(html) { pas.innerHTML = html; }
  function stav(t) {
    var e = pas.querySelector('.stav');
    if (e) e.textContent = t;
  }

  function nastav(li, text, jeZmena) {
    var tl = li.querySelector('.zpet');
    li.textContent = text;
    if (tl) li.appendChild(tl);
    li.classList.toggle('zmeneno', !!jeZmena);
  }

  claude.use('db').then(function (db) {
    if (!db) {
      hlaska('<b>Jen ke čtení.</b> Tenhle náhled teď neumí ukládat změny — ' +
             'pošli úpravy do chatu jako dřív.');
      return;
    }
    var kolekce = db.collection('upravy');
    var zapisuje = {};

    hlaska('<b>Piš přímo do listu.</b> Klikni do kterékoli otázky a přepiš ji. ' +
           'Změněné položky poznáš podle svislé linky a dají se vrátit. ' +
           'Claude si tvoje úpravy přečte odsud. ' +
           '<span class="stav"></span>');

    polozky.forEach(function (li) {
      var k = li.dataset.k;
      var tl = document.createElement('button');
      tl.type = 'button';
      tl.className = 'zpet';
      tl.textContent = 'vrátit';
      tl.addEventListener('click', function (ev) {
        ev.preventDefault();
        nastav(li, puvodni[k], false);
        kolekce.doc(k).delete().then(function () { stav('vráceno'); },
                                     function () { stav('vrátit se nepovedlo'); });
      });
      li.appendChild(tl);

      li.setAttribute('contenteditable', 'plaintext-only');
      li.setAttribute('spellcheck', 'true');

      li.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter') { ev.preventDefault(); li.blur(); }
        if (ev.key === 'Escape') { nastav(li, puvodni[k], li.classList.contains('zmeneno')); li.blur(); }
      });

      li.addEventListener('blur', function () {
        var text = li.textContent.replace(/vrátit$/, '').trim();
        if (!text) { nastav(li, puvodni[k], li.classList.contains('zmeneno')); return; }
        if (text === puvodni[k]) {
          if (!li.classList.contains('zmeneno')) return;
          nastav(li, text, false);
          kolekce.doc(k).delete().then(function () { stav('vráceno na původní'); });
          return;
        }
        if (zapisuje[k]) return;
        zapisuje[k] = true;
        nastav(li, text, true);
        stav('ukládám…');
        kolekce.doc(k).set({ text: text, puvodni: puvodni[k], kdy: new Date().toISOString() })
          .then(function () { stav('uloženo'); },
                function (e) { stav('neuložilo se: ' + (e && e.code || 'chyba')); })
          .then(function () { zapisuje[k] = false; });
      });
    });

    kolekce.onSnapshot(function (snap) {
      snap.docs.forEach(function (d) {
        var li = document.querySelector('li[data-k="' + d.id + '"]');
        if (!li || li === document.activeElement) return;
        var t = (d.data() || {}).text;
        if (typeof t === 'string' && t !== li.textContent.replace(/vrátit$/, '').trim()) {
          nastav(li, t, t !== puvodni[d.id]);
        }
      });
    }, function (e) { stav('spojení se ztratilo (' + e.code + ')'); });

    // volná poznámka pro cokoli, co se do položek nevejde
    var box = document.createElement('div');
    box.className = 'poznamka';
    box.innerHTML = '<label for="pozn">Vzkaz pro Clauda — co na listu chybí, ' +
                    'co vyhodit, co jinak</label><textarea id="pozn"></textarea>';
    var foot = document.querySelector('.foot');
    foot.parentNode.insertBefore(box, foot);
    var ta = box.querySelector('textarea');
    var ref = db.doc('vzkaz/text');
    ref.get().then(function (d) {
      if (d.exists && typeof (d.data() || {}).text === 'string') ta.value = d.data().text;
    });
    ta.addEventListener('blur', function () {
      ref.set({ text: ta.value, kdy: new Date().toISOString() })
        .then(function () { stav('vzkaz uložen'); },
              function () { stav('vzkaz se neuložil'); });
    });
  });
})();
</script>
'''

s = s.replace('</head>', STYL + '</head>', 1)
s = s.replace('</body>', SKRIPT + '</body>', 1)
open(f'{cil}/index.html', 'w', encoding='utf-8').write(s)

print('položek s klíčem:', len(re.findall(r'<li data-k="', s)))
print('styl:', '<style id="editace">' in s, '| skript:', "claude.use('db')" in s)
