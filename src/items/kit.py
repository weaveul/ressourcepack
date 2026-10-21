"""Kit pour fabriquer des modèles d'objets Minecraft en 3D (cubes texturés) dans le namespace evo.

Chaque objet produit :
  pack/assets/evo/textures/item/<id>.png   texture peinte texel par texel
  pack/assets/evo/models/item/<id>.json    modèle 3D (éléments cubiques)
  pack/assets/evo/items/<id>.json          définition d'objet, utilisée par le composant item_model "evo:<id>"

Unités : 16 = 1 bloc. Les armes sont modélisées debout (manche en bas, pointe vers +y, face avant vers +z)
puis inclinées à 45° sur z par la rotation des éléments, pour retomber sur la diagonale des épées vanilla
et réutiliser leurs positions en main.
"""
import json, math, os
from PIL import Image

PACK = os.path.join(os.path.dirname(__file__), '..', '..', 'pack', 'assets', 'evo')


def clamp(v):
    return max(0, min(255, int(round(v))))


def h(*a):
    """Bruit déterministe 0..1 à partir de coordonnées."""
    n = 0
    for v in a:
        n = (n * 73856093) ^ int(math.floor(v * 64 + 1000))
    n = (n ^ (n >> 13)) * 1274126177
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def mix(c1, c2, t):
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))


class Mat:
    """Matériau : couleur de base, bruit, liseré sombre sur les bords, dégradé le long de y, lumière."""

    def __init__(self, base, noise=10, edge=0.75, grad=0.0, light=0, pattern=None, hi=None):
        self.base, self.noise, self.edge, self.grad, self.light = base, noise, edge, grad, light
        self.pattern, self.hi = pattern, hi

    def color(self, p, face, px, py, w, hgt):
        c = self.base
        if self.pattern:
            c = self.pattern(c, p, face, px, py, w, hgt)
        if self.grad:
            c = tuple(v * (1 + self.grad * (p[1] - 8) / 16) for v in c)
        n = (h(p[0], p[1], p[2]) - 0.5) * 2 * self.noise
        c = tuple(v + n for v in c)
        edge = (px == 0 or py == 0 or px == w - 1 or py == hgt - 1) and w > 2 and hgt > 2
        if edge and self.edge < 1:
            c = tuple(v * self.edge for v in c)
        elif self.hi and (px == 1 or py == 1) and w > 3 and hgt > 3:
            c = mix(c, self.hi, 0.35)
        return tuple(clamp(v) for v in c) + (255,)


# --- Motifs ---------------------------------------------------------------------

def grain(c, p, face, px, py, w, hgt):
    """Bois : veines le long de y."""
    k = math.sin((p[0] * 3.1 + p[2] * 2.3) + h(round(p[0] * 2), round(p[2] * 2)) * 4)
    return tuple(v * (0.88 + 0.12 * k) for v in c)


def wrap(c, p, face, px, py, w, hgt):
    """Cuir enroulé : bandes en biais."""
    band = int((p[1] * 2 + p[0] + p[2]) * 1.0) % 3
    return tuple(v * (0.8 if band == 0 else 1.0) for v in c)


def rings(c, p, face, px, py, w, hgt):
    band = int(p[1] * 2) % 2
    return tuple(v * (0.85 if band else 1.05) for v in c)


def scales(c, p, face, px, py, w, hgt):
    a = (int(p[0] * 2) + (int(p[1] * 2) % 2)) % 2
    b = int(p[1] * 2) % 2
    return tuple(v * (0.8 if (a and b) else 1.0) for v in c)


def sparkle(c, p, face, px, py, w, hgt):
    return mix(c, (255, 255, 255), 0.6) if h(p[0] * 3, p[1] * 3, p[2] * 3) > 0.93 else c


def runes(c, p, face, px, py, w, hgt):
    """Pierre sombre gravée de traits lumineux."""
    if face not in ('north', 'south'):
        return c
    y = p[1] * 2
    x = (px - w / 2)
    glyph = int(y // 5)
    t = y % 5
    s = h(glyph, 7)
    on = (t < 0.6 and abs(x) <= 1) or (abs(x) < 0.6 and 0.6 <= t < 4) or (s > 0.5 and abs(t - 2.5) < 0.5 and abs(x) <= 1.2)
    return (90, 230, 255) if on else c


MATS = {
    'steel': Mat((178, 184, 196), 8, 0.7, 0.12, hi=(235, 240, 250)),
    'steel_dark': Mat((96, 102, 116), 8, 0.7, 0.1),
    'edge': Mat((222, 228, 238), 6, 0.9, 0.1),
    'iron': Mat((140, 144, 152), 12, 0.75),
    'gold': Mat((228, 180, 60), 10, 0.72, 0.1, hi=(255, 236, 150)),
    'gold_dark': Mat((168, 118, 34), 8, 0.75),
    'bronze': Mat((176, 112, 58), 10, 0.75),
    'silver': Mat((205, 212, 226), 8, 0.78, 0.08, hi=(255, 255, 255)),
    'mithril': Mat((176, 214, 226), 8, 0.78, 0.08, hi=(240, 255, 255)),
    'wood': Mat((122, 82, 46), 8, 0.8, pattern=grain),
    'wood_dark': Mat((74, 48, 30), 8, 0.8, pattern=grain),
    'wood_pale': Mat((170, 132, 84), 8, 0.82, pattern=grain),
    'leather': Mat((110, 62, 34), 6, 0.8, pattern=wrap),
    'leather_dark': Mat((62, 36, 24), 6, 0.8, pattern=wrap),
    'leather_bag': Mat((128, 78, 42), 9, 0.78),
    'leather_bag_dark': Mat((86, 50, 28), 8, 0.78),
    'cloth_red': Mat((150, 32, 36), 8, 0.8),
    'cloth_blue': Mat((40, 62, 150), 8, 0.8),
    'cloth_green': Mat((52, 110, 52), 8, 0.8),
    'string': Mat((230, 224, 205), 4, 1.0),
    'feather': Mat((235, 235, 235), 6, 0.85),
    'leaf': Mat((70, 140, 50), 18, 0.8),
    'leaf_dark': Mat((42, 96, 36), 14, 0.8),
    'moss': Mat((86, 120, 52), 18, 0.85),
    'bone': Mat((222, 214, 190), 8, 0.8),
    'stone': Mat((92, 92, 100), 14, 0.75),
    'obsidian': Mat((36, 28, 52), 8, 0.75),
    'runestone': Mat((44, 46, 60), 6, 0.8, pattern=runes),
    'rune_glow': Mat((90, 230, 255), 6, 0.95, light=12),
    'ruby': Mat((220, 30, 50), 14, 0.7, light=8, pattern=sparkle, hi=(255, 170, 180)),
    'sapphire': Mat((40, 90, 235), 14, 0.7, light=8, pattern=sparkle, hi=(170, 200, 255)),
    'emerald': Mat((40, 200, 90), 14, 0.7, light=8, pattern=sparkle, hi=(180, 255, 200)),
    'amethyst': Mat((160, 70, 230), 14, 0.7, light=10, pattern=sparkle, hi=(230, 190, 255)),
    'arcane': Mat((110, 220, 255), 10, 0.85, light=15, pattern=sparkle, hi=(230, 255, 255)),
    'holy': Mat((255, 236, 150), 8, 0.9, light=15, hi=(255, 255, 230)),
    'moonsteel': Mat((140, 170, 235), 10, 0.75, light=6, pattern=sparkle, hi=(220, 235, 255)),
    'moon': Mat((215, 230, 255), 8, 0.9, light=10, hi=(255, 255, 255)),
    'ember': Mat((255, 120, 40), 16, 0.85, light=15, pattern=sparkle),
    'silk': Mat((236, 236, 228), 6, 0.9, pattern=rings),
    'scale_red': Mat((168, 34, 30), 10, 0.7, pattern=scales, hi=(240, 120, 90)),
    'scale_gold': Mat((214, 150, 50), 8, 0.75),
    'paper': Mat((226, 210, 170), 6, 0.85),
}

HANDHELD = {
    'thirdperson_righthand': {'rotation': [0, -90, 55], 'translation': [0, 4, 0.5], 'scale': [0.85] * 3},
    'thirdperson_lefthand': {'rotation': [0, 90, -55], 'translation': [0, 4, 0.5], 'scale': [0.85] * 3},
    'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68] * 3},
    'firstperson_lefthand': {'rotation': [0, 90, -25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68] * 3},
    'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.5] * 3},
    'head': {'rotation': [0, 180, 0], 'translation': [0, 13, 7], 'scale': [1] * 3},
    'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [1] * 3},
    'gui': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.95] * 3},
}

BOW = dict(HANDHELD)
BOW.update({
    'thirdperson_righthand': {'rotation': [-80, 260, -40], 'translation': [-1, -2, 2.5], 'scale': [0.9] * 3},
    'thirdperson_lefthand': {'rotation': [-80, -280, 40], 'translation': [-1, -2, 2.5], 'scale': [0.9] * 3},
})

OBJECT = {
    'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.5] * 3},
    'thirdperson_lefthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.5] * 3},
    'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 2, 0], 'scale': [0.55] * 3},
    'firstperson_lefthand': {'rotation': [0, 225, 0], 'translation': [0, 2, 0], 'scale': [0.55] * 3},
    'ground': {'rotation': [0, 0, 0], 'translation': [0, 3, 0], 'scale': [0.5] * 3},
    'head': {'rotation': [0, 180, 0], 'translation': [0, 13, 7], 'scale': [1] * 3},
    'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [0.8] * 3},
    'gui': {'rotation': [25, -35, 0], 'translation': [0, 0, 0], 'scale': [0.95] * 3},
}

FACES = ('north', 'south', 'east', 'west', 'up', 'down')


def face_frame(f, a, b):
    """Coin haut-gauche, axe u et axe v (monde) d'une face, conventions UV de Minecraft."""
    x0, y0, z0 = a
    x1, y1, z1 = b
    return {
        'south': ((x0, y1, z1), (1, 0, 0), (0, -1, 0), x1 - x0, y1 - y0),
        'north': ((x1, y1, z0), (-1, 0, 0), (0, -1, 0), x1 - x0, y1 - y0),
        'east': ((x1, y1, z1), (0, 0, -1), (0, -1, 0), z1 - z0, y1 - y0),
        'west': ((x0, y1, z0), (0, 0, 1), (0, -1, 0), z1 - z0, y1 - y0),
        'up': ((x0, y1, z0), (1, 0, 0), (0, 0, 1), x1 - x0, z1 - z0),
        'down': ((x0, y0, z1), (1, 0, 0), (0, 0, -1), x1 - x0, z1 - z0),
    }[f]


class Item:
    def __init__(self, id, density=2, tilt=0, display=None):
        """tilt : rotation (degrés, axe z, autour du centre) appliquée à tous les éléments (-45 épée, 45 arc)."""
        self.id, self.D, self.tilt = id, density, tilt
        self.display = display or HANDHELD
        self.els = []

    def box(self, a, b, mat, faces=None, light=None):
        self.els.append({'from': list(a), 'to': list(b), 'mat': mat, 'faces': faces or {}, 'light': light})
        return self

    def col(self, y0, y1, w, d=None, mat='steel', cx=8, cz=8, **kw):
        """Pavé centré en (cx, cz), de y0 à y1, largeur w (x) et épaisseur d (z)."""
        d = w if d is None else d
        return self.box((cx - w / 2, y0, cz - d / 2), (cx + w / 2, y1, cz + d / 2), mat, **kw)

    # ---------------------------------------------------------------------------------
    def build(self):
        # 1) taille de chaque face en texels, puis rangement en étagères dans une texture carrée
        rects = []
        for i, e in enumerate(self.els):
            for f in FACES:
                _, _, _, du, dv = face_frame(f, e['from'], e['to'])
                w, hh = max(1, round(du * self.D)), max(1, round(dv * self.D))
                rects.append((hh, w, i, f))
        rects.sort(key=lambda r: (-r[0], -r[1]))
        W = 16
        while True:
            place, x, y, row = {}, 0, 0, 0
            ok = True
            for hh, w, i, f in rects:
                if w > W:
                    ok = False
                    break
                if x + w > W:
                    x, y, row = 0, y + row, 0
                if y + hh > W:
                    ok = False
                    break
                place[(i, f)] = (x, y, w, hh)
                x += w
                row = max(row, hh)
            if ok:
                break
            W *= 2
        img = Image.new('RGBA', (W, W), (0, 0, 0, 0))
        px = img.load()
        elements = []
        for i, e in enumerate(self.els):
            faces = {}
            light = 0
            for f in FACES:
                mat = MATS[e['faces'].get(f, e['mat'])]
                light = max(light, mat.light)
                o, u, v, du, dv = face_frame(f, e['from'], e['to'])
                X, Y, w, hh = place[(i, f)]
                for ty in range(hh):
                    for tx in range(w):
                        fu, fv = (tx + 0.5) / w * du, (ty + 0.5) / hh * dv
                        p = tuple(o[k] + u[k] * fu + v[k] * fv for k in range(3))
                        px[X + tx, Y + ty] = mat.color(p, f, tx, ty, w, hh)
                s = 16 / W
                faces[f] = {'uv': [X * s, Y * s, (X + w) * s, (Y + hh) * s], 'texture': '#0'}
            el = {'from': e['from'], 'to': e['to'], 'faces': faces}
            if e.get('rot'):
                el['rotation'] = e['rot']
            elif self.tilt:
                el['rotation'] = {'angle': self.tilt, 'axis': 'z', 'origin': [8, 8, 8]}
            lv = e['light'] if e['light'] is not None else light
            if lv:
                el['light_emission'] = lv
            elements.append(el)
        return img, elements

    def save(self, variants=None):
        """variants : {suffixe: Item} pour les états d'un arc (pulling_0..2)."""
        out = {}
        for suffix, it in [('', self)] + list((variants or {}).items()):
            name = self.id + suffix
            img, elements = it.build()
            os.makedirs(f'{PACK}/textures/item', exist_ok=True)
            os.makedirs(f'{PACK}/models/item', exist_ok=True)
            img.save(f'{PACK}/textures/item/{name}.png')
            model = {'textures': {'0': f'evo:item/{name}', 'particle': f'evo:item/{name}'},
                     'elements': elements, 'display': it.display}
            json.dump(model, open(f'{PACK}/models/item/{name}.json', 'w'), separators=(',', ':'))
            out[suffix] = (name, img, elements, it.display)
        os.makedirs(f'{PACK}/items', exist_ok=True)
        m = lambda n: {'type': 'minecraft:model', 'model': f'evo:item/{n}'}
        if variants:
            definition = {'model': {
                'type': 'minecraft:condition', 'property': 'minecraft:using_item',
                'on_false': m(self.id),
                'on_true': {'type': 'minecraft:range_dispatch', 'property': 'minecraft:use_duration', 'scale': 0.05,
                            'entries': [{'threshold': 0.65, 'model': m(self.id + '_pulling_1')},
                                        {'threshold': 0.9, 'model': m(self.id + '_pulling_2')}],
                            'fallback': m(self.id + '_pulling_0')}}}
        else:
            definition = {'model': m(self.id)}
        json.dump(definition, open(f'{PACK}/items/{self.id}.json', 'w'), indent=1)
        return out
