"""Spočítá, kolik řádků list zabere, ještě než se vysází.

    python3 .claude/skills/otazky-na-telo/rozpocet.py            # všechny díly
    python3 .claude/skills/otazky-na-telo/rozpocet.py 14 17      # jen některé

A4 sází bloky 1+2 do levého sloupce a 3+4 do pravého. Každý sloupec unese
**19 řádků**; 20 už bývá o řádek přes. Řádky se odhadnou z délky položky, protože takhle
se dá krátit bez spouštění buildu:

    do  43 znaků = 1 řádek      do 125 = 3
    do  86 znaků = 2 řádky      do 149 = 4

Odhad je kalibrovaný na všech vysázených listech a plete se nejvýš o řádek
na položce těsně nad hranou. Platné číslo dává až `mereni.py`.
"""
import glob, os, sys
import yaml

HRANICE = (43, 86, 125, 149, 181)
STROP = 19


def radky(text):
    for i, h in enumerate(HRANICE, 1):
        if len(text) <= h:
            return i
    return len(HRANICE) + 1


def main():
    if not os.path.isdir('src/otazky'):
        sys.exit('spusť to z korene repa')
    jen = set(sys.argv[1:])
    spadlo = []
    for cesta in sorted(glob.glob('src/otazky/*.md')):
        d = yaml.safe_load(open(cesta, encoding='utf-8').read().split('---')[1])
        if jen and str(d['dil']) not in jen:
            continue
        bl = [sum(radky(o) for o in b['otazky']) for b in d['bloky']]
        levy, pravy = sum(bl[:2]), sum(bl[2:])
        pres = max(levy - STROP, 0) + max(pravy - STROP, 0)
        stav = 'ok' if not pres else f'PŘETÉKÁ o {pres} ř'
        if pres:
            spadlo.append(str(d['dil']))
        print(f"díl {d['dil']:>2} {os.path.basename(cesta):26} "
              f"bloky {'-'.join(map(str, bl)):11} levý {levy:>2} | pravý {pravy:>2}  {stav}")
    print()
    print('přetéká: ' + (', '.join(spadlo) if spadlo else 'žádný'))


if __name__ == '__main__':
    main()
