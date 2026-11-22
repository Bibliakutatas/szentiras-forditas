import os
import re
import json
from collections import defaultdict, Counter

DOCS_DIR = "docs"
LEXICON_OUT = "data/lexicon.json"

def build_lexicon():
    lexicon = defaultdict(lambda: {
        "count": 0,
        "hungarian_contexts": Counter(),
        "references": []
    })

    files_parsed = 0

    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", "audit_riport.md", "kontextus_riport.md"]:
                continue

            filepath = os.path.join(root, file)
            # Konyv es fejezet kinyerese az utvonalbol (pl. 01-bereshit/01)
            rel_path = os.path.relpath(filepath, DOCS_DIR).replace(".md", "")
            parts = rel_path.split(os.sep)
            book_chap = f"{parts[-2]} {parts[-1]}" if len(parts) >= 2 else rel_path

            files_parsed += 1
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                if line.startswith("### Szövegkritikai"):
                    break

                clean_line = line.strip()
                vers_match = re.match(r"\*\*(\d+)\.\*\*", clean_line)
                if not vers_match:
                    continue
                ref = f"{book_chap}:{vers_match.group(1)}"

                # Megkeressuk az osszes (elotte allo 1-2 magyar szo) + (*heber*) part
                matches = re.finditer(r"([A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű\-]+\s+)?([A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű\-]+)\s*\(\*([^*]+)\*\)", clean_line)

                for m in matches:
                    prev1 = (m.group(1) or "").strip()
                    prev2 = (m.group(2) or "").strip()
                    heb_raw = m.group(3).strip()

                    # Kiszurjuk a hosszu magyarazatokat, LXX/Ketiv blokkokat
                    if len(heb_raw) > 35 or ":" in heb_raw or "=" in heb_raw or "LXX" in heb_raw:
                        continue

                    hu_phrase = f"{prev1} {prev2}".strip()
                    entry = lexicon[heb_raw]
                    entry["count"] += 1
                    if hu_phrase:
                        entry["hungarian_contexts"][hu_phrase] += 1
                    if len(entry["references"]) < 25:  # elso 25 igehely tarolasa
                        entry["references"].append(ref)

    # Rendezes gyakorisag szerint es JSON-barat formatumra alakitas
    sorted_lexicon = {}
    for heb, data in sorted(lexicon.items(), key=lambda x: x[1]["count"], reverse=True):
        sorted_lexicon[heb] = {
            "count": data["count"],
            "top_translations": dict(data["hungarian_contexts"].most_common(5)),
            "sample_refs": data["references"]
        }

    with open(LEXICON_OUT, "w", encoding="utf-8") as out:
        json.dump(sorted_lexicon, out, ensure_ascii=False, indent=2)

    print(f"Kész! {files_parsed} fejezetből {len(sorted_lexicon)} egyedi héber kifejezés kinyerve ide: {LEXICON_OUT}")
    print("\n--- TOP 15 LEGGYAKORIBB HÉBER KIFEJEZÉS A SZÖVEGEDBEN ---")
    for heb, data in list(sorted_lexicon.items())[:15]:
        top_hu = ", ".join(list(data["top_translations"].keys())[:2])
        print(f"  {heb:<22} ({data['count']:>4}x) -> pl.: {top_hu}")

if __name__ == "__main__":
    build_lexicon()
