"""Portes de style (Elfe, Nain, Sorcier, Orc) pour le mécanisme Oraxen « block: type: DOOR ».

Oraxen pose ces portes sous la forme des portes de cuivre cirées (custom-variation 1 à 4) ; on écrit nous-mêmes
leurs états de bloc et modèles dans le pack, Oraxen ne sert que pour la pose (son propre pack n'est pas envoyé).
Sorties : pack/assets/minecraft/blockstates/waxed_*copper_door.json, pack/assets/evo/models/block/portes,
pack/assets/evo/textures/block/portes, pack/assets/evo/items/porte_<style>.json et l'aperçu src/portes/apercu.png.
"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'items'))
from kit import h, mix, clamp

PACK = os.path.join(HERE, '..', '..', 'pack', 'assets')
# variation Oraxen -> bloc vanilla remplacé
BLOCKS = {1: 'waxed_copper_door', 2: 'waxed_exposed_copper_door', 3: 'waxed_weathered_copper_door',
          4: 'waxed_oxidized_copper_door'}
STYLES = [('elfe', 1, 'Porte sylvestre', '#9ad18a'), ('nain', 2, 'Porte du clan', '#e0a84a'),
          ('sorcier', 3, 'Porte arcanique', '#a98cff'), ('orc', 4, 'Porte de rondins', '#d0584a')]


def noisy(c, x, y, n=8, s=0):
    d = (h(x, y, s) - 0.5) * 2 * n
    return tuple(clamp(v + d) for v in c) + (255,)


def plank(x, y, base, s, vertical=True):
    """Planches verticales de 4 px avec sillons et grain."""
    k = 1.0
    if (x % 4 == 0) if vertical else (y % 4 == 0):
        k = 0.72
    elif h(x, y // 3, s) > 0.8:
        k = 0.88
    return tuple(v * k for v in base)


def paint(style, full):
    """full : coordonnées 0..15 en x, 0..31 en y (0 = haut de la porte). Renvoie RGBA ou None (transparent)."""
    def px(x, y):
        edge = x in (0, 15) or y in (0, 31)
        if style == 'elfe':
            wood, dark, leaf, moon = (222, 206, 168), (168, 142, 100), (96, 166, 84), (196, 228, 255)
            # fenêtre en ogive en haut
            cx = 7.5
            if 4 <= y <= 13 and abs(x - cx) <= 4.5 - max(0, 7 - y) * 0.7 and 3 <= x <= 12:
                if (x in (7, 8)) or y == 9:
                    return noisy(dark, x, y, 4)
                return (*mix(moon, (255, 255, 255), 0.2 if (x + y) % 5 == 0 else 0), 200)
            if edge or x == 1 and y > 2:
                return noisy(dark, x, y, 6)
            # liane
            vx = 3 + int(2 * __import__('math').sin(y / 3))
            if y > 14 and (x == vx or (y % 5 == 0 and x == vx + 1)):
                return noisy(leaf, x, y, 14)
            if y > 14 and y % 5 == 1 and x in (vx + 1, vx + 2):
                return noisy((130, 200, 100), x, y, 10)
            if 12 <= x <= 13 and 17 <= y <= 19:
                return noisy((214, 222, 232), x, y, 4)
            return noisy(plank(x, y, wood, 1), x, y, 6)
        if style == 'nain':
            wood, iron, gold, rune = (92, 60, 38), (84, 86, 94), (222, 168, 54), (255, 196, 70)
            if edge:
                return noisy((70, 68, 74), x, y, 6)
            if y in (3, 4, 15, 16, 27, 28):
                return noisy(iron if y % 2 else tuple(v * 1.3 for v in iron), x, y, 4)
            if (y in (3, 4, 15, 16, 27, 28)) or ((x in (2, 13)) and y in (5, 14, 17, 26) ):
                return noisy(iron, x, y, 4)
            # losange runique doré au centre
            dx, dy = abs(x - 7.5), abs(y - 9.5)
            if dx + dy <= 3.5:
                return noisy(rune if dx + dy <= 1.5 else gold, x, y, 6)
            if x in (12, 13) and 19 <= y <= 22:
                return noisy(gold, x, y, 6)
            return noisy(plank(x, y, wood, 2), x, y, 6)
        if style == 'sorcier':
            wood, cloth, gold, arc = (70, 46, 88), (52, 38, 120), (214, 176, 80), (190, 120, 255)
            if edge:
                return noisy(tuple(v * 0.75 for v in wood), x, y, 5)
            # hublot rond
            d2 = (x - 7.5) ** 2 + (y - 8) ** 2
            if d2 <= 12:
                return (*mix(arc, (255, 240, 255), 0.4 if d2 < 3 else 0), 210)
            if d2 <= 18:
                return noisy(gold, x, y, 6)
            # panneau étoilé
            if 3 <= x <= 12 and 15 <= y <= 28:
                if x in (3, 12) or y in (15, 28):
                    return noisy(gold, x, y, 6)
                if h(x, y, 9) > 0.9:
                    return (255, 236, 160, 255)
                return noisy(cloth, x, y, 8)
            if x in (12, 13) and y in (19, 20, 21):
                return noisy(arc, x, y, 6)
            return noisy(plank(x, y, wood, 3), x, y, 6)
        if style == 'orc':
            log, bark_c, bone, red, iron = (104, 74, 46), (70, 50, 32), (226, 216, 186), (150, 28, 26), (92, 84, 80)
            # haut en pointes de pieux
            if y < 3 and (x % 4 in (0, 3)) and y < 3 - (0 if x % 4 in (1, 2) else 2):
                return None
            if y == 0 and x % 4 in (0, 3):
                return None
            if y in (5, 6, 25, 26):
                return noisy(iron, x, y, 10)
            # crâne
            if 5 <= x <= 10 and 10 <= y <= 15:
                if (y == 12 and x in (6, 9)) or (y == 14 and x in (7, 8)):
                    return (40, 30, 24, 255)
                if y == 15 and x in (5, 10):
                    return noisy(log, x, y, 6)
                return noisy(bone, x, y, 6)
            # trait de peinture de guerre
            if abs((x - 2) - (y - 17) * 0.8) < 1 and 17 <= y <= 23:
                return noisy(red, x, y, 6)
            c = bark_c if x % 4 in (0, 3) else log
            if h(x, y // 2, 4) > 0.82:
                c = tuple(v * 0.8 for v in c)
            return noisy(c, x, y, 8)
    return px


def build():
    os.makedirs(os.path.join(PACK, 'evo', 'textures', 'block', 'portes'), exist_ok=True)
    os.makedirs(os.path.join(PACK, 'evo', 'models', 'block', 'portes'), exist_ok=True)
    os.makedirs(os.path.join(PACK, 'evo', 'models', 'item', 'portes'), exist_ok=True)
    os.makedirs(os.path.join(PACK, 'evo', 'textures', 'item', 'portes'), exist_ok=True)
    os.makedirs(os.path.join(PACK, 'minecraft', 'blockstates'), exist_ok=True)
    sheet = Image.new('RGBA', (len(STYLES) * 40, 76), (139, 139, 139, 255))
    for i, (style, var, name, color) in enumerate(STYLES):
        px = paint(style, True)
        full = Image.new('RGBA', (16, 32), (0, 0, 0, 0))
        for y in range(32):
            for x in range(16):
                c = px(x, y)
                if c:
                    full.putpixel((x, y), tuple(clamp(v) for v in c))
        tdir = os.path.join(PACK, 'evo', 'textures', 'block', 'portes')
        full.crop((0, 0, 16, 16)).save(os.path.join(tdir, f'{style}_top.png'))
        full.crop((0, 16, 16, 32)).save(os.path.join(tdir, f'{style}_bottom.png'))
        # icône : la porte entière réduite dans 16x16 (largeur 8)
        icon = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        icon.alpha_composite(full.resize((8, 16), Image.NEAREST), (4, 0))
        icon.save(os.path.join(PACK, 'evo', 'textures', 'item', 'portes', f'porte_{style}.png'))
        with open(os.path.join(PACK, 'evo', 'models', 'item', 'portes', f'porte_{style}.json'), 'w') as f:
            json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'evo:item/portes/porte_{style}'}}, f, indent=2)
        with open(os.path.join(PACK, 'evo', 'items', f'porte_{style}.json'), 'w') as f:
            json.dump({'model': {'type': 'minecraft:model', 'model': f'evo:item/portes/porte_{style}'}}, f, indent=2)
        # modèles des 8 formes de porte
        for half in ('bottom', 'top'):
            for hinge in ('left', 'right'):
                for op in ('', '_open'):
                    m = f'door_{half}_{hinge}{op}'
                    with open(os.path.join(PACK, 'evo', 'models', 'block', 'portes', f'{style}_{half}_{hinge}{op}.json'), 'w') as f:
                        json.dump({'parent': f'minecraft:block/{m}', 'textures': {
                            'bottom': f'evo:block/portes/{style}_bottom', 'top': f'evo:block/portes/{style}_top'}}, f, indent=2)
        # état de bloc (même logique que les portes vanilla)
        base = {'east': 0, 'south': 90, 'west': 180, 'north': 270}
        variants = {}
        for facing, r in base.items():
            for half, hm in (('lower', 'bottom'), ('upper', 'top')):
                for hinge in ('left', 'right'):
                    for op in (False, True):
                        y = (r + (90 if hinge == 'left' else 270) * op) % 360
                        v = {'model': f'evo:block/portes/{style}_{hm}_{hinge}{"_open" if op else ""}'}
                        if y:
                            v['y'] = y
                        variants[f'facing={facing},half={half},hinge={hinge},open={str(op).lower()}'] = v
        with open(os.path.join(PACK, 'minecraft', 'blockstates', BLOCKS[var] + '.json'), 'w') as f:
            json.dump({'variants': variants}, f, indent=2)
        sheet.alpha_composite(full.resize((32, 64), Image.NEAREST), (i * 40 + 4, 6))
    sheet.save(os.path.join(HERE, 'apercu.png'))


def oraxen_yml():
    out = ['# Généré par src/portes/generate.py (dépôt ressourcepack). Ne pas éditer à la main.',
           '# Les états de bloc et modèles sont dans le pack EvoExtract, pas dans le pack Oraxen.', '']
    for style, var, name, color in STYLES:
        out += [f'porte_{style}:', f'  itemname: "<{color}>{name}"', '  material: PAPER', '  lore:',
                f'    - "<gray>Porte de style {style.capitalize()}"', '  components:',
                f'    item_model: evo:porte_{style}', '  mechanics:', '    block:', '      type: DOOR',
                f'      custom_variation: {var}', f'      model: evo:block/portes/{style}_bottom_left',
                '      block_sounds:', '        break_sound: block.wood.break', '        place_sound: block.wood.place', '']
    path = os.path.join(HERE, '..', 'items', 'oraxen', 'items', 'evo_portes.yml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    return path


if __name__ == '__main__':
    build()
    print(oraxen_yml())
