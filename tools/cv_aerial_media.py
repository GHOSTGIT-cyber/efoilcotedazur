#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a self-contained, SOLAR-graded curated AERIAL webp library for the
   Croix-Valmer landings, sourced from efca-photo-tri.json (packs: top, aerien,
   sunset, lieu — NO 'rider'/'proscrire'/COMO-hotel). Output -> medias/web/cv/."""
import os, json
from PIL import Image, ImageOps, ImageEnhance, ImageStat

OUT = "medias/web/cv"
os.makedirs(OUT, exist_ok=True)

# Curated aerial / scenic sources (no classic rider close-ups, no COMO hotel rooms).
CURATED = [
    "medias/video-frames/drone/aw-040.2.jpg",
    "medias/video-frames/drone/aw-035.4.jpg",
    "medias/video-frames/drone/aw-018.6.jpg",
    "medias/video-frames/drone/aw-023.4.jpg",
    "medias/video-frames/drone/aw-017.0.jpg",
    "medias/video-frames/auto/ve-39.jpg",
    "medias/video-frames/auto/to-08.jpg",
    "medias/video-frames/auto/to-02.jpg",
    "medias/video-frames/auto/fo-05.jpg",
    "medias/video-frames/auto/aw-38.jpg",
    "medias/video-frames/auto/res-57.jpg",
    "medias/video-frames/auto/res-39.jpg",
    "medias/video-frames/auto/res-33.jpg",
    "medias/video-frames/auto/aw-10.jpg",
    "medias/video-frames/auto/aw-14.jpg",
    "medias/video-frames/auto/aw-30.jpg",
    "medias/video-frames/auto/aw-34.jpg",
    "medias/video-frames/auto/aw-42.jpg",
    "medias/video-frames/auto/pu-14.jpg",
    "medias/video-frames/auto/res-63.jpg",
    "medias/video-frames/auto/aw-02.jpg",
    "medias/video-frames/auto/aw-22.jpg",
    "medias/video-frames/auto/res-09.jpg",
    "medias/video-frames/auto/aw-58.jpg",
    "medias/video-frames/auto/ve-03.jpg",
    "medias/video-frames/awaking-65.jpg",
    "medias/cannes/Cannes_Cote-85.jpg",
    "medias/cannes/Cannes_Cote-53.jpg",
    "medias/cannes/Cannes_Cote-155.jpg",
    "medias/cannes/Cannes_Cote-57.jpg",
    "medias/cannes/Cannes_Cote-61.jpg",
    "medias/cannes/Cannes_Cote-58.jpg",
    "medias/cannes/Cannes_Cote-56.jpg",
    "medias/cannes/Cannes_Cote-83.jpg",
    "medias/cannes/Cannes_Cote-118.jpg",
    "medias/saint-tropez/Stropez_day2-7.jpg",
    "medias/saint-tropez/Stropez_day2-11.jpg",
]

# Hero crops (16:9 landscape, 1920) — one per edition, distinct mood.
HEROES = {
    "hero-orange": ("medias/video-frames/awaking-65.jpg", (16, 9), 1920, 0.46),  # golden hour
    "hero-bleu":   ("medias/video-frames/auto/to-08.jpg", (16, 9), 1920, 0.42),  # clear turquoise
    "hero-como":   ("medias/video-frames/drone/aw-035.4.jpg", (16, 9), 1920, 0.40),  # wild crique
    "hero-orange-v":("medias/video-frames/drone/aw-040.2.jpg", (9, 16), 1280, 0.4),  # mobile 9:16
    "hero-bleu-v":  ("medias/video-frames/auto/ve-39.jpg", (9, 16), 1280, 0.4),
    "hero-como-v":  ("medias/video-frames/drone/aw-018.6.jpg", (9, 16), 1280, 0.4),
}

def load(p):
    return ImageOps.exif_transpose(Image.open(p).convert("RGB"))

def solar_grade(im):
    """Bright, clean, realistic turquoise — Mediterranean noon, NOT warm/tropical."""
    # neutralise slight warm cast, keep blues honest
    r, g, b = im.split()
    r = r.point(lambda v: max(0, int(v * 0.985)))
    b = b.point(lambda v: min(255, int(v * 1.015 + 1)))
    im = Image.merge("RGB", (r, g, b))
    im = ImageEnhance.Color(im).enhance(1.07)       # vivid but real
    im = ImageEnhance.Contrast(im).enhance(1.045)
    im = ImageEnhance.Brightness(im).enhance(1.025) # solar, clear
    return im

def crop_ratio(im, ratio, vf=0.5, hf=0.5):
    W, H = im.size; rw, rh = ratio; tr = rw / rh; cur = W / H
    if cur > tr:
        nw, nh = int(round(H * tr)), H
    else:
        nw, nh = W, int(round(W / tr))
    x = int((W - nw) * hf); y = int((H - nh) * vf)
    return im.crop((x, y, x + nw, y + nh))

def save_webp(im, name, q=82):
    path = os.path.join(OUT, name + ".webp")
    im.save(path, "WEBP", quality=q, method=6)
    return path, im.size

# --- gallery library (native ratio, max 1600 wide) ---
n = 0
manifest = {"aer": [], "hero": {}}
for src in CURATED:
    if not os.path.exists(src):
        print("  skip missing", src); continue
    im = solar_grade(load(src))
    if im.width > 1600:
        im = im.resize((1600, int(round(im.height * 1600 / im.width))), Image.LANCZOS)
    n += 1
    name = "aer-%02d" % n
    _, (w, h) = save_webp(im, name)
    manifest["aer"].append({"name": name, "w": w, "h": h, "src": src})
print("aerial gallery frames:", n)

# --- heroes (cropped) ---
for name, (src, ratio, tw, vf) in HEROES.items():
    if not os.path.exists(src):
        print("  skip hero missing", src); continue
    im = solar_grade(load(src))
    im = crop_ratio(im, ratio, vf=vf)
    th = int(round(tw * ratio[1] / ratio[0]))
    im = im.resize((tw, th), Image.LANCZOS)
    _, (w, h) = save_webp(im, name, q=84)
    manifest["hero"][name] = {"w": w, "h": h}
    print("  hero", name, w, h)

with open(os.path.join(OUT, "_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)
print("done ->", OUT)
