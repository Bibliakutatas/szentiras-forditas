import os
import json
import re
from collections import defaultdict

DOCS_DIR = "docs"
GLOSSARY_FILE = "glossary.json"
REPORT_FILE = "audit_riport.md"

def run_audit():
    with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
        glossary = json.load(f)

    grouped_findings = defaultdict(list)
    files_checked = 0

    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", REPORT_FILE]:
                continue

            filepath = os.path.join(root, file)
            files_checked += 1

            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                if line.startswith("### Szövegkritikai"):
                    break

                for bad_term, suggestion in glossary.items():
                    if re.search(re.escape(bad_term), line, re.IGNORECASE):
                        vers_match = re.match(r"\*\*(\d+)\.\*\*", line.strip())
                        vers = f"{vers_match.group(1)}. vers" if vers_match else f"{line_num}. sor"
                        clean_term = bad_term.strip()
                        grouped_findings[clean_term].append(
                            f"  - **{filepath}** ({vers}): `{line.strip()[:100]}...`"
                        )

    total_findings = sum(len(items) for items in grouped_findings.values())

    with open(REPORT_FILE, "w", encoding="utf-8") as out:
        out.write("# Csoportosított Szöveghűségi Audit Riport\n\n")
        out.write(f"Átvizsgált fejezetek: **{files_checked}** | Összes találat: **{total_findings}**\n\n")
        
        out.write("## Összesítő táblázat\n\n")
        out.write("| Talált kifejezés | Darabszám | Javasolt irány / csere |\n")
        out.write("| :--- | :---: | :--- |\n")
        
        sorted_terms = sorted(grouped_findings.items(), key=lambda x: len(x[1]), reverse=True)
        for term, items in sorted_terms:
            suggestion = next((v for k, v in glossary.items() if k.strip() == term), "")
            out.write(f"| `{term}` | **{len(items)}** | {suggestion} |\n")
        
        out.write("\n---\n\n## Részletes lista kifejezésenként\n\n")
        for term, items in sorted_terms:
            out.write(f"### `{term}` ({len(items)} találat)\n\n")
            out.write("\n".join(items))
            out.write("\n\n")

    print("\n--- ÖSSZESÍTŐ ---")
    for term, items in sorted_terms:
        print(f"  {term:<18}: {len(items)} db")
    print(f"\nÖsszesen: {total_findings} találat mentve ide: {REPORT_FILE}")

if __name__ == "__main__":
    run_audit()
