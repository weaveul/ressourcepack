"""Catalogue des objets 3D d'Evo Extract : armes de classe, matériaux de raid, sacoches.

Lancer `python3 src/items/generate.py` pour régénérer les textures, modèles et définitions,
ainsi que l'aperçu src/items/apercu.png.
"""
from kit import Item, HANDHELD, BOW, OBJECT

SWORD = -45  # inclinaison des armes (pointe en haut à droite, comme les épées vanilla)


def tip(it, y, w, d, mat='edge'):
    """Pointe de lame en trois paliers."""
    it.col(y, y + 1.4, w * 0.75, d * 0.9, mat)
    it.col(y + 1.4, y + 2.4, w * 0.45, d * 0.8, mat)
    it.col(y + 2.4, y + 3.0, w * 0.2, d * 0.6, mat)


# =====================================================================================
#  Armes
# =====================================================================================

def guerrier_epee_longue():
    it = Item('guerrier_epee_longue', tilt=SWORD)
    it.col(-3.2, -1.6, 2.2, 2.2, 'gold')
    it.col(-2.8, -2.0, 2.4, 1.0, 'ruby')
    it.col(-1.6, 3.6, 1.4, 1.4, 'leather')
    it.box((3.4, 3.6, 7.2), (12.6, 4.8, 8.8), 'steel_dark')
    it.box((2.6, 3.3, 7.0), (3.6, 5.1, 9.0), 'gold')
    it.box((12.4, 3.3, 7.0), (13.4, 5.1, 9.0), 'gold')
    it.col(4.8, 6.0, 2.6, 1.3, 'steel')
    it.col(6.0, 16.0, 1.9, 1.0, 'steel')
    it.box((6.65, 6.0, 7.6), (7.05, 16.0, 8.4), 'edge')
    it.box((8.95, 6.0, 7.6), (9.35, 16.0, 8.4), 'edge')
    it.box((7.6, 6.6, 7.45), (8.4, 14.0, 8.55), 'steel_dark')
    tip(it, 16.0, 2.7, 1.0)
    return it


def guerrier_hache():
    it = Item('guerrier_hache', tilt=SWORD)
    it.col(-3.4, -2.6, 1.9, 1.9, 'iron')
    it.col(-2.6, 17.4, 1.4, 1.4, 'wood')
    it.col(-2.0, 3.0, 1.65, 1.65, 'leather')
    it.col(9.0, 9.8, 1.6, 1.6, 'iron')
    it.col(12.4, 17.6, 2.2, 2.0, 'steel_dark')
    it.box((9.1, 13.0, 7.4), (12.0, 16.8, 8.6), 'steel')
    it.box((12.0, 12.0, 7.5), (14.0, 17.8, 8.5), 'steel')
    it.box((14.0, 11.0, 7.6), (15.2, 18.8, 8.4), 'edge')
    it.box((13.4, 10.2, 7.65), (14.6, 11.2, 8.35), 'edge')
    it.box((13.4, 18.6, 7.65), (14.6, 19.6, 8.35), 'edge')
    it.box((5.0, 14.0, 7.7), (6.9, 15.8, 8.3), 'steel_dark')
    it.box((3.6, 14.4, 7.8), (5.0, 15.4, 8.2), 'steel')
    it.col(17.6, 19.2, 0.8, 0.8, 'steel')
    it.box((10.0, 14.2, 8.6), (11.4, 15.6, 8.8), 'bronze')
    return it


def paladin_marteau():
    it = Item('paladin_marteau', tilt=SWORD)
    it.col(-3.4, -2.4, 2.0, 2.0, 'gold')
    it.col(-2.4, 14.0, 1.4, 1.4, 'wood_pale')
    it.col(-1.8, 3.2, 1.7, 1.7, 'leather')
    it.col(6.0, 6.8, 1.7, 1.7, 'gold')
    it.col(11.0, 11.8, 1.7, 1.7, 'gold')
    it.box((3.6, 14.0, 6.0), (12.4, 19.0, 10.0), 'steel')
    it.box((3.2, 13.7, 5.7), (4.4, 19.3, 10.3), 'gold')
    it.box((11.6, 13.7, 5.7), (12.8, 19.3, 10.3), 'gold')
    it.box((7.0, 15.3, 9.9), (9.0, 17.7, 10.35), 'holy')
    it.box((7.0, 15.3, 5.65), (9.0, 17.7, 6.1), 'holy')
    it.box((7.7, 14.6, 9.95), (8.3, 18.4, 10.3), 'holy')
    it.box((6.3, 16.2, 9.95), (9.7, 16.8, 10.3), 'holy')
    it.col(19.0, 19.8, 1.6, 1.6, 'gold')
    return it


def paladin_epee():
    it = Item('paladin_epee', tilt=SWORD)
    it.col(-3.2, -1.6, 2.2, 2.2, 'gold')
    it.col(-1.6, 3.4, 1.4, 1.4, 'cloth_blue')
    it.col(0.8, 1.3, 1.6, 1.6, 'gold')
    it.col(3.4, 5.4, 3.0, 1.8, 'gold')
    it.box((2.2, 4.4, 7.4), (5.0, 5.2, 8.6), 'gold')
    it.box((11.0, 4.4, 7.4), (13.8, 5.2, 8.6), 'gold')
    it.box((1.4, 4.8, 7.5), (2.4, 6.4, 8.5), 'gold_dark')
    it.box((13.6, 4.8, 7.5), (14.6, 6.4, 8.5), 'gold_dark')
    it.box((7.3, 3.8, 8.85), (8.7, 5.0, 9.15), 'holy')
    it.box((7.3, 3.8, 6.85), (8.7, 5.0, 7.15), 'holy')
    it.col(5.4, 16.2, 2.8, 0.9, 'silver')
    it.box((7.7, 6.0, 7.5), (8.3, 15.0, 8.5), 'gold')
    tip(it, 16.2, 2.8, 0.9, 'silver')
    return it


def mage_baton():
    it = Item('mage_baton', tilt=SWORD)
    it.col(-4.0, -3.2, 1.6, 1.6, 'gold')
    it.col(-3.2, 14.6, 1.3, 1.3, 'wood_dark')
    it.col(0.6, 4.2, 1.6, 1.6, 'cloth_blue')
    it.col(4.2, 4.8, 1.7, 1.7, 'gold')
    it.col(10.0, 10.6, 1.6, 1.6, 'gold')
    it.col(14.4, 15.6, 2.6, 2.6, 'gold')
    it.col(15.6, 19.4, 1.8, 1.8, 'arcane')
    it.col(19.4, 20.6, 1.0, 1.0, 'arcane')
    for x, z in ((6.3, 6.3), (9.1, 6.3), (6.3, 9.1), (9.1, 9.1)):
        it.box((x, 15.6, z), (x + 0.6, 18.4, z + 0.6), 'gold')
        ix, iz = x + (0.5 if x < 8 else -0.5), z + (0.5 if z < 8 else -0.5)
        it.box((ix, 18.2, iz), (ix + 0.6, 19.0, iz + 0.6), 'gold')
    it.box((5.2, 16.8, 7.7), (6.2, 17.4, 8.3), 'arcane')
    it.box((9.8, 17.6, 7.7), (10.8, 18.2, 8.3), 'arcane')
    return it


def mage_sceptre():
    it = Item('mage_sceptre', tilt=SWORD)
    it.col(-2.6, -1.6, 1.5, 1.5, 'sapphire')
    it.col(-1.6, 13.0, 1.0, 1.0, 'gold')
    it.col(0.0, 4.0, 1.3, 1.3, 'cloth_blue')
    it.col(7.0, 7.6, 1.3, 1.3, 'gold_dark')
    it.col(12.6, 14.2, 2.4, 2.4, 'gold')
    it.col(14.0, 17.8, 3.4, 3.4, 'sapphire')
    it.box((5.6, 15.6, 7.6), (10.4, 16.2, 8.4), 'gold')
    it.box((7.6, 15.6, 5.6), (8.4, 16.2, 10.4), 'gold')
    it.col(17.8, 18.8, 1.2, 1.2, 'gold')
    it.col(18.8, 20.2, 0.6, 0.6, 'holy')
    it.box((7.1, 19.2, 7.7), (8.9, 19.8, 8.3), 'holy')
    return it


def rodeur_dague():
    it = Item('rodeur_dague', tilt=SWORD)
    it.col(-2.2, -1.0, 1.6, 1.6, 'steel_dark')
    it.col(-1.0, 2.6, 1.2, 1.2, 'leather_dark')
    it.box((5.2, 2.6, 7.4), (10.8, 3.4, 8.6), 'steel_dark')
    it.box((4.6, 1.8, 7.5), (5.4, 3.0, 8.5), 'steel_dark')
    it.box((10.6, 1.8, 7.5), (11.4, 3.0, 8.5), 'steel_dark')
    it.box((7.4, 2.7, 8.55), (8.6, 3.3, 8.8), 'emerald')
    it.col(3.4, 10.4, 1.8, 0.7, 'steel')
    it.box((8.6, 3.4, 7.7), (9.1, 10.4, 8.3), 'edge')
    it.box((7.8, 4.0, 7.62), (8.2, 9.0, 8.38), 'steel_dark')
    tip(it, 10.4, 2.3, 0.7)
    return it


def druide_baton():
    it = Item('druide_baton', tilt=SWORD)
    it.col(-4.0, 2.0, 1.5, 1.5, 'wood_dark', cx=8.0)
    it.col(2.0, 7.0, 1.5, 1.5, 'wood_dark', cx=8.3)
    it.col(7.0, 12.0, 1.5, 1.5, 'wood_dark', cx=7.8)
    it.col(12.0, 15.0, 1.6, 1.6, 'wood_dark', cx=8.1)
    it.box((8.9, 4.6, 7.6), (9.6, 5.6, 8.4), 'wood_dark')
    it.box((6.4, 9.6, 7.6), (7.1, 10.4, 8.4), 'wood_dark')
    it.col(4.4, 5.8, 1.75, 1.75, 'moss', cx=8.3)
    it.col(-1.0, 1.4, 1.7, 1.7, 'leather', cx=8.0)
    it.box((6.0, 14.6, 7.3), (7.0, 18.6, 8.7), 'wood_dark')
    it.box((9.0, 14.6, 7.3), (10.0, 18.6, 8.7), 'wood_dark')
    it.box((6.7, 18.2, 7.4), (7.7, 19.4, 8.6), 'wood_dark')
    it.box((8.3, 18.2, 7.4), (9.3, 19.4, 8.6), 'wood_dark')
    it.col(15.4, 18.2, 1.7, 1.7, 'emerald')
    it.box((3.8, 17.0, 7.8), (6.0, 18.2, 8.2), 'leaf')
    it.box((10.0, 16.0, 7.8), (12.4, 17.0, 8.2), 'leaf_dark')
    it.box((5.0, 19.0, 7.8), (6.8, 20.2, 8.2), 'leaf')
    it.box((9.4, 19.2, 7.8), (10.8, 20.0, 8.2), 'leaf_dark')
    return it


def druide_faucille():
    it = Item('druide_faucille', tilt=SWORD)
    it.col(-3.2, -2.4, 1.7, 1.7, 'silver')
    it.col(-2.4, 5.0, 1.4, 1.4, 'wood_pale')
    it.col(-1.8, 2.2, 1.6, 1.6, 'leather')
    it.col(5.0, 6.4, 1.9, 1.9, 'silver')
    it.box((7.3, 5.3, 8.9), (8.7, 6.3, 9.1), 'moon')
    it.box((8.0, 6.4, 7.6), (9.8, 10.0, 8.4), 'silver')
    it.box((8.6, 10.0, 7.6), (10.6, 13.0, 8.4), 'silver')
    it.box((8.0, 13.0, 7.6), (10.2, 15.6, 8.4), 'silver')
    it.box((6.0, 15.4, 7.6), (9.2, 17.0, 8.4), 'silver')
    it.box((3.6, 15.8, 7.6), (6.4, 17.4, 8.4), 'silver')
    it.box((2.0, 14.8, 7.65), (3.8, 16.6, 8.35), 'moon')
    it.box((7.5, 7.0, 7.7), (8.0, 12.6, 8.3), 'moon')
    it.box((7.6, 12.6, 7.7), (8.1, 15.0, 8.3), 'moon')
    it.box((4.0, 15.3, 7.7), (7.6, 15.8, 8.3), 'moon')
    return it


def lamerunique_lame():
    it = Item('lamerunique_lame', tilt=SWORD)
    it.col(-3.2, -1.8, 2.0, 2.0, 'obsidian')
    it.col(-1.8, -1.4, 1.7, 1.7, 'rune_glow')
    it.col(-1.4, 3.4, 1.3, 1.3, 'leather_dark')
    it.box((4.0, 3.4, 7.3), (12.0, 4.8, 8.7), 'obsidian')
    it.box((4.0, 2.4, 7.5), (5.0, 3.4, 8.5), 'obsidian')
    it.box((11.0, 2.4, 7.5), (12.0, 3.4, 8.5), 'obsidian')
    it.box((7.3, 3.7, 8.7), (8.7, 4.5, 8.95), 'arcane')
    it.box((7.3, 3.7, 7.05), (8.7, 4.5, 7.3), 'arcane')
    it.col(4.8, 17.0, 2.0, 1.0, 'runestone')
    it.box((6.65, 4.8, 7.7), (7.0, 17.0, 8.3), 'edge')
    it.box((9.0, 4.8, 7.7), (9.35, 17.0, 8.3), 'edge')
    tip(it, 17.0, 2.7, 0.9)
    return it


def lamerunique_glaive():
    it = Item('lamerunique_glaive', tilt=SWORD)
    it.col(-5.0, -3.6, 2.2, 2.2, 'obsidian')
    it.col(-4.6, -4.0, 2.4, 2.4, 'rune_glow')
    it.col(-3.6, 3.0, 1.4, 1.4, 'leather_dark')
    it.col(-1.2, -0.8, 1.55, 1.55, 'rune_glow')
    it.col(1.0, 1.4, 1.55, 1.55, 'rune_glow')
    it.box((2.4, 3.0, 7.2), (13.6, 4.6, 8.8), 'obsidian')
    it.box((1.6, 3.4, 7.3), (2.6, 5.6, 8.7), 'obsidian')
    it.box((13.4, 3.4, 7.3), (14.4, 5.6, 8.7), 'obsidian')
    it.box((3.0, 3.5, 8.75), (13.0, 4.1, 8.95), 'rune_glow')
    it.box((3.0, 3.5, 7.05), (13.0, 4.1, 7.25), 'rune_glow')
    it.col(4.6, 18.4, 3.0, 1.1, 'runestone')
    it.box((6.05, 4.6, 7.7), (6.5, 18.4, 8.3), 'edge')
    it.box((9.5, 4.6, 7.7), (9.95, 18.4, 8.3), 'edge')
    it.col(18.4, 19.8, 2.8, 1.0, 'runestone')
    it.col(19.8, 20.8, 1.6, 0.8, 'edge')
    it.col(20.8, 21.6, 0.7, 0.6, 'edge')
    return it


def rodeur_arc():
    def bow(pull):
        it = Item('rodeur_arc', tilt=45, display=BOW)
        limb = [(8.0, 11.0, 9.2, 10.6), (11.0, 14.0, 8.4, 9.8), (14.0, 16.4, 7.2, 8.6),
                (16.4, 18.4, 6.0, 7.4)]
        for y0, y1, x0, x1 in limb:
            it.box((x0, y0, 7.5), (x1, y1, 8.5), 'wood_pale')
            it.box((x0, 16 - y1, 7.5), (x1, 16 - y0, 8.5), 'wood_pale')
        it.box((5.2, 18.4, 7.6), (6.6, 19.6, 8.4), 'gold')
        it.box((5.2, -3.6, 7.6), (6.6, -2.4, 8.4), 'gold')
        it.box((9.2, 5.8, 7.3), (11.0, 10.2, 8.7), 'leather')
        it.box((10.8, 7.4, 7.7), (11.3, 8.6, 8.3), 'emerald')
        it.box((8.4, 12.4, 8.5), (10.0, 13.4, 8.8), 'leaf')
        it.box((8.4, 2.6, 8.5), (10.0, 3.6, 8.8), 'leaf_dark')
        # corde : escalier de segments entre les extrémités et le point tiré
        sx = 5.75
        steps = 4
        for half in (1, -1):
            for k in range(steps):
                t0, t1 = k / steps, (k + 1) / steps
                x = sx - pull * (1 - (t0 + t1) / 2)
                ya, yb = 8 + half * 11 * t0, 8 + half * 11 * t1
                it.box((x - 0.15, min(ya, yb), 7.9), (x + 0.15, max(ya, yb), 8.1), 'string')
        if pull:
            x0 = sx - pull
            it.box((x0, 7.85, 7.85), (x0 + 11.5, 8.15, 8.15), 'wood_pale')
            it.box((x0 + 11.5, 7.5, 7.8), (x0 + 12.7, 8.5, 8.2), 'steel')
            it.box((x0 + 12.7, 7.8, 7.85), (x0 + 13.3, 8.2, 8.15), 'edge')
            it.box((x0 + 0.2, 7.3, 7.95), (x0 + 2.0, 8.7, 8.05), 'feather')
        return it

    base = bow(0)
    base.variants = {f'_pulling_{i}': bow(p) for i, p in enumerate((1.4, 2.6, 3.6))}
    return base


# =====================================================================================
#  Matériaux de raid (resources.yml)
# =====================================================================================

def obj(id):
    return Item(id, density=4, display=OBJECT)


def scrap_metal():
    it = obj('scrap_metal')
    it.box((3, 0, 6), (11, 1.5, 9), 'iron')
    it.box((6, 1.5, 4), (8, 3, 12), 'steel_dark')
    it.box((9, 0, 9), (13, 2, 11.5), 'bronze')
    it.box((4, 1.5, 9), (6, 4.5, 11), 'iron')
    it.box((10, 0.4, 3.5), (11, 1.2, 8.5), 'steel')
    it.box((3, 0, 3), (5, 1, 5), 'bronze')
    it.box((7.5, 3, 6.5), (11.5, 4, 8), 'iron')
    it.box((5, 4.5, 8), (7.5, 7, 10.5), 'steel_dark')
    it.box((8, 4, 7), (9, 8, 8), 'iron')
    it.box((4.5, 7, 8.5), (8, 7.8, 10), 'bronze')
    return it


def electronic_parts():
    it = obj('electronic_parts')

    def gear(cx, cy, r, z0, z1, mat, hub):
        it.box((cx - r, cy - r, z0), (cx + r, cy + r, z1), mat)
        t = r * 0.45
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if dx:
                x0 = cx + dx * r if dx > 0 else cx - r - 1.2
                it.box((x0, cy - t, z0 + 0.1), (x0 + 1.2, cy + t, z1 - 0.1), mat)
            else:
                y0 = cy + dy * r if dy > 0 else cy - r - 1.2
                it.box((cx - t, y0, z0 + 0.1), (cx + t, y0 + 1.2, z1 - 0.1), mat)
        it.box((cx - r * 0.4, cy - r * 0.4, z0 - 0.2), (cx + r * 0.4, cy + r * 0.4, z1 + 0.2), hub)

    gear(7, 6.2, 3.2, 7.4, 8.8, 'bronze', 'gold')
    gear(11.6, 3.6, 2.0, 9.0, 10.2, 'iron', 'bronze')
    it.box((2, 0, 5), (14, 1, 11), 'wood_dark')
    return it


def power_cell():
    it = obj('power_cell')
    it.box((3, 0, 3), (13, 1.6, 13), 'stone')
    it.col(1.6, 10.5, 2.6, 2.6, 'arcane')
    it.col(10.5, 12.5, 1.4, 1.4, 'arcane')
    it.col(1.6, 7.0, 1.8, 1.8, 'sapphire', cx=5.2, cz=9.4)
    it.col(7.0, 8.4, 0.9, 0.9, 'sapphire', cx=5.2, cz=9.4)
    it.col(1.6, 6.0, 1.6, 1.6, 'arcane', cx=10.8, cz=6.0)
    it.col(6.0, 7.2, 0.8, 0.8, 'arcane', cx=10.8, cz=6.0)
    it.col(1.6, 4.4, 1.4, 1.4, 'amethyst', cx=10.2, cz=11.0)
    return it


def alloy_plate():
    it = obj('alloy_plate')
    it.box((2, 0, 7), (14, 12, 8.6), 'mithril')
    it.box((2, 5.5, 8.6), (14, 6.5, 8.8), 'silver')
    for x, y in ((3, 1), (12.2, 1), (3, 10.2), (12.2, 10.2)):
        it.box((x, y, 8.6), (x + 0.8, y + 0.8, 9.0), 'silver')
    it.box((6.5, 8, 8.6), (9.5, 9, 8.8), 'moon')
    it.box((2.5, 0, 6), (13.5, 0.6, 7), 'stone')
    return it


def colossus_core():
    it = obj('colossus_core')
    it.box((3, 1, 3), (13, 11, 13), 'stone')
    it.box((5.5, 3.5, 2.6), (10.5, 8.5, 13.4), 'ember')
    it.box((2.6, 3.5, 5.5), (13.4, 8.5, 10.5), 'ember')
    it.box((5.5, 10.6, 5.5), (10.5, 11.4, 10.5), 'ember')
    it.box((2.6, 0.6, 2.6), (13.4, 1.6, 13.4), 'obsidian')
    it.box((2.6, 10.4, 2.6), (4.2, 11.6, 4.2), 'obsidian')
    it.box((11.8, 10.4, 11.8), (13.4, 11.6, 13.4), 'obsidian')
    return it


def spider_silk():
    it = obj('spider_silk')
    it.box((4, 0, 4), (12, 1.2, 12), 'wood')
    it.col(1.2, 8.8, 6, 6, 'silk')
    it.box((4, 8.8, 4), (12, 10, 12), 'wood')
    it.col(10, 10.8, 1.4, 1.4, 'wood_dark')
    it.box((10.6, 0.2, 11), (14.5, 0.5, 11.3), 'silk')
    it.box((10.6, 1.4, 10.6), (11, 5, 11), 'silk')
    return it


def runic_leather():
    it = obj('runic_leather')
    it.box((2, 0, 5), (14, 4, 9), 'leather_bag')
    it.box((2, 0.6, 4.4), (14, 3.4, 9.6), 'leather_bag')
    it.box((4.5, -0.1, 4.3), (5.3, 4.1, 9.7), 'leather_dark')
    it.box((10.7, -0.1, 4.3), (11.5, 4.1, 9.7), 'leather_dark')
    it.box((6.8, 0.9, 9.6), (9.2, 3.1, 9.8), 'rune_glow')
    it.box((1.8, 1.2, 5.6), (2, 2.8, 8.4), 'leather_bag_dark')
    it.box((14, 1.2, 5.6), (14.2, 2.8, 8.4), 'leather_bag_dark')
    it.box((5, 0, 9), (12, 0.4, 13), 'leather_bag')
    return it


def moon_silver():
    it = obj('moon_silver')
    it.box((3, 0, 4), (13, 2.5, 8), 'silver')
    it.box((3.6, 2.5, 4.5), (12.4, 3.0, 7.5), 'silver')
    it.box((3.5, 0, 8.6), (13.5, 2.5, 12.6), 'silver')
    it.box((4.1, 2.5, 9.1), (12.9, 3.0, 12.1), 'silver')
    it.box((4, 3.0, 6), (12, 5.5, 10), 'moonsteel')
    it.box((4.6, 5.5, 6.5), (11.4, 6.0, 9.5), 'moonsteel')
    it.box((7.2, 6.0, 7.4), (8.8, 6.3, 8.6), 'moon')
    return it


def dragon_scale():
    it = obj('dragon_scale')
    it.box((3, 6, 7), (13, 13, 8.6), 'scale_red')
    it.box((4, 3, 7.1), (12, 6, 8.5), 'scale_red')
    it.box((5.5, 1, 7.2), (10.5, 3, 8.4), 'scale_red')
    it.box((7, 0, 7.3), (9, 1, 8.3), 'scale_red')
    it.box((2.6, 12.6, 6.8), (13.4, 13.6, 8.8), 'scale_gold')
    it.box((7.5, 1, 8.5), (8.5, 13, 9.0), 'scale_gold')
    it.box((7.5, 1, 6.6), (8.5, 13, 7.1), 'scale_gold')
    it.box((5, 9, 8.6), (6, 11, 8.8), 'ember')
    return it


# =====================================================================================
#  Sacoches sécurisées (raid.yml)
# =====================================================================================

def bag(id, reinforced=False):
    it = obj(id)
    it.box((3, 0, 4), (13, 8, 12), 'leather_bag')
    it.box((5, 8, 6), (11, 10, 10), 'leather_bag')
    it.box((4.6, 9, 5.6), (11.4, 9.8, 10.4), 'leather_dark')
    it.box((3.4, 4, 11.8), (12.6, 8.4, 12.4), 'leather_bag_dark')
    it.box((7.3, 4.6, 12.3), (8.7, 5.8, 12.6), 'gold')
    it.box((2.4, 4, 7), (3, 13, 9), 'leather_dark')
    it.box((13, 4, 7), (13.6, 13, 9), 'leather_dark')
    it.box((2.4, 12.4, 7), (13.6, 13, 9), 'leather_dark')
    if reinforced:
        for x in (2.8, 11.8):
            it.box((x, -0.2, 3.8), (x + 1.4, 3, 12.2), 'iron')
        it.box((2.8, -0.2, 3.8), (13.2, 0.6, 12.2), 'iron')
        it.box((6.6, 3.4, 12.2), (9.4, 6.8, 12.8), 'gold')
        it.box((7.4, 4.4, 12.8), (8.6, 5.6, 13.0), 'ruby')
    return it


def pouch_1():
    return bag('pouch_1')


def pouch_2():
    return bag('pouch_2', reinforced=True)


def pouch_3():
    it = obj('pouch_3')
    it.box((2, 0, 4), (14, 7, 12), 'wood_dark')
    it.box((1.8, 7, 3.8), (14.2, 10, 12.2), 'wood_dark')
    it.box((2.2, 10, 5), (13.8, 11, 11), 'wood_dark')
    for x in (3.5, 11.5):
        it.box((x, -0.1, 3.7), (x + 1, 11.1, 12.3), 'steel_dark')
    it.box((1.7, -0.1, 3.7), (14.3, 0.8, 12.3), 'steel_dark')
    it.box((6.5, 5, 12.2), (9.5, 8.6, 12.7), 'gold')
    it.box((7.4, 5.8, 12.7), (8.6, 7.2, 12.9), 'obsidian')
    it.box((5, 8, 12.2), (11, 9, 12.4), 'rune_glow')
    return it


WEAPONS = [guerrier_epee_longue, guerrier_hache, paladin_marteau, paladin_epee, mage_baton, mage_sceptre,
           rodeur_arc, rodeur_dague, druide_baton, druide_faucille, lamerunique_lame, lamerunique_glaive]
MATERIALS = [scrap_metal, electronic_parts, power_cell, alloy_plate, colossus_core,
             spider_silk, runic_leather, moon_silver, dragon_scale]
POUCHES = [pouch_1, pouch_2, pouch_3]
ALL = WEAPONS + MATERIALS + POUCHES
