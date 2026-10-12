# Odevzdání listu

Tenhle soubor se čte, až když jsou položky napsané a projdou pravidly ze `SKILL.md`.
Je to plumbing: soubor, sazba, náhled, schválení, publikování.

## Soubor

`src/otazky/<poradi>-<adresa>.md`, například `28-bud-laskavy.md`.

```yaml
---
titul: Buď laskavý           # bez čísla
serie: Boží design
dil: 28
datum: 2026-10-11            # neděle, kdy kázání zaznělo – ber ji z názvu videa,
                             # ne z data vzniku dokumentu v Outline, ten bývá starší
citat: Pravda bez lásky láme. Láska bez pravdy klame.
zdroj: 28. Buď laskavý       # název dokumentu v Outline
video: https://youtu.be/…    # dokud kázání nebylo, pole vynech
koncept: true                # dokud to Radomil neschválí
bloky:
- nazev: chesed
  otazky:
  - …
---
```

**Citát** je věta z kázání nebo punchline z hodnot — něco, co si člověk pamatuje
z neděle. Ne teze a ne věta o listu samotném.

### Dvě pasti v YAML

- **Dvojtečka.** `- Jeremiáš řekl: neumím mluvit` si YAML přečte jako mapu a díl se
  **vůbec nevysází** — build spadne na `html.escape`. Celou položku dej do dvojitých
  uvozovek: `- "Umíš říct stejně dobře: „Ani já tě nesoudím“ a …?"`
- Stejně hlídej položku, která začíná `- `, `#`, `>` nebo `[`.

Po každé úpravě souboru se vyplatí ověřit, že se to vůbec načte:

```bash
python3 -c "
import yaml
d=yaml.safe_load(open('src/otazky/28-bud-laskavy.md',encoding='utf-8').read().split('---')[1])
for b in d['bloky']:
    assert all(isinstance(o,str) for o in b['otazky']), b['nazev']
print('ok', sum(len(b['otazky']) for b in d['bloky']), 'položek')
"
```

### Video

Z kanálu `@acnjcz`. Nejspolehlivější zdroj je feed playlistu série — je v
`src/serie/<serie>.md` v poli `playlist`:

```bash
curl -sS "https://www.youtube.com/feeds/videos.xml?playlist_id=<ID>" | grep -A2 '<title>'
```

Datum je **v názvu videa**, ne v datu publikace. ID si ověř přes oembed, aby na listu
neskončilo cizí kázání:

```bash
curl -sS "https://www.youtube.com/oembed?url=https://youtu.be/<ID>&format=json"
```

Když pole `video` chybí, panel *(B)učení* i odkaz na záznam se prostě nevykreslí —
nikde nezůstane prázdné místo. Dá se tedy vydat list bez videa a odkaz doplnit potom.

## Sazba

```bash
CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  python3 build.py --koncepty --pdf
```

Bez `CHROME_PATH` se PDF nevysází. `--koncepty` přibere i rozpracované díly.

**Platit musí dvě věci, nic víc:**

1. PDF má **jednu stranu**
2. obsah **nenarazí do patky** — patka má vůli do 993 px, pod 45 px spodního okraje
   (12 mm) už to netiskne každá tiskárna

```bash
python3 -c "
d=open('docs/28-bud-laskavy/otazky-na-telo.pdf','rb').read()
n=d.count(b'/Type /Page')-d.count(b'/Type /Pages')
print('PDF:', 'jedna strana' if n==1 else f'ROZBITÉ: {n} stran')
"
```

A4 sází bloky dva vlevo, dva vpravo, takže o výšku sloupců rozhoduje počet **řádků**,
ne počet položek. Obvyklé dělení 4–4–4–3, zrcadlo 4–3–5–3 drží stejně dobře.

**Čísla sloupců jsou tvoje potrubí. Radomilovi je nehlas** — ozvi se jen tehdy, když se
list rozbije.

### Když se to nevejde

Nikdy nekrať dobrou větu, aby se vešla jiná. Pořadí, co jde z listu první:

1. co je **redundantní** — dvě položky, které se ptají na totéž
2. co je **tvoje** a nese nejmíň
3. **nic dalšího** — radši jdi s okrajem na 47 px a nech list být

Čtyři pixely nejsou důvod zahodit větu z kázání. Devět milimetrů spodního okraje je
důvod něco vyhodit.

## Editovatelný náhled

Nejlepší podoba náhledu je ta, do které autor píše přímo. Ušetří to kolo, ve kterém
posílá věty do chatu a ty je přepisuješ — a hlavně vidí svou úpravu hned v sazbě.

Skript `editor.py` (ve scratchpadu, přiložen k tomuhle postupu) vezme vysázenou stránku
dílu a přidá do ní editační vrstvu:

- každé `<li>` dostane klíč `data-k="b<blok>q<poradi>"` a `contenteditable`
- Enter uloží, Escape zahodí, změněná položka má svislou linku a tlačítko **vrátit**
- dole je pole **Vzkaz pro Clauda** na to, co se do položek nevejde
- `@media print` celou tu vrstvu skryje, takže PDF i tisk zůstávají beze změny

Publikuje se s `capabilities: {"db": {}, "user": {}}`. Úpravy padají do kolekce `upravy`,
jeden dokument na položku: `{text, puvodni, kdy}`. Vzkaz leží v `vzkaz/text`.

Pak si je vytáhneš nástrojem `ArtifactData`:

```
action: list, collection: upravy      # úpravy položek
action: get,  collection: vzkaz, doc_id: text
```

**Po zapsání úprav do zdroje ty dokumenty smaž** (`action: batch`, samé `delete`,
s `if_version` z toho čtení) a náhled přesázej a publikuj znovu. Tím se stane autorovo
znění novým základem a další kolo začíná na čisté stránce.

Dvě věci, které se u toho pokaždé hodí vědět:

- **Klíče jsou podle pozice.** Dokud položky nepřehazuješ, drží. Když mezi autorovým
  psaním a čtením něco přidáš nebo smažeš, úpravy se rozsypou — tak do souboru nesahej,
  dokud si je nevytáhneš. Proto se vedle `text` ukládá i `puvodni`: podle něj poznáš,
  co přesně bylo čím nahrazeno.
- **Autor v editaci občas nechá zbytek staré věty.** Osmička takhle dostala položku
  „Šimon je jméno, se kterým jsme se narodili… **Kým jsi podle povolání.** Kde jsi mezi
  nimi dneska?“ — ten prostřední úryvek byl kus předchozího znění. Projdi úpravy očima,
  než je zapíšeš, a na takový zbytek se zeptej.

A pořád platí pravidlo 6: **co autor přepíše, jde přes kontrolu češtiny.** Jeho věty
nejsou výjimka, jen o nich rozhoduje on.

## Náhled

`docs/` je výstup CI. **Nikdy ho necommituj** a po každém lokálním buildu ho zahoď:

```bash
git checkout -- docs && git clean -fdq docs
```

Dvě pasti, které se tím řeší: `rm -rf docs/<slug>` maže **verzované** soubory
u vydaných dílů, a `build.py --koncepty` přepisuje rozcestníky a PDF vydaných dílů,
protože se do výpisů připletou koncepty.

Náhled se publikuje jako artefakt — zkopíruj stránku, `assets/` a PDF do scratchpadu
a přepiš v HTML absolutní cesty:

```python
s = s.replace('"/assets/', '"assets/').replace('url(/assets/', 'url(assets/')
s = re.sub(r'href="/(?!/)', 'href="https://otazky.cirkevjakokrava.cz/', s)
s = s.replace('href="https://otazky.cirkevjakokrava.cz/<slug>/otazky-na-telo.pdf"',
              'href="otazky-na-telo.pdf"')
```

Při kontrole obsahu v HTML pozor: build vkládá po jednoslabičných předložkách
**nezlomitelné mezery**, takže `grep` na frázi s „s “, „o “, „z “ nebo „i “ nenajde nic.
Ověřuj v Pythonu s `.replace(' ', ' ')`.

## Schválení a publikování

1. `koncept: true`, náhled poslaný Radomilovi
2. **na web to nepouštěj sám** — čeká se na jeho slovo
3. až pak `koncept: false`, commit, push

Commituje se **jen `src/`, `build.py` a `.claude/`.** Vysázené `docs/` dělá CI.

## Git

```bash
for i in 1 2 3 4 5; do
  if git push origin main; then echo PUSH_OK; break
  else sleep $((2**i)); git fetch -q origin main && git rebase -q FETCH_HEAD; fi
done
```

- **Nikdy `git push | tail`.** Výsledek se pak bere z `tail`, push může selhat a vypadá
  to jako úspěch. Stalo se.
- **Po vydání dílu si CI samo commitne vysázené `docs/` do main** (commit „Přesázeno ze
  zdrojů“). Takže před dalším commitem `git fetch` a rebase, jinak push odmítne.
- GitHub občas vrátí 500. Jeden push dneska prošel až na pátý pokus.
- Vydání má **dvě fáze**: workflow *Web* vysází a commitne `docs/`, pak na to navazuje
  *pages build and deployment*. Dokud neběží druhá, vrací nová stránka 404 — to je
  normální, ne chyba.

## Ověření na živém webu

```bash
curl -sS https://otazky.cirkevjakokrava.cz/<slug>/ -o z.html -w 'HTTP %{http_code}\n'
python3 -c "
import re
s=open('z.html',encoding='utf-8').read().replace(' ',' ')
ot=[re.sub(r'<[^>]+>','',o).strip() for o in re.findall(r'<li>(.*?)</li>', s, re.S)]
print('položek:', len(ot))
for o in ot: print(' ·', o)
print('panel videa:', 'je' if 'class=\"buceni\"' in s else 'není')
"
curl -sS -o /dev/null -w 'PDF %{http_code}\n' \
  https://otazky.cirkevjakokrava.cz/<slug>/otazky-na-telo.pdf
```

Zkontroluj ještě, že je díl v rozcestníku `/dily/` a že stálý odkaz
`/otazky-na-telo.pdf` (vede vždy na aktuální díl) míří na ten nový.
