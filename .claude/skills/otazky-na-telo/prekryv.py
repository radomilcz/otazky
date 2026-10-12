"""Hledá překryvy mezi listy — všechny páry, nebo jeden díl proti ostatním.

    python3 .claude/skills/otazky-na-telo/prekryv.py            # všechny páry
    python3 .claude/skills/otazky-na-telo/prekryv.py 14         # jen díl 14
    python3 .claude/skills/otazky-na-telo/prekryv.py 14 0.12    # s jiným prahem

Strojová shoda najde nejvýš půlku duplikátů. Stejný motiv jinými slovy
nenajde vůbec — na to je potřeba listy přečíst. Tenhle skript je síto na
to zřejmé, ne verdikt.
"""
import glob, os, re, sys, unicodedata
import yaml

STOP = set('''a i v z s o u k na do se si je to ten ta ten toho tom tomu tím ty tvůj tvoje
tvá tvé tvých tvým tobě tebe ti te co kdo kde kdy jak proč který která které kterém kterou
kterého kdož jsi jsem je jsou být byl byla bylo budeš bude budou máš mám má mají měl
nemáš není ale nebo než když aby jen už také taky pro při přes pod nad za od po bez
víc nejvíc líp nejlíp tak takhle tam tady teď dneska pořád ještě svůj svoje svá své
tvoji jeho její jejich nás nám my vy vám jim jemu jí ho mu
tenhle tyden'''.split())

# „tenhle týden“ je jediná vazba, kterou skill napříč díly povoluje — jinak
# zaslepí všechny poslední bloky a skutečné duplikáty se v tom utopí.


def bezdiakritiky(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                   if unicodedata.category(c) != 'Mn')


def kmeny(text):
    slova = re.findall(r'[a-zA-Zá-žÁ-Ž]+', text)
    return {bezdiakritiky(w)[:6] for w in slova
            if len(w) > 2 and bezdiakritiky(w) not in STOP}


def nacti():
    listy = {}
    for cesta in sorted(glob.glob('src/otazky/*.md')):
        hlava = open(cesta, encoding='utf-8').read().split('---')[1]
        d = yaml.safe_load(hlava)
        polozky = []
        for b in d['bloky']:
            for o in b['otazky']:
                assert isinstance(o, str), f'{cesta}: {b["nazev"]} není text'
                polozky.append((b['nazev'], o))
        listy[int(d['dil'])] = (os.path.basename(cesta), polozky)
    return listy


def podobnost(a, b):
    ka, kb = kmeny(a), kmeny(b)
    if not ka or not kb:
        return 0.0, set()
    spol = ka & kb
    return len(spol) / len(ka | kb), spol


def main():
    if not os.path.isdir('src/otazky'):
        sys.exit('spusť to z korene repa')
    jen = int(sys.argv[1]) if len(sys.argv) > 1 else None
    prah = float(sys.argv[2]) if len(sys.argv) > 2 else 0.15
    listy = nacti()
    nalezy = []
    cisla = sorted(listy)
    for i, x in enumerate(cisla):
        for y in cisla[i + 1:]:
            if jen is not None and jen not in (x, y):
                continue
            for bx, ox in listy[x][1]:
                for by, oy in listy[y][1]:
                    s, spol = podobnost(ox, oy)
                    if s >= prah:
                        nalezy.append((s, x, bx, ox, y, by, oy, spol))
    nalezy.sort(reverse=True, key=lambda t: t[0])
    print(f'listů: {len(listy)} | prah: {prah} | nálezů: {len(nalezy)}\n')
    for s, x, bx, ox, y, by, oy, spol in nalezy:
        print(f'{s:.2f}  díl {x} [{bx}] {ox}')
        print(f'      díl {y} [{by}] {oy}')
        print(f'      spol.: {" ".join(sorted(spol))}\n')
    if not nalezy:
        print('nic nad prahem — a to neznamená, že tam duplikát není.')


if __name__ == '__main__':
    main()
