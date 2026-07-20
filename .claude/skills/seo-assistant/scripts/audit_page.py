#!/usr/bin/env python3
"""Bir URL'nin statik HTML'inden temel SEO sinyallerini çıkarır.
Kullanım: python3 audit_page.py <URL>
Not: JavaScript ile sonradan render edilen (client-side rendered) sayfalarda
bazı sinyaller (özellikle içerik/kelime sayısı) eksik/yanlış çıkabilir.
"""

import sys
import re
import json
import urllib.request
import urllib.error
from html.parser import HTMLParser


class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.meta_description = None
        self.canonical = None
        self.robots_meta = None
        self.h1_list = []
        self.h_counts = {"h1": 0, "h2": 0, "h3": 0, "h4": 0, "h5": 0, "h6": 0}
        self.images = []
        self.viewport = None
        self.hreflangs = []
        self.json_ld_count = 0
        self.word_count = 0

        self._in_title = False
        self._in_h = None
        self._in_script_jsonld = False
        self._text_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (attrs_dict.get("name") or "").lower()
            prop = (attrs_dict.get("property") or "").lower()
            if name == "description":
                self.meta_description = attrs_dict.get("content", "")
            elif name == "robots":
                self.robots_meta = attrs_dict.get("content", "")
            elif name == "viewport":
                self.viewport = attrs_dict.get("content", "")
        elif tag == "link":
            rel = (attrs_dict.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = attrs_dict.get("href")
            elif rel == "alternate" and attrs_dict.get("hreflang"):
                self.hreflangs.append(attrs_dict.get("hreflang"))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.h_counts[tag] += 1
            self._in_h = tag
        elif tag == "img":
            alt = attrs_dict.get("alt")
            src = attrs_dict.get("src", "")
            self.images.append({"src": src, "has_alt": bool(alt and alt.strip())})
        elif tag == "script":
            script_type = (attrs_dict.get("type") or "").lower()
            if script_type == "application/ld+json":
                self.json_ld_count += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._in_h = None

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_h == "h1":
            self.h1_list.append(data.strip())
        stripped = data.strip()
        if stripped:
            self.word_count += len(stripped.split())


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (SEO-Audit-Skill)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        status = resp.status
        content_type = resp.headers.get("Content-Type", "")
        raw = resp.read()
    encoding = "utf-8"
    m = re.search(r"charset=([\w-]+)", content_type)
    if m:
        encoding = m.group(1)
    try:
        html = raw.decode(encoding, errors="replace")
    except LookupError:
        html = raw.decode("utf-8", errors="replace")
    return status, html


def audit(url):
    try:
        status, html = fetch(url)
    except urllib.error.HTTPError as e:
        return {"url": url, "error": f"HTTP hatası: {e.code} {e.reason}"}
    except urllib.error.URLError as e:
        return {"url": url, "error": f"Bağlantı hatası: {e.reason}"}
    except Exception as e:
        return {"url": url, "error": f"Beklenmeyen hata: {e}"}

    parser = SEOParser()
    parser.feed(html)

    title = (parser.title or "").strip()
    meta_desc = (parser.meta_description or "").strip()
    images_missing_alt = [img["src"] for img in parser.images if not img["has_alt"]]

    result = {
        "url": url,
        "http_status": status,
        "title": {
            "text": title,
            "length": len(title),
            "in_range_50_60": 50 <= len(title) <= 60,
        },
        "meta_description": {
            "text": meta_desc,
            "length": len(meta_desc),
            "in_range_150_160": 150 <= len(meta_desc) <= 160,
            "present": bool(meta_desc),
        },
        "canonical": parser.canonical,
        "robots_meta": parser.robots_meta,
        "viewport_present": bool(parser.viewport),
        "heading_counts": parser.h_counts,
        "h1_count_ok": parser.h_counts["h1"] == 1,
        "h1_texts": parser.h1_list,
        "images_total": len(parser.images),
        "images_missing_alt_count": len(images_missing_alt),
        "images_missing_alt_examples": images_missing_alt[:5],
        "hreflang_tags": parser.hreflangs,
        "json_ld_blocks_found": parser.json_ld_count,
        "approx_word_count": parser.word_count,
    }
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 audit_page.py <URL>")
        sys.exit(1)
    target_url = sys.argv[1]
    output = audit(target_url)
    print(json.dumps(output, ensure_ascii=False, indent=2))
