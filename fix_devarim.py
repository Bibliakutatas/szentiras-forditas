import os
import re
import json

DOCS_DIR = "docs"
GLOSSARY_FILE = "glossary.json"

REPLACEMENTS = [
    (r"\bTízparancsolatnak\b", "Tíz Igének"),
    (r"\bTízparancsolatot\b", "Tíz Igét"),
    (r"\bTízparancsolatban\b", "Tíz Igében"),
    (r"\bTízparancsolat\b", "Tíz Ige (*Aseret HaDevarim*)"),
]

def fix_devarim():
    modified_files = 0
    total_changes = 0

    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", "audit_riport.md", "kontextus_riport.md"]:
                continue

            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            updated = content
            file_changes = 0
            for pattern, replacement in REPLACEMENTS:
                updated, count = re.subn(pattern, replacement, updated)
                file_changes += count

            if file_changes > 0:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(updated)
                modified_files += 1
                total_changes += file_changes

    # Glossary frissitese
    if os.path.exists(GLOSSARY_FILE):
        with open(GLOSSARY_FILE, "r", encoding="utf-8") as f:
            glossary = json.load(f)
        glossary["Tízparancsolat"] = "Tíz Ige (Aseret HaDevarim)"
        with open(GLOSSARY_FILE, "w", encoding="utf-8") as f:
            json.dump(glossary, f, ensure_ascii=False, indent=2)

    print(f"Kész! {modified_files} fájlban összesen {total_changes} 'Tízparancsolat' -> 'Tíz Ige' csere történt.")

if __name__ == "__main__":
    fix_devarim()
