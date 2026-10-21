"""Régénère les objets 3D (textures, modèles, définitions) dans pack/assets/evo et l'aperçu apercu.png."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw
from catalog import ALL
from mobs import MOB_WEAPONS, FURNITURE_ITEMS
from meubles import STYLE_ITEMS, OPEN_ITEMS, oraxen_meubles
from render import render

CELL = 160
tiles = []
for fn in ALL + MOB_WEAPONS + FURNITURE_ITEMS + STYLE_ITEMS + OPEN_ITEMS:
    it = fn()
    out = it.save(getattr(it, 'variants', None))
    for suffix, (name, img, elements, display) in out.items():
        tiles.append((name, render(img, elements, display, CELL - 20)))
    print(fn.__name__, 'ok')

cols = 6
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGBA', (cols * CELL, rows * (CELL + 14)), (40, 40, 48, 255))
d = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(tiles):
    x, y = (i % cols) * CELL, (i // cols) * (CELL + 14)
    d.rectangle([x + 4, y + 4, x + CELL - 4, y + CELL - 4], fill=(139, 139, 139, 255), outline=(60, 60, 60, 255))
    sheet.alpha_composite(im, (x + 10, y + 10))
    d.text((x + 6, y + CELL - 2), name, fill=(230, 230, 230, 255))
sheet.save(os.path.join(os.path.dirname(__file__), 'apercu.png'))
print(len(tiles), 'modèles')
print('oraxen :', oraxen_meubles())
