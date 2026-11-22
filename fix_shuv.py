import os
import re

DOCS_DIR = "docs"

SHUV_REPLACEMENTS = [
    (r"\bTérjetek meg\b", "Forduljatok vissza"),
    (r"\btérjetek meg\b", "forduljatok vissza"),
    (r"\bmegtérnek\b", "visszafordulnak"),
    (r"\bmegtértek\b", "visszafordultak"),
    (r"\bmegtérjenek\b", "visszaforduljanak"),
    (r"\bmegtérjen\b", "visszaforduljon"),
    (r"\bmegtérsz/lefekszel\b", "lefekszel"),
    (r"\bmegtérsz\b", "visszafordulsz"),
    (r"\bmegtértem\b", "visszafordultam"),
    (r"\bmegtért\b", "visszafordult"),
    (r"\bmegtérői\b", "visszafordulói"),
    (r"\bmegtér\b", "visszafordul"),
]

def fix_shuv():
    modified_files = 0
    total_changes = 0

    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", "audit_riport.md", "kontextus_riport.md"]:
                continue

            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            in_notes = False
            file_changed = False

            for line in lines:
                if line.startswith("### Szövegkritikai"):
                    in_notes = True

                if not in_notes:
                    updated_line = line
                    for pattern, replacement in SHUV_REPLACEMENTS:
                        updated_line, count = re.subn(pattern, replacement, updated_line)
                        if count > 0:
                            total_changes += count
                            file_changed = True
                    new_lines.append(updated_line)
                else:
                    new_lines.append(line)

            if file_changed:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                modified_files += 1

    print(f"Kész! {modified_files} fájlban összesen {total_changes} 'shuv' alak pontosítva.")

if __name__ == "__main__":
    fix_shuv()
