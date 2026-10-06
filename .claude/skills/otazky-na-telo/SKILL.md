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

5. **Napiš otázky.** Každá projde zkouškou změny (níž). Jedna otázka = jeden pohyb.

6. **Zkontroluj češtinu** skillem `kontrola-cestiny`. Co projde strojem, přečti ještě
   nahlas.

7. **Rozděl je 4–4–4–3.** Ne kvůli estetice: A4 sází bloky do dvou sloupců po dvou a při
   jiném dělení se sazba vysype z jedné strany. Osm otázek vlevo, sedm vpravo.

8. **Sestav a změř.** PDF musí mít jednu stranu a spodní okraj kolem 61 px (16 mm).
   Pak publikuj náhled a zeptej se — nepouštěj to na web sám.

## Zkouška změny

Otázka projde, když se na ni dá odpovědět **jménem člověka, místem, časem nebo skutkem**.
Neprojde, když si vystačí s „asi jo“, „nevím“ nebo „to je těžké“.

| neprojde | projde |
|---|---|
| Jak vnímáš Boží štědrost? | Co máš doma za nářadí, které se už rok nehnulo? |
| Je pro tebe důležité sloužit druhým? | Komu tenhle týden otevřeš dveře, kdo u tebe ještě nebyl? |
| Co pro tebe znamená být správce? | Co hlídáš jako majitel, i když jsi jen správce? |

Zkouška má i druhou stranu: otázka nesmí mít předepsanou odpověď. „Nemyslíš, že bys měl
víc dávat?“ není otázka, to je kázání s otazníkem.

## Hlas

- **Ty, ne vy.** Jeden člověk nad listem, ne sál.
- **Jedna věta.** Dvě jen tehdy, když druhá obrací nůž: „Oba o tobě vědí totéž — čím se
  liší?“
- **Konkrétní slova z kázání** místo obecných. Hrnec, gauč, francouzák. Ne „zdroje“,
  „oblasti“, „možnosti“.
- **Přítomný čas a sloveso.** Ne „k zamyšlení nad tvým postojem k“.
- Kázání samo to říká nejlíp: *„Nemáme používat biblickou, ale lidskou řeč.“* Takže
  žádné „sdílet“ ve významu říct, žádné „mít dopad“, „nastavit si“, „v rámci“, „na denní
  bázi“, „komunikovat něco někomu“, žádný trpný rod a žádná terapeutická čeština
  („jak se v tom cítíš“).
- Vykej jen Bohu, a to taky ne.

## Stavba listu

Čtyři bloky mají pořadí, ne jen jména:

1. **kde jsi** — situace, kterou čtenář pozná (samaří, hrnec)
2. **co ti brání** — nebo co se v tom děje (žízeň, strach)
3. **co nevidíš** — obrat, který kázání nabízí (poledne, správce)
4. **co s tím tenhle týden** — poslední blok vždycky míří ven, do týdne

Poslední otázka listu je akce s datem: „tenhle týden“. Je to jediná vazba, která se smí
opakovat napříč díly.

## Hlavička souboru

```yaml
titul: Bůh, ty a buchty      # bez čísla
serie: Boží design
dil: 15
datum: 2026-03-15            # neděle, kdy kázání zaznělo
citat: …                     # věta z kázání, ne z manifestu, když je po ruce
zdroj: 15. Bůh, ty a buchty
video: https://youtu.be/…    # z kanálu @acnjcz, páruj podle data, ne podle názvu
koncept: true
```

Citát vybírej z „Nejsilnějších hlášek“ nebo z kázání — má to být věta, kterou si člověk
pamatuje z neděle, ne teze.

## Než to odevzdáš

- [ ] patnáct otázek, čtyři bloky, dělení 4–4–4–3
- [ ] každá otázka projde zkouškou změny
- [ ] otázky z kázání jsou v jeho slovech
- [ ] nic se netluče s předchozími díly — slovně ani motivem
- [ ] každá otázka stojí sama, bez kázání za zády („ti dva“ nikdo nezná)
- [ ] kontrola češtiny proběhla
- [ ] PDF má jednu stranu, okraj dole ~61 px
- [ ] `koncept: true` a náhled poslaný ke schválení
