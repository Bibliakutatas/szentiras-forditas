PROJEKT EMLÉKEZTETŐ – A Bibliát Kutatom (Szöveghű Bibliafordítás)

1. RÓLAM ÉS A SZEMLÉLETEMRŐL
- Név: Ferenc (Lexcom, Linux és open source rendszerek).
- Zsinórmérték: Kizárólag a leírt Ige („Meg van írva” / „It is Written”). Elutasítom a dogmatikus vallási sallangokat, üres hagyományok és a mainstream egyházi felekezeteket és a reflex-ámeneket.
- Műhely: „A Bibliát Kutatom” – tiszta szellemi műhely a Tóra megélésére és mély szövegkutatásra.
- Teológiai látás: A Tóra érvényes, kóser valósága, a Tóra belső jogi logikája (pl. a Férj halálának jogi szükségessége), a prófétai összefüggések, valamint Yehoshua (Jézus) istensége (YHWH).
- Kommunikációs elvárás: Légy lényegretörő, pontos, ne magyarázd túl a hátteret, kerüld a vallásos kliséket, és használj mély héber/görög szövegkritikát (MT, LXX, Qumrán, Ketiv/Qere) és jogi logikát.

2. PROJEKT KÖRNYEZET ÉS STRUKTÚRA
- Helyi könyvtár: ~/szentiras-forditas/
- Élő oldal: MkDocs Material + GitHub Pages
- Publikálási munkafolyamat: fájl írása/bővítése -> mkdocs.yml navigáció frissítése -> git add . && git commit && git push && mkdocs gh-deploy

3. RÖGZÍTETT FORMÁTUM, SZÓHASZNÁLAT ÉS MUNKAFolyAMAT (SZIGORÚAN BETARTANDÓ!)
- Szent nevek és héber tulajdonnevek: Mindenhol az angolosított héber alakokat használjuk félkövérrel kiemelve (pl. **YHWH**, **Elohim**, **Yisrael** – aposztróf nélkül!, **David**, **Shlomoh**, **Yerushalayim**, **Yehudah**, **Micrayim**, **Cor**, **Cidon**, **Rekhav'am**, **Jarov'am**, **Chizkijahu**, **Joshijahu**, **Jeshajahu**, **Mashiach** stb.), az első előfordulásnál magyar névalakkal zárójelben.
- Tagmondatonkénti héber átírás: Minden egyes tagmondat mögött ott szerepel a héber eredeti átírása dőlt zárójelben ((*va-jomer*), (*asher-itto*), (*be-khol-ha-arec*)), magyaros fonetikus írásmóddal (`j` a jod-nál, `c` a cádé-nál, `sz` a szin/számekh-nél, `kh` a káf/chét-nél, kötőjeles előtagokkal: `va-`, `be-`, `le-`, `ha-`, `et-`).
- Tiszta versszöveg: A versekbe nem kerül magyarázó kommentár vagy mértékegység-átszámítás, csak a pontos fordítás és a szövegkritikai variánsok (MT, LXX, Qumrán, Ketiv/Qere, párhuzamos helyek).
- Főcím (H1): `# Héber Név (Magyar Név) Fejezetszám` (pl. `# Jeshajahu (Ézsaiás) 1`)
- Versek tördelése: Minden vers külön bekezdésként, pontosan egy üres sorral elválasztva (`**1.** Szöveg...`).
- Elválasztó és elemzés (H3): `---` után egységesen `### Szövegkritikai, teológiai és jogi elemzés` alcím alatt pontokba szedett Tóra-jogi, szövetségteológiai, messiási, történeti-régészeti és szövegkritikai jegyzetek.

4. TERMINÁL-KOMPATIBILITÁS ÉS KÓDOLÁSI SZABÁLYOK (KRITIKUS!)
- Névellenőrző `grep` parancsokat NE használj!
- Minden szöveges kimenet közvetlenül futtatható bash kódblokkban érkezzen (`cat << 'EOF' > ~/szentiras-forditas/docs/tanakh/.../01.md` majd `>>` a folytatáshoz).
- A tagmondatonkénti héber átírás miatt minden blokk legfeljebb 10–14 verset tartalmazzon, hogy a terminálba másolva ne törjön meg.
- Az elemzés a fejezet utolsó blokkjának végén szerepeljen.
- A fejezet lezárásakor mindig egyetlen futtatható egysoros élesítő parancsot adj meg a végén:
  `echo "      - X. fejezet: tanakh/XX-konyv-neve/XX.md" >> ~/szentiras-forditas/mkdocs.yml && cd ~/szentiras-forditas && git add . && git commit -m "Könyv X. fejezet" && git push && mkdocs gh-deploy`

5. A PROJEKT JELENLEGI ÁLLÁSA (100%-BAN ELKÉSZÜLT ÉS ÉLESÍTETT RÉSZEK)
- Tóra: 01-bereshit (1–50), 02-shemot (1–40), 03-vayikra (1–27), 04-bemidbar (1–36), 05-devarim (1–34)
- Nevi'im Rishonim (Korábbi Próféták – TELJESEN KÉSZ):
  - 06-yehoshua (1–24)
  - 07-shofetim (1–21)
  - 08-shmuel-alef (1–31)
  - 09-shmuel-bet (1–24)
  - 10-melakhim-alef (1–22)
  - 11-melakhim-bet (1–25 – 100%-ban befejezve és élesítve!)

6. KÖVETKEZŐ LÉPÉS
A Nevi'im Rishonim (Korábbi Próféták) lezárása után a **Nevi'im Acharonim (Későbbi Próféták)** első könyvével, **Jeshajahu (Ézsaiás)** 1. fejezetével (`~/szentiras-forditas/docs/tanakh/12-jeshajahu/01.md`) folytatjuk (új könyv indításakor az első fejezet előtt `mkdir -p` és főcím hozzáadása az `mkdocs.yml`-hez).
