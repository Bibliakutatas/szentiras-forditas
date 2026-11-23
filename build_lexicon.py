import os
import re
import json
from collections import defaultdict, Counter

DOCS_DIR = "docs"
LEXICON_OUT = "docs/assets/lexicon.json"

def build_lexicon():
    lexicon = defaultdict(lambda: {
        "c": 0,
        "t": Counter(),
        "r": []
    })

    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", "audit_riport.md", "kontextus_riport.md"]:
                continue

            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, DOCS_DIR).replace(".md", "")
            parts = rel_path.split(os.sep)
            book_chap = f"{parts[-2]}/{parts[-1]}" if len(parts) >= 2 else rel_path

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

                matches = re.finditer(r"([A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű\-]+\s+)?([A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű\-]+)\s*\(\*([^*]+)\*\)", clean_line)

                for m in matches:
                    prev1 = (m.group(1) or "").strip()
                    prev2 = (m.group(2) or "").strip()
                    heb_raw = m.group(3).strip()

                    if len(heb_raw) > 35 or ":" in heb_raw or "=" in heb_raw or "LXX" in heb_raw:
                        continue

                    hu_phrase = f"{prev1} {prev2}".strip()
                    entry = lexicon[heb_raw]
                    entry["c"] += 1
                    if hu_phrase:
                        entry["t"][hu_phrase] += 1
                    if len(entry["r"]) < 15 and ref not in entry["r"]:
                        entry["r"].append(ref)

    compact_lexicon = {}
    for heb, data in sorted(lexicon.items(), key=lambda x: x[1]["c"], reverse=True):
        compact_lexicon[heb] = {
            "c": data["c"],
            "t": dict(data["t"].most_common(5)),
            "r": data["r"]
        }

    with open(LEXICON_OUT, "w", encoding="utf-8") as out:
        json.dump(compact_lexicon, out, ensure_ascii=False, separators=(',', ':'))

    size_mb = os.path.getsize(LEXICON_OUT) / (1024 * 1024)
    print(f"Kész! {len(compact_lexicon)} héber kifejezés mentve ide: {LEXICON_OUT} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    build_lexicon()
