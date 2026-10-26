"""Planche des armes de butin par classe (vue inventaire), à côté des deux armes de base de la classe."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import catalog
from armes_butin import ARMES_BUTIN
from render import render

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
CELL = 280
RAR = {}
try:
    import yaml
    w = yaml.safe_load(open('/mnt/project-files/evo-extract/src/main/resources/weapons.yml'))['weapons']
    RAR = {k: v.get('rarity', '') for k, v in w.items()}
    NAME = {k: v.get('name', k) for k, v in w.items()}
except Exception:
    NAME = {}
COL = {'RARE': (90, 150, 255), 'EPIC': (190, 110, 255), 'LEGENDARY': (255, 190, 60)}


def tile(fn):
    it = fn()
    img, els = it.build()
    disp = dict(it.display)
    g = dict(disp.get('gui', {}))
    g["scale"] = [0.62] * 3
    disp['gui'] = g
    return it.id, render(img, els, disp, CELL - 20)


for cls in ('mage', 'druide', 'guerrier', 'paladin', 'rodeur', 'lamerunique'):
    fns = [f for f in ARMES_BUTIN if f.__name__.startswith(cls + '_')]
    order = {'RARE': 0, 'EPIC': 1, 'LEGENDARY': 2}
    fns.sort(key=lambda f: order.get(RAR.get(f.__name__), 9))
    tiles = [tile(f) for f in fns]
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGBA', (cols * CELL, rows * (CELL + 30)), (40, 40, 48, 255))
    d = ImageDraw.Draw(sheet)
    for i, (id, im) in enumerate(tiles):
        x, y = (i % cols) * CELL, (i // cols) * (CELL + 30)
        c = COL.get(RAR.get(id), (200, 200, 200))
        d.rectangle([x + 4, y + 4, x + CELL - 4, y + CELL + 24], fill=(120, 120, 124, 255), outline=c, width=3)
        sheet.alpha_composite(im, (x + 10, y + 6))
        d.text((x + 10, y + CELL + 6), NAME.get(id, id)[:30], fill=(255, 255, 255, 255))
    p = os.path.join(OUT, f'armes_butin_{cls}.png')
    sheet.save(p)
    print(p)
