# Projekt Emlékeztető – A Bibliát Kutatom (Szöveghű Fordítás)

**Utolsó frissítés:** 2026. november 25.

## 1. Jelenlegi készültségi állapot
* **Tanakh (Ószövetség):** 100% kész (Torah, Nevi'im, K'tuvim – beleértve a 151. zsoltárt).
* **Brit Chadashah (Újszövetség):**
  * **Mattitjáhú (Máté) 1–28. fejezet:** Kész, auditálva és publikálva.
  * **Markus (Márk) 1–16. fejezet:** Teljes egészében kész, szövegkritikai/Tóra-jogi elemzésekkel ellátva, auditálva és publikálva.
* **Következő lépés:** **Lukas (Lukács) 1. fejezet** (`docs/brit-chadashah/03-lukas/01.md`) elindítása.

## 2. Mai technikai és szövegkritikai finomítások
* **Audit-szigorítás (`audit.py` + `glossary.json`):**
  * Bővítve a `Tízparancsolat` / `tízparancsolat` / `tizparancsolat` / `Dekalógus` → **Tíz Ige** (*Aseret HaDevarim*) tiltással.
  * Kiszűrve a zárójeles héber fonetika `(*...*)`, a szögletes jegyzetek `[...]`, valamint a legitim `Adonaj` (*Szuverén Úr*) és világi törvény (`dát`, `chók`, `mishpat`) alakok.
  * A teljes meglévő korpusz (974+ fájl) megtisztítva.

## 3. Kötelező munkamódszer a következő munkamenethez
1. **Zsinórmérték:** Kizárólag a leírt Ige (`MESTER_UTASITAS.md`), dogmatikus sallangok nélkül, Tóra-jogi (*halakhikus*) és szövegkritikai elemzéssel.
2. **Névhasználat:** **YHWH**, **Elohim**, **Yehoshua**, **Moshe**, **David**, **Shlomoh**, **Avraham**, **Ja'akov**, **Yisrael**, **Yehudah**, **Yerushalayim**, **Cijon**, **Micrayim**, **Kefa**, **Yochanan**, **Mirjam**.
3. **Kulcsfogalmak:** **Tóra** (nem „törvény”, ha *Torah*), **Tíz Ige** (nem „Tízparancsolat”), **bemerítkezés** (*tevilah* / *baptizō*), **visszafordulás / szemléletváltás** (*shuv* / *metanoia*), **kihívott közösség** (*ekklēsia*).
4. **Kimeneti formátum:** Hosszú fejezeteket mindig **2–3 kompakt bash kódblokkra** bontva (`cat > ...` + `cat >> ...` + `mkdocs.yml` / `docs/index.md` regisztráció + `python3 audit.py && ./frissit.sh`), hogy ne vágódjon el a terminálban.
