"""Armes de butin d'EvoExtract : un modèle 3D propre pour chacune des 60 armes à compétence.

Les armes de base (catalog.py) restent telles quelles ; chaque arme de butin <base>_<compétence> reçoit ici sa
propre silhouette, inspirée de son nom et de sa compétence, et plus richement ornée selon sa rareté (rare : métal
simple, épique : gemmes et métaux nobles, légendaire : or, matières lumineuses). Toutes les pièces sont
attachées à l'arme : rien ne flotte autour.
Modèle : evo:<id>, la valeur par défaut d'EvoExtract (weapons.yml n'a pas besoin de champ model).
"""
import mobs  # noqa: F401  (matériaux partagés : ice, frost_glow, void_glow, flame, glass)
from kit import Item, Mat, MATS, BOW, grain, wrap, sparkle, scales, rings
from catalog import SWORD

MATS.update({
    'b_ice_dark': Mat((80, 140, 205), 10, 0.75, hi=(170, 220, 255)),
    'b_frost': Mat((225, 245, 255), 6, 0.9, light=10, hi=(255, 255, 255)),
    'b_void': Mat((26, 12, 40), 6, 0.75, hi=(90, 50, 130)),
    'b_blood': Mat((132, 16, 26), 10, 0.72, hi=(210, 70, 80)),
    'b_blood_glow': Mat((235, 40, 55), 8, 0.95, light=11),
    'b_poison': Mat((96, 210, 70), 12, 0.9, light=9, pattern=sparkle),
    'b_venom_steel': Mat((70, 96, 74), 8, 0.72, hi=(150, 200, 150)),
    'b_lightning': Mat((255, 238, 120), 6, 1.0, light=15),
    'b_spectral': Mat((150, 240, 228), 8, 0.92, light=12, hi=(230, 255, 250)),
    'b_shadow': Mat((44, 42, 60), 8, 0.75, hi=(110, 100, 150)),
    'b_bark': Mat((88, 62, 40), 12, 0.8, pattern=grain),
    'b_birch': Mat((214, 206, 188), 8, 0.85, pattern=grain),
    'b_cap': Mat((186, 40, 40), 10, 0.8, pattern=lambda c, p, face, px, py, w, hgt: (
        (240, 232, 214) if ((px * 7 + py * 5 + int(p[0] * 3)) % 9 == 0) else c)),
    'b_spore': Mat((230, 214, 160), 8, 0.9, light=8),
    'b_honey': Mat((240, 168, 36), 10, 0.85, light=5, hi=(255, 220, 120)),
    'b_comb': Mat((200, 140, 30), 8, 0.8, pattern=lambda c, p, face, px, py, w, hgt: (
        tuple(v * 0.7 for v in c) if (px % 3 == 0 or (py + (px // 3) % 2) % 3 == 0) else c)),
    'b_black': Mat((34, 30, 30), 6, 0.8),
    'b_fur': Mat((112, 84, 56), 18, 0.8),
    'b_antler': Mat((226, 212, 182), 8, 0.8, hi=(255, 248, 230)),
    'b_sand': Mat((236, 200, 120), 8, 0.9, light=8),
    'b_mirror': Mat((205, 228, 255), 6, 0.85, light=7, hi=(255, 255, 255)),
    'b_sun': Mat((255, 206, 90), 8, 0.92, light=15, hi=(255, 250, 200)),
    'b_chain': Mat((126, 130, 140), 8, 0.7, pattern=rings),
    'b_brass': Mat((198, 150, 70), 10, 0.74, hi=(250, 210, 130)),
    'b_copper': Mat((190, 108, 66), 10, 0.74, hi=(240, 170, 120)),
    'b_jade': Mat((70, 184, 132), 10, 0.75, light=6, pattern=sparkle, hi=(180, 255, 210)),
    'b_pearl': Mat((242, 238, 226), 6, 0.85, light=5),
    'b_white': Mat((232, 234, 242), 6, 0.78, 0.08, hi=(255, 255, 255)),
    'b_black_steel': Mat((56, 58, 70), 8, 0.72, hi=(120, 124, 140)),
    'b_blue_steel': Mat((110, 140, 190), 8, 0.72, 0.1, hi=(200, 220, 250)),
    'b_cloth_white': Mat((230, 228, 220), 6, 0.82),
    'b_cloth_purple': Mat((96, 40, 136), 8, 0.8),
    'b_cloth_grey': Mat((140, 140, 146), 10, 0.85),
    'b_cloth_jade': Mat((60, 150, 120), 8, 0.82),
    'b_smoke': Mat((190, 192, 198), 18, 0.9),
    'b_rope': Mat((176, 146, 98), 8, 0.85, pattern=wrap),
    'b_dragon': Mat((150, 30, 26), 10, 0.7, pattern=scales, hi=(240, 120, 80)),
    'b_dragon_glow': Mat((255, 110, 30), 10, 0.95, light=14, pattern=sparkle),
    'b_horn': Mat((60, 50, 44), 8, 0.78, hi=(140, 120, 100)),
    'b_rock': Mat((104, 100, 98), 18, 0.72),
    'b_crack': Mat((255, 130, 40), 8, 1.0, light=13),
    'b_holy_white': Mat((250, 246, 225), 6, 0.9, light=12),
    'b_storm': Mat((90, 100, 120), 10, 0.75),
    'b_gold_rune': Mat((255, 214, 110), 4, 0.95, light=14),
    'b_red_enamel': Mat((170, 30, 36), 6, 0.78),
    'b_blue_enamel': Mat((40, 70, 170), 6, 0.78),
    'b_leaf_gold': Mat((236, 190, 60), 14, 0.8, light=6),
})


# =====================================================================================
#  Pièces communes
# =====================================================================================

def blade(it, y0, widths, seg, mat, edge=None, d=1.0, offs=None, fuller=None, fw=0.5, cz=8):
    """Lame en tronçons : widths = largeur de chaque tronçon (le dernier fait la pointe), offs = décalage x
    de chaque tronçon (lame courbe, ondulée). Les bords (edge) sont des liserés plus fins que le cœur."""
    for i, w in enumerate(widths):
        ya, yb = y0 + i * seg, y0 + (i + 1) * seg
        cx = 8 + (offs[i] if offs else 0)
        if edge and w > 1.3:
            core = w - 0.7
            it.col(ya, yb, core, d, mat, cx=cx, cz=cz)
            it.box((cx - w / 2, ya, cz - d * 0.32), (cx - core / 2, yb, cz + d * 0.32), edge)
            it.box((cx + core / 2, ya, cz - d * 0.32), (cx + w / 2, yb, cz + d * 0.32), edge)
        else:
            it.col(ya, yb, w, d * (0.8 if edge else 1), edge or mat, cx=cx, cz=cz)
        if fuller and w > 1.6 and i < len(widths) - 2:
            it.box((cx - fw / 2, ya, cz - d / 2 - 0.06), (cx + fw / 2, yb, cz + d / 2 + 0.06), fuller)
    return y0 + len(widths) * seg


def taper(n, w0, w1=0.5):
    """n largeurs qui s'affinent de w0 à w1."""
    return [w0 + (w1 - w0) * i / max(1, n - 1) for i in range(n)]


def hilt(it, grip, pommel, y0=-1.6, y1=3.4, w=1.4, pw=2.2, pmat2=None):
    it.col(y0, y1, w, w, grip)
    it.col(y0 - 1.6, y0, pw, pw, pommel)
    if pmat2:
        it.col(y0 - 1.3, y0 - 0.3, pw + 0.3, pw * 0.5, pmat2)


def bar(it, y, w, hgt, d, mat, cx=8):
    it.box((cx - w / 2, y, 8 - d / 2), (cx + w / 2, y + hgt, 8 + d / 2), mat)


def inlay(it, x0, y0, x1, y1, mat, d=1.0):
    """Incrustation visible des deux côtés d'une lame d'épaisseur d."""
    it.box((x0, y0, 8 - d / 2 - 0.06), (x1, y1, 8 + d / 2 + 0.06), mat)


def staff(it, y0, y1, mat, w=1.3, grip=None, gy=(0.4, 4.2), foot=None):
    it.col(y0, y1, w, w, mat)
    if grip:
        it.col(gy[0], gy[1], w + 0.3, w + 0.3, grip)
    if foot:
        it.col(y0 - 0.8, y0, w + 0.4, w + 0.4, foot)


# =====================================================================================
#  Mage
# =====================================================================================

def mage_baton_orbe_mana():
    it = Item('mage_baton_orbe_mana', tilt=SWORD)
    staff(it, -3.4, 14.4, 'wood_pale', grip='cloth_blue', foot='silver')
    it.col(13.6, 14.6, 2.0, 2.0, 'silver')
    # anneau carré autour de l'orbe
    bar(it, 14.4, 5.0, 0.6, 0.8, 'silver')
    bar(it, 19.4, 5.0, 0.6, 0.8, 'silver')
    it.box((5.5, 14.4, 7.6), (6.1, 20.0, 8.4), 'silver')
    it.box((9.9, 14.4, 7.6), (10.5, 20.0, 8.4), 'silver')
    it.col(15.4, 18.6, 2.6, 2.6, 'arcane')
    it.box((6.1, 16.6, 7.8), (6.9, 17.4, 8.2), 'silver')
    it.box((9.1, 16.6, 7.8), (9.9, 17.4, 8.2), 'silver')
    it.col(20.0, 20.8, 0.8, 0.8, 'sapphire')
    return it


def mage_baton_lance_givre():
    it = Item('mage_baton_lance_givre', tilt=SWORD)
    staff(it, -3.4, 13.0, 'b_birch', grip='b_ice_dark', foot='silver')
    it.col(12.4, 13.6, 2.2, 2.2, 'silver')
    for y, w in ((13.6, 1.9), (15.0, 1.6), (16.6, 1.3), (18.2, 1.0), (19.6, 0.7), (20.6, 0.4)):
        it.col(y, y + 1.6, w, w, 'ice')
    it.col(14.0, 18.0, 0.6, 0.6, 'frost_glow')
    # éclats latéraux plantés dans le collier
    it.box((5.6, 13.2, 7.6), (7.0, 15.6, 8.4), 'ice')
    it.box((5.0, 15.2, 7.7), (5.8, 16.6, 8.3), 'ice')
    it.box((9.0, 13.2, 7.6), (10.4, 15.0, 8.4), 'ice')
    it.box((10.2, 14.8, 7.7), (10.9, 15.9, 8.3), 'ice')
    return it


def mage_sceptre_flammeches():
    it = Item('mage_sceptre_flammeches', tilt=SWORD)
    it.col(-2.6, -1.6, 1.5, 1.5, 'b_copper')
    it.col(-1.6, 12.4, 1.0, 1.0, 'forge_iron')
    it.col(0.0, 4.0, 1.3, 1.3, 'leather_dark')
    # coupelle de braises
    it.col(11.8, 12.8, 1.8, 1.8, 'b_copper')
    it.col(12.8, 13.8, 3.2, 3.2, 'b_copper')
    it.col(13.8, 14.4, 3.8, 3.8, 'b_copper')
    it.col(13.9, 15.0, 3.0, 3.0, 'ember')
    for (x, z, hgt) in ((7.2, 7.2, 2.4), (8.8, 8.4, 3.2), (7.6, 8.9, 1.8), (8.6, 7.0, 2.0)):
        it.box((x - 0.4, 15.0, z - 0.4), (x + 0.4, 15.0 + hgt, z + 0.4), 'flame')
    it.col(15.0, 16.0, 1.2, 1.2, 'flame')
    return it


def mage_sceptre_intrication_arcanique():
    it = Item('mage_sceptre_intrication_arcanique', tilt=SWORD)
    it.col(-2.6, -1.6, 1.5, 1.5, 'amethyst')
    it.col(-1.6, 12.6, 1.0, 1.0, 'silver')
    it.col(0.0, 4.0, 1.3, 1.3, 'b_cloth_purple')
    it.col(12.4, 13.4, 2.0, 2.0, 'silver')
    # croissant de lune ouvert vers le haut, œil d'améthyste au centre
    for (x0, x1, y0, y1) in ((5.0, 6.2, 14.6, 17.4), (5.6, 7.0, 13.4, 14.8), (7.0, 9.0, 13.0, 13.8),
                             (9.0, 10.4, 13.4, 14.8), (9.8, 11.0, 14.6, 17.4), (4.6, 5.6, 17.2, 18.6),
                             (10.4, 11.4, 17.2, 18.6)):
        it.box((x0, y0, 7.6), (x1, y1, 8.4), 'silver')
    it.col(13.8, 16.6, 2.0, 1.4, 'amethyst')
    it.col(14.6, 15.8, 0.8, 1.6, 'b_void')
    return it


def mage_baton_prison_givre():
    it = Item('mage_baton_prison_givre', tilt=SWORD)
    staff(it, -3.6, 13.4, 'wood_dark', grip='b_ice_dark', foot='b_blue_steel')
    it.col(13.0, 14.0, 3.6, 3.6, 'b_blue_steel')
    for (x, z) in ((6.6, 6.6), (9.4, 6.6), (6.6, 9.4), (9.4, 9.4)):
        it.box((x - 0.4, 14.0, z - 0.4), (x + 0.4, 19.0, z + 0.4), 'ice')
    it.col(19.0, 19.8, 3.6, 3.6, 'b_blue_steel')
    it.col(19.8, 21.0, 1.2, 1.2, 'ice')
    it.col(15.0, 18.0, 2.0, 2.0, 'b_frost')
    # pointes de givre au collier
    for (x0, x1) in ((4.6, 6.2), (9.8, 11.4)):
        it.box((x0, 13.2, 7.7), (x1, 13.8, 8.3), 'ice')
    it.col(10.0, 10.8, 1.7, 1.7, 'b_blue_steel')
    return it


def mage_sceptre_mur_flammes():
    it = Item('mage_sceptre_mur_flammes', tilt=SWORD)
    it.col(-2.8, -1.6, 1.8, 1.8, 'ruby')
    it.col(-1.6, 12.2, 1.1, 1.1, 'gold')
    it.col(0.0, 4.2, 1.4, 1.4, 'cloth_red')
    it.col(6.4, 7.0, 1.4, 1.4, 'gold_dark')
    # couronne d'or et éventail de trois flammes
    it.col(12.0, 13.2, 4.6, 2.0, 'gold')
    for (cx, hgt, w) in ((5.9, 4.0, 1.2), (8.0, 5.6, 1.6), (10.1, 4.0, 1.2)):
        it.col(13.2, 13.2 + hgt * 0.5, w, 1.0, 'ember', cx=cx)
        it.col(13.2 + hgt * 0.5, 13.2 + hgt * 0.8, w * 0.7, 0.8, 'flame', cx=cx + (0.2 if cx < 8 else -0.2 if cx > 8 else 0))
        it.col(13.2 + hgt * 0.8, 13.2 + hgt, w * 0.35, 0.6, 'flame', cx=cx)
    it.box((7.4, 12.2, 8.95), (8.6, 13.0, 9.2), 'ruby')
    return it


def mage_sceptre_singularite():
    it = Item('mage_sceptre_singularite', tilt=SWORD)
    it.col(-2.8, -1.6, 1.8, 1.8, 'b_void')
    it.col(-1.6, 12.4, 1.0, 1.0, 'b_black_steel')
    it.col(0.0, 4.0, 1.3, 1.3, 'b_cloth_purple')
    it.col(12.2, 13.4, 1.8, 1.8, 'b_black_steel')
    it.col(13.4, 17.4, 3.2, 3.2, 'b_void')
    it.col(14.4, 16.4, 3.5, 3.5, 'void_glow')
    # anneau horizontal (plan xz) qui ceint l'orbe
    it.box((4.6, 15.1, 4.6), (11.4, 15.7, 5.4), 'b_black_steel')
    it.box((4.6, 15.1, 10.6), (11.4, 15.7, 11.4), 'b_black_steel')
    it.box((4.6, 15.1, 5.4), (5.4, 15.7, 10.6), 'b_black_steel')
    it.box((10.6, 15.1, 5.4), (11.4, 15.7, 10.6), 'b_black_steel')
    for (a, b) in (((5.4, 15.2, 7.6), (6.4, 15.6, 8.4)), ((9.6, 15.2, 7.6), (10.6, 15.6, 8.4))):
        it.box(a, b, 'b_black_steel')
    it.col(17.4, 18.2, 1.0, 1.0, 'void_glow')
    return it


def mage_baton_miroirs():
    it = Item('mage_baton_miroirs', tilt=SWORD)
    staff(it, -3.4, 14.6, 'silver', w=1.1, grip='b_cloth_white', foot='silver')
    it.col(13.6, 14.4, 6.4, 0.9, 'silver')
    # deux éclats de miroir en losange, portés par la traverse
    for cx in (5.4, 10.6):
        it.col(14.4, 15.4, 1.2, 0.5, 'b_mirror', cx=cx)
        it.col(15.4, 17.4, 1.8, 0.5, 'b_mirror', cx=cx)
        it.col(17.4, 18.8, 1.2, 0.5, 'b_mirror', cx=cx)
        it.col(18.8, 19.6, 0.5, 0.5, 'b_mirror', cx=cx)
        it.col(14.0, 14.6, 1.4, 0.8, 'silver', cx=cx)
    it.col(14.4, 17.0, 1.4, 1.4, 'silver')
    it.col(17.0, 18.6, 1.6, 1.6, 'b_pearl')
    return it


def mage_sceptre_tempete_solaire():
    it = Item('mage_sceptre_tempete_solaire', tilt=SWORD)
    it.col(-3.0, -1.6, 2.0, 2.0, 'gold')
    it.col(-1.6, 11.8, 1.1, 1.1, 'gold')
    it.col(0.0, 4.2, 1.4, 1.4, 'cloth_red')
    it.col(5.6, 6.2, 1.5, 1.5, 'ruby')
    it.col(11.6, 12.6, 2.0, 2.0, 'gold_dark')
    # disque solaire et rayons, dans le plan de l'arme
    c = 15.2
    it.col(c - 2.4, c + 2.4, 3.2, 1.2, 'b_sun')
    it.col(c - 1.6, c + 1.6, 4.8, 1.2, 'b_sun')
    it.col(c - 0.8, c + 0.8, 1.6, 1.6, 'ruby')
    for (x0, y0, x1, y1) in ((7.5, c + 2.4, 8.5, c + 4.6), (7.5, c - 3.0, 8.5, c - 2.4), (3.0, c - 0.5, 5.6, c + 0.5),
                             (10.4, c - 0.5, 13.0, c + 0.5), (4.6, c + 1.6, 5.8, c + 2.8), (10.2, c + 1.6, 11.4, c + 2.8),
                             (4.6, c - 2.8, 5.8, c - 1.6), (10.2, c - 2.8, 11.4, c - 1.6)):
        it.box((x0, y0, 7.7), (x1, y1, 8.3), 'gold')
    return it


def mage_baton_arret_temps():
    it = Item('mage_baton_arret_temps', tilt=SWORD)
    staff(it, -3.8, 13.0, 'wood_dark', grip='b_cloth_purple', foot='gold')
    it.col(9.0, 9.6, 1.6, 1.6, 'gold')
    # sablier : socle, deux bulbes de verre, piliers d'or, chapeau
    it.col(12.6, 13.4, 4.2, 3.0, 'gold')
    it.col(13.4, 15.0, 2.8, 2.0, 'glass')
    it.col(13.4, 14.4, 2.4, 1.6, 'b_sand')
    it.col(15.0, 15.8, 0.9, 0.9, 'b_sand')
    it.col(15.8, 17.4, 2.8, 2.0, 'glass')
    it.col(16.8, 17.4, 1.4, 1.0, 'b_sand')
    it.col(17.4, 18.2, 4.2, 3.0, 'gold')
    for x in (6.1, 9.9):
        it.box((x - 0.3, 13.4, 7.7), (x + 0.3, 17.4, 8.3), 'gold')
    it.col(18.2, 19.6, 1.0, 1.0, 'gold')
    it.col(19.6, 20.6, 1.6, 1.6, 'sapphire')
    return it


# =====================================================================================
#  Druide
# =====================================================================================

def druide_baton_lierre_etrangleur():
    it = Item('druide_baton_lierre_etrangleur', tilt=SWORD)
    staff(it, -3.6, 15.0, 'wood_pale', grip='leather', foot='wood_dark')
    # lierre en spirale autour du bâton
    for i in range(12):
        y = -1.0 + i * 1.35
        side = i % 4
        x0, z0 = [(8.6, 7.5), (7.5, 8.6), (6.9, 7.5), (7.5, 6.9)][side]
        it.box((x0 - 0.1, y, z0 - 0.1), (x0 + 0.6, y + 0.9, z0 + 0.6), 'leaf_dark')
    # crosse recourbée et feuilles
    it.box((7.4, 15.0, 7.4), (9.8, 16.2, 8.6), 'wood_pale')
    it.box((9.0, 16.2, 7.4), (10.2, 18.2, 8.6), 'wood_pale')
    it.box((7.8, 18.0, 7.4), (10.0, 19.0, 8.6), 'wood_pale')
    it.box((7.2, 17.0, 7.5), (8.2, 18.4, 8.5), 'wood_pale')
    for (a, b, m) in (((5.6, 15.4, 7.8), (7.4, 16.4, 8.2), 'leaf'), ((10.2, 17.0, 7.8), (12.0, 18.0, 8.2), 'leaf'),
                      ((8.4, 19.0, 7.8), (9.8, 20.2, 8.2), 'leaf_dark'), ((6.6, 18.4, 7.8), (7.4, 19.6, 8.2), 'leaf')):
        it.box(a, b, m)
    return it


def druide_faucille_graine_explosive():
    it = Item('druide_faucille_graine_explosive', tilt=SWORD)
    it.col(-3.2, -2.4, 1.7, 1.7, 'wood_dark')
    it.col(-2.4, 5.0, 1.4, 1.4, 'wood')
    it.col(-1.8, 2.2, 1.6, 1.6, 'cloth_green')
    it.col(5.0, 6.4, 2.0, 2.0, 'bronze')
    for (x0, y0, x1, y1) in ((8.0, 6.4, 9.8, 9.6), (8.8, 9.6, 10.8, 12.8), (8.4, 12.8, 10.6, 15.2),
                             (6.4, 15.0, 9.6, 16.6), (4.0, 15.4, 6.6, 16.8), (2.8, 14.6, 4.2, 16.0)):
        it.box((x0, y0, 7.6), (x1, y1, 8.4), 'bronze')
    it.box((7.4, 7.0, 7.7), (8.0, 14.0, 8.3), 'edge')
    # cosse : grosse graine verte à la jonction
    it.col(4.6, 7.0, 2.2, 2.2, 'cloth_green', cx=6.6)
    it.col(5.0, 6.6, 2.5, 1.2, 'b_poison', cx=6.6)
    it.box((6.2, 7.0, 7.8), (7.0, 7.6, 8.2), 'ember')
    return it


def druide_baton_souffle_vent():
    it = Item('druide_baton_souffle_vent', tilt=SWORD)
    staff(it, -3.6, 14.0, 'b_birch', grip='b_cloth_jade', foot='silver')
    # tourbillon en S
    for (x0, y0, x1, y1) in ((7.4, 14.0, 10.6, 15.0), (9.8, 15.0, 11.0, 17.0), (6.8, 17.0, 11.0, 18.0),
                             (5.4, 18.0, 7.2, 20.0), (5.4, 20.0, 9.4, 21.0), (8.6, 19.0, 9.4, 20.0)):
        it.box((x0, y0, 7.6), (x1, y1, 8.4), 'b_jade')
    it.col(15.0, 16.8, 1.2, 1.2, 'b_pearl', cx=8.2)
    # plumes nouées sous la tête
    it.box((5.4, 11.6, 7.85), (6.6, 14.2, 8.15), 'feather')
    it.box((6.6, 13.2, 7.8), (7.4, 14.0, 8.2), 'b_rope')
    it.box((9.4, 11.0, 7.85), (10.4, 13.4, 8.15), 'feather')
    it.box((8.6, 12.6, 7.8), (9.4, 13.4, 8.2), 'b_rope')
    return it


def druide_faucille_esprit_cerf():
    it = Item('druide_faucille_esprit_cerf', tilt=SWORD)
    it.col(-3.2, -2.4, 1.7, 1.7, 'b_antler')
    it.col(-2.4, 5.0, 1.4, 1.4, 'b_antler')
    it.col(-1.8, 2.2, 1.6, 1.6, 'leather')
    it.col(5.0, 6.2, 1.9, 1.9, 'silver')
    # ramure : merrain qui monte en arc, andouillers
    for (x0, y0, x1, y1) in ((8.0, 6.2, 9.4, 10.0), (8.6, 10.0, 10.0, 14.0), (7.6, 14.0, 9.6, 15.4),
                             (5.2, 15.0, 7.8, 16.2), (3.4, 14.2, 5.4, 15.4)):
        it.box((x0, y0, 7.6), (x1, y1, 8.4), 'b_antler')
    for (x0, y0, x1, y1) in ((10.0, 11.0, 11.8, 11.8), (11.2, 11.8, 11.9, 13.2), (9.6, 14.6, 10.4, 16.8),
                             (6.0, 16.2, 6.8, 17.8), (3.4, 15.4, 4.2, 16.6)):
        it.box((x0, y0, 7.7), (x1, y1, 8.3), 'b_antler')
    it.box((7.4, 6.8, 7.7), (8.0, 13.6, 8.3), 'moon')
    it.box((7.4, 5.2, 8.95), (8.6, 6.0, 9.15), 'b_pearl')
    return it


def druide_baton_essaim_spores():
    it = Item('druide_baton_essaim_spores', tilt=SWORD)
    staff(it, -3.6, 14.6, 'b_bark', grip='leather', foot='b_bark')
    it.col(4.0, 5.2, 1.7, 1.7, 'moss')
    # bouquet de champignons
    it.col(14.6, 17.4, 0.9, 0.9, 'bone')
    it.col(17.4, 18.6, 4.2, 4.2, 'b_cap')
    it.col(18.6, 19.4, 2.8, 2.8, 'b_cap')
    it.col(13.0, 15.0, 0.7, 0.7, 'bone', cx=6.4)
    it.box((6.0, 13.0, 7.65), (7.6, 13.6, 8.35), 'bone')
    it.col(15.0, 15.8, 2.4, 2.4, 'b_cap', cx=6.0)
    it.col(12.0, 13.6, 0.7, 0.7, 'bone', cx=9.8)
    it.box((8.4, 12.0, 7.65), (9.8, 12.6, 8.35), 'bone')
    it.col(13.6, 14.4, 2.0, 2.0, 'b_cap', cx=10.0)
    for (x, y, z) in ((8.0, 19.4, 8.0), (6.4, 18.6, 9.4), (10.2, 18.6, 6.8), (6.0, 15.8, 8.0), (10.0, 14.4, 8.0)):
        it.box((x - 0.3, y, z - 0.3), (x + 0.3, y + 0.5, z + 0.3), 'b_spore')
    return it


def druide_faucille_nuee_abeilles():
    it = Item('druide_faucille_nuee_abeilles', tilt=SWORD)
    it.col(-3.2, -2.4, 1.7, 1.7, 'b_honey')
    it.col(-2.4, 5.0, 1.4, 1.4, 'b_black')
    for y in (-1.6, 0.0, 1.6, 3.2):
        it.col(y, y + 0.8, 1.6, 1.6, 'b_honey')
    it.col(5.0, 6.4, 2.2, 2.2, 'b_comb')
    for (x0, y0, x1, y1) in ((8.0, 6.4, 10.0, 9.6), (8.6, 9.6, 11.0, 12.6), (8.2, 12.6, 10.6, 15.0),
                             (6.0, 14.8, 9.4, 16.4), (3.6, 15.2, 6.2, 16.6), (2.2, 14.4, 3.8, 15.8)):
        it.box((x0, y0, 7.6), (x1, y1, 8.4), 'b_comb')
    it.box((7.4, 7.0, 7.7), (8.0, 14.0, 8.3), 'b_honey')
    it.box((4.0, 14.8, 7.7), (7.6, 15.2, 8.3), 'b_honey')
    it.box((10.0, 10.4, 7.85), (11.6, 11.4, 8.15), 'b_honey')
    return it


def druide_baton_bosquet_sacre():
    it = Item('druide_baton_bosquet_sacre', tilt=SWORD)
    staff(it, -3.6, 14.0, 'wood', grip='cloth_green', foot='wood_dark')
    # trois branches qui s'ouvrent et bercent une gemme de jade
    for (x0, y0, x1, y1) in ((7.4, 14.0, 8.6, 18.8), (5.6, 14.0, 7.4, 15.0), (4.8, 15.0, 5.8, 18.6),
                             (8.6, 14.0, 10.4, 15.0), (10.2, 15.0, 11.2, 18.6)):
        it.box((x0, y0, 7.4), (x1, y1, 8.6), 'wood')
    it.col(15.2, 17.2, 1.8, 1.8, 'b_jade', cx=8.0)
    for (x, y, m) in ((5.3, 18.6, 'leaf'), (10.7, 18.6, 'leaf'), (8.0, 18.8, 'leaf_dark')):
        it.box((x - 1.3, y, 7.0), (x + 1.3, y + 1.4, 9.0), m)
        it.box((x - 0.8, y + 1.4, 7.3), (x + 0.8, y + 2.2, 8.7), 'leaf')
    return it


def druide_faucille_morsure_ours():
    it = Item('druide_faucille_morsure_ours', tilt=SWORD)
    it.col(-3.2, -2.4, 1.8, 1.8, 'bone')
    it.col(-2.4, 5.0, 1.4, 1.4, 'wood_dark')
    it.col(-1.8, 2.6, 2.0, 2.0, 'b_fur')
    it.col(5.0, 7.0, 3.6, 2.0, 'b_fur')
    # patte : trois griffes recourbées
    for k, cx in enumerate((5.8, 8.0, 10.2)):
        lift = 1.2 if k == 1 else 0
        it.box((cx - 0.6, 7.0, 7.5), (cx + 0.6, 10.2 + lift, 8.5), 'bone')
        it.box((cx - 1.2, 10.2 + lift, 7.6), (cx + 0.2, 12.4 + lift, 8.4), 'bone')
        it.box((cx - 1.8, 12.4 + lift, 7.7), (cx - 0.6, 13.6 + lift, 8.3), 'b_horn')
    it.box((7.4, 6.0, 8.95), (8.6, 6.8, 9.2), 'amethyst')
    return it


def druide_baton_avatar_foret():
    it = Item('druide_baton_avatar_foret', tilt=SWORD)
    staff(it, -2.6, 13.4, 'b_bark', w=1.7, grip='leather_dark')
    # racines au pied
    for (x0, x1) in ((6.2, 7.2), (8.8, 9.8)):
        it.box((x0, -4.2, 7.4), (x1, -2.6, 8.6), 'b_bark')
    it.col(-4.0, -2.6, 1.0, 1.0, 'b_bark')
    # couronne d'arbre, cœur d'émeraude, feuilles d'or
    it.col(13.4, 15.0, 2.4, 2.4, 'b_bark')
    it.box((4.4, 15.0, 6.2), (11.6, 18.6, 9.8), 'leaf_dark')
    it.box((5.4, 18.6, 6.6), (10.6, 20.4, 9.4), 'leaf')
    it.box((6.6, 20.4, 7.2), (9.4, 21.4, 8.8), 'b_leaf_gold')
    it.col(15.8, 18.0, 1.8, 3.8, 'emerald')
    for (x, y) in ((4.2, 16.2), (11.8, 17.0), (5.0, 18.4), (11.0, 19.0)):
        it.box((x - 0.4, y, 7.4), (x + 0.4, y + 0.9, 8.6), 'b_leaf_gold')
    return it


def druide_faucille_colere_ciel():
    it = Item('druide_faucille_colere_ciel', tilt=SWORD)
    it.col(-3.4, -2.4, 2.0, 2.0, 'sapphire')
    it.col(-2.4, 5.0, 1.4, 1.4, 'b_storm')
    it.col(-1.8, 2.4, 1.6, 1.6, 'b_cloth_grey')
    it.col(5.0, 6.6, 2.2, 2.2, 'silver')
    # lame en éclair : zigzag qui monte puis se recourbe
    for (x0, y0, x1, y1) in ((8.0, 6.6, 10.0, 9.0), (9.2, 9.0, 11.4, 10.6), (7.8, 10.6, 10.4, 12.2),
                             (8.8, 12.2, 11.2, 13.8), (6.6, 13.8, 10.0, 15.4), (3.8, 15.0, 6.8, 16.6),
                             (2.4, 14.0, 4.0, 15.4)):
        it.box((x0, y0, 7.6), (x1, y1, 8.4), 'b_blue_steel')
    for (x0, y0, x1, y1) in ((8.6, 7.0, 9.2, 9.4), (9.6, 9.4, 10.2, 10.6), (8.4, 10.6, 9.0, 12.4),
                             (9.4, 12.4, 10.0, 13.8), (5.0, 14.4, 9.4, 14.9)):
        inlay(it, x0, y0, x1, y1, 'b_lightning', 0.8)
    return it


# =====================================================================================
#  Guerrier
# =====================================================================================

def guerrier_epee_longue_coup_bouclier():
    it = Item('guerrier_epee_longue_coup_bouclier', tilt=SWORD)
    hilt(it, 'leather', 'iron')
    # garde en rondache : petit bouclier rond et son umbo
    it.col(3.4, 6.0, 3.6, 0.8, 'iron')
    it.col(3.0, 6.4, 2.4, 0.8, 'iron')
    it.col(3.9, 5.5, 4.4, 0.8, 'iron')
    it.col(4.1, 5.3, 1.6, 1.4, 'bronze')
    blade(it, 6.4, [2.8, 2.8, 2.7, 2.6, 2.4, 2.0, 1.2], 1.4, 'steel', 'edge', d=1.0, fuller='steel_dark')
    return it


def guerrier_epee_longue_taillade():
    it = Item('guerrier_epee_longue_taillade', tilt=SWORD)
    hilt(it, 'leather_dark', 'steel', pw=1.6)
    # garde à branche : arc de protection de la main
    bar(it, 3.4, 4.4, 0.8, 1.0, 'steel')
    it.box((9.6, -1.4, 7.6), (10.4, 3.4, 8.4), 'steel')
    it.box((8.0, -2.2, 7.6), (10.4, -1.4, 8.4), 'steel')
    it.box((5.4, 3.0, 7.6), (6.2, 4.2, 8.4), 'steel')
    # sabre fin et courbe
    n = 10
    offs = [-0.06 * i * i * 0.5 for i in range(n)]
    blade(it, 4.2, taper(n, 1.7, 0.5), 1.4, 'steel', 'edge', d=0.8, offs=offs)
    return it


def guerrier_hache_bond_lion():
    it = Item('guerrier_hache_bond_lion', tilt=SWORD)
    it.col(-3.4, -2.6, 1.9, 1.9, 'gold_dark')
    it.col(-2.6, 17.4, 1.4, 1.4, 'wood')
    it.col(-2.0, 3.0, 1.65, 1.65, 'leather')
    it.col(12.0, 17.6, 2.2, 2.0, 'steel_dark')
    # lame en croissant
    it.box((9.1, 12.8, 7.4), (11.6, 16.8, 8.6), 'steel')
    it.box((11.6, 11.4, 7.5), (13.4, 18.2, 8.5), 'steel')
    it.box((13.2, 10.4, 7.6), (14.4, 19.2, 8.4), 'edge')
    it.box((12.6, 9.6, 7.65), (13.6, 10.6, 8.35), 'edge')
    it.box((12.6, 19.0, 7.65), (13.6, 20.0, 8.35), 'edge')
    # tête de lion dorée au dos
    it.box((4.0, 13.0, 7.0), (6.9, 17.0, 9.0), 'gold')
    it.box((3.4, 13.6, 7.2), (4.0, 16.4, 8.8), 'gold_dark')
    it.box((4.4, 14.4, 6.8), (5.4, 15.2, 7.0), 'ruby')
    it.box((4.4, 14.4, 9.0), (5.4, 15.2, 9.2), 'ruby')
    it.box((4.2, 17.0, 7.4), (6.0, 17.8, 8.6), 'gold_dark')
    it.box((4.2, 12.2, 7.4), (6.0, 13.0, 8.6), 'gold_dark')
    it.col(17.6, 19.0, 0.9, 0.9, 'gold')
    return it


def guerrier_hache_provocation():
    it = Item('guerrier_hache_provocation', tilt=SWORD)
    it.col(-3.4, -2.6, 1.9, 1.9, 'iron')
    it.col(-2.6, 18.0, 1.4, 1.4, 'wood_dark')
    it.col(-2.0, 3.0, 1.65, 1.65, 'cloth_red')
    it.col(12.6, 17.8, 2.2, 2.0, 'iron')
    # hache barbue : la lame descend en pointe le long du manche
    it.box((9.1, 13.4, 7.4), (12.0, 17.6, 8.6), 'b_red_enamel')
    it.box((12.0, 10.4, 7.5), (13.8, 17.6, 8.5), 'steel')
    it.box((13.6, 9.0, 7.6), (14.6, 17.8, 8.4), 'edge')
    it.box((10.6, 10.4, 7.6), (12.0, 13.4, 8.4), 'steel')
    it.box((9.4, 11.4, 7.65), (10.6, 13.4, 8.35), 'steel')
    # fanion rouge noué sous la tête
    it.box((6.0, 11.0, 7.85), (7.3, 16.6, 8.15), 'cloth_red')
    it.box((5.0, 11.8, 7.85), (6.0, 16.6, 8.15), 'cloth_red')
    it.box((5.0, 16.6, 7.8), (7.4, 17.2, 8.2), 'b_rope')
    it.col(18.0, 19.2, 1.0, 1.0, 'steel')
    return it


def guerrier_epee_longue_tourbillon_lames():
    it = Item('guerrier_epee_longue_tourbillon_lames', tilt=SWORD)
    hilt(it, 'cloth_blue', 'b_blue_steel', pmat2='sapphire')
    # garde à ailettes tournées
    bar(it, 3.4, 5.0, 1.0, 1.2, 'b_blue_steel')
    it.box((4.4, 4.0, 7.6), (5.8, 5.8, 8.4), 'b_blue_steel')
    it.box((10.2, 2.0, 7.6), (11.6, 3.8, 8.4), 'b_blue_steel')
    it.col(3.6, 4.2, 1.4, 1.6, 'sapphire')
    y = blade(it, 4.4, [2.4] * 8 + [1.8, 1.0], 1.3, 'b_blue_steel', 'edge', fuller='sapphire', fw=0.4)
    # crochets alternés en spirale le long de la lame
    for k, yy in enumerate((6.0, 8.6, 11.2)):
        if k % 2 == 0:
            it.box((8.6, yy, 7.65), (10.6, yy + 1.1, 8.35), 'edge')
            it.box((9.8, yy + 0.8, 7.65), (11.0, yy + 2.0, 8.35), 'edge')
        else:
            it.box((5.4, yy, 7.65), (7.4, yy + 1.1, 8.35), 'edge')
            it.box((5.0, yy + 0.8, 7.65), (6.2, yy + 2.0, 8.35), 'edge')
    return it


def guerrier_epee_longue_lame_choc():
    it = Item('guerrier_epee_longue_lame_choc', tilt=SWORD)
    hilt(it, 'leather_dark', 'b_rock', w=1.6, pw=2.6)
    bar(it, 3.4, 6.6, 1.8, 1.8, 'b_rock')
    it.col(3.8, 4.8, 1.2, 1.9, 'b_crack')
    # lame massive fendue de fissures ardentes
    blade(it, 5.2, [3.6] * 7 + [3.0, 1.8], 1.3, 'steel_dark', 'iron', d=1.3)
    for (x0, y0, x1, y1) in ((7.6, 6.0, 8.1, 8.4), (8.0, 8.2, 8.6, 9.8), (7.2, 9.6, 7.8, 11.6),
                             (7.7, 11.4, 8.3, 13.2), (6.6, 7.6, 7.6, 8.0), (8.4, 10.8, 9.4, 11.2)):
        inlay(it, x0, y0, x1, y1, 'b_crack', 1.3)
    return it


def guerrier_hache_chaine_guerre():
    it = Item('guerrier_hache_chaine_guerre', tilt=SWORD)
    it.col(-3.4, -2.6, 1.9, 1.9, 'iron')
    it.col(-2.6, 17.4, 1.4, 1.4, 'b_black_steel')
    it.col(-2.0, 3.0, 1.65, 1.65, 'leather_dark')
    it.col(12.4, 17.6, 2.2, 2.0, 'b_black_steel')
    it.box((9.1, 13.0, 7.4), (12.0, 16.8, 8.6), 'steel_dark')
    it.box((12.0, 12.0, 7.5), (14.0, 17.8, 8.5), 'steel')
    it.box((14.0, 11.0, 7.6), (15.2, 18.8, 8.4), 'edge')
    # chaîne enroulée autour du manche, crochet au bout
    for i in range(7):
        y = 4.0 + i * 1.2
        if i % 2:
            it.box((7.0, y, 6.9), (9.0, y + 0.7, 9.1), 'b_chain')
        else:
            it.box((6.9, y, 7.0), (9.1, y + 0.7, 9.0), 'b_chain')
    it.box((5.6, 12.4, 7.6), (7.4, 14.6, 8.4), 'b_black_steel')
    it.box((4.6, 12.4, 7.65), (5.6, 13.2, 8.35), 'b_black_steel')
    it.box((4.6, 13.2, 7.7), (5.2, 14.2, 8.3), 'edge')
    it.col(17.6, 19.0, 0.8, 0.8, 'b_chain')
    return it


def guerrier_hache_peau_fer():
    it = Item('guerrier_hache_peau_fer', tilt=SWORD)
    it.col(-3.4, -2.6, 2.0, 2.0, 'iron')
    it.col(-2.6, 17.4, 1.5, 1.5, 'iron')
    it.col(-2.0, 3.0, 1.75, 1.75, 'leather')
    it.col(12.0, 18.0, 2.4, 2.4, 'iron')
    # bipenne en plaques rivetées
    for s in (1, -1):
        x = lambda v: 8 + s * v
        it.box((min(x(1.2), x(3.8)), 12.6, 7.4), (max(x(1.2), x(3.8)), 17.4, 8.6), 'steel_dark')
        it.box((min(x(3.8), x(5.6)), 11.2, 7.5), (max(x(3.8), x(5.6)), 18.8, 8.5), 'steel')
        it.box((min(x(5.6), x(6.6)), 10.4, 7.6), (max(x(5.6), x(6.6)), 19.6, 8.4), 'edge')
        for yy in (13.4, 16.0):
            it.box((min(x(2.2), x(2.9)), yy, 8.6), (max(x(2.2), x(2.9)), yy + 0.7, 8.8), 'bronze')
            it.box((min(x(2.2), x(2.9)), yy, 7.2), (max(x(2.2), x(2.9)), yy + 0.7, 7.4), 'bronze')
    it.col(18.0, 19.4, 1.2, 1.2, 'steel')
    return it


def guerrier_hache_colere_titan():
    it = Item('guerrier_hache_colere_titan', tilt=SWORD)
    it.col(-3.8, -2.6, 2.4, 2.4, 'gold')
    it.col(-2.6, 17.0, 1.6, 1.6, 'b_rock')
    it.col(-2.0, 3.4, 1.9, 1.9, 'leather_dark')
    for y in (6.0, 9.0):
        it.col(y, y + 0.8, 1.9, 1.9, 'gold')
    # tête de roche cerclée d'or, fendue de lave
    it.box((8.8, 11.0, 6.8), (13.6, 18.6, 9.2), 'b_rock')
    it.box((13.6, 10.0, 7.2), (15.6, 19.6, 8.8), 'b_rock')
    it.box((15.4, 10.6, 7.5), (16.2, 19.0, 8.5), 'edge')
    it.box((3.6, 12.6, 7.0), (8.8, 17.0, 9.0), 'b_rock')
    it.box((8.6, 11.6, 6.6), (9.6, 18.0, 9.4), 'gold')
    it.box((12.8, 11.0, 6.7), (13.6, 18.6, 9.3), 'gold')
    for (x0, y0, x1, y1) in ((10.2, 12.4, 10.8, 15.8), (10.8, 15.6, 12.2, 16.2), (11.4, 13.0, 12.0, 15.0),
                             (4.6, 14.4, 7.6, 15.0)):
        inlay(it, x0, y0, x1, y1, 'b_crack', 2.6)
    it.col(17.0, 19.0, 2.0, 2.0, 'b_rock')
    it.col(19.0, 19.8, 1.0, 1.0, 'gold')
    return it


def guerrier_epee_longue_dernier_rempart():
    it = Item('guerrier_epee_longue_dernier_rempart', tilt=SWORD)
    hilt(it, 'cloth_red', 'gold', w=1.5, pw=2.6, pmat2='ruby')
    # garde en tour crénelée
    bar(it, 3.4, 7.4, 1.6, 1.8, 'gold')
    for x in (4.3, 5.9, 10.1, 11.7):
        it.box((x - 0.5, 5.0, 7.4), (x + 0.5, 5.8, 8.6), 'gold')
    it.col(3.6, 5.4, 1.8, 2.0, 'ruby')
    blade(it, 5.0, [3.2] * 9 + [2.6, 1.6, 0.7], 1.3, 'b_white', 'edge', d=1.1, fuller='b_gold_rune', fw=0.6)
    return it


# =====================================================================================
#  Paladin
# =====================================================================================

def paladin_epee_bouclier_renvoye():
    it = Item('paladin_epee_bouclier_renvoye', tilt=SWORD)
    hilt(it, 'cloth_blue', 'gold')
    # garde en écu : bouclier en amande, émail bleu, croix d'or
    it.col(3.4, 4.4, 2.0, 1.0, 'gold')
    it.col(4.4, 7.4, 4.6, 1.0, 'gold')
    it.col(4.8, 7.0, 3.8, 1.2, 'b_blue_enamel')
    it.col(7.4, 8.2, 3.4, 1.0, 'gold')
    it.box((7.7, 5.0, 8.55), (8.3, 7.0, 8.7), 'gold')
    it.box((7.0, 5.8, 8.55), (9.0, 6.4, 8.7), 'gold')
    blade(it, 8.2, [2.2] * 6 + [1.6, 0.8], 1.3, 'silver', 'edge', d=0.9)
    return it


def paladin_marteau_lumiere_purifiante():
    it = Item('paladin_marteau_lumiere_purifiante', tilt=SWORD)
    it.col(-3.4, -2.4, 2.0, 2.0, 'silver')
    it.col(-2.4, 14.0, 1.4, 1.4, 'b_birch')
    it.col(-1.8, 3.2, 1.7, 1.7, 'b_cloth_white')
    # tête à ailettes (masse d'armes) et orbe sacré
    it.col(14.0, 19.0, 3.4, 3.4, 'silver')
    for (a, b) in (((4.2, 14.4, 7.6), (6.3, 18.6, 8.4)), ((9.7, 14.4, 7.6), (11.8, 18.6, 8.4)),
                   ((7.6, 14.4, 4.2), (8.4, 18.6, 6.3)), ((7.6, 14.4, 9.7), (8.4, 18.6, 11.8))):
        it.box(a, b, 'silver')
    it.col(15.6, 17.4, 3.6, 3.6, 'holy')
    it.col(19.0, 19.8, 1.4, 1.4, 'silver')
    return it


def paladin_epee_frappe_sacree():
    it = Item('paladin_epee_frappe_sacree', tilt=SWORD)
    hilt(it, 'b_cloth_white', 'silver')
    bar(it, 3.4, 7.2, 1.0, 1.2, 'silver')
    it.box((7.4, 3.0, 7.4), (8.6, 4.6, 8.6), 'silver')
    blade(it, 4.4, [2.4] * 9 + [1.8, 1.0], 1.2, 'silver', 'edge', fuller='holy', fw=0.6)
    return it


def paladin_marteau_benediction():
    it = Item('paladin_marteau_benediction', tilt=SWORD)
    it.col(-3.4, -2.4, 2.0, 2.0, 'gold')
    it.col(-2.4, 13.6, 1.4, 1.4, 'wood_pale')
    it.col(-1.8, 3.2, 1.7, 1.7, 'cloth_blue')
    # tête en cloche
    it.col(13.6, 14.6, 1.8, 1.8, 'gold')
    it.col(14.6, 15.4, 2.4, 2.4, 'gold')
    it.col(15.4, 17.8, 3.4, 3.4, 'gold')
    it.col(17.8, 18.8, 4.6, 4.6, 'gold')
    it.col(18.8, 19.4, 5.0, 5.0, 'gold_dark')
    it.box((7.3, 15.8, 9.65), (8.7, 17.2, 9.85), 'holy')
    it.box((7.3, 15.8, 6.15), (8.7, 17.2, 6.35), 'holy')
    return it


def paladin_marteau_marteau_celeste():
    it = Item('paladin_marteau_marteau_celeste', tilt=SWORD)
    it.col(-3.4, -2.4, 2.0, 2.0, 'gold')
    it.col(-2.4, 14.0, 1.4, 1.4, 'b_white')
    it.col(-1.8, 3.2, 1.7, 1.7, 'cloth_blue')
    it.box((4.6, 14.0, 6.2), (11.4, 18.6, 9.8), 'b_white')
    it.box((4.2, 13.7, 5.9), (5.0, 18.9, 10.1), 'gold')
    it.box((11.0, 13.7, 5.9), (11.8, 18.9, 10.1), 'gold')
    it.box((6.8, 15.0, 9.8), (9.2, 17.6, 10.2), 'holy')
    it.box((6.8, 15.0, 5.8), (9.2, 17.6, 6.2), 'holy')
    # ailes de chaque côté de la tête
    for s in (1, -1):
        x = lambda v: 8 + s * v
        it.box((min(x(3.4), x(5.6)), 14.6, 7.65), (max(x(3.4), x(5.6)), 18.6, 8.35), 'feather')
        it.box((min(x(5.0), x(6.8)), 16.0, 7.7), (max(x(5.0), x(6.8)), 19.8, 8.3), 'feather')
        it.box((min(x(6.2), x(7.6)), 17.6, 7.75), (max(x(6.2), x(7.6)), 20.6, 8.25), 'feather')
    it.col(18.6, 19.6, 1.6, 1.6, 'gold')
    return it


def paladin_marteau_sanctuaire():
    it = Item('paladin_marteau_sanctuaire', tilt=SWORD)
    it.col(-3.4, -2.4, 2.0, 2.0, 'gold')
    it.col(-2.4, 13.6, 1.4, 1.4, 'wood_pale')
    it.col(-1.8, 3.2, 1.7, 1.7, 'cloth_blue')
    # petit temple : socle, colonnes d'or, cœur sacré, toit à deux pans
    it.box((4.0, 13.6, 6.0), (12.0, 14.6, 10.0), 'stone')
    for x in (4.8, 7.0, 9.0, 11.2):
        it.box((x - 0.4, 14.6, 6.4), (x + 0.4, 17.4, 7.2), 'gold')
        it.box((x - 0.4, 14.6, 8.8), (x + 0.4, 17.4, 9.6), 'gold')
    it.box((5.2, 14.6, 7.2), (10.8, 17.4, 8.8), 'holy')
    it.box((3.6, 17.4, 5.8), (12.4, 18.2, 10.2), 'stone')
    it.box((5.0, 18.2, 6.2), (11.0, 19.0, 9.8), 'stone')
    it.box((6.6, 19.0, 6.6), (9.4, 19.8, 9.4), 'gold')
    return it


def paladin_epee_charge_croise():
    it = Item('paladin_epee_charge_croise', tilt=SWORD)
    hilt(it, 'cloth_red', 'silver', pw=2.4)
    bar(it, 3.4, 9.6, 1.2, 1.4, 'silver')
    it.box((2.8, 3.0, 7.4), (4.0, 5.0, 8.6), 'silver')
    it.box((12.0, 3.0, 7.4), (13.2, 5.0, 8.6), 'silver')
    blade(it, 4.6, [3.0] * 8 + [2.2, 1.2], 1.3, 'silver', 'edge', d=1.1)
    # croix rouge sur le plat
    inlay(it, 7.5, 6.0, 8.5, 12.0, 'b_red_enamel', 1.1)
    inlay(it, 6.4, 9.6, 9.6, 10.6, 'b_red_enamel', 1.1)
    return it


def paladin_epee_chaines_lumiere():
    it = Item('paladin_epee_chaines_lumiere', tilt=SWORD)
    hilt(it, 'cloth_blue', 'gold', pmat2='holy')
    bar(it, 3.4, 6.4, 1.2, 1.2, 'gold')
    blade(it, 4.6, [2.6] * 9 + [1.8, 0.9], 1.25, 'silver', 'edge', d=0.9)
    # maillons de lumière enroulés autour de la lame
    for i in range(5):
        y = 6.0 + i * 1.9
        it.box((6.3, y, 7.2), (9.7, y + 0.6, 8.8), 'holy' if i % 2 else 'gold')
    return it


def paladin_epee_ailes_aube():
    it = Item('paladin_epee_ailes_aube', tilt=SWORD)
    hilt(it, 'b_cloth_white', 'b_sun', pw=2.4)
    it.col(-3.6, -3.0, 3.2, 1.0, 'gold')
    bar(it, 3.4, 4.0, 1.2, 1.4, 'gold')
    # garde en ailes déployées vers le haut
    for s in (1, -1):
        x = lambda v: 8 + s * v
        it.box((min(x(1.6), x(4.2)), 3.4, 7.65), (max(x(1.6), x(4.2)), 5.6, 8.35), 'feather')
        it.box((min(x(3.2), x(5.4)), 4.8, 7.7), (max(x(3.2), x(5.4)), 7.2, 8.3), 'feather')
        it.box((min(x(4.4), x(6.2)), 6.4, 7.75), (max(x(4.4), x(6.2)), 8.8, 8.25), 'feather')
        it.box((min(x(2.0), x(2.6)), 4.4, 7.6), (max(x(2.0), x(2.6)), 5.0, 8.4), 'gold')
    it.col(3.6, 4.8, 1.2, 1.6, 'b_sun')
    blade(it, 4.6, [2.6] * 10 + [2.0, 1.2, 0.5], 1.15, 'b_white', 'b_holy_white', d=0.9, fuller='gold', fw=0.4)
    return it


def paladin_marteau_resurrection():
    it = Item('paladin_marteau_resurrection', tilt=SWORD)
    it.col(-3.6, -2.4, 2.2, 2.2, 'gold')
    it.col(-2.4, 14.0, 1.4, 1.4, 'gold')
    it.col(-1.8, 3.2, 1.7, 1.7, 'cloth_red')
    it.col(7.0, 7.8, 1.7, 1.7, 'ruby')
    # tête de phénix : corps d'or, cœur sacré, ailes de flammes
    it.box((5.6, 14.0, 6.4), (10.4, 19.0, 9.6), 'gold')
    it.box((6.6, 15.0, 9.6), (9.4, 18.0, 9.9), 'b_sun')
    it.box((6.6, 15.0, 6.1), (9.4, 18.0, 6.4), 'b_sun')
    for s in (1, -1):
        x = lambda v: 8 + s * v
        it.box((min(x(2.4), x(4.4)), 15.0, 7.6), (max(x(2.4), x(4.4)), 18.4, 8.4), 'ember')
        it.box((min(x(4.4), x(6.0)), 16.4, 7.7), (max(x(4.4), x(6.0)), 19.8, 8.3), 'ember')
        it.box((min(x(6.0), x(7.0)), 18.0, 7.75), (max(x(6.0), x(7.0)), 20.8, 8.25), 'flame')
    it.col(19.0, 20.2, 1.6, 1.6, 'gold')
    it.col(20.2, 21.0, 0.8, 0.8, 'flame')
    return it


# =====================================================================================
#  Rôdeur : dagues
# =====================================================================================

def rodeur_dague_lame_empoisonnee():
    it = Item('rodeur_dague_lame_empoisonnee', tilt=SWORD)
    it.col(-2.2, -1.0, 1.6, 1.6, 'emerald')
    it.col(-1.0, 2.6, 1.2, 1.2, 'leather_dark')
    # garde en serpent
    it.box((5.0, 2.6, 7.4), (11.0, 3.4, 8.6), 'b_venom_steel')
    it.box((4.2, 3.0, 7.5), (5.2, 4.2, 8.5), 'b_venom_steel')
    it.box((10.8, 1.8, 7.5), (11.8, 3.0, 8.5), 'b_venom_steel')
    it.box((4.0, 4.0, 7.6), (4.8, 4.6, 8.4), 'b_poison')
    blade(it, 3.4, [1.8, 1.8, 1.7, 1.6, 1.4, 1.1, 0.7, 0.4], 0.9, 'b_venom_steel', 'edge', d=0.7,
          offs=[0, 0.4, 0.5, 0.1, -0.4, -0.4, 0, 0.2])
    inlay(it, 7.8, 4.0, 8.2, 8.0, 'b_poison', 0.7)
    return it


def rodeur_dague_pluie_ombres():
    it = Item('rodeur_dague_pluie_ombres', tilt=SWORD)
    it.col(-2.4, -1.0, 1.8, 1.8, 'amethyst')
    it.col(-1.0, 2.6, 1.2, 1.2, 'b_cloth_purple')
    it.box((5.6, 2.6, 7.4), (10.4, 3.4, 8.6), 'b_shadow')
    it.box((10.0, 3.4, 7.5), (10.8, 4.4, 8.5), 'b_shadow')
    # kriss courbe et noir
    n = 8
    blade(it, 3.4, taper(n, 2.0, 0.5), 0.95, 'b_shadow', 'b_black_steel', d=0.7,
          offs=[-0.035 * i * i for i in range(n)])
    it.box((7.4, 2.7, 8.55), (8.6, 3.3, 8.8), 'amethyst')
    return it


def rodeur_dague_danse_lames():
    it = Item('rodeur_dague_danse_lames', tilt=SWORD)
    it.col(-2.2, -1.0, 1.6, 1.6, 'b_jade')
    it.col(-1.0, 2.6, 1.2, 1.2, 'b_cloth_jade')
    # rubans de vent noués au pommeau
    it.box((5.6, -3.6, 7.85), (7.0, -1.2, 8.15), 'b_cloth_jade')
    it.box((9.0, -4.2, 7.85), (10.2, -1.6, 8.15), 'b_cloth_jade')
    it.box((7.0, -1.8, 7.8), (9.0, -1.0, 8.2), 'gold')
    bar(it, 2.6, 6.0, 0.8, 1.2, 'gold')
    # deux lames jumelles parallèles
    for cx in (6.6, 9.4):
        for i, w in enumerate((1.3, 1.2, 1.1, 1.0, 0.8, 0.6, 0.4)):
            it.col(3.4 + i * 1.1, 4.5 + i * 1.1, w, 0.6, 'mithril' if i < 6 else 'edge', cx=cx)
    it.box((6.6, 3.4, 7.7), (9.4, 4.0, 8.3), 'gold')
    it.box((7.6, 2.7, 8.55), (8.4, 3.3, 8.75), 'b_jade')
    return it


# =====================================================================================
#  Rôdeur : arcs (avec états de tension)
# =====================================================================================

def make_bow(id, limb, wood, grip, tip, deco=None, strings=(8.0,), string='string', arrow=('wood_pale', 'steel'),
             tips=None):
    """limb : profil d'une branche [(y0, y1, x0, x1)] de y=8 vers le haut (copié en miroir vers le bas)."""
    top = limb[-1]
    sx = (top[2] + top[3]) / 2 - 0.25

    def bow(pull):
        it = Item(id, tilt=45, display=BOW)
        for y0, y1, x0, x1 in limb:
            it.box((x0, y0, 7.5), (x1, y1, 8.5), wood)
            it.box((x0, 16 - y1, 7.5), (x1, 16 - y0, 8.5), wood)
        ty = top[1]
        it.box((top[2] - 0.3, ty, 7.6), (top[3] + 0.3, ty + 1.2, 8.4), tip)
        it.box((top[2] - 0.3, 16 - ty - 1.2, 7.6), (top[3] + 0.3, 16 - ty, 8.4), tip)
        if tips:
            tips(it, ty)
        it.box((9.2, 5.8, 7.3), (11.0, 10.2, 8.7), grip)
        if deco:
            deco(it)
        span = ty - 8
        for z in strings:
            for half in (1, -1):
                steps = 4
                for k in range(steps):
                    t0, t1 = k / steps, (k + 1) / steps
                    x = sx - pull * (1 - (t0 + t1) / 2)
                    ya, yb = 8 + half * span * t0, 8 + half * span * t1
                    it.box((x - 0.15, min(ya, yb), z - 0.1), (x + 0.15, max(ya, yb), z + 0.1), string)
        if pull:
            x0 = sx - pull
            it.box((x0, 7.85, 7.85), (x0 + 11.5, 8.15, 8.15), arrow[0])
            it.box((x0 + 11.5, 7.5, 7.8), (x0 + 12.7, 8.5, 8.2), arrow[1])
            it.box((x0 + 12.7, 7.8, 7.85), (x0 + 13.3, 8.2, 8.15), 'edge')
            it.box((x0 + 0.2, 7.3, 7.95), (x0 + 2.0, 8.7, 8.05), 'feather')
        return it

    base = bow(0)
    base.variants = {f'_pulling_{i}': bow(p) for i, p in enumerate((1.4, 2.6, 3.6))}
    return base


RECURVE = [(8.0, 11.0, 9.2, 10.6), (11.0, 14.0, 8.4, 9.8), (14.0, 16.4, 7.2, 8.6), (16.4, 18.0, 6.2, 7.4),
           (18.0, 19.0, 6.6, 7.6)]
LONG = [(8.0, 12.0, 9.2, 10.4), (12.0, 16.0, 8.6, 9.8), (16.0, 19.0, 7.6, 8.8), (19.0, 21.0, 6.6, 7.8)]
SHORT = [(8.0, 10.6, 9.2, 10.6), (10.6, 13.0, 8.2, 9.8), (13.0, 15.4, 6.8, 8.4)]
WIDE = [(8.0, 10.4, 9.2, 10.8), (10.4, 13.0, 8.6, 10.2), (13.0, 15.4, 7.4, 9.2), (15.4, 17.6, 6.0, 7.8),
        (17.6, 19.4, 5.0, 6.4)]


def rodeur_arc_volee_acier():
    def deco(it):
        for y in (12.0, 3.0):
            it.box((8.2, y, 7.4), (10.0, y + 1.0, 8.6), 'steel')
        it.box((10.8, 7.2, 7.6), (11.4, 8.8, 8.4), 'steel')
    return make_bow('rodeur_arc_volee_acier', RECURVE, 'wood', 'leather', 'steel', deco, strings=(7.6, 8.0, 8.4))


def rodeur_arc_fleche_fumigene():
    def deco(it):
        it.box((8.6, 10.2, 7.3), (10.2, 11.6, 8.7), 'b_cloth_grey')
        it.box((8.6, 4.4, 7.3), (10.2, 5.8, 8.7), 'b_cloth_grey')
        for (x, y) in ((11.2, 6.4), (11.2, 8.6), (10.8, 10.0)):
            it.box((x - 0.2, y - 0.6, 7.4), (x + 0.8, y + 0.6, 8.6), 'b_smoke')
    return make_bow('rodeur_arc_fleche_fumigene', SHORT, 'b_birch', 'b_cloth_grey', 'b_cloth_grey', deco,
                    arrow=('b_birch', 'b_smoke'))


def rodeur_arc_marque_chasseur():
    def deco(it):
        it.box((10.95, 7.0, 7.5), (11.25, 9.0, 8.5), 'cloth_red')
        it.box((10.95, 7.6, 7.3), (11.25, 8.4, 8.7), 'cloth_red')
        it.box((9.6, 12.6, 8.5), (10.2, 13.6, 8.8), 'bone')
        it.box((9.6, 2.4, 8.5), (10.2, 3.4, 8.8), 'bone')
    return make_bow('rodeur_arc_marque_chasseur', LONG, 'wood_dark', 'leather_dark', 'bone', deco)


def rodeur_arc_fleche_explosive():
    def deco(it):
        for y in (6.0, 7.6, 9.2):
            it.box((9.0, y, 7.1), (11.2, y + 0.5, 8.9), 'b_copper')
        it.box((11.2, 9.6, 7.8), (11.8, 10.6, 8.2), 'b_rope')
        it.box((11.6, 10.4, 7.85), (12.0, 10.8, 8.15), 'ember')
        for y in (11.6, 3.8):
            it.box((8.4, y, 7.4), (10.0, y + 0.6, 8.6), 'b_copper')
    return make_bow('rodeur_arc_fleche_explosive', RECURVE, 'wood', 'b_black', 'b_copper', deco,
                    arrow=('wood', 'ember'))


def rodeur_arc_filet():
    def deco(it):
        # filet de corde tendu entre la poignée et les branches
        for k, y in enumerate((11.0, 12.6, 14.2)):
            it.box((8.0 - k * 0.6, y, 7.85), (9.4, y + 0.3, 8.15), 'b_rope')
            it.box((8.0 - k * 0.6, 16 - y - 0.3, 7.85), (9.4, 16 - y, 8.15), 'b_rope')
        it.box((8.0, 10.2, 7.85), (8.3, 15.0, 8.15), 'b_rope')
        it.box((8.0, 1.0, 7.85), (8.3, 5.8, 8.15), 'b_rope')
        it.box((11.0, 7.4, 7.6), (12.0, 8.6, 8.4), 'steel_dark')
        it.box((11.6, 8.6, 7.7), (12.2, 9.4, 8.3), 'steel_dark')
    return make_bow('rodeur_arc_filet', RECURVE, 'wood_pale', 'b_rope', 'steel_dark', deco, string='b_rope')


def rodeur_arc_compagnon_faucon():
    def tips(it, ty):
        it.box((6.0, ty + 1.2, 7.6), (7.2, ty + 2.0, 8.4), 'gold')
        it.box((6.0, 16 - ty - 2.0, 7.6), (7.2, 16 - ty - 1.2, 8.4), 'gold')

    def deco(it):
        # rémiges le long des branches
        for (y0, y1, x0, x1) in ((11.0, 14.0, 9.8, 11.0), (14.0, 16.4, 8.6, 9.8), (16.4, 18.0, 7.4, 8.4)):
            it.box((x0, y0, 7.9), (x1, y1, 8.1), 'feather')
            it.box((x0, 16 - y1, 7.9), (x1, 16 - y0, 8.1), 'b_fur')
        it.box((10.8, 7.2, 7.5), (11.4, 8.8, 8.5), 'gold')
    return make_bow('rodeur_arc_compagnon_faucon', RECURVE, 'wood', 'leather', 'gold', deco, tips=tips)


def rodeur_arc_fleche_dragon():
    def tips(it, ty):
        it.box((4.6, ty + 0.4, 7.6), (5.6, ty + 2.0, 8.4), 'b_horn')
        it.box((4.6, 16 - ty - 2.0, 7.6), (5.6, 16 - ty - 0.4, 8.4), 'b_horn')

    def deco(it):
        it.box((10.8, 6.6, 7.4), (11.6, 9.4, 8.6), 'b_dragon_glow')
        for (y0, y1, x0, x1) in ((10.4, 13.0, 10.2, 11.0), (13.0, 15.4, 9.2, 10.0)):
            it.box((x0, y0, 7.6), (x1, y1, 8.4), 'b_horn')
            it.box((x0, 16 - y1, 7.6), (x1, 16 - y0, 8.4), 'b_horn')
    return make_bow('rodeur_arc_fleche_dragon', WIDE, 'b_dragon', 'b_black', 'b_dragon_glow', deco, tips=tips,
                    string='b_dragon_glow', arrow=('b_black', 'b_dragon_glow'))


# =====================================================================================
#  Lame-runique
# =====================================================================================

def lamerunique_lame_rune_foudre():
    it = Item('lamerunique_lame_rune_foudre', tilt=SWORD)
    hilt(it, 'leather_dark', 'b_copper', w=1.3, pw=2.0)
    bar(it, 3.4, 7.6, 1.2, 1.4, 'b_copper')
    it.box((3.8, 4.6, 7.5), (4.8, 5.6, 8.5), 'b_copper')
    it.box((11.2, 4.6, 7.5), (12.2, 5.6, 8.5), 'b_copper')
    blade(it, 4.6, [2.2] * 9 + [1.6, 0.8], 1.2, 'steel', 'edge', d=1.0)
    for (x0, y0, x1, y1) in ((7.6, 5.4, 8.2, 7.4), (8.0, 7.2, 8.8, 7.8), (8.2, 7.8, 8.8, 9.8), (7.4, 9.6, 8.6, 10.2),
                             (7.4, 10.2, 8.0, 12.2), (7.8, 12.0, 8.6, 12.6), (8.0, 12.6, 8.6, 14.4)):
        inlay(it, x0, y0, x1, y1, 'b_lightning')
    return it


def lamerunique_lame_entaille_spectrale():
    it = Item('lamerunique_lame_entaille_spectrale', tilt=SWORD)
    hilt(it, 'leather_dark', 'silver', w=1.3, pw=2.0)
    bar(it, 3.4, 6.8, 1.0, 1.4, 'silver')
    # cadre d'argent ouvert, cœur spectral
    for cx in (6.7, 9.3):
        it.col(4.4, 15.6, 0.6, 0.9, 'silver', cx=cx)
    it.col(4.4, 15.6, 2.0, 0.6, 'b_spectral')
    it.col(15.6, 16.8, 2.4, 0.8, 'silver')
    it.col(16.8, 18.0, 1.4, 0.6, 'b_spectral')
    it.col(18.0, 18.8, 0.6, 0.5, 'b_spectral')
    return it


def lamerunique_lame_rune_vitesse():
    it = Item('lamerunique_lame_rune_vitesse', tilt=SWORD)
    hilt(it, 'b_cloth_jade', 'mithril', w=1.2, pw=1.8)
    # garde en ailes rabattues vers l'arrière
    bar(it, 3.4, 3.4, 0.8, 1.0, 'mithril')
    it.box((3.6, 2.4, 7.6), (6.4, 3.4, 8.4), 'mithril')
    it.box((2.8, 1.4, 7.7), (4.0, 2.6, 8.3), 'mithril')
    it.box((9.6, 2.4, 7.6), (12.4, 3.4, 8.4), 'mithril')
    it.box((12.0, 1.4, 7.7), (13.2, 2.6, 8.3), 'mithril')
    blade(it, 4.2, taper(11, 1.6, 0.5), 1.25, 'mithril', 'edge', d=0.7, fuller='b_jade', fw=0.3)
    return it


def lamerunique_glaive_brise_garde():
    it = Item('lamerunique_glaive_brise_garde', tilt=SWORD)
    it.col(-5.0, -3.6, 2.2, 2.2, 'obsidian')
    it.col(-3.6, 3.0, 1.5, 1.5, 'leather_dark')
    bar(it, 3.0, 8.4, 1.4, 1.6, 'obsidian')
    # couperet : lame large à bout carré
    it.col(4.4, 18.4, 4.0, 1.2, 'runestone')
    it.box((10.0, 4.4, 7.6), (10.6, 18.4, 8.4), 'edge')
    it.box((5.4, 17.6, 7.6), (10.6, 18.6, 8.4), 'edge')
    it.box((5.4, 6.0, 7.6), (6.0, 16.0, 8.4), 'obsidian')
    return it


def lamerunique_glaive_sceau_abime():
    it = Item('lamerunique_glaive_sceau_abime', tilt=SWORD)
    it.col(-5.0, -3.6, 2.2, 2.2, 'b_void')
    it.col(-4.6, -4.0, 2.4, 2.4, 'void_glow')
    it.col(-3.6, 3.0, 1.4, 1.4, 'b_cloth_purple')
    # sceau circulaire dans la garde
    it.col(2.4, 6.0, 3.6, 1.2, 'b_void')
    it.col(3.0, 5.4, 5.0, 1.2, 'b_void')
    it.col(3.4, 5.0, 1.8, 1.5, 'void_glow')
    blade(it, 6.0, [2.8] * 9 + [2.2, 1.4], 1.2, 'b_void', 'b_black_steel', d=1.1, fuller='void_glow', fw=0.4)
    # crochet de l'abîme
    it.box((5.4, 14.6, 7.7), (6.6, 15.8, 8.3), 'b_black_steel')
    it.box((4.8, 15.8, 7.7), (5.8, 17.2, 8.3), 'b_black_steel')
    return it


def lamerunique_lame_lames_tournoyantes():
    it = Item('lamerunique_lame_lames_tournoyantes', tilt=SWORD)
    hilt(it, 'leather_dark', 'obsidian', w=1.3, pw=2.0)
    # garde en croissant
    it.box((4.0, 3.4, 7.4), (12.0, 4.4, 8.6), 'obsidian')
    it.box((3.2, 4.0, 7.5), (4.4, 5.6, 8.5), 'obsidian')
    it.box((11.6, 4.0, 7.5), (12.8, 5.6, 8.5), 'obsidian')
    blade(it, 4.4, [2.4] * 9 + [1.8, 0.9], 1.2, 'runestone', 'edge', d=1.0)
    for (y, m) in ((6.2, 'arcane'), (9.0, 'amethyst'), (11.8, 'emerald')):
        inlay(it, 7.4, y, 8.6, y + 1.2, m)
    return it


def lamerunique_lame_rune_vol_vie():
    it = Item('lamerunique_lame_rune_vol_vie', tilt=SWORD)
    hilt(it, 'b_blood', 'b_black_steel', w=1.3, pw=2.0, pmat2='ruby')
    # garde en ailes de chauve-souris
    bar(it, 3.4, 4.0, 1.0, 1.2, 'b_black_steel')
    for s in (1, -1):
        x = lambda v: 8 + s * v
        it.box((min(x(2.0), x(4.4)), 3.6, 7.7), (max(x(2.0), x(4.4)), 4.8, 8.3), 'b_black_steel')
        it.box((min(x(3.6), x(5.0)), 4.8, 7.7), (max(x(3.6), x(5.0)), 5.8, 8.3), 'b_black_steel')
        it.box((min(x(3.0), x(3.8)), 3.0, 7.75), (max(x(3.0), x(3.8)), 3.6, 8.25), 'b_black_steel')
    # lame dentelée
    widths = [2.4, 2.0] * 5 + [1.6, 0.8]
    blade(it, 4.4, widths, 1.0, 'b_blood', 'b_black_steel', d=0.9, fuller='b_blood_glow', fw=0.5)
    return it


def lamerunique_glaive_prison_runique():
    it = Item('lamerunique_glaive_prison_runique', tilt=SWORD)
    it.col(-5.0, -3.6, 2.2, 2.2, 'obsidian')
    it.col(-3.6, 3.0, 1.4, 1.4, 'leather_dark')
    # garde en cage : barreaux autour de la poignée
    for (x, z) in ((6.4, 6.4), (9.6, 6.4), (6.4, 9.6), (9.6, 9.6)):
        it.box((x - 0.3, -3.0, z - 0.3), (x + 0.3, 3.4, z + 0.3), 'b_chain')
    it.col(-3.6, -3.0, 3.8, 3.8, 'obsidian')
    it.col(3.0, 4.6, 5.6, 2.2, 'obsidian')
    it.col(3.4, 4.2, 1.2, 2.4, 'rune_glow')
    blade(it, 4.6, [3.0] * 10 + [2.2, 1.2], 1.15, 'runestone', 'edge', d=1.1, fuller='rune_glow', fw=0.4)
    return it


def lamerunique_glaive_lame_apocalypse():
    it = Item('lamerunique_glaive_lame_apocalypse', tilt=SWORD)
    it.col(-5.2, -3.8, 2.4, 2.4, 'b_black_steel')
    it.col(-4.8, -4.2, 2.6, 2.6, 'b_crack')
    it.col(-3.8, 3.0, 1.5, 1.5, 'leather_dark')
    # garde à cornes
    bar(it, 3.0, 8.0, 1.6, 1.8, 'b_black_steel')
    for s in (1, -1):
        x = lambda v: 8 + s * v
        it.box((min(x(3.6), x(4.6)), 4.6, 7.5), (max(x(3.6), x(4.6)), 6.4, 8.5), 'b_horn')
        it.box((min(x(4.2), x(5.2)), 6.4, 7.6), (max(x(4.2), x(5.2)), 7.8, 8.4), 'b_horn')
    it.col(3.4, 4.4, 1.4, 2.0, 'b_crack')
    # flamberge noire au fil ardent
    n = 12
    offs = [(0.35 if i % 2 else -0.35) if i < n - 2 else 0 for i in range(n)]
    blade(it, 4.6, [3.4] * (n - 3) + [2.8, 1.8, 0.8], 1.35, 'b_black_steel', 'b_crack', d=1.2, offs=offs)
    return it


def lamerunique_lame_eveil_runique():
    it = Item('lamerunique_lame_eveil_runique', tilt=SWORD)
    hilt(it, 'b_cloth_white', 'gold', w=1.3, pw=2.2, pmat2='arcane')
    # cercle runique d'or serti dans la garde
    it.col(2.6, 6.4, 4.4, 1.0, 'gold')
    it.col(3.2, 5.8, 5.4, 1.0, 'gold')
    it.col(3.2, 5.8, 3.0, 1.3, 'arcane')
    it.col(3.8, 5.2, 1.2, 1.5, 'b_gold_rune')
    blade(it, 6.4, [2.6] * 9 + [2.0, 1.0], 1.25, 'b_white', 'edge', d=1.0, fuller='b_gold_rune', fw=0.6)
    return it


ARMES_BUTIN = [
    mage_baton_orbe_mana, mage_baton_lance_givre, mage_sceptre_flammeches, mage_sceptre_intrication_arcanique,
    mage_baton_prison_givre, mage_sceptre_mur_flammes, mage_sceptre_singularite, mage_baton_miroirs,
    mage_sceptre_tempete_solaire, mage_baton_arret_temps,
    druide_baton_lierre_etrangleur, druide_faucille_graine_explosive, druide_baton_souffle_vent,
    druide_faucille_esprit_cerf, druide_baton_essaim_spores, druide_faucille_nuee_abeilles,
    druide_baton_bosquet_sacre, druide_faucille_morsure_ours, druide_baton_avatar_foret, druide_faucille_colere_ciel,
    guerrier_epee_longue_coup_bouclier, guerrier_epee_longue_taillade, guerrier_hache_bond_lion,
    guerrier_hache_provocation, guerrier_epee_longue_tourbillon_lames, guerrier_epee_longue_lame_choc,
    guerrier_hache_chaine_guerre, guerrier_hache_peau_fer, guerrier_hache_colere_titan,
    guerrier_epee_longue_dernier_rempart,
    paladin_epee_bouclier_renvoye, paladin_marteau_lumiere_purifiante, paladin_epee_frappe_sacree,
    paladin_marteau_benediction, paladin_marteau_marteau_celeste, paladin_marteau_sanctuaire,
    paladin_epee_charge_croise, paladin_epee_chaines_lumiere, paladin_epee_ailes_aube, paladin_marteau_resurrection,
    rodeur_arc_volee_acier, rodeur_arc_fleche_fumigene, rodeur_dague_lame_empoisonnee, rodeur_arc_marque_chasseur,
    rodeur_arc_fleche_explosive, rodeur_dague_pluie_ombres, rodeur_arc_filet, rodeur_arc_compagnon_faucon,
    rodeur_arc_fleche_dragon, rodeur_dague_danse_lames,
    lamerunique_lame_rune_foudre, lamerunique_lame_entaille_spectrale, lamerunique_lame_rune_vitesse,
    lamerunique_glaive_brise_garde, lamerunique_glaive_sceau_abime, lamerunique_lame_lames_tournoyantes,
    lamerunique_lame_rune_vol_vie, lamerunique_glaive_prison_runique, lamerunique_glaive_lame_apocalypse,
    lamerunique_lame_eveil_runique,
]
