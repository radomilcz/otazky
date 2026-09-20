# Otázky na tělo

Koučovací otázky ke kultuře komunity **Církev jako kráva** – jedna stránka ke čtení i k vytištění.

**Živě:** https://otazky.cirkevjakokrava.cz (GitHub Pages ze složky `docs/`, aktualizuje se s každým pushem do `main`)

Sourozenec [manifestu](https://manifest.cirkevjakokrava.cz) – stejné barvy (`#3b2f2f` / `#e6acac`),
stejné písmo Agrandir i stejný otisk z [Figmy](https://www.figma.com/design/RT5auaz60q3F1kL5eAmKwG/C%C3%ADrkev-jako-kr%C3%A1va).

## Struktura

```
src/otazky/*.txt           díly – jeden soubor = jeden list otázek i jedna adresa
src/index.template.html    šablona stránky: sazba pro obrazovku i @media print pro A4
src/assets/otisk-paths.txt křivky otisku (vektor „Group 14“ z Figmy, 55 cest)
src/assets/favicon.svg     ikona webu – terč v barvách značky (+ favicon-32.png, icon-180.png)
src/assets/og.jpg          náhled při sdílení odkazu (1200×630, vyfocená hlavička stránky)
src/fonts/*.woff           Agrandir – subset (latinka, čeština, šipka), 4 řezy
build.py                   sestaví docs/
docs/index.html            aktuální díl (kořen domény)
docs/<díl>/                stránka dílu a jeho A4
docs/otazky-na-telo.pdf    A4 aktuálního dílu – stálá adresa pro sdílení
```

Aktuální je nejnovější díl, jehož datum není v budoucnu – ten sedí na kořeni domény a na
něj míří i `/otazky-na-telo.pdf`. Ostatní díly zůstávají na svých adresách a přepínač
v hlavičce mezi nimi přepíná.

## Nový díl

1. Založ `src/otazky/<adresa>.txt` – název souboru je adresa stránky (`/26-bud-otevreny/`).
2. Nahoru hlavičku, pod ni bloky otázek:

```
titul: Buď otevřený
serie: Boží design
dil: 26
datum: 2026-09-20
citat: Přežvykujeme, dokud je nevstřebáme celé…      (nepovinné, jinak věta z manifestu)
zdroj: manifest · kultura                            (nepovinné)
koncept: ano                                         (nepovinné – drží díl mimo web)

postoj
- První otázka?
- Druhá otázka?

zranitelnost
- …
```

3. Spusť `python3 build.py --pdf` – přegeneruje `docs/` i A4 každého dílu.
4. Commitni a pushni; GitHub web nasadí sám.

Rozepsaný díl nech označený `koncept: ano`, dokud nemá jít ven. Prohlédnout si ho jde
přes `python3 build.py --koncepty --pdf` (jen lokálně, do `docs/` na push to nepatří).
Prázdný řádek odděluje bloky, první řádek bloku je jeho název, řádky s pomlčkou jsou otázky.
Otevři `docs/index.html` nejlíp přes lokální server – přes `file://` Chrome nenačte fonty
ani odkazy od kořene.

Web a A4 se nemůžou rozejít: tisková podoba je v šabloně jako `@media print` a PDF je její
výtisk. Co vyjede z `--pdf`, vyjede návštěvníkovi i z Ctrl+P.

Jednopísmenné předložky a spojky lepí na další slovo build (`nbsp()`), v `otazky.txt` se
tedy píšou jako obyčejná mezera.

```
python3 build.py            jen stránky
python3 build.py --pdf      stránky + A4 každého dílu   (pip install playwright)
python3 build.py --og       přegeneruje náhled sdílení  (pip install playwright pillow)
python3 build.py --koncepty přibere i rozepsané díly
```

Obojí potřebuje Chromium; když ho playwright nemá vlastní, ukaž na jiný přes `CHROME_PATH=/cesta/k/chrome`.
Adresa v absolutních odkazech (`og:image`, `canonical`) je konstanta `SITE` v `build.py` – musí
sedět s doménou v `docs/CNAME`.

## Nasazení

Jednorázově, ručně – publikování umí zapnout jen člověk s právy správce repozitáře.
Token GitHub App ani `GITHUB_TOKEN` ve workflow na to nestačí (`POST /repos/.../pages`
vrací 403), takže to nejde obejít ani automatizací.

1. **Settings → Pages → Build and deployment**: Source `Deploy from a branch`,
   větev `main`, složka `/docs`, Save.
2. **Custom domain**: `otazky.cirkevjakokrava.cz` (vyplní se z `docs/CNAME`), Save.
3. Až projde kontrola DNS a vystaví se certifikát, zaškrtnout **Enforce HTTPS**.

**DNS** (hotové): `otazky` míří na GitHub Pages – přebíjí wildcard `*.cirkevjakokrava.cz`,
který jinak vede na hlavní hosting.

Potom web staví GitHub sám při každém pushi do `main`; stačí tedy commitnout přegenerované
`docs/`.

## Náhled při sdílení

Když někdo pošle odkaz na WhatsApp nebo Messenger, ukáže se `assets/og.jpg` s titulkem
„Otázky na tělo“. Náhled není sázený ručně – je to fotka hlavičky hotové stránky, takže
vypadá přesně jako web. Po změně vyčistí keš
[Sharing Debugger](https://developers.facebook.com/tools/debug/), jinak Facebook drží starý obrázek.
