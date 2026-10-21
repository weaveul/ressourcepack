"""Barre d'énergie du HUD (au-dessus de la barre de nourriture).

Dessine pack/assets/evo/textures/hud/energie_cadre.png et energie_<k>.png (k = 1..40, remplissage)
et ajoute leurs glyphes U+E220 (cadre) et U+E221..U+E248 (remplissages) à minecraft:default.
EvoPerso compose la barre dans la barre d'action avec les espaces U+F1xx / U+F3xx.
Usage : python3 src/energy_hud.py   (depuis la racine du dépôt)
"""
import json, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'pack/assets/evo/textures/hud')
FONT = os.path.join(ROOT, 'pack/assets/minecraft/font/default.json')

W, H = 81, 9            # même largeur que la barre de nourriture
INNER = W - 2           # remplissage entre les deux bords
STEPS = 40
ASCENT = -16            # descend la barre de la ligne d'action jusqu'au-dessus de la nourriture

OUTL, BACK, BACK_D = (18, 22, 44), (40, 48, 82), (30, 36, 64)
GOLD, GOLD_D = (232, 190, 70), (150, 105, 25)
FILL_L, FILL, FILL_D, SHINE = (140, 235, 255), (60, 170, 245), (35, 105, 200), (220, 250, 255)


def frame():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for x in range(W):
        for y in range(H):
            edge = x in (0, W - 1) or y in (0, H - 1)
            if edge:
                if (x, y) in ((0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)):
                    continue
                img.putpixel((x, y), OUTL + (255,))
            else:
                img.putpixel((x, y), (BACK if y < H // 2 else BACK_D) + (230,))
    # coins dorés
    for x, y in ((1, 1), (W - 2, 1), (1, H - 2), (W - 2, H - 2)):
        img.putpixel((x, y), GOLD + (255,))
    # graduations tous les quarts
    for q in (1, 2, 3):
        x = 1 + round(INNER * q / 4)
        img.putpixel((x, H - 2), GOLD_D + (255,))
    return img


def fill(w):
    img = Image.new('RGBA', (w, H), (0, 0, 0, 0))
    for x in range(w):
        for y in range(1, H - 1):
            c = FILL_L if y <= 2 else FILL if y <= 5 else FILL_D   # bandes franches (cel)
            img.putpixel((x, y), c + (255,))
        if x == w - 1 and w > 2:
            for y in range(1, H - 1):
                img.putpixel((x, y), SHINE + (255,))             # bord lumineux
    for x in range(1, w - 1, 6):
        img.putpixel((x, 2), SHINE + (255,))
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    frame().save(os.path.join(OUT, 'energie_cadre.png'))
    providers = [{'type': 'bitmap', 'file': 'evo:hud/energie_cadre.png', 'ascent': ASCENT, 'height': H, 'chars': ['']}]
    for k in range(1, STEPS + 1):
        w = max(1, round(INNER * k / STEPS))
        fill(w).save(os.path.join(OUT, 'energie_%d.png' % k))
        providers.append({'type': 'bitmap', 'file': 'evo:hud/energie_%d.png' % k, 'ascent': ASCENT, 'height': H,
                          'chars': [chr(0xE220 + k)]})
    font = json.load(open(FONT, encoding='utf-8'))
    font['providers'] = [p for p in font['providers'] if not str(p.get('file', '')).startswith('evo:hud/energie')]
    # avant le fournisseur d'espaces pour garder l'ordre lisible
    i = next((n for n, p in enumerate(font['providers']) if p.get('type') == 'space'), len(font['providers']))
    font['providers'][i:i] = providers
    json.dump(font, open(FONT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('largeurs :', [max(1, round(INNER * k / STEPS)) for k in range(1, STEPS + 1)][:5], '...')


if __name__ == '__main__':
    main()
