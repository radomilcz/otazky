# Otázky na tělo

Jeden list A4 ke každému kázání Církve jako kráva. Člověk si ho odnese z neděle
a odpovídá si na něj sám.

Tenhle soubor čte každý agent, který sem přijde. Je to rozcestník, ne návod —
návod je ve skillu.

## Než napíšeš jedinou otázku

Přečti **[`.claude/skills/otazky-na-telo/SKILL.md`](.claude/skills/otazky-na-telo/SKILL.md)**
celý. Je to norma: šest pravidel, počítání P a V, stavba listu, hlas, odevzdání.
Totéž leží pod `.agents/skills/otazky-na-telo/` pro agenty, kteří hledají skilly tam.

Pak přečti **[`src/otazky/28-bud-laskavy.md`](src/otazky/28-bud-laskavy.md)**. To je
vzorový list, který prošel autorovým schválením po víc než třiceti jeho úpravách.

## Zdroj je kázání, ne tvoje hlava

Kázání leží v Outline v kolekci *Církev jako kráva › Série*. Pole `zdroj:` v každém
listu říká, které kázání k němu patří. Čti ho **celé**, včetně poznámek pod snímky —
tam kazatel mluví k sobě a bývá to to nejlepší. Věty označené `==takhle==` jsou jeho
vlastní důraz.

Bez přístupu k Outline tenhle úkol nedělej. Vymyšlené otázky jsou horší než žádné.

## Nástroje

Všechno je obyčejný Python, běží pod čímkoli. Potřebuje Playwright a Chromium
(`CHROME_PATH` musí ukazovat na binárku).

```bash
python3 build.py --pdf --koncepty        # vysází docs/ včetně konceptů
python3 .claude/skills/otazky-na-telo/mereni.py    # vejde se každý list na A4?
python3 .claude/skills/otazky-na-telo/prekryv.py   # netluče se něco s jiným dílem?
python3 .claude/skills/otazky-na-telo/rozpocet.py  # kolik řádků položka zabere
python3 .claude/skills/otazky-na-telo/editor.py <slug> <cíl>   # editovatelný náhled
```

## Co se nesmí

- **`docs/` je výstup CI.** Necommituj ho. Po buildu `git checkout -- docs && git clean -fdq docs`.
- **Nic nepouštěj na web bez autorova slova.** `koncept: true` drží list mimo web;
  CI staví bez `--koncepty`, takže koncepty na web nepropadnou.
- **Nekrať autorovy věty.** Jeho úpravy slovo přidávají, ne ubírají. Když krátíš ty,
  obvykle z věty vysáváš význam.
- **Každá věta jde přes kontrolu češtiny**, a znovu po každé úpravě. Na jednom listu
  běžela třikrát a každé kolo oprav přineslo novou chybu.

## Jak poznáš, že je list hotový

`mereni.py` řekne „rozbité: žádný“, `prekryv.py` nenajde nic nad 0,3, položek je
patnáct nebo šestnáct, nejmíň devět z nich hledá v člověku to lepší, nejvýš čtyři jsou
výslech, první blok je laskavý celý a poslední položka je praktická výzva do příštího
týdne. Zbytek je ve skillu.
