"""Zkontroluje vysázený list: jedna strana PDF a obsah nenarazí do patky.

    python3 .claude/skills/otazky-na-telo/mereni.py 08-jmeno-ktere-neses
    python3 .claude/skills/otazky-na-telo/mereni.py            # všechny díly v docs/

Předpokládá, že už proběhlo `build.py --koncepty --pdf` s CHROME_PATH.
Platí dvě věci, nic víc: PDF má jednu stranu a spodní okraj je aspoň 45 px
(12 mm) — pod tím to netiskne každá tiskárna. Čísla sloupců jsou potrubí,
autorovi se nehlásí.
"""
import functools, glob, http.server, os, sys, threading

PORT = 8977
KOREN = 'docs'
OKRAJ_MIN = 45


def stran(pdf):
    d = open(pdf, 'rb').read()
    return d.count(b'/Type /Page') - d.count(b'/Type /Pages')


def mer(slugy):
    from playwright.sync_api import sync_playwright
    exe = os.environ.get('CHROME_PATH')
    ven = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        pg = b.new_page(viewport={'width': 794, 'height': 1123})
        for slug in slugy:
            pg.goto(f'http://127.0.0.1:{PORT}/{slug}/')
            pg.emulate_media(media='print')
            pg.wait_for_timeout(250)
            ven.append((slug, pg.evaluate("""() => {
              const bl = [...document.querySelectorAll('.block')].map(b => ({
                blok: b.querySelector('h2,h3')?.textContent.trim(),
                levy: Math.round(b.getBoundingClientRect().left),
                dole: Math.round(b.getBoundingClientRect().bottom)}));
              const f = document.querySelector('.foot').getBoundingClientRect();
              return {bloky: bl, okraj: Math.round(1123 - f.bottom)};
            }""")))
        b.close()
    return ven


def main():
    if not os.path.isdir(KOREN):
        sys.exit('spusť to z korene repa (chybí docs/)')
    if len(sys.argv) > 1:
        slugy = sys.argv[1:]
    else:
        slugy = sorted(os.path.basename(os.path.dirname(p))
                       for p in glob.glob(f'{KOREN}/*/otazky-na-telo.pdf'))
    if not slugy:
        sys.exit('v docs/ nejsou žádné díly — proběhl build?')

    os.chdir(KOREN)
    class Tichy(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(('127.0.0.1', PORT),
                                          functools.partial(Tichy))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        vysledky = mer(slugy)
    finally:
        srv.shutdown()

    spadlo = []
    for slug, m in vysledky:
        n = stran(f'{slug}/otazky-na-telo.pdf')
        sloupce = {}
        for b in m['bloky']:
            sloupce[b['levy']] = max(sloupce.get(b['levy'], 0), b['dole'])
        potrubi = ' / '.join(str(v) for _, v in sorted(sloupce.items()))
        chyby = []
        if n != 1:
            chyby.append(f'{n} stran')
        if m['okraj'] < OKRAJ_MIN:
            chyby.append(f"okraj {m['okraj']} px")
        stav = 'ROZBITÉ: ' + ', '.join(chyby) if chyby else 'ok'
        if chyby:
            spadlo.append(slug)
        print(f"{slug:28} {stav:24} okraj {m['okraj']:>3} | sloupce {potrubi}")
    print()
    print(f'{len(vysledky)} dílů, rozbité: ' + (', '.join(spadlo) if spadlo else 'žádný'))
    sys.exit(1 if spadlo else 0)


if __name__ == '__main__':
    main()
