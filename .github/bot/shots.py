"""Phone screenshots of a rotating subset of pages (4 pages x 4 langs per run)."""
import datetime, glob, os
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(os.path.dirname(__file__), "shots")
os.makedirs(OUT, exist_ok=True)
pages = ["index.html"] + sorted(os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/ops/*.html"))
day = datetime.date.today().toordinal()
pick = [pages[(day * 4 + i) % len(pages)] for i in range(4)]
if "index.html" not in pick:
    pick[0] = "index.html"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1,
                        is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    for rel in pick:
        for l in ["ru", "he", "ar", "en"]:
            pg.goto(f"file://{ROOT}/{rel}#lang={l}")
            pg.evaluate(f"window.setL && setL('{l}')")
            pg.wait_for_timeout(1500)
            name = rel.replace("/", "_").replace(".html", "")
            pg.screenshot(path=f"{OUT}/{name}_{l}.png", full_page=True)
    b.close()
print("shots:", pick)
