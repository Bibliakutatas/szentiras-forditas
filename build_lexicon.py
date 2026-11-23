import os, re, json, unicodedata
from collections import defaultdict, Counter

DOCS_DIR = "docs"
LEXICON_OUT = "docs/assets/lexicon.json"
STRONGS_CACHE = "data/strongs-hebrew-dictionary.js"

def load_strongs():
    with open(STRONGS_CACHE, "r", encoding="utf-8") as f:
        raw = f.read()
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])

def norm_phon(text):
    t = "".join(c for c in unicodedata.normalize("NFD", text.lower().strip()) if unicodedata.category(c) != "Mn")
    t = t.replace("sz", "s").replace("cs", "ch").replace("kh", "k").replace("ch", "h").replace("tz", "ts").replace("c", "ts").replace("j", "y").replace("v", "w")
    return re.sub(r"[^a-z]", "", t)

def build_lexicon():
    strongs_db = load_strongs()
    lookup = {}
    for code, entry in strongs_db.items():
        defn = entry.get("strongs_def", "").strip()
        info = {"s": code, "h": entry.get("lemma", ""), "d": defn[:107] + "..." if len(defn) > 110 else defn}
        for v in [entry.get("xlit", ""), entry.get("pron", "")]:
            n = norm_phon(v)
            if n and n not in lookup:
                lookup[n] = info

    prefixes = ("va", "ve", "vi", "ha", "he", "ho", "ba", "be", "bi", "la", "le", "li", "ma", "me", "mi", "u", "ki", "el")
    def match_strong(heb):
        for cand in [heb] + [p for p in re.split(r"[\s\-]+", heb) if len(p) > 1]:
            n = norm_phon(cand)
            if n in lookup: return lookup[n]
            for pref in prefixes:
                if n.startswith(pref) and len(n) - len(pref) >= 3 and n[len(pref):] in lookup:
                    return lookup[n[len(pref):]]
        return None

    lexicon = defaultdict(lambda: {"c": 0, "t": Counter(), "r": []})
    for root, _, files in os.walk(DOCS_DIR):
        for file in sorted(files):
            if not file.endswith(".md") or file in ["index.md", "audit_riport.md", "kontextus_riport.md"]: continue
            filepath = os.path.join(root, file)
            parts = os.path.relpath(filepath, DOCS_DIR).replace(".md", "").split(os.sep)
            book_chap = f"{parts[-2]}/{parts[-1]}" if len(parts) >= 2 else parts[0]
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("### Szövegkritikai"): break
                    vm = re.match(r"\*\*(\d+)\.\*\*", line.strip())
                    if not vm: continue
                    ref = f"{book_chap}:{vm.group(1)}"
                    for m in re.finditer(r"\(\*([^*]+)\*\)", line):
                        heb = m.group(1).strip()
                        if len(heb) <= 1 or len(heb) > 35 or ":" in heb or "=" in heb or "LXX" in heb: continue
                        words = [w for w in re.sub(r"\*\*|\(\*[^*]+\*\)|[^\w\sÁÉÍÓÖŐÚÜŰáéíóöőúüű\-]", " ", line[:m.start()]).split() if not w.isdigit()]
                        hu = " ".join(words[-2:]) if len(words) >= 2 else (words[-1] if words else "")
                        lexicon[heb]["c"] += 1
                        if hu: lexicon[heb]["t"][hu] += 1
                        if len(lexicon[heb]["r"]) < 15 and ref not in lexicon[heb]["r"]: lexicon[heb]["r"].append(ref)

    out_db, matched = {}, 0
    for heb, d in sorted(lexicon.items(), key=lambda x: x[1]["c"], reverse=True):
        item = {"c": d["c"], "t": dict(d["t"].most_common(5)), "r": d["r"]}
        s = match_strong(heb)
        if s: item.update(s); matched += 1
        out_db[heb] = item

    with open(LEXICON_OUT, "w", encoding="utf-8") as out:
        json.dump(out_db, out, ensure_ascii=False, separators=(',', ':'))
    print(f"Kész! {len(out_db)} kifejezés mentve, ebből {matched} összekötve Strong's kóddal!")

if __name__ == "__main__":
    build_lexicon()
