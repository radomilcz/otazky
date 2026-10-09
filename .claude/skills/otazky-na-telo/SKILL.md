---
name: otazky-na-telo
description: Napíše list otázek na tělo k jednomu kázání Církve jako kráva – čtyři bloky, patnáct otázek, hotový soubor do src/otazky/ a náhled. Použij, když padne „otázky k dílu“, „otázky na tělo“, „otázky z kázání“, „nový díl“ nebo když přijde odkaz na kázání v Outline s prosbou o otázky.
---

# Otázky na tělo

Z kázání udělej list patnácti otázek. Ne shrnutí, ne poznámky, ne úvahu — otázky, které
člověk v pondělí ráno použije.

## Co z toho vyleze

Soubor `src/otazky/<adresa>.md` ve stejném tvaru jako díly, které tam už jsou:
čtyři bloky, dohromady patnáct otázek, `koncept: true`, dokud to Radomil neschválí.
Pak sestavení (`build.py --koncepty --pdf`) a náhled, ne rovnou push na web.

## Postup

1. **Přečti celé kázání.** Ne shrnutí. Poznámky pod snímky jsou často to nejlepší — tam
   kazatel mluví k sobě. K ruce si vem i stránku série (Hlavní poselství, Nejsilnější
   hlášky) a díly okolo, ať víš, kde v příběhu tenhle stojí.

2. **Posbírej otázky, které v kázání už jsou.** Řádky „Otázka:“ i věty s otazníkem v
   textu. **Tyhle mají přednost před čímkoli, co vymyslíš ty.** Zachovej jejich slova;
   mění se jen plurál na „ty“ a odřízne se, co bez kázání nedává smysl.

3. **Vypiš obrazy, na kterých kázání stojí.** Samaří, poledne u studny, buchta, umaštěné
   nářadí, zakopaná hřivna. Z nich budou jména bloků — jedno malé slovo, žádné nadpisy
   typu „Praktická aplikace“. Obraz je taky to, co drží otázku na zemi: „Kde je tvoje
   Samaří?“ unese víc než „Komu se vyhýbáš?“.

4. **Přečti předchozí díly v `src/otazky/`.** Nic se nesmí opakovat. Pozor: strojová
   shoda slov najde jen půlku. Druhou půlku najdeš čtením — stejný motiv jinými slovy je
   pořád duplikát. Skutečné případy, které takhle prošly a musely ven:
   - „Komu jsi naposledy dovolil, aby něco přinesl on tobě?“ ← díl 26 měl „…aby on podal
     vodu nebo pomohl tobě?“
   - „Kdo by o tobě řekl, že tě vidí i s tím, co jsi pokazil?“ ← díl 26 měl totéž, jen
     zrcadlově.
   Kázání samo předchozí díly rekapituluje; to je v kázání správně, na listu ne.

5. **Napiš otázky.** Jedna otázka = jeden pohyb.

6. **Projdi poslední půlku každé z patnácti.** Vezmi tu část, kterou čtenář odpovídá, a
   napiš si k ní konkrétní odpověď. Jde to jménem, časem, místem nebo věcí? Když ne,
   vrať se do kázání a najdi slovo, které to umí. Tenhle krok nepřeskakuj u otázek, kde
   je první polovina výborná — právě tam se chyba schovává.

   Ve stejném průchodu napiš ke každé otázce **N** nebo **P** a sečti to (viz *Hledáme
   poklad, ne odpad*). Když nálezů vyjde víc než osm nebo pokladů méně než čtyři,
   přepisuješ první blok, ne jednotlivé věty.

7. **Zkontroluj češtinu** skillem `kontrola-cestiny`. Co projde strojem, přečti ještě
   nahlas. **Kontrola platí jen pro ty věty, které jí prošly.** Každá otázka, kterou po
   ní napíšeš nebo přepíšeš — i jediná věta hozená do chatu jako návrh — musí projít
   znovu. Jinak jde na list text, který neviděl nikdo. Nejčastěji na tom padá mlhavé
   „to“ bez odkazu, kolize časů mezi první a druhou půlkou a vedlejší věta přilepená
   k jinému podstatnému jménu, než na které míří.

8. **Rozděl je 4–4–4–3.** Ne kvůli estetice: A4 sází bloky do dvou sloupců po dvou a při
   jiném dělení se sazba vysype z jedné strany. Osm otázek vlevo, sedm vpravo.

9. **Sestav a změř.** PDF musí mít jednu stranu a spodní okraj kolem 61 px (16 mm).
   Pak publikuj náhled a zeptej se — nepouštěj to na web sám.

## Zkouška změny

Otázka projde, když se na ni dá odpovědět **jménem člověka, časem, místem nebo věcí, na
kterou se dá ukázat**. Neprojde, když si vystačí s „asi jo“, „nevím“ nebo „to je těžké“.

| neprojde | projde |
|---|---|
| Jak vnímáš Boží štědrost? | Co máš doma za nářadí, které se už rok nehnulo? |
| Je pro tebe důležité sloužit druhým? | Komu tenhle týden otevřeš dveře, kdo u tebe ještě nebyl? |
| Co pro tebe znamená být správce? | Co hlídáš jako majitel, i když jsi jen správce? |

### Zkoušej tu půlku, kterou čtenář odpovídá

Tedy poslední. **Tady se to láme, a téměř vždycky.** První polovina nese obraz z kázání,
je konkrétní a zkoušku projde — a já k ní přilepím druhou, která se ptá na postoj.
Celá otázka pak propadne a mně to kvůli té dobré první půlce unikne.

| co jsem napsal | co z toho udělal autor |
|---|---|
| Obejmeš stín, nebo zvedneš hlavu? | Obejmeš stín, nebo **syna**? |
| …aby ti Ježíš stačil? | …aby ti Ježíš stačil **v pondělí ráno**? |
| Co u tebe vidí lidé zdola? | Vidí lidé, že **máš doma rozsvíceno**? |
| Co u tebe stojí nejvíc zvlášť? | Co u tebe stojí nejvíc **mimo Boží záměr**? |
| Kde ten řez poznáš? | **Na co přepínáš v neděli ráno?** |
| Kde to máš jen od lidí? | Co z toho **stojí na tradici otců**? |

Vlevo je šestkrát postoj nebo pohled, vpravo šestkrát něco, na co se dá ukázat. A každé
to slovo vpravo v kázání bylo — jen jsem si ho tam nedošel přečíst.

Z toho dvě pravidla pro druhou půlku:

- **Potřebuje slovo? Ber ho z kázání, ne ze sebe** — a ber to nejkonkrétnější, co tam je.
- **Nevyráběj z jeho sloves podstatná jména ani k jeho obrazu nelep svůj.** On krájí
  týden, tak se ptej, kdy *přepíná*, ne „kde se pozná ten řez“ — řez v kázání není. Jeho
  seznam „dům zvlášť, kostel zvlášť, práce zvlášť“ se doptává slovem *zvlášť*, ne tím, že
  věci spolu „nemluví“.

**Výjimka: ano/ne projde, když je to zrcadlo.** Když první polovina pojmenuje tu
konkrétní věc tak přesně, že „ano“ je samo přiznání, druhá půlka smí být ano/ne.
„Šest dní přežívám, v neděli ožívám. Platí to o tobě?“ — tady se vyhnout nedá,
diagnóza už ve větě stojí. Nepřepisuj to na „který den“; rozmělníš tím ránu.

Zkouška má i druhou stranu: otázka nesmí mít předepsanou odpověď. „Nemyslíš, že bys měl
víc dávat?“ není otázka, to je kázání s otazníkem.

## Hlas

- **Ty, ne vy.** Jeden člověk nad listem, ne sál.
- **Jedna věta.** Dvě jen tehdy, když druhá obrací nůž: „Oba o tobě vědí totéž — čím se
  liší?“ Na tu druhou platí zkouška dvojnásob, viz výš.
- **Konkrétní slova z kázání** místo obecných. Hrnec, gauč, francouzák. Ne „zdroje“,
  „oblasti“, „možnosti“.
- **Přítomný čas a sloveso.** Ne „k zamyšlení nad tvým postojem k“.
- Kázání samo to říká nejlíp: *„Nemáme používat biblickou, ale lidskou řeč.“* Takže
  žádné „sdílet“ ve významu říct, žádné „mít dopad“, „nastavit si“, „v rámci“, „na denní
  bázi“, „komunikovat něco někomu“, žádný trpný rod a žádná terapeutická čeština
  („jak se v tom cítíš“).
- Vykej jen Bohu, a to taky ne.
- Obrazná vazba musí být česká. „Kde se to láme?“ zní jako překlad; „U čeho stojíš?“
  je totéž česky. Když si obraz nedokážeš představit doslova, přepiš ho.
- Rejstřík není chyba. „Co se musíš odnaučit“ je hovorové a správné, „čemu“ je
  knižnější varianta téže vazby — na listu platí ta mluvená.
- Kontrola je návrh, ne rozsudek. Autor rozhoduje. Co už rozhodl: „vzít něco kvůli
  někomu“ je ve významu pohnutky v pořádku a nepřepisuje se na „pro někoho“.
- **Čtyři slovesa na jednu otázku jsou tři moc.** Když se v otázce hromadí děje
  („schováváš se za výmluvu a tváříš se, že je to slabost“), čeština na to většinou má
  jedno sloveso: *vydávat něco za něco*. Najdi ho.
- Když otázka stojí na biblickém příběhu, **nevyprávěj ho — doveď otázku k tomu, co z
  něj plyne.** „Co bys musel prodat, abys mohl jít?“ nikdo nepochopí; „Co bys musel
  prodat, abys mohl jít za Ježíšem?“ ano, a je to pořád jedna řádka. Celá věta o
  bohatém mladíkovi je až třetí možnost, ne první.

## Stavba listu

Čtyři bloky mají pořadí, ne jen jména:

1. **co máš** — co už čtenář dostal, umí nebo zažil (hrnec a francouzák, tvůj dar)
2. **co ti brání** — nebo co se v tom děje (žízeň, strach, závěs)
3. **co nevidíš** — obrat, který kázání nabízí (poledne, správce, stín)
4. **co s tím tenhle týden** — poslední blok vždycky míří ven, do týdne

Poslední otázka listu je akce s datem: „tenhle týden“. Je to jediná vazba, která se smí
opakovat napříč díly.

### Hledáme poklad, ne odpad

První blok je **inventář, ne diagnóza.** Dlouho jsem si „kde jsi“ vykládal jako „kde je
ten problém“ — a tím jsem čtenáře obvinil hned v první otázce a dál už se to jen
přitahovalo. Autorovo vlastní pravidlo z šestnáctky to říká přesně:

> **Hledáme v lidech to, co do nich vložil Stvořitel — ne to, co jim chybí.**
> **Nehledáme chyby. Odhalujeme poklady. Lovec pokladů, ne detektor chyb.**

**Spočítej to, než list odevzdáš.** Napiš si ke každé z patnácti **N** (předjímá, že
čtenář dělá něco blbě) nebo **P** (ptá se na to, co má nebo zažil) a sečti. **Nejvýš
osm N, nejméně čtyři P**, a ta čtyři P patří do prvního bloku.

Na čem se to měřilo: patnáctka a šestnáctka mají 7 N a jsou nejlepší listy v sérii.
Pětka a sedmička měly 12 N, trojka 10 N a ani jedno P. Rozdíl nebyl v tématu — kázání
o rodokmenu je to nejmilostivější z celé série a jeho list byl na jedenácti N.

**Pozor na cukr.** Neřeš to tím, že přilepíš „pozitivní“ otázku jako protiváhu. Poklad
musí být stejně konkrétní jako nález: *hrnec a vařečku, francouzák a vrtačku, nebo
pastelky?* a *Co umíš tak dobře, že ti to přijde obyčejné?* unesou list. „Za co jsi
vděčný?“ ne.

## Hlavička souboru

```yaml
titul: Bůh, ty a buchty      # bez čísla
serie: Boží design
dil: 15
datum: 2026-03-22            # neděle, kdy kázání zaznělo – ber ji z názvu videa,
                             # ne z data vzniku dokumentu v Outline, ten bývá starší
citat: …                     # věta z kázání, ne z manifestu, když je po ruce
zdroj: 15. Bůh, ty a buchty
video: https://youtu.be/…    # z kanálu @acnjcz, páruj podle data, ne podle názvu.
                             # Starší díly jsou ve feedu playlistu série:
                             # youtube.com/feeds/videos.xml?playlist_id=…
koncept: true
```

**Pozor na dvojtečku.** `- Jeremiáš řekl: neumím mluvit` si YAML přečte jako mapu a
otázka se rozpadne. Buď ji přepiš (pomlčka, uvozovky), nebo celou otázku uzavři do
apostrofů. Stejně tak hlídej otázku začínající `- ` nebo `#`.

Citát vybírej z „Nejsilnějších hlášek“ nebo z kázání — má to být věta, kterou si člověk
pamatuje z neděle, ne teze.

## Než to odevzdáš

- [ ] patnáct otázek, čtyři bloky, dělení 4–4–4–3
- [ ] u každé z patnácti prošla zkouškou změny ta půlka, kterou čtenář odpovídá
- [ ] spočítané N a P: nejvýš osm nálezů, nejméně čtyři poklady, a ty v prvním bloku
- [ ] otázky z kázání jsou v jeho slovech
- [ ] nic se netluče s předchozími díly — slovně ani motivem
- [ ] každá otázka stojí sama, bez kázání za zády („ti dva“ nikdo nezná) —
      u otázky na biblický příběh to zkus přečíst jako první v životě
- [ ] kontrola češtiny proběhla, a to i na všem, co jsem přepsal po ní
- [ ] PDF má jednu stranu, okraj dole ~61 px
- [ ] `koncept: true` a náhled poslaný ke schválení
