"""Free deterministic site checks -> .github/bot/report_checks.md"""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LANGS = ["ru", "he", "ar", "en"]
issues = []


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.langs, self.imgs_noalt, self.title = [], {}, 0, ""
        self._t = False

    def handle_starttag(self, tag, a):
        a = dict(a)
        for k in ("href", "src", "poster"):
            if a.get(k):
                self.refs.append(a[k])
        if a.get("data-l") in LANGS:
            self.langs[a["data-l"]] = self.langs.get(a["data-l"], 0) + 1
        if tag == "img" and not a.get("alt"):
            self.imgs_noalt += 1
        if tag == "title":
            self._t = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False

    def handle_data(self, d):
        if self._t:
            self.title += d


pages = [os.path.join(dp, f) for dp, _, fs in os.walk(ROOT)
         if "/.git" not in dp and "/.github" not in dp
         for f in fs if f.endswith(".html")]
for path in sorted(pages):
    rel = os.path.relpath(path, ROOT)
    html = open(path, encoding="utf-8").read()
    p = P()
    p.feed(html)
    kb = len(html.encode()) // 1024
    if kb > 150:
        issues.append(f"{rel}: страница {kb} КБ (тяжело для телефона)")
    if not p.title.strip():
        issues.append(f"{rel}: нет <title>")
    counts = [p.langs.get(l, 0) for l in LANGS]
    if len(set(counts)) > 1:
        issues.append(f"{rel}: разное число языковых блоков ru/he/ar/en = {counts}")
    if p.imgs_noalt:
        issues.append(f"{rel}: {p.imgs_noalt} картинок без alt")
    for r in p.refs:
        u = urlparse(r)
        if u.scheme or r.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
            continue
        f = unquote(u.path)
        if not f:
            continue
        tgt = os.path.normpath(os.path.join(os.path.dirname(path), f))
        if not os.path.exists(tgt):
            issues.append(f"{rel}: битая ссылка → {r}")

for dp, _, fs in os.walk(os.path.join(ROOT, "video")):
    for f in fs:
        mb = os.path.getsize(os.path.join(dp, f)) / 1e6
        if mb > 25:
            issues.append(f"video/{f}: {mb:.0f} МБ (долго грузится)")

out = os.path.join(os.path.dirname(__file__), "report_checks.md")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(f"# Автопроверки: {len(issues)} замечаний, страниц {len(pages)}\n\n")
    fh.write("\n".join(f"- {i}" for i in issues) or "- замечаний нет")
    fh.write("\n")
print(f"{len(issues)} issues -> {out}")
