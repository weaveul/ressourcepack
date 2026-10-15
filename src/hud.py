"""Icônes et ornements de la tablist et du scoreboard (TAB).

Dessine les images dans pack/assets/evo/textures/hud/ et ajoute leurs glyphes
(U+E200 et suivants) à la police minecraft:default, sans toucher aux glyphes des menus.
Usage : python3 src/hud.py   (depuis la racine du dépôt)
"""
import json, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'pack/assets/evo/textures/hud')
FONT = os.path.join(ROOT, 'pack/assets/minecraft/font/default.json')

GOLD_L, GOLD, GOLD_D, OUTL = (255, 236, 160), (232, 190, 70), (150, 105, 25), (45, 30, 8)
SILV_L, SILV, SILV_D = (240, 244, 250), (190, 198, 210), (110, 118, 130)


def px(img, pts, c):
    for x, y in pts:
        img.putpixel((x, y), c + (255,) if len(c) == 3 else c)


def grid(rows, pal):
    """Dessine une icône à partir d'une grille de caractères."""
    h, w = len(rows), max(len(r) for r in rows)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in pal:
                img.putpixel((x, y), pal[ch] + (255,))
    return img


PAL = {'o': OUTL, 'g': GOLD, 'l': GOLD_L, 'd': GOLD_D, 's': SILV, 'S': SILV_L, 'k': SILV_D,
       'r': (190, 45, 45), 'R': (240, 95, 80), 'm': (120, 20, 25), 'p': (225, 205, 160), 'P': (250, 238, 205),
       'b': (95, 70, 40), 'w': (235, 235, 235), 'W': (255, 255, 255), 'x': (150, 150, 150), 'B': (90, 190, 255)}

ICONS = {
    # pièce d'or
    'coin': ['..oooo..', '.ollllo.', 'olggggdo', 'olgddgdo', 'olgddgdo', 'olggggdo', '.oddddo.', '..oooo..'],
    # épée (classe)
    'sword': ['......So', '.....Sko', '....Sko.', 'o..Sko..', 'odSko...', '.odo....', 'odgdo...', 'oo.oo...'],
    # repère de carte (lieu)
    'pin': ['..ooo...', '.oRRro..', 'oRRWRro.', 'oRRRrro.', '.orrrm..', '..orm...', '..om....', '...o....'],
    # silhouette (joueurs en ligne)
    'player': ['..ooo...', '.owwwo..', '.owWwo..', '..ooo...', '.owwwo..', 'owwWwwo.', 'owwwwwo.', 'ooooooo.'],
    # barres de réseau (ping)
    'ping': ['......oo', '......ow', '...oo.ow', '...ow.ow', 'oo.ow.ow', 'ow.ow.ow', 'ow.ow.ow', 'oooooooo'],
    # parchemin (astuces)
    'scroll': ['.oooooo.', 'oPPPPPpo', '.opbbpo.', '.oPPPPo.', '.opbbpo.', '.oPPPPo.', 'oPPPPPpo', '.oooooo.'],
    # étoile (niveau)
    'star': ['...oo...', '...ol...', 'oooglooo', 'olggggdo', '.oggggo.', '.ogddgo.', 'ogo..ogo', 'oo....oo'],
    # casque (race)
    'helmet': ['..oRRo..', '.ooRmoo.', 'oSSSSSko', 'oSoooSko', 'oSo.oSko', 'oSo.oSko', 'oko.okko', 'ooo.oooo'],
    # grimoire (talents)
    'book': ['.oooooo.', 'oBBBBBWo', 'oBWWBBWo', 'oBBBBBWo', 'oBBWWBWo', 'oBBBBBWo', 'oooooowo', '.oooooo.'],
    # sablier (heure)
    'clock': ['oooooooo', '.oPPPPo.', '..oggo..', '...oo...', '...oo...', '..oPPo..', '.oggggo.', 'oooooooo'],
}

# Police du logo : lettres 5x7 étirées à 10 de haut, en gras, contour sombre et dégradé or.
LETTERS = {
    'E': ['#####', '#....', '#....', '####.', '#....', '#....', '#####'],
    'V': ['#...#', '#...#', '#...#', '#...#', '.#.#.', '.#.#.', '..#..'],
    'O': ['.###.', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.'],
    'X': ['#...#', '#...#', '.#.#.', '..#..', '.#.#.', '#...#', '#...#'],
    'T': ['#####', '..#..', '..#..', '..#..', '..#..', '..#..', '..#..'],
    'R': ['####.', '#...#', '#...#', '####.', '#.#..', '#..#.', '#...#'],
    'A': ['.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#'],
    'C': ['.###.', '#...#', '#....', '#....', '#....', '#...#', '.###.'],
}
ROWMAP = [0, 1, 1, 2, 3, 3, 4, 5, 5, 6]


def logo(text='EVO EXTRACT'):
    cols = []  # masque binaire colonne par colonne
    for ch in text:
        if ch == ' ':
            cols += [[0] * 10] * 3
            continue
        g = LETTERS[ch]
        for x in range(5):
            cols.append([1 if g[ROWMAP[y]][x] == '#' else 0 for y in range(10)])
        cols.append([0] * 10)
        cols.append([0] * 10)
    w, h = len(cols) + 4, 10 + 3
    m = [[0] * w for _ in range(h)]
    for x, col in enumerate(cols):
        for y, v in enumerate(col):
            if v:
                m[y + 1][x + 1] = 1; m[y + 1][x + 2] = 1  # gras : on double vers la droite
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    top, mid, bot = (255, 246, 205), (245, 205, 90), (190, 120, 25)
    for y in range(h):
        for x in range(w):
            if m[y][x]:
                t = (y - 1) / 9
                c = [int(top[i] + (mid[i] - top[i]) * t * 2) if t < .5 else int(mid[i] + (bot[i] - mid[i]) * (t - .5) * 2) for i in range(3)]
                img.putpixel((x, y), tuple(c) + (255,))
            elif any(0 <= y + dy < h and 0 <= x + dx < w and m[y + dy][x + dx] for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                img.putpixel((x, y), OUTL + (255,))
            elif y > 0 and x > 0 and m[y - 1][x - 1]:
                img.putpixel((x, y), (20, 12, 2, 160))  # ombre portée
    return img


PANEL_W = 150
FILL, BAR, EDGE = (16, 13, 10, 165), (120, 85, 20, 190), (200, 155, 50, 230)


def panel(kind):
    """Tranche de panneau de 9 px (une ligne de scoreboard) : top = barre de titre, mid, bot = fermeture."""
    w, h = PANEL_W, 9
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if kind == 'top':
        d.rectangle([1, 0, w - 2, h - 1], fill=BAR)
        d.line([2, 0, w - 3, 0], fill=EDGE); d.point([(1, 1), (w - 2, 1)], fill=EDGE)
        d.line([0, 2, 0, h - 1], fill=EDGE); d.line([w - 1, 2, w - 1, h - 1], fill=EDGE)
    elif kind == 'mid':
        d.rectangle([1, 0, w - 2, h - 1], fill=FILL)
        d.line([0, 0, 0, h - 1], fill=EDGE); d.line([w - 1, 0, w - 1, h - 1], fill=EDGE)
    else:
        d.rectangle([1, 0, w - 2, 1], fill=FILL)
        d.line([0, 0, 0, 1], fill=EDGE); d.line([w - 1, 0, w - 1, 1], fill=EDGE)
        d.point([(1, 2), (w - 2, 2)], fill=EDGE); d.line([2, 3, w - 3, 3], fill=EDGE)
    return img

EMBLEM = [  # blason : écu rouge bordé d'or, épée dorée
    'ooooooooooo',
    'olllllllldo',
    'olmmmlmmmdo',
    'olmRmlmrmdo',
    'olmRlllrmdo',
    'olmrmlmrmdo',
    'odmrmlmrmdo',
    '.odmmlmmdo.',
    '..odmlmdo..',
    '...odddo...',
    '....ooo....',
]


def divider(w, name):
    """Filet doré qui s'efface vers les bords, losange au centre."""
    h = 5
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    c = w // 2
    for x in range(w):
        t = 1 - abs(x - c) / c
        a = int(255 * min(1, t * 1.6) ** 1.3)
        col = tuple(int(GOLD_D[i] + (GOLD[i] - GOLD_D[i]) * t) for i in range(3))
        if a > 0:
            img.putpixel((x, 2), col + (a,))
    for dy, half in ((0, 0), (1, 1), (2, 2), (3, 1), (4, 0)):
        for dx in range(-half, half + 1):
            img.putpixel((c + dx, dy), (GOLD_L if abs(dx) < half else GOLD) + (255,))
    img.putpixel((c, 2), OUTL + (255,))
    for q in (c // 2, c + c // 2):
        img.putpixel((q, 1), GOLD + (200,)); img.putpixel((q, 3), GOLD + (200,))
    return img


def official_logo():
    """Logo du serveur (src/assets/logo_evo_source.png) sans son halo. Max 256 px de large : au-delà le jeu ne peut pas charger le glyphe."""
    im = Image.open(os.path.join(ROOT, 'src/assets/logo_evo_source.png')).convert('RGBA')
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3] < 110:
                px[x, y] = (0, 0, 0, 0)
    im = im.crop(im.getbbox())
    w = 240
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    glyphs = []  # (nom, image, ascent, height)
    late = ('helmet', 'book', 'clock')
    for name, rows in ICONS.items():
        if name not in late:
            glyphs.append((name, grid(rows, PAL), 7, 8))
    glyphs.append(('emblem', grid(EMBLEM, PAL), 8, 10))
    glyphs.append(('divider', divider(181, 'divider'), 2, 5))
    glyphs.append(('divider_short', divider(91, 'divider_short'), 2, 5))
    # ajouts du scoreboard en panneaux (toujours à la fin pour garder les codes existants)
    for name in late:
        glyphs.append((name, grid(ICONS[name], PAL), 7, 8))
    lg = logo()
    glyphs.append(('logo', lg, 10, lg.height))
    for k in ('top', 'mid', 'bot'):
        glyphs.append(('panel_' + k, panel(k), 8, 9))

    font = json.load(open(FONT, encoding='utf-8'))
    font['providers'] = [p for p in font['providers'] if not str(p.get('file', '')).startswith('evo:hud/')]
    table = {}
    for i, (name, img, ascent, height) in enumerate(glyphs):
        img.save(os.path.join(OUT, name + '.png'))
        ch = chr(0xE200 + i)
        font['providers'].insert(len(font['providers']) - 1,
                                 {'type': 'bitmap', 'file': f'evo:hud/{name}.png', 'ascent': ascent, 'height': height, 'chars': [ch]})
        table[name] = f'\\u{0xE200 + i:04X}'
    # logo officiel (île EVO), discret : 20 px dans la tablist, 13 px dans le titre du scoreboard (images à 2x)
    base = official_logo()
    for j, (name, ascent, height) in enumerate((('logo_tab', 15, 20), ('logo_sb', 10, 13))):
        img = base.resize((round(base.width * height * 2 / base.height), height * 2), Image.LANCZOS)
        img.save(os.path.join(OUT, name + '.png'))
        ch = chr(0xE200 + len(glyphs) + j)
        font['providers'].insert(len(font['providers']) - 1,
                                 {'type': 'bitmap', 'file': f'evo:hud/{name}.png', 'ascent': ascent, 'height': height, 'chars': [ch]})
        table[name] = f'\\u{ord(ch):04X}'
    json.dump(font, open(FONT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k, v in table.items():
        print(k, v)


if __name__ == '__main__':
    main()
