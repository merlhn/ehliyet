#!/usr/bin/env python3
"""
Ehliyet.digital MCP veri dosyalarini olusturur.
questions-{1..4}.js, hap-bilgiler ve ders sayfalarindan JSON cikarir.
"""
import json
import os
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "mcp" / "data"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1) questions.json
# ---------------------------------------------------------------------------

def parse_questions():
    all_questions = []
    for i in range(1, 5):
        js_path = ROOT / "assets" / "js" / f"questions-{i}.js"
        text = js_path.read_text(encoding="utf-8")
        exam_name = f"Sinav {i}"

        # Extract exam name from comment line
        m = re.search(r'//.*?—\s*(Sınav \d+)', text)
        if m:
            exam_name = m.group(1)

        # Find each question block: { n:NN, ... }
        # We need to handle nested braces for media objects etc.
        # Strategy: find each "{ n:" start, then match balanced braces
        pattern = re.compile(r'\{\s*n\s*:\s*(\d+)')
        positions = [m.start() for m in pattern.finditer(text)]

        for pos_idx, start_pos in enumerate(positions):
            # Find end: next question start or end of array
            if pos_idx + 1 < len(positions):
                end_region = positions[pos_idx + 1]
            else:
                end_region = len(text)

            block = text[start_pos:end_region]

            # Extract n
            n_match = re.search(r'n\s*:\s*(\d+)', block)
            n = int(n_match.group(1)) if n_match else pos_idx + 1

            # Extract section
            sec_match = re.search(r'section\s*:\s*"([^"]+)"', block)
            section = sec_match.group(1) if sec_match else "Bilinmeyen"

            # Extract stem (backtick string)
            stem_match = re.search(r'stem\s*:\s*`((?:[^`\\]|\\[`\\])*)`', block)
            stem = stem_match.group(1).strip() if stem_match else ""

            # Extract options array of backtick strings
            opts_match = re.search(r'options\s*:\s*\[(.*?)\]', block, re.DOTALL)
            options = []
            if opts_match:
                opts_text = opts_match.group(1)
                options = re.findall(r'`((?:[^`\\]|\\[`\\])*)`', opts_text)
                options = [o.strip() for o in options]

            # Extract correct index
            corr_match = re.search(r'correct\s*:\s*(\d+)', block)
            correct_idx = int(corr_match.group(1)) if corr_match else 0

            # Detect image/video
            has_image = bool(re.search(r'media\s*:\s*\{', block) or
                           re.search(r'optionImages\s*:', block))

            letters = ["A", "B", "C", "D"]
            correct_letter = letters[correct_idx] if correct_idx < len(letters) else "?"
            correct_text = options[correct_idx] if correct_idx < len(options) else ""

            # Format options with letters
            labeled_options = []
            for oi, opt in enumerate(options):
                letter = letters[oi] if oi < len(letters) else "?"
                labeled_options.append(f"{letter}) {opt}")

            q_id = f"sinav{i}-q{n:02d}"

            all_questions.append({
                "id": q_id,
                "exam": exam_name,
                "section": section,
                "stem": stem,
                "options": labeled_options,
                "correct_index": correct_idx,
                "correct_letter": correct_letter,
                "correct_text": correct_text,
                "has_image": has_image,
            })

    return all_questions


# ---------------------------------------------------------------------------
# 2) quick-facts.json — hap bilgiler
# ---------------------------------------------------------------------------

class HapParser(HTMLParser):
    """Extract facts from hap-bilgiler pages.
    Facts are in <div class="hap"><a class="hap-num">...</a><span>FACT</span></div>
    (hap-num was a <span> before the per-fact pages; both forms are accepted).
    """
    def __init__(self):
        super().__init__()
        self.facts = []
        self._in_hap = False
        self._in_num = False
        self._in_fact_span = False
        self._span_count = 0
        self._current_text = []
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        if tag == "div" and "hap" in cls.split() and "hap-list" not in cls:
            self._in_hap = True
            self._span_count = 0
        elif self._in_hap and "hap-num" in cls.split():
            self._in_num = True
        elif self._in_hap and tag == "span" and not self._in_num:
            self._in_fact_span = True
            self._current_text = []

    def handle_endtag(self, tag):
        if tag in ("span", "a") and self._in_num:
            self._in_num = False
        elif tag == "span" and self._in_fact_span:
            self._in_fact_span = False
            fact_text = "".join(self._current_text).strip()
            if fact_text:
                self.facts.append(fact_text)
        elif tag == "div" and self._in_hap:
            self._in_hap = False
            self._span_count = 0

    def handle_data(self, data):
        if self._in_fact_span:
            self._current_text.append(data)

    def handle_entityref(self, name):
        if self._in_fact_span:
            self._current_text.append(f"&{name};")


def parse_quick_facts():
    section_map = {
        "ilk-yardim": "İlk Yardım",
        "trafik-ve-cevre": "Trafik ve Çevre",
        "arac-teknigi": "Araç Tekniği",
        "trafik-adabi": "Trafik Adabı",
    }
    all_facts = []
    hap_dir = ROOT / "hap-bilgiler"
    for slug, section in section_map.items():
        page = hap_dir / slug / "index.html"
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8")
        parser = HapParser()
        parser.feed(html)
        for fact in parser.facts:
            all_facts.append({"section": section, "fact": fact})
    return all_facts


# ---------------------------------------------------------------------------
# 3) lesson-summaries.json — atomik bloklar
# ---------------------------------------------------------------------------

class AtomikParser(HTMLParser):
    """Extract <li> items from <ul class="atomik"> blocks."""
    def __init__(self):
        super().__init__()
        self.facts = []
        self._in_atomik = False
        self._in_li = False
        self._current_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")
        if tag == "ul" and "atomik" in cls.split():
            self._in_atomik = True
        elif self._in_atomik and tag == "li":
            self._in_li = True
            self._current_text = []

    def handle_endtag(self, tag):
        if tag == "li" and self._in_li:
            self._in_li = False
            text = "".join(self._current_text).strip()
            if text:
                self.facts.append(text)
        elif tag == "ul" and self._in_atomik:
            self._in_atomik = False

    def handle_data(self, data):
        if self._in_li and self._in_atomik:
            self._current_text.append(data)

    def handle_entityref(self, name):
        if self._in_li and self._in_atomik:
            self._current_text.append(f"&{name};")


def extract_lesson_title(html):
    """Extract <h1> content from lesson page."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        # Strip HTML tags from h1 content
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return ""


def parse_lesson_summaries():
    section_map = {
        "ilk-yardim": "İlk Yardım",
        "trafik-ve-cevre": "Trafik ve Çevre",
        "arac-teknigi": "Araç Tekniği",
        "trafik-adabi": "Trafik Adabı",
    }
    all_lessons = []
    dersler_dir = ROOT / "dersler"
    for slug, section in section_map.items():
        section_dir = dersler_dir / slug
        if not section_dir.exists():
            continue
        for lesson_dir in sorted(section_dir.iterdir()):
            page = lesson_dir / "index.html"
            if not page.is_file():
                continue
            if lesson_dir.name == slug:
                continue  # skip section index
            html = page.read_text(encoding="utf-8")
            title = extract_lesson_title(html)
            if not title:
                title = lesson_dir.name.replace("-", " ").title()

            parser = AtomikParser()
            parser.feed(html)
            if not parser.facts:
                continue

            url = f"/dersler/{slug}/{lesson_dir.name}/"
            all_lessons.append({
                "section": section,
                "lesson": title,
                "url": url,
                "facts": parser.facts,
            })
    return all_lessons


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Sorular ayiklaniyor...")
    questions = parse_questions()
    q_path = OUT / "questions.json"
    q_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {len(questions)} soru -> {q_path}")

    print("Hap bilgiler ayiklaniyor...")
    facts = parse_quick_facts()
    f_path = OUT / "quick-facts.json"
    f_path.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {len(facts)} bilgi -> {f_path}")

    print("Ders ozetleri ayiklaniyor...")
    lessons = parse_lesson_summaries()
    l_path = OUT / "lesson-summaries.json"
    l_path.write_text(json.dumps(lessons, ensure_ascii=False, indent=2), encoding="utf-8")
    total_facts = sum(len(ls["facts"]) for ls in lessons)
    print(f"  {len(lessons)} ders, {total_facts} bilgi -> {l_path}")

    print("Tamamlandi.")
