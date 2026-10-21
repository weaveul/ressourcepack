"""Armures de classe pour Oraxen : une panoplie par classe Heroes, visible portée.

Sortie (à copier dans plugins/Oraxen/ sur le serveur) :
  src/armures/oraxen/pack/textures/evo/armures/<classe>_armor_layer_1.png  casque, plastron, bras, bottes
  src/armures/oraxen/pack/textures/evo/armures/<classe>_armor_layer_2.png  jambières
  src/armures/oraxen/pack/textures/evo/armures/<classe>_<pièce>.png        icônes 16x16
  src/armures/oraxen/items/evo_armures.yml                                 objets Oraxen
  src/armures/apercu.png                                                   aperçu de face

Côté client, le script écrit aussi directement dans pack/assets/oraxen/ ce qu'Oraxen générerait
(items/<id>.json, equipment/<classe>.json, calques d'armure), sans ses fichiers lang/font/atlas qui
écraseraient ceux du serveur. Oraxen pose item_model = oraxen:<id> sur l'objet, le pack fournit le reste.

Les calques suivent la disposition vanilla 64x32 : tête (0,0) 8x8x8, corps (16,16) 8x12x4,
bras (40,16) 4x12x4, jambe (0,16) 4x12x4.
"""
import json, os, sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'items'))
from kit import h, mix, clamp  # noqa: E402

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, 'oraxen')
PACK = os.path.join(HERE, '..', '..', 'pack', 'assets', 'oraxen')
TEX = os.path.join(OUT, 'pack', 'textures', 'evo', 'armures')


def faces(u, v, w, hh, d):
    """Rectangles (nom, x, y, largeur, hauteur) d'une boîte dépliée à la mode Minecraft."""
    return {
        'top': (u + d, v, w, d),
        'bottom': (u + d + w, v, w, d),
        'right': (u, v + d, d, hh),
        'front': (u + d, v + d, w, hh),
        'left': (u + d + w, v + d, d, hh),
        'back': (u + 2 * d + w, v + d, w, hh),
    }


HEAD = (0, 0, 8, 8, 8)
BODY = (16, 16, 8, 12, 4)
ARM = (40, 16, 4, 12, 4)
LEG = (0, 16, 4, 12, 4)


class Theme:
    def __init__(self, key, cls, set_name, names, base, dark, light, trim, accent, glow=None, noise=12,
                 hood=False, sleeves=True, stats=None, durability=300, color='#ffffff', lore=''):
        self.key, self.cls, self.set_name, self.names = key, cls, set_name, names
        self.base, self.dark, self.light, self.trim, self.accent, self.glow = base, dark, light, trim, accent, glow
        self.noise, self.hood, self.sleeves = noise, hood, sleeves
        self.stats, self.durability, self.color, self.lore = stats, durability, color, lore


def px_color(t, c, x, y, seed):
    n = (h(x, y, seed) - 0.5) * 2 * t.noise
    return tuple(clamp(v + n) for v in c) + (255,)


def paint_face(img, t, rect, kind, face, rows=None, seed=0):
    """Peint une face. kind = pièce (helmet, chest, arm, legs, boots), rows = (début, fin) en lignes."""
    x0, y0, w, hh = rect
    r0, r1 = rows if rows else (0, hh)
    for py in range(r0, r1):
        for px in range(w):
            c = motif(t, kind, face, px, py, w, hh, r0, r1)
            if c is None:
                continue
            if len(c) == 3:
                c = px_color(t, c, x0 + px, y0 + py, seed)
            img.putpixel((x0 + px, y0 + py), c)


def motif(t, kind, face, px, py, w, hh, r0, r1):
    """Couleur d'un texel selon la classe, la pièce et la face. None = transparent."""
    k = t.key
    edge_x = px == 0 or px == w - 1
    top_row, bot_row = py == r0, py == r1 - 1
    c = t.base
    # dégradé léger vers le bas
    c = mix(c, t.dark, 0.25 * (py - r0) / max(1, r1 - r0))
    if face in ('top', 'bottom'):
        c = mix(t.base, t.light, 0.25) if face == 'top' else t.dark
        if edge_x or py == 0 or py == hh - 1:
            c = t.trim if kind in ('helmet', 'boots') else t.dark
        return c

    # ---- casque -----------------------------------------------------------------------------------
    if kind == 'helmet':
        if face == 'front':
            if t.hood:
                # capuche ouverte : le visage reste visible
                if 1 <= px <= 6 and 2 <= py <= 7:
                    return None
                if py >= 1 and (px == 1 or px == 6) and py <= 7:
                    return t.trim
                return mix(c, t.dark, 0.2)
            if k == 'paladin':
                # fente en croix
                if (py == 3 and 1 <= px <= 6) or (px in (3, 4) and 2 <= py <= 6):
                    return (20, 20, 26)
            elif k == 'guerrier':
                if (py == 3 and 1 <= px <= 6) or (px in (3, 4) and 3 <= py <= 5):
                    return (16, 16, 18)
                if px in (3, 4) and py in (6, 7):
                    return t.trim
            elif k == 'lamerunique':
                if py == 3 and 1 <= px <= 6:
                    return t.glow + (255,)
                if px in (3, 4) and py in (5, 6):
                    return t.glow + (255,)
            elif k == 'druide':
                if 2 <= px <= 5 and 3 <= py <= 6:
                    return None
                if py <= 1 and px % 2 == 0:
                    return t.accent
            if py == 0:
                return t.trim
        if face == 'top' and k == 'druide':
            return t.accent
        if py == 0 or py == hh - 1:
            return t.trim
        if k == 'lamerunique' and face in ('left', 'right') and px == 4 and 2 <= py <= 5:
            return t.glow + (255,)
        if k == 'druide' and face in ('left', 'right') and h(px, py, 7) > 0.65:
            return t.accent
        return c

    # ---- plastron ---------------------------------------------------------------------------------
    if kind == 'chest':
        if face == 'front':
            cx = px - 3.5
            if k == 'paladin':
                if (px in (3, 4) and 2 <= py <= 9) or (py == 4 and 1 <= px <= 6):
                    return t.trim
            elif k == 'guerrier':
                if py in (4, 8):
                    return t.dark
                if py == 1 and px in (1, 6):
                    return t.light
                if px in (3, 4) and py in (2, 3):
                    return t.accent
            elif k == 'mage':
                if px in (3, 4):
                    return t.trim
                if px in (2, 5) and py % 3 == 1:
                    return t.glow + (255,)
            elif k == 'rodeur':
                if px == 7 - (py * 7) // 11 or px == 7 - (py * 7) // 11 - 1 and py > 0:
                    return t.trim
                if py == 9:
                    return t.dark
            elif k == 'druide':
                leaf = abs(cx) + abs(py - 5) * 0.6
                if leaf < 2.2:
                    return t.accent
                if px in (3, 4) and py > 7:
                    return t.light
            elif k == 'lamerunique':
                if (px in (3, 4) and 2 <= py <= 8) or (py == 5 and px in (2, 5)) or (py == 2 and px in (2, 5)):
                    return t.glow + (255,)
        if face == 'back' and k == 'mage' and py > 2:
            return mix(c, t.dark, 0.3)
        if top_row or bot_row:
            return t.trim
        if edge_x and face in ('front', 'back'):
            return mix(c, t.dark, 0.5)
        return c

    if kind == 'arm':
        if not t.sleeves and py > 4:
            return None
        if py == 0 or (not t.sleeves and py == 4):
            return t.trim
        if t.sleeves and py == hh - 1:
            return t.trim
        if k == 'guerrier' and py in (1, 2):
            return t.light if face in ('front', 'right', 'left') and py == 1 else c
        if k == 'lamerunique' and face == 'front' and px in (1, 2) and py in (6, 7):
            return t.glow + (255,)
        if k == 'druide' and h(px, py, 3) > 0.7:
            return t.accent
        return c

    # ---- jambières (calque 2) ---------------------------------------------------------------------
    if kind == 'legs':
        if top_row:
            return t.trim
        if k == 'mage' and face == 'front' and px in (1, 2) and py % 3 == 2:
            return t.glow + (255,)
        if k == 'guerrier' and py == 5:
            return t.light
        if k == 'paladin' and py == 5:
            return t.trim
        if k == 'rodeur' and py in (6, 7) and face == 'front':
            return t.trim
        if k == 'lamerunique' and face in ('front',) and px == 1 and 3 <= py <= 7:
            return t.glow + (255,)
        if k == 'druide' and h(px, py, 11) > 0.72:
            return t.accent
        if edge_x and face in ('front', 'back'):
            return mix(c, t.dark, 0.4)
        return c

    if kind == 'body_legs':
        # ceinture : bas du torse sur le calque 2
        if py == r0:
            return t.trim
        if face == 'front' and px in (3, 4) and py == r0 + 1:
            return t.accent
        return mix(c, t.dark, 0.3)

    # ---- bottes -----------------------------------------------------------------------------------
    if kind == 'boots':
        if py == r0:
            return t.trim
        if py == hh - 1:
            return mix(t.dark, (0, 0, 0), 0.3)
        if k == 'lamerunique' and face == 'front' and py == r0 + 2:
            return t.glow + (255,)
        return mix(c, t.dark, 0.2)
    return c


def layer1(t):
    img = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
    for name, rect in faces(*HEAD).items():
        if name == 'bottom':
            continue
        paint_face(img, t, rect, 'helmet', name, seed=1)
    for name, rect in faces(*BODY).items():
        paint_face(img, t, rect, 'chest', name, seed=2)
    for name, rect in faces(*ARM).items():
        paint_face(img, t, rect, 'arm', name, seed=3)
    for name, rect in faces(*LEG).items():
        if name in ('top',):
            continue
        rows = None if name == 'bottom' else (rect[3] - 4, rect[3])
        paint_face(img, t, rect, 'boots', name, rows=rows, seed=4)
    return img


def layer2(t):
    img = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
    for name, rect in faces(*BODY).items():
        if name in ('front', 'back', 'left', 'right'):
            paint_face(img, t, rect, 'body_legs', name, rows=(rect[3] - 3, rect[3]), seed=5)
    for name, rect in faces(*LEG).items():
        if name in ('top', 'bottom'):
            continue
        paint_face(img, t, rect, 'legs', name, rows=(0, rect[3] - 3), seed=6)
    return img


# ---- icônes 16x16 -----------------------------------------------------------------------------------

ICONS = {
    'helmet': [
        '................',
        '................',
        '.....oooooo.....',
        '....obhbbbbbo...',
        '...obhbbbbbbbo..',
        '...obbbbbbbbbo..',
        '...otttttttttto.',
        '...obbbbbbbbbo..',
        '...obbvvvvvbbo..',
        '...obo.....obo..',
        '...obo.....obo..',
        '...ooo.....ooo..',
        '................',
        '................',
        '................',
        '................',
    ],
    'chestplate': [
        '................',
        '.ooo..oooo..ooo.',
        'obbbooobbooobbbo',
        'obhbbbbbbbbbbbbo',
        'obbbbbbttbbbbbbo',
        'ooobbbbttbbbbooo',
        '..obbbbttbbbbo..',
        '..obbbbttbbbbo..',
        '..obbbbbbbbbbo..',
        '..otttttttttto..',
        '..obbbbbbbbbbo..',
        '..obbbbbbbbbbo..',
        '..oooooooooooo..',
        '................',
        '................',
        '................',
    ],
    'leggings': [
        '................',
        '................',
        '...oooooooooo...',
        '...otttttttto...',
        '...obhbbbbbbo...',
        '...obbbbbbbbo...',
        '...obbbooobbo...',
        '...obbo..obbo...',
        '...obbo..obbo...',
        '...obho..obbo...',
        '...obbo..obbo...',
        '...obbo..obbo...',
        '...obbo..obbo...',
        '...oooo..oooo...',
        '................',
        '................',
    ],
    'boots': [
        '................',
        '................',
        '................',
        '................',
        '................',
        '..oooo....oooo..',
        '..otto....otto..',
        '..obho....obho..',
        '..obbo....obbo..',
        '..obbo....obbo..',
        '.obbbo...obbbo..',
        'obbbbo..obbbbo..',
        'oddddo..oddddo..',
        'oooooo..oooooo..',
        '................',
        '................',
    ],
}


def icon(t, piece):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    rows = ICONS[piece]
    for y, row in enumerate(rows):
        assert len(row) == 16, (piece, y, len(row))
        for x, ch in enumerate(row):
            col = {
                'o': mix(t.dark, (0, 0, 0), 0.45),
                'b': t.base,
                'h': t.light,
                't': t.trim,
                'd': t.dark,
                'v': (t.glow or (18, 18, 22)),
            }.get(ch)
            if col is None:
                continue
            if ch == 'b':
                col = mix(t.base, t.dark, 0.35 * y / 15)
                if t.key == 'druide' and h(x, y, 9) > 0.7:
                    col = t.accent
            img.putpixel((x, y), px_color(t, col, x, y, 20) if ch == 'b' else tuple(clamp(v) for v in col) + (255,))
    # emblème de classe sur le plastron
    if piece == 'chestplate' and t.glow:
        for (x, y) in ((7, 4), (8, 4), (7, 6), (8, 6)):
            img.putpixel((x, y), t.glow + (255,))
    return img


# ---- classes ----------------------------------------------------------------------------------------

PIECES = [('helmet', 'HEAD', 0.69), ('chestplate', 'CHEST', 1.0), ('leggings', 'LEGS', 0.94),
          ('boots', 'FEET', 0.81)]

THEMES = [
    Theme('guerrier', 'Guerrier', 'Rempart de fer', ['Heaume', 'Cuirasse', 'Jambières', 'Solerets'],
          base=(138, 143, 153), dark=(70, 72, 80), light=(205, 210, 218), trim=(150, 34, 38), accent=(196, 60, 52),
          sleeves=True, durability=420, color='#c9483f', lore='Acier martelé, taillé pour encaisser.',
          stats={'ARMOR': [3, 8, 6, 3], 'ARMOR_TOUGHNESS': [2, 2, 2, 2], 'KNOCKBACK_RESISTANCE': [0, 0.1, 0, 0]}),
    Theme('paladin', 'Paladin', 'Aube sacrée', ['Heaume', 'Cuirasse', 'Jambières', 'Solerets'],
          base=(214, 218, 226), dark=(130, 136, 150), light=(250, 250, 252), trim=(212, 160, 23), accent=(240, 200, 80),
          sleeves=True, durability=400, color='#f0c850', lore='Argent béni, liseré d\'or.',
          stats={'ARMOR': [3, 7, 6, 2], 'ARMOR_TOUGHNESS': [1, 1, 1, 1], 'MAX_HEALTH': [0, 2, 0, 0]}),
    Theme('mage', 'Mage', 'Arcaniste', ['Capuche', 'Robe', 'Chausses', 'Bottines'],
          base=(75, 42, 115), dark=(38, 20, 64), light=(124, 86, 170), trim=(196, 170, 90), accent=(76, 201, 240),
          glow=(110, 225, 255), hood=True, sleeves=True, durability=220, color='#9b6bff',
          lore='Tissu tissé de fils de mana.',
          stats={'ARMOR': [1, 3, 2, 1], 'MAX_HEALTH': [0, 2, 0, 0]}),
    Theme('rodeur', 'Rôdeur', 'Traqueur', ['Capuche', 'Veste', 'Pantalon', 'Bottes'],
          base=(59, 83, 35), dark=(32, 46, 20), light=(98, 128, 62), trim=(107, 68, 35), accent=(160, 112, 60),
          hood=True, sleeves=False, durability=280, color='#7fae4a', lore='Cuir souple, fait pour la traque.',
          stats={'ARMOR': [2, 5, 4, 2], 'MOVEMENT_SPEED': [0, 0, 0.005, 0.005]}),
    Theme('druide', 'Druide', 'Sylvestre', ['Couronne', 'Plastron', 'Jambières', 'Bottes'],
          base=(96, 66, 46), dark=(52, 36, 24), light=(140, 104, 72), trim=(70, 110, 52), accent=(92, 150, 64),
          sleeves=False, durability=300, color='#5c9640', lore='Écorce vivante et mousse des bois anciens.',
          stats={'ARMOR': [2, 5, 4, 2], 'MAX_HEALTH': [1, 1, 1, 1]}),
    Theme('lamerunique', 'Lame-runique', 'Runes d\'obsidienne', ['Heaume', 'Cuirasse', 'Jambières', 'Bottes'],
          base=(40, 38, 58), dark=(18, 16, 28), light=(78, 74, 104), trim=(74, 82, 120), accent=(62, 230, 230),
          glow=(80, 240, 235), sleeves=True, durability=360, color='#3ee6e6', lore='Obsidienne gravée de runes vives.',
          stats={'ARMOR': [2, 6, 5, 2], 'ARMOR_TOUGHNESS': [1, 1, 1, 1], 'ATTACK_DAMAGE': [0, 0.5, 0, 0]}),
]

STAT_LABEL = {
    'ARMOR': 'Armure', 'ARMOR_TOUGHNESS': 'Robustesse', 'MAX_HEALTH': 'Vie max',
    'MOVEMENT_SPEED': 'Vitesse', 'ATTACK_DAMAGE': 'Dégâts', 'KNOCKBACK_RESISTANCE': 'Résistance au recul',
}


def fmt(v):
    return ('%g' % v)


def yaml_for(t):
    out = []
    for i, (piece, slot, mult) in enumerate(PIECES):
        iid = f'{t.key}_{piece}'
        title = f'{t.names[i]} {de(t.set_name)}'
        out.append(f'{iid}:')
        out.append(f'  itemname: "<{t.color}>{title}"')
        out.append('  material: PAPER')
        out.append('  lore:')
        out.append(f'    - "<gray>{t.lore}"')
        out.append('    - ""')
        out.append(f'    - "<dark_gray>Classe : <yellow>{t.cls}"')
        out.append(f'    - "<dark_gray>Panoplie : <white>{t.set_name}"')
        out.append('  components:')
        out.append('    max_stack_size: 1')
        out.append('    durability:')
        out.append(f'      value: {int(t.durability * mult)}')
        out.append('    equippable:')
        out.append(f'      slot: {slot}')
        out.append(f'      model: oraxen:{t.key}')
        out.append('  AttributeModifiers:')
        for attr, vals in t.stats.items():
            if vals[i]:
                out.append(f'    - {{ attribute: {attr}, amount: {fmt(vals[i])}, operation: 0, slot: {slot} }}')
        out.append('  pack:')
        out.append('    generate_model: true')
        out.append('    parent_model: item/generated')
        out.append('    textures:')
        out.append(f'      - evo/armures/{iid}')
        out.append('')
    return out


def de(name):
    return ("de l'" + name) if name[0] in 'AEIOUÉ' else ('des ' + name if name.startswith('Runes') else 'du ' + name)


def preview(themes):
    """Vue de face de chaque panoplie, sur un mannequin gris."""
    S = 8
    W, H = 16, 32
    sheet = Image.new('RGBA', (len(themes) * (W + 4) * S, (H + 4) * S), (40, 42, 48, 255))
    for n, t in enumerate(themes):
        l1, l2 = layer1(t), layer2(t)
        fig = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        skin = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for (x, y, w, hh) in ((4, 0, 8, 8), (4, 8, 8, 12), (0, 8, 4, 12), (12, 8, 4, 12), (4, 20, 4, 12),
                              (8, 20, 4, 12)):
            for yy in range(hh):
                for xx in range(w):
                    skin.putpixel((x + xx, y + yy), (150, 120, 100, 255) if y == 0 else (90, 90, 96, 255))
        fig.alpha_composite(skin)

        def put(layer, src, dst):
            sx, sy, w, hh = src
            fig.alpha_composite(layer.crop((sx, sy, sx + w, sy + hh)), dst)
        put(l2, (20, 20, 8, 12), (4, 8))
        put(l2, (4, 20, 4, 12), (4, 20))
        put(l2, (4, 20, 4, 12), (8, 20))
        put(l1, (8, 8, 8, 8), (4, 0))
        put(l1, (20, 20, 8, 12), (4, 8))
        put(l1, (44, 20, 4, 12), (0, 8))
        put(l1, (44, 20, 4, 12), (12, 8))
        put(l1, (4, 20, 4, 12), (4, 20))
        put(l1, (4, 20, 4, 12), (8, 20))
        sheet.alpha_composite(fig.resize((W * S, H * S), Image.NEAREST), ((n * (W + 4) + 2) * S, 2 * S))
    return sheet


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))


def pack_files(t, l1, l2, icons):
    eq = os.path.join(PACK, 'textures', 'entity', 'equipment')
    for folder, img in (('humanoid', l1), ('humanoid_leggings', l2)):
        os.makedirs(os.path.join(eq, folder), exist_ok=True)
        img.save(os.path.join(eq, folder, f'{t.key}.png'))
    layer = [{'texture': f'oraxen:{t.key}'}]
    write_json(os.path.join(PACK, 'equipment', f'{t.key}.json'),
               {'layers': {'humanoid': layer, 'humanoid_leggings': layer}})
    for piece, img in icons.items():
        iid = f'{t.key}_{piece}'
        os.makedirs(os.path.join(PACK, 'textures', 'item', 'armures'), exist_ok=True)
        img.save(os.path.join(PACK, 'textures', 'item', 'armures', f'{iid}.png'))
        write_json(os.path.join(PACK, 'models', 'item', 'armures', f'{iid}.json'),
                   {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'oraxen:item/armures/{iid}'}})
        write_json(os.path.join(PACK, 'items', f'{iid}.json'),
                   {'model': {'type': 'minecraft:model', 'model': f'oraxen:item/armures/{iid}'}})


def main():
    os.makedirs(TEX, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'items'), exist_ok=True)
    yml = ['# Généré par src/armures/generate.py (dépôt ressourcepack). Ne pas éditer à la main.', '']
    for t in THEMES:
        l1, l2 = layer1(t), layer2(t)
        l1.save(os.path.join(TEX, f'{t.key}_armor_layer_1.png'))
        l2.save(os.path.join(TEX, f'{t.key}_armor_layer_2.png'))
        icons = {piece: icon(t, piece) for piece, _, _ in PIECES}
        for piece, img in icons.items():
            img.save(os.path.join(TEX, f'{t.key}_{piece}.png'))
        pack_files(t, l1, l2, icons)
        yml += yaml_for(t)
    with open(os.path.join(OUT, 'items', 'evo_armures.yml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(yml))
    preview(THEMES).save(os.path.join(HERE, 'apercu.png'))
    print(f'{len(THEMES)} panoplies, {len(THEMES) * 4} pièces')


if __name__ == '__main__':
    main()
