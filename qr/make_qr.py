"""QR codes for the patient site.

Usage:  python3 qr/make_qr.py [BASE]
BASE defaults to https://pravopomosh-rf.github.io/ortho-guide

Creates:
  qr/<op>.png            -> page without a language (opens in the visitor's last language, default Hebrew)
  qr/<lang>/<op>.png     -> page opened directly in he / ar / ru / en
  qr/links.csv           -> every link, for checking and printing
"""
import csv, os, sys
import qrcode

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://pravopomosh-rf.github.io/ortho-guide").rstrip("/")
OPS = ["thr", "thr-anterior", "tkr", "hip-fracture", "kyphoplasty", "laminectomy",
       "fusion-discectomy", "spine-other", "preop", "postop", "after-surgery", "why-wait", "ankle-fracture", "knee-arthroscopy", "osteosynthesis", "enoxaparin-injections", "amputation", "shoulder-fracture", "wrist-fracture", "delirium", "falls", "pain"]
LANGS = ["he", "ar", "ru", "en"]
HERE = os.path.dirname(os.path.abspath(__file__))


def save(url, path):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    q.add_data(url)
    q.make(fit=True)
    q.make_image(fill_color="black", back_color="white").save(path)


rows = []
for op in OPS:
    url = f"{BASE}/ops/{op}.html"
    save(url, os.path.join(HERE, f"{op}.png"))
    rows.append([op, "", url, f"{op}.png"])
    for lang in LANGS:
        os.makedirs(os.path.join(HERE, lang), exist_ok=True)
        u = f"{url}#lang={lang}"
        save(u, os.path.join(HERE, lang, f"{op}.png"))
        rows.append([op, lang, u, f"{lang}/{op}.png"])

with open(os.path.join(HERE, "links.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["page", "lang", "url", "file"])
    w.writerows(rows)
print(len(rows), "QR codes ->", HERE)
