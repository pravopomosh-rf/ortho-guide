"""vcheck.py — objective check of a rendered video against its reference (approved render / timeline audio).
Usage: python3 vcheck.py test.mp4 [ref.mp4]
Reports with timecodes: black frames, frozen/silent gaps, audio deviating from reference (cut speech, doubled voice),
picture deviating from reference (mirrored frames, extra/changed text overlays)."""
import sys, subprocess, re, numpy as np

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr

def audio(path, sr=8000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768, sr

def frames(path, fps=10, w=90, h=160):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32), fps

def spans(mask, step, minlen):
    out, s = [], None
    for i, m in enumerate(list(mask) + [False]):
        if m and s is None: s = i
        if not m and s is not None:
            if (i - s) * step >= minlen: out.append((round(s * step, 1), round(i * step, 1)))
            s = None
    return out

test = sys.argv[1]; ref = sys.argv[2] if len(sys.argv) > 2 else None
rep = []
for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", run(["ffmpeg", "-i", test, "-vf", "blackdetect=d=0.1:pix_th=0.10", "-an", "-f", "null", "-"])):
    rep.append(f"ЧЁРНЫЙ КАДР {float(m[1]):.1f}–{float(m[2]):.1f} с")
if ref:
    a, sr = audio(test); b, _ = audio(ref)
    n = min(len(a), len(b)); a, b = a[:n], b[:n]
    win = sr // 10
    k = n // win
    ea = np.sqrt((a[:k*win].reshape(k, win) ** 2).mean(1)); eb = np.sqrt((b[:k*win].reshape(k, win) ** 2).mean(1))
    ed = np.sqrt(((a - b)[:k*win].reshape(k, win) ** 2).mean(1))
    lost = (eb > 0.01) & (ea < eb * 0.2)
    for s, e in spans(lost, 0.1, 0.3): rep.append(f"ПРОПАЛА РЕЧЬ {s}–{e} с (в эталоне звук есть)")
    extra = (ed > np.maximum(eb * 0.35, 0.004)) & ~lost
    for s, e in spans(extra, 0.1, 0.5): rep.append(f"ЗВУК ОТЛИЧАЕТСЯ ОТ ЭТАЛОНА {s}–{e} с (двойной голос/лишний звук)")
    fa, fps = frames(test); fb, _ = frames(ref)
    m = min(len(fa), len(fb)); fa, fb = fa[:m], fb[:m]
    d = np.abs(fa - fb).mean((1, 2))
    dm = np.abs(fa - fb[:, :, ::-1]).mean((1, 2))
    mirror = (d > 8) & (dm < d * 0.5)
    for s, e in spans(mirror, 1 / fps, 0.3): rep.append(f"КАДР ОТЗЕРКАЛЕН {s}–{e} с")
    diffpix = (np.abs(fa - fb) > 40).mean((1, 2))
    blackm = fa.mean((1, 2)) < 12
    other = (diffpix > 0.01) & ~mirror & ~blackm
    for s, e in spans(other, 1 / fps, 0.5):
        i = int((s + e) / 2 * fps); ys = np.where((np.abs(fa[i] - fb[i]) > 40).any(1))[0]
        zone = "верх" if ys.mean() < 53 else ("низ" if ys.mean() > 106 else "середина")
        rep.append(f"КАРТИНКА/НАДПИСЬ ОТЛИЧАЕТСЯ ОТ ЭТАЛОНА {s}–{e} с (зона: {zone}) — проверить текст по кадру")
print("\n".join(rep) if rep else "ЗАМЕЧАНИЙ НЕТ")
