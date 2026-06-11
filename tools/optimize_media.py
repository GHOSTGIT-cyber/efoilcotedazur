#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Optimise les photos du dossier medias/ en derivés web (WebP), recadrés au ratio
de chaque slot de la landing eFoil COMO Le Beauvallon.

Usage :  python tools/optimize_media.py   (depuis la racine du projet)
Sortie : medias/web/*.webp
Dépendance : Pillow (PIL).  Aucune dépendance vidéo (pas de ffmpeg requis).

Pour ajouter / remplacer une photo : édite SRC + JOBS puis relance le script,
puis relance tools/build_versions.py.
"""
import os
from PIL import Image, ImageOps

os.makedirs('medias/web', exist_ok=True)
M = 'medias'

SRC = {
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
}

# (sortie, clé source, (ratio_w, ratio_h), largeur cible, vfocus 0..1, hfocus 0..1)
JOBS = [
    ('hero-sunset','ST7',(16,9),1920,.60,.5), ('hero-domaine','BVland',(16,9),1920,.46,.5),
    ('hero-formation','CAN167',(16,9),1920,.5,.5),
    ('lieu-domaine','BVland',(4,3),1280,.5,.5),
    ('beach-terrasse','CANday',(16,9),1280,.5,.5), ('beach-ponton','CAN2',(3,4),1000,.5,.42),
    ('breath-sunset','ST11',(16,9),1920,.55,.5), ('breath-redrock','CAN103',(16,9),1920,.5,.5),
    ('breath-golfe','CAN99',(16,9),1920,.5,.5), ('exp-formation','CAN167',(16,9),1920,.5,.5),
    ('ride-women','BVp2',(3,4),1000,.42,.5), ('ride-lerins-orange','LER26',(3,4),1000,.42,.5),
    ('ride-lerins-green','LER25',(3,4),1000,.42,.5), ('ride-esterel','EST5',(3,4),1000,.45,.5),
    ('ride-redrock','CAN99',(4,3),1280,.5,.5), ('ride-formation','CAN167',(4,3),1280,.5,.5),
    ('session-briefing','CAN2',(16,9),1280,.5,.5), ('session-gear','BVp2',(16,9),1280,.4,.5),
    ('session-water','BVp1',(16,9),1280,.45,.5), ('session-flight','CAN103',(16,9),1280,.5,.5),
]

def make(out, srckey, ratio, tw, vf, hf, q=80):
    im = ImageOps.exif_transpose(Image.open(SRC[srckey]).convert('RGB'))
    W, H = im.size; rw, rh = ratio; tr = rw / rh; cur = W / H
    if cur > tr: nw, nh = int(round(H * tr)), H
    else:        nw, nh = W, int(round(W / tr))
    x = int((W - nw) * hf); y = int((H - nh) * vf)
    im = im.crop((x, y, x + nw, y + nh)).resize((tw, int(round(tw / tr))), Image.LANCZOS)
    p = f'medias/web/{out}.webp'; im.save(p, 'WEBP', quality=q, method=6)
    return im.size, os.path.getsize(p) // 1024

if __name__ == '__main__':
    total = 0
    for out, sk, r, tw, vf, hf in JOBS:
        (w, h), kb = make(out, sk, r, tw, vf, hf); total += kb
        print(f"{out:22}{sk:8}{w}x{h:<8} {kb:>4} Ko")
    print(f"\n{len(JOBS)} fichiers · {total} Ko (~{total/1024:.1f} Mo) → medias/web/")
