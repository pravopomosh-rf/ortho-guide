"""Reverts any change outside the bot's allowed scope (visible text, media)."""
import subprocess, sys
from html.parser import HTMLParser

FORBIDDEN = ("video/", "media/", "qr/", "shots/")


class T(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, t, a):
        if t in ("script", "style"): self.skip += 1
    def handle_endtag(self, t):
        if t in ("script", "style") and self.skip: self.skip -= 1
    def handle_data(self, d):
        if not self.skip and d.strip(): self.out.append(" ".join(d.split()))


def text(s):
    p = T(); p.feed(s); return p.out


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout

changed = [f for f in sh("git", "diff", "--name-only").split("\n") if f]
changed += [f for f in sh("git", "ls-files", "--others", "--exclude-standard").split("\n")
            if f and not f.startswith(".github/bot/")]
reverted = []
for f in changed:
    bad = f.startswith(FORBIDDEN)
    if not bad and f.endswith(".html"):
        old = sh("git", "show", f"HEAD:{f}")
        new = open(f, encoding="utf-8").read()
        bad = text(old) != text(new)
    if bad:
        subprocess.run(["git", "checkout", "--", f]) if sh("git", "ls-files", f) else \
            subprocess.run(["rm", "-f", f])
        reverted.append(f)
with open(".github/bot/report_guard.md", "w", encoding="utf-8") as fh:
    fh.write("Откачено защитой (менялся видимый текст или медиа): "
             + (", ".join(reverted) if reverted else "ничего") + "\n")
print("reverted:", reverted)
