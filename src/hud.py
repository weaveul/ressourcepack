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
}

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


def main():
    os.makedirs(OUT, exist_ok=True)
    glyphs = []  # (nom, image, ascent, height)
    for name, rows in ICONS.items():
        glyphs.append((name, grid(rows, PAL), 7, 8))
    glyphs.append(('emblem', grid(EMBLEM, PAL), 8, 10))
    glyphs.append(('divider', divider(181, 'divider'), 2, 5))
    glyphs.append(('divider_short', divider(91, 'divider_short'), 2, 5))

    font = json.load(open(FONT, encoding='utf-8'))
    font['providers'] = [p for p in font['providers'] if not str(p.get('file', '')).startswith('evo:hud/')]
    table = {}
    for i, (name, img, ascent, height) in enumerate(glyphs):
        img.save(os.path.join(OUT, name + '.png'))
        ch = chr(0xE200 + i)
        font['providers'].insert(len(font['providers']) - 1,
                                 {'type': 'bitmap', 'file': f'evo:hud/{name}.png', 'ascent': ascent, 'height': height, 'chars': [ch]})
        table[name] = f'\\u{0xE200 + i:04X}'
    json.dump(font, open(FONT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k, v in table.items():
        print(k, v)


if __name__ == '__main__':
    main()
