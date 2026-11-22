import os
import re

DOCS_DIR = "docs"

# Sorrend fontos: hosszabb / ragozott előtagok előre
REPLACEMENTS = [
    (r"\bEgyiptom", "Micrayim"),
    (r"\bDávid", "David"),
    (r"\bSalamon", "Shlomoh"),
    (r"\bMózes", "Moshe"),
    (r"\bÁbrahám", "Avraham"),
]

def fix_files():
    modified_files = 0
    total_changes = 0

    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", "audit_riport.md"]:
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

                if not in_notes and line.strip().startswith("**"):
                    updated_line = line
                    for pattern, replacement in REPLACEMENTS:
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

    print(f"Kész! {modified_files} fájlban összesen {total_changes} név lecserélve.")

if __name__ == "__main__":
    fix_files()
