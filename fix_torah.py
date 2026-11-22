import os
import re

DOCS_DIR = "docs"

# Csak ott cserel, ahol kozvetlenul utana (*...Torah...*) all
TORAH_PATTERNS = [
    (r"\btörvénye(\s*\(\*[^*]*Torah[^*]*\*\))", r"Tórája\1"),
    (r"\btörvényt(\s*\(\*[^*]*Torah[^*]*\*\))", r"Tórát\1"),
    (r"\btörvény(\s*\(\*[^*]*Torah[^*]*\*\))", r"Tóra\1"),
]

def fix_torah():
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

            for line_num, line in enumerate(lines, 1):
                if line.startswith("### Szövegkritikai"):
                    in_notes = True

                if not in_notes:
                    if re.search(r"egyház", line, re.IGNORECASE):
                        print(f"[EGYHÁZ TALÁLAT] {filepath} ({line_num}. sor): {line.strip()}")

                    updated_line = line
                    for pattern, replacement in TORAH_PATTERNS:
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

    print(f"Kész! {modified_files} fájlban összesen {total_changes} 'törvény (*Torah*)' -> 'Tóra' csere történt.")

if __name__ == "__main__":
    fix_torah()
