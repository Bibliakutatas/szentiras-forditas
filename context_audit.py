import os
import re
from collections import defaultdict

DOCS_DIR = "docs"
OUT_FILE = "kontextus_riport.md"

def analyze_context():
    ur_groups = defaultdict(list)
    torveny_groups = defaultdict(list)
    other_items = []

    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", "audit_riport.md", OUT_FILE]:
                continue

            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                if line.startswith("### Szövegkritikai"):
                    break

                clean_line = line.strip()
                if not clean_line:
                    continue

                vers_match = re.match(r"\*\*(\d+)\.\*\*", clean_line)
                loc = f"**{filepath}** ({vers_match.group(1)}. vers)" if vers_match else f"**{filepath}** ({line_num}. sor)"

                # Zárójeles héber átírások kinyerése a sorból
                hebrew_hints = re.findall(r"\(\*([^*]+)\*\)", clean_line)
                hints_str = ", ".join(hebrew_hints) if hebrew_hints else "nincs zárójeles héber"

                # 1. 'Úr' (nagybetűvel, önálló szóként vagy ragozva: Úr, Úrnak, Úrtól, stb.)
                if re.search(r"\bÚr\w*", clean_line):
                    if any(h in hints_str.lower() for h in ["yhwh", "jahuah", "jahve"]):
                        cat = "Valószínű YHWH (zárójelben szerepel)"
                    elif any(h in hints_str.lower() for h in ["adónáj", "adonai", "adón"]):
                        cat = "Adonai / Adon (Úr/Gazda)"
                    else:
                        cat = "Egyéb / Cím / Kézi ellenőrzés"
                    ur_groups[cat].append(f"- {loc} | Héber: `[{hints_str}]`\n  > {clean_line}")

                # 2. 'törvény' (kis- és nagybetűvel, ragozva is)
                if re.search(r"\btörvény\w*", clean_line, re.IGNORECASE):
                    if any(h in hints_str.lower() for h in ["tór", "torah", "tórá"]):
                        cat = "Tóra (Tóráh) -> cserélhető Tórára"
                    elif any(h in hints_str.lower() for h in ["mishpát", "hóq", "huqq", "micv", "dát"]):
                        cat = "Más jogi fogalom (mishpát / chóq / micvá / dát)"
                    else:
                        cat = "Nincs egyértelmű héber jelölés (kézi ellenőrzés)"
                    torveny_groups[cat].append(f"- {loc} | Héber: `[{hints_str}]`\n  > {clean_line}")

                # 3. Maradék nevek és 'egyház'
                for rem in ["Egyiptom", "Dávid", "Salamon", "egyház"]:
                    if re.search(re.escape(rem), clean_line, re.IGNORECASE):
                        other_items.append(f"- `{rem}` -> {loc}: `{clean_line}`")

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        out.write("# Kontextuális Elemzés: `Úr`, `törvény` és maradék tételek\n\n")

        out.write("## 1. `törvény` előfordulások csoportosítva\n\n")
        for cat, items in sorted(torveny_groups.items(), key=lambda x: len(x[1]), reverse=True):
            out.write(f"### {cat} ({len(items)} db)\n\n")
            out.write("\n".join(items) + "\n\n")

        out.write("---\n\n## 2. `Úr` előfordulások csoportosítva\n\n")
        for cat, items in sorted(ur_groups.items(), key=lambda x: len(x[1]), reverse=True):
            out.write(f"### {cat} ({len(items)} db)\n\n")
            out.write("\n".join(items) + "\n\n")

        out.write("---\n\n## 3. Maradék nevek és `egyház` ({} db)\n\n".format(len(other_items)))
        out.write("\n".join(other_items) + "\n")

    print("--- KONTEXTUS ÖSSZESÍTŐ ---")
    print("TÖRVÉNY:")
    for cat, items in torveny_groups.items():
        print(f"  - {cat}: {len(items)} db")
    print("ÚR:")
    for cat, items in ur_groups.items():
        print(f"  - {cat}: {len(items)} db")
    print(f"MARADÉK (nevek + egyház): {len(other_items)} db")
    print(f"\nRészletes riport mentve: {OUT_FILE}")

if __name__ == "__main__":
    analyze_context()
