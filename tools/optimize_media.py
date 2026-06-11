#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Optimise les photos (et images extraites des vidéos) en derivés web WebP recadrés
par slot, pour la landing eFoil COMO Le Beauvallon.

- Applique un grade chaud SUBTIL aux photos plein-jour/froides (grade=1) pour les
  unifier avec les plans golden-hour, sans gros filtre orange.
- Les plans déjà chauds (COMO, couchers de soleil) ne sont PAS gradés (grade=0).

Usage : python tools/optimize_media.py    (Pillow requis ; pas de dépendance vidéo)
"""
import os
from PIL import Image, ImageOps, ImageEnhance

os.makedirs('medias/web', exist_ok=True)
M = 'medias'

SRC = {
    # eFoil — golfe / Beauvallon
    'ST7':   f'{M}/saint-tropez/Stropez_day2-7.jpg',
    'ST11':  f'{M}/saint-tropez/Stropez_day2-11.jpg',
    'BVland':f'{M}/como-beauvallon/a715426f-04a3-4407-abce-65a7dffb1f08.JPG',
    'BVp1':  f'{M}/como-beauvallon/6f9dea10-981b-4b23-8fde-4a21f87acd52.JPG',
    'BVp2':  f'{M}/como-beauvallon/19a1d93b-24c7-4ce7-8e34-fc634e6ce764.JPG',
    'LER26': f'{M}/iles-lerins/Post_4x5-26_First.jpg',
    'LER25': f'{M}/iles-lerins/Post_4x5-25_Secondd.jpg',
    'EST5':  f'{M}/esterel/Post_4x5-5.jpg',
    'CAN2':  f'{M}/cannes/Cannes_Cote-2.jpg',
    'CANday':f'{M}/cannes/Cannes_day1-2.jpg',
    'CAN99': f'{M}/cannes/Cannes_Cote-99.jpg',
    'CAN103':f'{M}/cannes/Cannes_Cote-103.jpg',
    'CAN167':f'{M}/cannes/Cannes_Cote-167.jpg',
    'CAN172':f'{M}/cannes/Cannes_Cote-172.jpg',
    'CAN161':f'{M}/cannes/Cannes_Cote-161.jpg',
    # COMO officiel (comohotels.com — droits à clearer avant prod)
    'CO_grandevue':f'{M}/como-web/raw/hero.jpg',
    'CO_chateau':  f'{M}/como-web/raw/location.jpg',
    'CO_parasols': f'{M}/como-web/raw/exp2.jpg',
    'CO_loungers': f'{M}/como-web/raw/exp1.jpg',
    # images extraites des vidéos
    'VF_sunset': f'{M}/video-frames/awaking-sunset-hi.jpg',
    'VF_cannes': f'{M}/video-frames/puerto-cannes-hi.jpg',
    'VF_esterel':f'{M}/video-frames/torre-esterel-hi.jpg',
}

def warm_grade(im):
    """Grade chaud cinématique SUBTIL (unifie le plein-jour, pas un filtre orange)."""
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.045 + 3)))
    b = b.point(lambda v: max(0, int(v * 0.95 - 1)))
    im = Image.merge('RGB', (r, g, b))
    im = ImageEnhance.Color(im).enhance(0.90)      # -10 % saturation
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Brightness(im).enhance(1.015)
    return im

# (out, srckey, (rw,rh), largeur, vfocus, hfocus, grade)
JOBS = [
    # HÉROS
    ('hero-sunset','ST7',(16,9),1920,.60,.5,0),
    ('hero-grandevue','CO_grandevue',(16,9),1920,.5,.5,0),
    ('hero-formation','CAN167',(16,9),1920,.5,.5,1),
    # LIEU (château / domaine COMO)
    ('lieu-chateau','CO_chateau',(4,3),1280,.42,.5,0),
    ('lieu-grandevue','CO_grandevue',(4,3),1280,.5,.5,0),
    # BEACH CLUB COMO (parasols / transats)
    ('beach-parasols','CO_parasols',(16,9),1280,.5,.5,0),
    ('beach-loungers','CO_loungers',(3,4),1000,.5,.30,0),
    # EXPÉRIENCE (3 plans, section image-led)
    ('exp-silence','ST11',(16,9),1280,.55,.5,0),
    ('exp-apesanteur','BVland',(4,3),1280,.46,.5,1),
    ('exp-rythme','CAN161',(3,4),1000,.45,.5,1),
    # RESPIRATIONS
    ('breath-sunset','VF_sunset',(16,9),1920,.5,.5,0),
    ('breath-redrock','CAN103',(16,9),1920,.5,.5,1),
    ('breath-golfe','CAN172',(16,9),1920,.5,.5,1),
    # EXPÉRIENCE bg fallback (si une édition garde une image plein cadre)
    ('exp-formation','CAN167',(16,9),1920,.5,.5,1),
    # GALERIE (8)
    ('ride-women','BVp2',(3,4),1000,.42,.5,1),
    ('ride-lerins-orange','LER26',(3,4),1000,.42,.5,1),
    ('ride-lerins-green','LER25',(3,4),1000,.42,.5,1),
    ('ride-esterel','EST5',(3,4),1000,.45,.5,1),
    ('ride-redrock','CAN99',(4,3),1280,.5,.5,1),
    ('ride-formation','CAN167',(4,3),1280,.5,.5,1),
    ('ride-yacht','VF_cannes',(3,4),1000,.5,.5,1),
    ('ride-esterel-vert','VF_esterel',(3,4),1000,.45,.5,1),
    # DÉROULÉ (4)
    ('session-briefing','CAN2',(16,9),1280,.5,.5,1),
    ('session-gear','BVp2',(16,9),1280,.4,.5,1),
    ('session-water','BVp1',(16,9),1280,.45,.5,1),
    ('session-flight','CAN103',(16,9),1280,.5,.5,1),
]

def make(out, srckey, ratio, tw, vf, hf, grade, q=80):
    im = ImageOps.exif_transpose(Image.open(SRC[srckey]).convert('RGB'))
    if grade: im = warm_grade(im)
    W, H = im.size; rw, rh = ratio; tr = rw / rh; cur = W / H
    if cur > tr: nw, nh = int(round(H * tr)), H
    else:        nw, nh = W, int(round(W / tr))
    x = int((W - nw) * hf); y = int((H - nh) * vf)
    im = im.crop((x, y, x + nw, y + nh)).resize((tw, int(round(tw / tr))), Image.LANCZOS)
    p = f'medias/web/{out}.webp'; im.save(p, 'WEBP', quality=q, method=6)
    return im.size, os.path.getsize(p) // 1024

if __name__ == '__main__':
    # poster vidéo jpg -> webp (cohérence)
    if os.path.exists('medias/web/hero-video-poster.jpg'):
        Image.open('medias/web/hero-video-poster.jpg').convert('RGB').save(
            'medias/web/hero-video-poster.webp', 'WEBP', quality=82, method=6)
        print("hero-video-poster.webp (depuis le jpg)")
    total = 0
    for out, sk, r, tw, vf, hf, g in JOBS:
        (w, h), kb = make(out, sk, r, tw, vf, hf, g); total += kb
        print(f"{out:22}{sk:13}{w}x{h:<6} {('grade' if g else 'natif'):6} {kb:>4} Ko")
    print(f"\n{len(JOBS)} fichiers · {total} Ko (~{total/1024:.1f} Mo) → medias/web/")
