#!/usr/bin/env python3
"""Sestaví stránku otazky.cirkevjakokrava.cz ze src/.

Výstup: docs/ (GitHub Pages)
  index.html                 aktuální díl (kopie, kanonicky odkazuje na jeho adresu)
  <díl>/index.html           každý díl na vlastní adrese
  <díl>/otazky-na-telo.pdf   A4 toho dílu
  dily/index.html            rozcestník – všechny díly po sériích
  otazky-na-telo.pdf         A4 aktuálního dílu (stálá adresa pro sdílení)
  assets/                    fonty, ikony, náhled sdílení

Jeden díl = jeden soubor v src/otazky/. Název souboru je adresa. Z hlavičky
souboru se bere titul, série, datum a citát, ze zbytku bloky otázek. Z téhož
zdroje se sází web i A4: tisková podoba stránky je v šabloně jako @media print
a PDF je její výtisk, takže se leták a web nemůžou rozejít.

Aktuální je nejnovější díl, jehož datum není v budoucnu – ten sedí na kořeni
domény. Rozepsaný díl drž mimo web řádkem „koncept: ano“ v hlavičce;
--koncepty ho do sestavení pustí (na prohlédnutí, ne na push).

Placeholdery v šabloně:
  {{SITE}} {{KANONICKA}}         adresa webu a tohohle dílu (absolutní odkazy)
  {{SADA}} {{SERIE}}             popis dílu do titulku a hlavičky
  {{CITAT}} {{ZDROJ}}            citát nad otázkami
  {{PREPINAC}}                   rozbalovací seznam dílů
  {{BLOKY}}                      bloky otázek
  {{BLOB_PATHS}}                 křivky otisku (src/assets/otisk-paths.txt)
  {{PDF}}                        odkaz na A4 tohohle dílu
  {{F_GRANDHEAVY}} {{F_REGULAR}} {{F_NARROWBLACK}} {{F_GRAND}}   fonty (src/fonts/*.woff)

Použití:  python3 build.py
Volitelně:
  python3 build.py --pdf         vysází A4 každého dílu (pip install playwright)
  python3 build.py --og          přegeneruje náhled sdílení (pip install playwright pillow)
  python3 build.py --koncepty    přibere i díly označené jako koncept
"""
import argparse, datetime, functools, html, http.server, os, re, shutil, socketserver, sys, threading

SITE = 'https://otazky.cirkevjakokrava.cz'   # doména z docs/CNAME – sdílené odkazy musí být absolutní

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
SADY = os.path.join(SRC, 'otazky')
DOCS = os.path.join(ROOT, 'docs')
PDF = 'otazky-na-telo.pdf'

FONTS = {
    '{{F_GRANDHEAVY}}': 'Agrandir-GrandHeavy.woff',
    '{{F_REGULAR}}': 'Agrandir-Regular.woff',
    '{{F_NARROWBLACK}}': 'Agrandir-NarrowBlack.woff',
    '{{F_GRAND}}': 'Agrandir-Grand.woff',
}
# ikony a náhled sdílení – hotové soubory, jen se kopírují (og.jpg dělá --og)
STATIC = ('favicon.svg', 'favicon-32.png', 'icon-180.png', 'og.jpg')

# jednopísmenné předložky a spojky nesmí zůstat na konci řádku (česká sazba)
PREDLOZKY = re.compile(r'(^|[\s„“(>])([KkSsVvZzOoUuAaIi])\s+')

MESICE = ('ledna', 'února', 'března', 'dubna', 'května', 'června',
          'července', 'srpna', 'září', 'října', 'listopadu', 'prosince')

CITAT = 'Přežvykujeme, dokud je nevstřebáme celé. Od pondělí do neděle. V práci, doma i ve škole. Nejen v kostele.'
ZDROJ = 'manifest · kultura'


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def zapis(cesta, text):
    with open(cesta, 'w', encoding='utf-8') as f:
        f.write(text)


def nbsp(text):
    """Přilepí jednopísmenná slova k následujícímu – jen v textu, ne uvnitř značek."""
    out = []
    for part in re.split(r'(<[^>]+>)', text):
        out.append(part if part.startswith('<') else PREDLOZKY.sub('\\1\\2 ', part))
    return ''.join(out)


def otisk():
    """Křivky otisku z src/assets/otisk-paths.txt slepené do <path> elementů."""
    paths = [l.strip() for l in read(os.path.join(SRC, 'assets', 'otisk-paths.txt')).splitlines() if l.strip()]
    return ''.join(f'<path d="{d}"/>' for d in paths)


# ---------- díly ----------

KLIC = re.compile(r'^[a-zěščřžýáíéúůďťň]+:\s')


class Dil:
    """Jeden díl: hlavička a bloky otázek."""

    def __init__(self, cesta):
        self.slug = os.path.splitext(os.path.basename(cesta))[0]
        self.hlavicka, self.bloky = self._rozeber(read(cesta))
        chybi = [k for k in ('titul', 'datum') if k not in self.hlavicka]
        if chybi:
            sys.exit(f'{self.slug}: v hlavičce chybí {", ".join(chybi)}')
        try:
            self.datum = datetime.date.fromisoformat(self.hlavicka['datum'])
        except ValueError:
            sys.exit(f'{self.slug}: datum musí být ve tvaru 2026-09-20')
        if not self.bloky:
            sys.exit(f'{self.slug}: žádné bloky otázek')

    @staticmethod
    def _rozeber(text):
        hlavicka, bloky, blok, v_hlavicce = {}, [], None, True
        for radek in text.splitlines():
            radek = radek.strip()
            if radek.startswith('#'):
                continue
            if not radek:
                blok = None                      # prázdný řádek ukončuje blok
                continue
            if v_hlavicce and KLIC.match(radek + ' '):
                klic, _, hodnota = radek.partition(':')
                hlavicka[klic.strip()] = hodnota.strip()
                continue
            v_hlavicce = False                   # první nadpis bloku hlavičku zavře
            if radek.startswith('- '):
                if blok is None:
                    sys.exit('Otázka bez bloku: ' + radek)
                blok[1].append(radek[2:])
            else:
                blok = (radek, [])
                bloky.append(blok)
        return hlavicka, bloky

    @property
    def koncept(self):
        return self.hlavicka.get('koncept', '').lower() in ('ano', 'true', '1')

    @property
    def nazev(self):
        """Jak se díl jmenuje v přepínači a v hlavičce: „26. Buď otevřený“."""
        cislo = self.hlavicka.get('dil', '')
        return f'{cislo}. {self.hlavicka["titul"]}' if cislo else self.hlavicka['titul']

    @property
    def serie(self):
        return self.hlavicka.get('serie', '')

    @property
    def kdy(self):
        return f'{self.datum.day}. {MESICE[self.datum.month - 1]} {self.datum.year}'

    def html_bloky(self):
        """Bloky do dvou sloupců.

        Sloupce jsou dva kvůli A4 – na úzkém displeji se z nich stejně stane
        jeden proud, takže pořadí bloků v souboru je zároveň pořadí čtení.
        """
        def sekce(i, nazev, otazky):
            li = '\n'.join(f'          <li>{html.escape(o)}</li>' for o in otazky)
            return ('      <section class="block">\n'
                    f'        <h2>{html.escape(nazev)} <span class="n">{i}/{len(self.bloky)}</span></h2>\n'
                    f'        <ul>\n{li}\n        </ul>\n'
                    '      </section>')

        pul = (len(self.bloky) + 1) // 2
        ven, i = ['  <div class="cols">'], 0
        for sloupec in (self.bloky[:pul], self.bloky[pul:]):
            ven.append('    <div class="col">')
            for nazev, otazky in sloupec:
                i += 1
                ven.append(sekce(i, nazev, otazky))
            ven.append('    </div>')
        ven.append('  </div>')
        return '\n'.join(ven)


def nacti_dily(koncepty=False):
    """Díly od nejnovějšího. Koncepty se na web nedostanou, dokud si je nevyžádáš."""
    if not os.path.isdir(SADY):
        sys.exit('Chybí složka src/otazky s díly.')
    dily = [Dil(os.path.join(SADY, f)) for f in sorted(os.listdir(SADY)) if f.endswith('.txt')]
    dily = [d for d in dily if koncepty or not d.koncept]
    if not dily:
        sys.exit('Žádný díl k sestavení.')
    return sorted(dily, key=lambda d: d.datum, reverse=True)


def aktualni(dily):
    """Nejnovější díl, jehož datum není v budoucnu – ten sedí na kořeni domény."""
    dnes = datetime.date.today()
    return next((d for d in dily if d.datum <= dnes), dily[-1])


POSLEDNI = 4        # kolik dílů ukázat rovnou v hlavičce, než se odkáže na rozcestník


def prepinac(dily, tenhle):
    """Poslední díly po ruce, zbytek na rozcestníku.

    Rozbalit v hlavičce celý archiv nedává smysl – po dvacátém dílu by z toho
    byla tapeta. Nabídne se pár posledních a odkaz na /dily/.
    """
    if len(dily) == 1:
        return f'  <p class="prepinac sam">{html.escape(tenhle.nazev)}</p>'
    blizke = [d for d in dily if d.slug != tenhle.slug][:POSLEDNI]
    polozky = [f'      <li><a href="/{d.slug}/">{html.escape(d.nazev)}'
               f'<span class="kdy">{d.kdy}</span></a></li>' for d in blizke]
    polozky.append(f'      <li class="vsechny"><a href="/dily/">Všechny série '
                   f'<span class="kdy">{len(dily)}</span></a></li>')
    return ('  <details class="prepinac">\n'
            f'    <summary><span class="stitek">díl</span> {html.escape(tenhle.nazev)}</summary>\n'
            '    <ul>\n' + '\n'.join(polozky) + '\n    </ul>\n'
            '  </details>')


def archiv(dily):
    """Rozcestník „Všechny série“: díly seskupené po sériích, od nejnovějšího."""
    ven, serie = ['  <div class="archiv">'], object()
    for d in dily:
        if d.serie != serie:
            if serie is not object():
                ven.append('    </ul>\n    </section>')
            serie = d.serie
            ven.append('    <section class="rada">')
            ven.append(f'      <h2>{html.escape(serie or "Mimo sérii")}</h2>')
            ven.append('    <ul>')
        ven.append(f'      <li><a class="list" href="/{d.slug}/">'
                   f'<span class="nazev">{html.escape(d.nazev)}</span>'
                   f'<span class="kdy">{d.kdy}</span></a>'
                   f'<a class="a4" href="/{d.slug}/{PDF}">A4</a></li>')
    ven.append('    </ul>\n    </section>')
    ven.append('  </div>')
    return '\n'.join(ven)


def stranka(sablona, dil, dily, kanonicka):
    text = (sablona
            .replace('{{BLOB_PATHS}}', otisk())
            .replace('{{BLOKY}}', dil.html_bloky())
            .replace('{{PREPINAC}}', prepinac(dily, dil))
            .replace('{{SADA}}', html.escape(dil.nazev))
            .replace('{{SERIE}}', html.escape(dil.serie or 'pastva'))
            .replace('{{CITAT}}', html.escape(dil.hlavicka.get('citat', CITAT)))
            .replace('{{ZDROJ}}', html.escape(dil.hlavicka.get('zdroj', ZDROJ)))
            .replace('{{PDF}}', f'/{dil.slug}/{PDF}')
            .replace('{{KANONICKA}}', kanonicka)
            .replace('{{SITE}}', SITE))
    check(text)
    return nbsp(text)


def uklid(dily):
    """Smaže složky dílů, které ze zdrojů zmizely (nebo se staly konceptem)."""
    zive = {d.slug for d in dily}
    for jmeno in os.listdir(DOCS):
        cesta = os.path.join(DOCS, jmeno)
        if os.path.isdir(cesta) and jmeno not in ('assets', 'dily') and jmeno not in zive:
            shutil.rmtree(cesta)
            print('smazáno:', jmeno)


def build(koncepty=False):
    sablona = read(os.path.join(SRC, 'index.template.html'))
    sablona_dily = read(os.path.join(SRC, 'dily.template.html'))
    styl = read(os.path.join(SRC, 'styl.css'))
    dily = nacti_dily(koncepty)
    ted = aktualni(dily)

    assets = os.path.join(DOCS, 'assets')
    os.makedirs(os.path.join(assets, 'fonts'), exist_ok=True)
    for key, name in FONTS.items():
        shutil.copy(os.path.join(SRC, 'fonts', name), os.path.join(assets, 'fonts', name))
        styl = styl.replace(key, '/assets/fonts/' + name)
        sablona = sablona.replace(key, '/assets/fonts/' + name)
        sablona_dily = sablona_dily.replace(key, '/assets/fonts/' + name)
    sablona = sablona.replace('{{STYL}}', styl)
    sablona_dily = sablona_dily.replace('{{STYL}}', styl)
    for name in STATIC:
        zdroj = os.path.join(SRC, 'assets', name)
        if os.path.exists(zdroj):          # og.jpg vzniká až z hotové stránky, viz --og
            shutil.copy(zdroj, os.path.join(assets, name))

    uklid(dily)
    for dil in dily:
        slozka = os.path.join(DOCS, dil.slug)
        os.makedirs(slozka, exist_ok=True)
        zapis(os.path.join(slozka, 'index.html'), stranka(sablona, dil, dily, f'{SITE}/{dil.slug}/'))
    # kořen domény je kopie aktuálního dílu; kanonická adresa vede na jeho vlastní,
    # ať se dvě stejné stránky nepřetahují o to, která je ta pravá
    zapis(os.path.join(DOCS, 'index.html'), stranka(sablona, ted, dily, f'{SITE}/{ted.slug}/'))

    os.makedirs(os.path.join(DOCS, 'dily'), exist_ok=True)
    pocet = f'{len(dily)} díl' + ('' if len(dily) == 1 else 'y' if len(dily) < 5 else 'ů')
    rozcestnik = (sablona_dily.replace('{{BLOB_PATHS}}', otisk())
                              .replace('{{ARCHIV}}', archiv(dily))
                              .replace('{{POCET}}', pocet)
                              .replace('{{SITE}}', SITE))
    check(rozcestnik)
    zapis(os.path.join(DOCS, 'dily', 'index.html'), nbsp(rozcestnik))
    print('díly:', ', '.join(d.slug + (' ← na kořeni' if d is ted else '') for d in dily))
    return dily, ted


# ---------- PDF a náhled sdílení ----------

def chromium(pw):
    """Prohlížeč pro renderování. CHROME_PATH ukáže na vlastní Chromium, když ho playwright nemá svůj."""
    exe = os.environ.get('CHROME_PATH')
    return pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()


class Server(socketserver.TCPServer):
    allow_reuse_address = True


def serve():
    """Rozjede docs/ na localhostu a vrátí (adresa, vypni).

    Přes file:// Chromium fonty nenačte a odkazy od kořene (/assets/…) by
    nikam nevedly, takže i lokální render jede přes HTTP.
    """
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DOCS)
    httpd = Server(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{httpd.server_address[1]}/', httpd.shutdown


def make_pdf(dily, ted):
    """Vytiskne A4 každého dílu (vyžaduje playwright).

    Tiskne se to, co je v šabloně pod @media print – co vyjede tady, vyjede
    návštěvníkovi i z Ctrl+P.
    """
    from playwright.sync_api import sync_playwright
    url, vypni = serve()
    with sync_playwright() as pw:
        br = chromium(pw)
        page = br.new_page()
        for dil in dily:
            out = os.path.join(DOCS, dil.slug, PDF)
            page.goto(f'{url}{dil.slug}/')
            page.wait_for_function('document.fonts.status === "loaded"')
            page.pdf(path=out, format='A4', print_background=True,
                     margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
            print(f'{dil.slug}/{PDF}:', f'{os.path.getsize(out) / 1024:.0f} kB')
        br.close()
    vypni()
    # stálá adresa /otazky-na-telo.pdf vede vždy na aktuální díl
    shutil.copy(os.path.join(DOCS, ted.slug, PDF), os.path.join(DOCS, PDF))


def make_og():
    """Vyfotí hlavičku stránky do src/assets/og.jpg 1200×630 (vyžaduje playwright a pillow).

    Náhled tak vypadá přesně jako web – stejné písmo, stejný otisk, žádná ruční sazba.
    """
    from playwright.sync_api import sync_playwright
    from PIL import Image
    if not os.path.exists(os.path.join(DOCS, 'index.html')):
        sys.exit('Nejdřív spusť build – náhled se fotí z docs/index.html.')
    url, vypni = serve()
    png = os.path.join(SRC, 'assets', 'og.png')
    with sync_playwright() as pw:
        br = chromium(pw)
        page = br.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=2)
        page.goto(url)
        page.wait_for_function('document.fonts.status === "loaded"')
        page.add_style_tag(content='.tools,.prepinac{display:none}')   # ovládání do náhledu nepatří
        page.screenshot(path=png)
        br.close()
    vypni()
    im = Image.open(png).convert('RGB').resize((1200, 630), Image.LANCZOS)
    im.save(os.path.join(SRC, 'assets', 'og.jpg'), 'JPEG', quality=82, optimize=True, progressive=True)
    os.remove(png)
    print('og.jpg: 1200×630')


def check(text):
    m = re.search(r'\{\{[A-Z_]+\}\}', text)
    if m:
        sys.exit('V šabloně zůstal nenahrazený placeholder: ' + m.group(0))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdf', action='store_true', help='vysází A4 každého dílu')
    ap.add_argument('--og', action='store_true', help='přegeneruje náhled sdílení')
    ap.add_argument('--koncepty', action='store_true', help='přibere i rozepsané díly')
    a = ap.parse_args()
    dily, ted = build(a.koncepty)
    if a.og:
        make_og()                        # fotí se z hotové stránky, proto až po buildu
        dily, ted = build(a.koncepty)    # a znovu, ať se nový náhled zkopíruje do docs/
    if a.pdf:
        make_pdf(dily, ted)
