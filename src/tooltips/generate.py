"""Cadres d'infobulle par rareté (composant item minecraft:tooltip_style = evo:<rareté>).
Écrit pack/assets/evo/textures/gui/sprites/tooltip/<rareté>_{background,frame}.png (+ .mcmeta nine-slice).
Le jeu dessine le sprite 9 px autour de la boîte vanilla (marge 9) : le cadre occupe cette marge."""
import json, os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'pack', 'assets', 'evo', 'textures', 'gui', 'sprites', 'tooltip')
N, B = 100, 9
MCMETA = {"gui": {"scaling": {"type": "nine_slice", "width": N, "height": N, "border": B}}}

# rareté : (couleur vive, couleur sombre, reflet, fond RGBA, niveau d'ornement 0-4)
RARETES = {
    'commun':     ((170, 170, 176), (90, 90, 98),   (230, 230, 236), (16, 16, 20, 238), 0),
    'peu_commun': ((92, 200, 92),   (34, 100, 40),  (190, 255, 170), (10, 20, 12, 238), 1),
    'rare':       ((70, 160, 255),  (24, 70, 140),  (180, 225, 255), (8, 14, 28, 240), 2),
    'epique':     ((180, 92, 255),  (80, 30, 130),  (235, 200, 255), (18, 8, 28, 240), 3),
    'legendaire': ((255, 176, 46),  (140, 80, 14),  (255, 236, 160), (26, 16, 6, 242), 4),
}
OUTLINE = (10, 8, 6, 255)


def frame(main, dark, hi, lvl):
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    px = im.load()

    def rect(i, col):
        for k in range(i, N - i):
            for p in ((k, i), (k, N - 1 - i), (i, k), (N - 1 - i, k)):
                px[p] = col + (255,) if len(col) == 3 else col

    rect(2, OUTLINE)
    rect(3, main)
    rect(4, dark)
    rect(5, OUTLINE)
    if lvl >= 2:            # double filet
        rect(6, dark if lvl == 2 else main)
        rect(7, OUTLINE if lvl >= 3 else (0, 0, 0, 0))
    # reflet en haut à gauche du filet principal
    for k in range(4, N - 4):
        px[k, 3] = hi + (255,)
        px[3, k] = hi + (255,)

    def diamond(cx, cy, r, col, core=None):
        for y in range(cy - r - 1, cy + r + 2):
            for x in range(cx - r - 1, cx + r + 2):
                d = abs(x - cx) + abs(y - cy)
                if 0 <= x < N and 0 <= y < N:
                    if d == r + 1:
                        px[x, y] = OUTLINE
                    elif d <= r:
                        px[x, y] = (core if core and d <= max(0, r - 2) else col) + (255,)

    corners = [(4, 4), (N - 5, 4), (4, N - 5), (N - 5, N - 5)]
    for cx, cy in corners:
        if lvl == 1:
            diamond(cx, cy, 1, main, hi)
        elif lvl == 2:
            for y in range(cy - 2, cy + 3):
                for x in range(cx - 2, cx + 3):
                    px[x, y] = (OUTLINE if abs(x - cx) == 2 or abs(y - cy) == 2 else main + (255,)) if True else 0
            px[cx, cy] = hi + (255,)
        elif lvl == 3:
            diamond(cx, cy, 3, main, hi)
        elif lvl == 4:
            diamond(cx, cy, 4, main, hi)
            px[cx, cy] = (255, 255, 255, 255)
    # clous le long des bords (les bords sont répétés : un clou au milieu de chaque segment de 82 px)
    if lvl >= 3:
        for c in (N // 2 - 20, N // 2, N // 2 + 20):
            for (x, y) in ((c, 3), (c, N - 4), (3, c), (N - 4, c)):
                diamond(x, y, 1 if lvl == 3 else 2, hi if lvl == 4 else main, (255, 255, 255) if lvl == 4 else hi)
    return im


def background(bg, main, lvl):
    """Fond sombre teinté, avec une lueur de la couleur de rareté qui s'estompe vers l'intérieur."""
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    px = im.load()
    glow = 2 + lvl              # profondeur de la lueur : reste dans la bordure de 9 px (sinon raccords visibles)
    for y in range(3, N - 3):
        for x in range(3, N - 3):
            d = min(x, y, N - 1 - x, N - 1 - y) - 3
            t = max(0.0, 1 - d / glow) * (0.10 + 0.05 * lvl)
            px[x, y] = tuple(int(bg[i] * (1 - t) + main[i] * t) for i in range(3)) + (bg[3],)
    return im


os.makedirs(ROOT, exist_ok=True)
for r, (main, dark, hi, bg, lvl) in RARETES.items():
    for kind, im in (('frame', frame(main, dark, hi, lvl)), ('background', background(bg, main, lvl))):
        p = os.path.join(ROOT, f'{r}_{kind}.png')
        im.save(p)
        json.dump(MCMETA, open(p + '.mcmeta', 'w'), indent=2)
print('ok', sorted(os.listdir(ROOT)))
