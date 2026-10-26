"""Planche par classe : lignes = paliers de rareté, colonnes = variantes ; casque 3D au-dessus du mannequin de face.

À lancer après generate.py (lit les calques du pack et les planches de casques dans apercus/).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'items'))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw  # noqa: E402

PACK = os.path.join(HERE, '..', '..', 'pack', 'assets', 'oraxen', 'textures', 'entity', 'equipment')
APERCUS = os.path.join(HERE, 'apercus')
TIERS = ['commun', 'rare', 'epique', 'legendaire']
K, S = 2, 4


def faces(u, v, w, hh, d):
    return {'front': (u + d, v + d, w, hh), 'back': (u + 2 * d + w, v + d, w, hh)}


BODY, ARM, LEG = (16, 16, 8, 12, 4), (40, 16, 4, 12, 4), (0, 16, 4, 12, 4)


def figure(name, side):
    l1 = Image.open(os.path.join(PACK, 'humanoid', name + '.png'))
    l2 = Image.open(os.path.join(PACK, 'humanoid_leggings', name + '.png'))
    fig = Image.new('RGBA', (16 * K, 24 * K), (0, 0, 0, 0))
    for (x, y, w, hh) in ((4, 0, 8, 12), (0, 0, 4, 12), (12, 0, 4, 12), (4, 12, 4, 12), (8, 12, 4, 12)):
        fig.paste((90, 90, 96, 255), (x * K, y * K, (x + w) * K, (y + hh) * K))

    def put(layer, box, dst):
        fx, fy, w, hh = faces(*box)[side]
        fig.alpha_composite(layer.crop((fx * K, fy * K, (fx + w) * K, (fy + hh) * K)), (dst[0] * K, dst[1] * K))
    put(l2, BODY, (4, 0)); put(l2, LEG, (4, 12)); put(l2, LEG, (8, 12))
    put(l1, BODY, (4, 0)); put(l1, ARM, (0, 0)); put(l1, ARM, (12, 0)); put(l1, LEG, (4, 12)); put(l1, LEG, (8, 12))
    return fig.resize((16 * K * S, 24 * K * S), Image.NEAREST)


def sheet(key):
    helm = Image.open(os.path.join(APERCUS, f'casques_{key}.png'))
    cw, ch = 300, 200 + 24 * K * S + 10
    out = Image.new('RGBA', (110 + 4 * cw, 4 * ch), (44, 46, 52, 255))
    d = ImageDraw.Draw(out)
    for r, tier in enumerate(TIERS):
        d.text((8, r * ch + ch // 2), tier, fill=(230, 230, 230, 255))
        for v in range(4):
            x0, y0 = 110 + v * cw, r * ch
            out.alpha_composite(helm.crop((110 + v * 200, r * 200, 310 + v * 200, r * 200 + 200)), (x0 + 50, y0))
            name = f'{key}_{tier}_{v + 1}'
            out.alpha_composite(figure(name, 'front'), (x0 + 10, y0 + 190))
            out.alpha_composite(figure(name, 'back'), (x0 + 20 + 16 * K * S // 1 - 0, y0 + 190)) if False else None
            out.alpha_composite(figure(name, 'back'), (x0 + 150, y0 + 190))
            d.text((x0 + 8, y0 + 8), f'variante {v + 1}', fill=(200, 200, 200, 255))
    return out


if __name__ == '__main__':
    keys = sys.argv[1:] or ['guerrier', 'paladin', 'mage', 'rodeur', 'druide', 'lamerunique', 'gardeserment',
                            'sentinelle', 'arcaniste']
    for key in keys:
        sheet(key).save(os.path.join(APERCUS, f'classe_{key}.png'))
        print(key)
