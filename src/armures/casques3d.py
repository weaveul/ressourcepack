"""Casques de classe modelés en 3D (cubes texturés), portés sur la tête à la place du calque d'armure.

Le casque EvoPerso garde item_model oraxen:<classe>_helmet ; pack/assets/oraxen/items/<classe>_helmet.json pointe ici
vers evo:item/casque3d_<classe>. EvoPerso retire l'equippable « model » du casque : le jeu affiche alors l'objet
lui-même sur la tête (transformation « head »).

Repère : la tête occupe 4..12 sur les trois axes, l'avant est côté z bas. head scale 1.6 : 8 unités = la tête.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'items'))
from PIL import Image, ImageDraw  # noqa: E402
from kit import Item, Mat, MATS, h, mix, OBJECT  # noqa: E402
from render import render  # noqa: E402

HELMET = dict(OBJECT)
HELMET.update({
    'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1.6, 1.6, 1.6]},
    'gui': {'rotation': [18, 160, 0], 'translation': [0, -1, 0], 'scale': [0.62] * 3},
    'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.45] * 3},
    'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [0.8] * 3},
})


# --- Motifs (c, p, face, px, py, w, hgt) ------------------------------------------------------------------------

def hammered(c, p, face, px, py, w, hgt):
    """Métal martelé : cellules d'un demi-pixel plus ou moins claires, quelques creux sombres."""
    k = 0.9 + 0.16 * h(int(p[0] * 2), int(p[1] * 2), int(p[2] * 2))
    if h(p[0] * 4, p[1] * 4, p[2] * 4) > 0.965:
        k *= 0.7
    return tuple(v * k for v in c)


def brushed(c, p, face, px, py, w, hgt):
    """Métal brossé : stries horizontales."""
    return tuple(v * (0.92 + 0.12 * h(int(p[1] * 4), 7)) for v in c)


def filigree(c, p, face, px, py, w, hgt):
    """Or ciselé : volutes sombres."""
    s = math.sin(p[0] * 2.3 + math.sin(p[1] * 2.1) * 1.5) + math.sin(p[2] * 2.3 + p[1] * 1.2)
    return tuple(v * 0.72 for v in c) if abs(s) < 0.22 else c


def runes_glow(c, p, face, px, py, w, hgt):
    """Acier noir gravé de runes violettes lumineuses."""
    gx, gy = int(p[0] * 2 + p[2] * 2) % 5, int(p[1] * 2) % 4
    if ((gx == 1 and gy in (0, 1, 2)) or (gy == 1 and gx in (1, 2, 3))) and h(int(p[0] * 2 + p[2] * 2) // 5, int(p[1] * 2) // 4) > 0.7:
        return (196, 110, 255)
    return tuple(v * (0.9 + 0.15 * h(int(p[0] * 2), int(p[1] * 2), int(p[2] * 2))) for v in c)


def cloth_folds(c, p, face, px, py, w, hgt):
    """Étoffe : plis verticaux et trame fine."""
    k = 0.86 + 0.14 * (0.5 + 0.5 * math.sin((p[0] + p[2]) * 1.9))
    if (px + py) % 2 == 0:
        k *= 0.96
    return tuple(v * k for v in c)


def starry(c, p, face, px, py, w, hgt):
    c = cloth_folds(c, p, face, px, py, w, hgt)
    if h(int(p[0] * 4), int(p[1] * 4), int(p[2] * 4)) > 0.975:
        return (255, 238, 170)
    return c


def leather(c, p, face, px, py, w, hgt):
    """Cuir : grain, couture claire en pointillés le long des bords."""
    k = 0.9 + 0.14 * h(int(p[0] * 3), int(p[1] * 3), int(p[2] * 3))
    if (px == 1 or py == 1 or px == w - 2 or py == hgt - 2) and w > 5 and hgt > 5 and (px + py) % 2 == 0:
        return (214, 190, 140)
    return tuple(v * k for v in c)


def fur(c, p, face, px, py, w, hgt):
    k = 0.75 + 0.4 * h(int(p[0] * 4), int(p[1] * 1.5), int(p[2] * 4))
    return tuple(v * k for v in c)


def horn_rings(c, p, face, px, py, w, hgt):
    k = 0.82 if int(p[1] * 2.5) % 3 == 0 else 1.0
    return tuple(v * k * (0.94 + 0.1 * h(p[0] * 4, p[1] * 4, p[2] * 4)) for v in c)


def feathers(c, p, face, px, py, w, hgt):
    """Plumes : barbes en biais et hampe sombre."""
    if abs(((p[0] + p[2]) * 4) % 3 - (p[1] * 4) % 3) < 0.5:
        return tuple(v * 0.82 for v in c)
    return c


def bark_grain(c, p, face, px, py, w, hgt):
    k = 0.78 if int(p[0] * 3 + p[2] * 3 + h(int(p[1] * 2), 2) * 2) % 4 == 0 else 1.0
    return tuple(v * k * (0.94 + 0.1 * h(p[0] * 4, p[1] * 4, p[2] * 4)) for v in c)


def leaves(c, p, face, px, py, w, hgt):
    v = h(int(p[0] * 3), int(p[1] * 3), int(p[2] * 3))
    if v > 0.8:
        return mix(c, (170, 220, 110), 0.6)
    if v < 0.15:
        return tuple(x * 0.7 for x in c)
    return c


MATS.update({
    'skin': Mat((196, 148, 118), 4, 0.9),
    # Guerrier
    'gu_steel': Mat((148, 154, 166), 6, 0.72, pattern=hammered, hi=(220, 226, 236)),
    'gu_steel_l': Mat((178, 184, 194), 5, 0.75, pattern=brushed, hi=(240, 242, 248)),
    'gu_bronze': Mat((196, 132, 70), 6, 0.74, pattern=filigree, hi=(250, 204, 136)),
    'gu_red': Mat((150, 32, 30), 8, 0.82, pattern=cloth_folds),
    'gu_horn': Mat((220, 194, 148), 6, 0.8, grad=-0.3, pattern=horn_rings),
    'gu_horn_tip': Mat((96, 74, 54), 5, 0.8),
    'slit': Mat((16, 14, 20), 2, 1),
    # Paladin
    'pa_silver': Mat((214, 218, 228), 5, 0.76, pattern=brushed, hi=(255, 255, 255)),
    'pa_gold': Mat((226, 182, 74), 6, 0.74, pattern=filigree, hi=(255, 236, 150)),
    'pa_white': Mat((240, 238, 230), 6, 0.86, pattern=feathers),
    'pa_holy': Mat((255, 236, 150), 4, 0.95, light=12, hi=(255, 255, 230)),
    'pa_blue': Mat((44, 70, 150), 6, 0.82, pattern=cloth_folds),
    # Mage
    'ma_cloth': Mat((48, 52, 140), 6, 0.84, pattern=starry),
    'ma_cloth_d': Mat((32, 34, 96), 6, 0.84, pattern=cloth_folds),
    'ma_gold': Mat((220, 178, 80), 6, 0.76, pattern=filigree, hi=(255, 232, 150)),
    'ma_gem': Mat((90, 190, 255), 4, 0.9, light=13, hi=(220, 245, 255)),
    'ma_star': Mat((255, 230, 140), 4, 0.95, light=14),
    # Rôdeur
    'ro_cloth': Mat((62, 92, 52), 6, 0.84, pattern=cloth_folds),
    'ro_cloth_d': Mat((40, 60, 36), 6, 0.84, pattern=cloth_folds),
    'ro_leather': Mat((118, 78, 46), 6, 0.8, pattern=leather),
    'ro_shadow': Mat((22, 26, 22), 3, 1),
    'ro_feather': Mat((200, 70, 50), 6, 0.84, pattern=feathers),
    'ro_buckle': Mat((190, 190, 196), 5, 0.75),
    # Druide
    'dr_wood': Mat((110, 78, 48), 6, 0.78, pattern=bark_grain),
    'dr_antler': Mat((222, 204, 168), 6, 0.8, grad=-0.2, pattern=horn_rings),
    'dr_leaf': Mat((80, 150, 64), 10, 0.82, pattern=leaves),
    'dr_leaf_d': Mat((52, 110, 48), 10, 0.82, pattern=leaves),
    'dr_flower': Mat((240, 150, 200), 6, 0.9, light=4),
    'dr_moss': Mat((96, 120, 60), 12, 0.85, pattern=fur),
    # Lame-runique
    'lr_steel': Mat((52, 50, 64), 6, 0.78, pattern=runes_glow, hi=(110, 108, 130)),
    'lr_steel_l': Mat((84, 82, 100), 5, 0.78, pattern=brushed),
    'lr_glow': Mat((190, 100, 255), 4, 0.95, light=15, hi=(240, 210, 255)),
    'lr_silver': Mat((170, 170, 186), 5, 0.76, pattern=brushed),
})

S, E = 3.4, 12.6  # coque à 0.6 px autour de la tête


def shell(it, mat, y0=3.6, y1=12.4, top=True):
    it.box((S, y0, S), (E, y1, E), mat)
    if top:
        it.box((S + 0.6, y1, S + 0.6), (E - 0.6, y1 + 0.8, E - 0.6), mat)


def curve(it, x0, side, n, f, mats):
    """Pièce courbe (corne, bois de cerf, plume) : f(t) -> (dx, y, dz, w)."""
    for i in range(n):
        t = i / (n - 1)
        dx, y, dz, w = f(t)
        cx = x0 + side * dx
        mat = mats[0] if i == 0 else (mats[2] if i == n - 1 else mats[1])
        it.box((cx - w, y - w * 0.8, dz - w), (cx + w, y + w * 0.8, dz + w), mat)


def guerrier():
    it = Item('casque3d_guerrier', density=4, display=HELMET)
    shell(it, 'gu_steel')
    for x0 in (4.6, 9.0):
        it.box((x0, 7.6, S - 0.05), (x0 + 2.4, 8.4, S), 'slit')
    for x in (5.0, 6.0, 9.6, 10.6):
        it.box((x, 5.0, S - 0.85), (x + 0.4, 5.8, S - 0.8), 'slit')
    it.box((7.3, 3.6, S - 0.6), (8.7, 13.4, S), 'gu_bronze')
    it.box((7.3, 13.2, S - 0.6), (8.7, 13.8, E - 1.5), 'gu_bronze')
    it.box((S - 0.4, 8.8, S - 0.4), (E + 0.4, 9.6, E + 0.4), 'gu_bronze')
    it.box((S - 0.3, 3.4, S - 0.3), (E + 0.3, 4.2, E + 0.3), 'gu_steel_l')
    it.box((4.6, 4.2, S - 0.8), (7.3, 7.4, S), 'gu_steel_l')
    it.box((8.7, 4.2, S - 0.8), (11.4, 7.4, S), 'gu_steel_l')
    for x in (S - 0.5, E):
        for y in (5.0, 7.0, 11.0):
            it.box((x, y, 7.4), (x + 0.5, y + 0.6, 8.0), 'gu_bronze')
    for i in range(5):
        z = 9 + i * 1.1
        it.box((7.5, 12.6 - i * 1.0, z), (8.5, 14.6 - i * 0.8, z + 1.2), 'gu_red')
    for side in (-1, 1):
        curve(it, S if side < 0 else E, side, 11,
              lambda t: (0.8 + 3.4 * math.sin(t * math.pi * 0.75), 10 + 6 * (1 - math.cos(t * math.pi * 0.75)),
                         8.4 - 3 * t ** 1.5, 1.5 - t),
              ('gu_bronze', 'gu_horn', 'gu_horn_tip'))
    return it


def paladin():
    it = Item('casque3d_paladin', density=4, display=HELMET)
    shell(it, 'pa_silver')
    # visière en croix
    it.box((4.4, 7.8, S - 0.05), (11.6, 8.6, S), 'slit')
    it.box((7.6, 4.6, S - 0.05), (8.4, 7.8, S), 'slit')
    it.box((S - 0.6, 7.2, S - 0.6), (7.0, 7.8, S), 'pa_gold')
    it.box((9.0, 7.2, S - 0.6), (E + 0.6, 7.8, S), 'pa_gold')
    it.box((7.0, 8.6, S - 0.6), (9.0, 12.4, S), 'pa_gold')                 # croix du front
    it.box((5.8, 10.2, S - 0.6), (10.2, 11.0, S), 'pa_gold')
    it.box((7.5, 10.3, S - 0.9), (8.5, 10.9, S - 0.6), 'pa_holy')
    it.box((S - 0.3, 3.4, S - 0.3), (E + 0.3, 4.2, E + 0.3), 'pa_gold')
    it.box((S - 0.3, 12.0, S - 0.3), (E + 0.3, 12.6, E + 0.3), 'pa_gold')
    # ailes dorées et blanches sur les côtés
    for side in (-1, 1):
        x0 = S if side < 0 else E
        it.box((x0 + side * 0.1 - 0.5, 8.4, 6.6), (x0 + side * 0.1 + 0.5, 11.4, 9.6), 'pa_gold')
        for j in range(6):
            y = 9.2 + j * 1.25
            ln = 6.2 - j * 0.7
            x1 = x0 + side * (0.5 + j * 0.3)
            a, b = sorted((x1, x1 + side * 0.9))
            it.box((a, y, 7.0 + j * 0.4), (b, y + 1.2, 7.0 + j * 0.4 + ln), 'pa_gold' if j == 5 else 'pa_white')
    # plumet
    for i in range(6):
        it.box((7.3, 13.2 + i * 0.7, 8 + i * 0.9), (8.7, 14.4 + i * 0.6, 9.4 + i * 0.9), 'pa_white')
    it.box((7.0, 13.0, 7.4), (9.0, 13.8, 9.4), 'pa_gold')
    return it


def mage():
    it = Item('casque3d_mage', density=4, display=HELMET)
    # chapeau pointu : bord large, cône en segments qui ploie vers l'arrière
    it.box((1.0, 11.2, 1.0), (15.0, 12.0, 15.0), 'ma_cloth_d')
    it.box((S, 11.0, S), (E, 12.6, E), 'ma_cloth')
    it.box((S - 0.2, 12.2, S - 0.2), (E + 0.2, 13.4, E + 0.2), 'ma_gold')     # bandeau
    it.box((7.2, 12.3, S - 0.6), (8.8, 13.3, S - 0.2), 'ma_gem')
    n = 12
    for i in range(n):
        t = i / (n - 1)
        w = 4.5 * (1 - t) ** 1.2 + 0.45
        cz = 8 + 4.6 * t * t
        y = 13.4 + i * 0.95
        it.box((8 - w, y, cz - w), (8 + w, y + 1.05, cz + w), 'ma_cloth')
    it.box((7.4, 24.8, 12.0), (8.6, 26.0, 13.2), 'ma_star')
    # cheveux / col sombre sous le bord (sur la nuque) et étoiles brodées
    it.box((S, 7.0, 10.6), (E, 11.2, E), 'ma_cloth_d')
    for (x, y, z) in ((5, 15.4, 4.6), (10.2, 17.2, 5.6), (6.4, 19.6, 7.2)):
        it.box((x, y, z - 0.2), (x + 0.8, y + 0.8, z), 'ma_star')
    return it


def rodeur():
    it = Item('casque3d_rodeur', density=4, display=HELMET)
    # capuche creuse : dos, côtés et dessus, visage ouvert
    it.box((S, 3.6, E - 0.8), (E, 12.6, E), 'ro_cloth')
    it.box((S, 3.6, S), (S + 0.6, 12.6, E - 0.8), 'ro_cloth')
    it.box((E - 0.6, 3.6, S), (E, 12.6, E - 0.8), 'ro_cloth')
    it.box((S + 0.6, 12.0, S), (E - 0.6, 12.6, E - 0.8), 'ro_cloth')
    it.box((S + 0.6, 10.4, S), (E - 0.6, 12.0, S + 0.8), 'ro_cloth')        # rebord du front
    it.box((S + 0.6, 3.6, S), (5.0, 10.4, S + 0.8), 'ro_cloth')             # pans le long des joues
    it.box((11.0, 3.6, S), (E - 0.6, 10.4, S + 0.8), 'ro_cloth')
    it.box((S + 0.6, 12.6, S + 0.6), (E - 0.6, 13.4, E - 0.2), 'ro_cloth')
    it.box((5.0, 9.8, S + 0.8), (11.0, 10.4, S + 1.0), 'ro_shadow')         # ombre sous le rebord
    # pointe de la capuche qui retombe dans le dos
    for i in range(5):
        it.box((6.0 + i * 0.3, 12.4 - i * 1.2, E - 0.2 + i * 0.5), (10.0 - i * 0.3, 13.4 - i * 1.1, E + 0.8 + i * 0.5), 'ro_cloth_d')
    # pèlerine sur les épaules (bas de la capuche)
    it.box((2.6, 2.8, 2.6), (13.4, 4.0, 13.4), 'ro_cloth_d')
    # bandeau de cuir, boucle et plume
    it.box((S - 0.2, 10.6, S - 0.2), (E + 0.2, 11.6, E + 0.2), 'ro_leather')
    it.box((E, 10.4, 6.0), (E + 0.4, 11.8, 7.4), 'ro_buckle')
    for i in range(6):
        it.box((E + 0.2, 11.4 + i * 0.9, 7.6 + i * 0.6), (E + 0.8, 12.4 + i * 0.9, 9.4 + i * 0.5), 'ro_feather')
    return it


def druide():
    it = Item('casque3d_druide', density=4, display=HELMET)
    # couronne de bois et mousse, visage libre
    it.box((S, 10.2, S), (E, 12.0, E), 'dr_wood')
    it.box((S + 0.4, 12.0, S + 0.4), (E - 0.4, 12.6, E - 0.4), 'dr_moss')
    it.box((S, 6.0, 10.6), (E, 10.2, E), 'dr_moss')                           # mousse sur la nuque
    for (x, z) in ((4.0, S - 0.6), (6.4, S - 0.8), (9.0, S - 0.8), (11.4, S - 0.6), (S - 0.6, 6.0), (E, 9.0)):
        it.box((x, 11.0, z), (x + 1.6, 13.0, z + 1.2), 'dr_leaf')
    for (x, z) in ((5.2, S - 0.9), (10.0, S - 0.9)):
        it.box((x, 12.0, z), (x + 0.8, 12.8, z + 0.4), 'dr_flower')
    # bois de cerf ramifiés
    for side in (-1, 1):
        x0 = 5.0 if side < 0 else 11.0
        curve(it, x0, side, 9, lambda t: (2.4 * t, 12.4 + 6.4 * t, 8.6 - 1.6 * t, 0.85 - 0.4 * t),
              ('dr_wood', 'dr_antler', 'dr_antler'))
        for (t0, ln, up) in ((0.35, 2.4, 1.2), (0.65, 2.0, 1.6)):
            bx = x0 + side * 2.4 * t0
            by = 12.4 + 6.4 * t0
            for j in range(4):
                u = j / 3
                cx = bx + side * (0.4 + u * ln * 0.3)
                it.box((cx - 0.4, by + u * up * 2, 8.4 - 1.6 * t0 - u * ln - 0.4),
                       (cx + 0.4, by + u * up * 2 + 0.7, 8.4 - 1.6 * t0 - u * ln + 0.4), 'dr_antler')
        it.box((x0 + side * 1.2 - 0.8, 17.0, 6.6), (x0 + side * 1.2 + 0.8, 17.8, 8.0), 'dr_leaf_d')
    return it


def lamerunique():
    it = Item('casque3d_lamerunique', density=4, display=HELMET)
    shell(it, 'lr_steel')
    it.box((4.4, 7.6, S - 0.05), (11.6, 8.2, S), 'lr_glow')                  # fente lumineuse
    it.box((S - 0.4, 7.0, S - 0.6), (E + 0.4, 7.6, S), 'lr_silver')
    it.box((S - 0.4, 8.2, S - 0.6), (E + 0.4, 8.8, S), 'lr_silver')
    it.box((7.4, 3.6, S - 0.6), (8.6, 7.0, S), 'lr_steel_l')                 # mentonnière
    it.box((S - 0.3, 3.4, S - 0.3), (E + 0.3, 4.2, E + 0.3), 'lr_silver')
    it.box((7.4, 9.4, S - 0.4), (8.6, 11.4, S), 'lr_glow')                   # rune du front
    # couronne de pointes
    for i, x in enumerate((S + 0.2, 5.6, 7.2, 8.8, 10.4, E - 1.4)):
        ht = 2.6 if i in (2, 3) else 1.6
        it.box((x, 13.2, S + 0.2), (x + 1.2, 13.2 + ht, S + 1.4), 'lr_silver')
        it.box((x + 0.3, 13.2 + ht, S + 0.5), (x + 0.9, 13.8 + ht, S + 1.1), 'lr_steel_l')
    # cornes courtes vers l'avant
    for side in (-1, 1):
        curve(it, S if side < 0 else E, side, 7,
              lambda t: (0.4 + 1.6 * t, 11 + 2.8 * t, 8 - 4.2 * t, 1.1 - 0.6 * t),
              ('lr_silver', 'lr_steel_l', 'lr_glow'))
    return it


# --- Panoplies multiclasses ---------------------------------------------------------------------------------------
MATS.update({
    'gs_helm': Mat((100, 106, 120), 6, 0.72, pattern=hammered, hi=(176, 184, 200)),
    'gs_gold': Mat((214, 168, 70), 6, 0.74, pattern=filigree, hi=(255, 230, 150)),
    'gs_red': Mat((128, 28, 34), 8, 0.82, pattern=cloth_folds),
    'gs_blue': Mat((36, 56, 124), 8, 0.82, pattern=cloth_folds),
    'sn_hood': Mat((46, 72, 50), 6, 0.84, pattern=cloth_folds),
    'sn_hood_d': Mat((32, 50, 36), 6, 0.84, pattern=cloth_folds),
    'sn_amber': Mat((240, 170, 50), 4, 0.9, light=8, hi=(255, 230, 150)),
    'ar_hood': Mat((50, 34, 80), 6, 0.84, pattern=cloth_folds),
    'ar_hood_d': Mat((34, 24, 56), 6, 0.84, pattern=cloth_folds),
    'ar_rune': Mat((90, 220, 255), 4, 0.95, light=14, hi=(220, 250, 255)),
})


def gardeserment():
    it = Item('casque3d_gardeserment', density=4, display=HELMET)
    shell(it, 'gs_helm')                                                      # heaume à sommet plat
    it.box((4.4, 8.0, S - 0.05), (11.6, 8.8, S), 'slit')                     # fente des yeux
    for x in (5.2, 6.2, 9.4, 10.4):
        for y in (5.0, 6.2):
            it.box((x, y, S - 0.05), (x + 0.5, y + 0.5, S), 'slit')          # trous de respiration
    it.box((S - 0.3, 8.8, S - 0.3), (E + 0.3, 9.6, E + 0.3), 'gs_gold')      # bandeau d'or
    it.box((S - 0.3, 3.4, S - 0.3), (E + 0.3, 4.2, E + 0.3), 'gs_gold')
    it.box((7.4, 3.6, S - 0.6), (8.6, 8.0, S), 'gs_gold')                    # arête du nasal
    it.box((7.4, 9.6, S - 0.6), (8.6, 12.4, S), 'gs_helm')
    # cimier en éventail, bandes rouges et bleues
    for i in range(7):
        z = S + 0.4 + i * 1.2
        ht = 1.2 + 2.6 * math.sin((i + 0.5) / 7 * math.pi)
        it.box((7.4, 13.2, z), (8.6, 13.2 + ht, z + 1.2), 'gs_red' if i % 2 == 0 else 'gs_blue')
    it.box((7.2, 13.0, S + 0.2), (8.8, 13.6, E - 0.2), 'gs_gold')
    for side in (-1, 1):                                                      # rosaces latérales
        x0 = S - 0.5 if side < 0 else E
        it.box((x0, 7.0, 7.0), (x0 + 0.5, 9.0, 9.0), 'gs_gold')
    return it


def sentinelle():
    it = Item('casque3d_sentinelle', density=4, display=HELMET)
    # capuche creuse, rebord de feuilles, couronne de rameaux
    it.box((S, 3.6, E - 0.8), (E, 12.6, E), 'sn_hood')
    it.box((S, 3.6, S), (S + 0.6, 12.6, E - 0.8), 'sn_hood')
    it.box((E - 0.6, 3.6, S), (E, 12.6, E - 0.8), 'sn_hood')
    it.box((S + 0.6, 12.0, S), (E - 0.6, 12.6, E - 0.8), 'sn_hood')
    it.box((S + 0.6, 10.4, S), (E - 0.6, 12.0, S + 0.8), 'sn_hood')
    it.box((S + 0.6, 3.6, S), (5.0, 10.4, S + 0.8), 'sn_hood')
    it.box((11.0, 3.6, S), (E - 0.6, 10.4, S + 0.8), 'sn_hood')
    it.box((S + 0.6, 12.6, S + 0.6), (E - 0.6, 13.4, E - 0.2), 'sn_hood')
    it.box((5.0, 9.8, S + 0.8), (11.0, 10.4, S + 1.0), 'ro_shadow')
    for (x, y) in ((S - 0.2, 11.4), (5.4, 12.0), (7.2, 12.2), (9.0, 12.0), (10.8, 11.4)):
        it.box((x, y, S - 0.5), (x + 1.8, y + 1.4, S + 0.4), 'dr_leaf')     # feuilles du rebord
    for (x, y) in ((S - 0.4, 6.0), (S - 0.4, 8.6)):
        it.box((x, y, S - 0.3), (x + 1.2, y + 1.6, S + 0.6), 'dr_leaf_d')
        it.box((E - 0.8, y, S - 0.3), (E + 0.4, y + 1.6, S + 0.6), 'dr_leaf_d')
    it.box((S - 0.2, 10.6, S - 0.2), (E + 0.2, 11.4, E + 0.2), 'dr_wood')    # bandeau de bois
    it.box((7.3, 10.4, S - 0.5), (8.7, 11.6, S - 0.1), 'sn_amber')
    for side in (-1, 1):                                                     # rameaux
        x0 = 5.6 if side < 0 else 10.4
        curve(it, x0, side, 6, lambda t: (1.6 * t, 13.2 + 3.2 * t, 9.0 + 1.2 * t, 0.45 - 0.15 * t),
              ('dr_wood', 'dr_wood', 'dr_leaf'))
    it.box((2.6, 2.8, 2.6), (13.4, 4.0, 13.4), 'sn_hood_d')
    return it


def arcaniste():
    it = Item('casque3d_arcaniste', density=4, display=HELMET)
    # capuche violette, mentonnière d'acier, cristal runique flottant
    it.box((S, 3.6, E - 0.8), (E, 12.6, E), 'ar_hood')
    it.box((S, 3.6, S), (S + 0.6, 12.6, E - 0.8), 'ar_hood')
    it.box((E - 0.6, 3.6, S), (E, 12.6, E - 0.8), 'ar_hood')
    it.box((S + 0.6, 12.0, S), (E - 0.6, 12.6, E - 0.8), 'ar_hood')
    it.box((S + 0.6, 10.2, S), (E - 0.6, 12.0, S + 0.8), 'ar_hood_d')
    it.box((S + 0.6, 12.6, S + 0.6), (E - 0.6, 13.6, E - 0.4), 'ar_hood')
    for i in range(4):                                                       # pointe de la capuche
        it.box((6.6 + i * 0.3, 13.4 + i * 0.6, 9 + i * 1.0), (9.4 - i * 0.3, 14.2 + i * 0.6, 10.6 + i * 1.0), 'ar_hood_d')
    it.box((S - 0.1, 3.6, S - 0.4), (E + 0.1, 7.0, S + 0.6), 'lr_steel_l')   # mentonnière
    it.box((S - 0.1, 6.8, S - 0.5), (E + 0.1, 7.4, S + 0.6), 'lr_silver')
    for x in (5.0, 6.6, 9.0, 10.6):
        it.box((x, 4.4, S - 0.5), (x + 0.4, 6.2, S - 0.4), 'ar_rune')
    for side in (-1, 1):                                                     # plaques de tempe
        x0 = S - 0.5 if side < 0 else E
        it.box((x0, 6.6, 5.0), (x0 + 0.5, 11.0, 9.0), 'lr_steel_l')
        it.box((x0 - 0.05 * side, 8.2, 6.4), (x0 + 0.5 + 0.05 * side, 9.4, 7.6), 'ar_rune')
    # cristal en losange au-dessus du front (empilement de pavés)
    for i, w in enumerate((0.3, 0.6, 0.9, 0.6, 0.3)):
        it.box((8 - w, 14.4 + i * 0.6, S - 1.0 - w * 0.5), (8 + w, 15.0 + i * 0.6, S - 1.0 + w * 0.5), 'ar_rune')
    return it


CASQUES = {'guerrier': guerrier, 'paladin': paladin, 'mage': mage, 'rodeur': rodeur,
           'druide': druide, 'lamerunique': lamerunique,
           'gardeserment': gardeserment, 'sentinelle': sentinelle, 'arcaniste': arcaniste}


VARIANTS = 4


def variants(key):
    """Les 4 silhouettes de la classe : 1 calotte simple, 2 casque historique, 3 et 4 formes de casques_paliers."""
    from casques_paliers import PALIERS
    return [PALIERS[(key, 'commun')], CASQUES[key], PALIERS[(key, 'epique')], PALIERS[(key, 'legendaire')]]


def build(pack_oraxen, preview_dir=None):
    """Écrit evo:item/casque3d_<classe>_<palier>_<variante> pour chaque palier et chaque variante, repointe
    oraxen:<classe>_<palier>_<variante>_helmet dessus, et oraxen:<classe>_helmet (pièces historiques) sur rare 2."""
    import json
    import raretes
    tiles = {}
    for tier in raretes.TIERS:
        with raretes.palier(tier):
            for key in CASQUES:
                for v, fn in enumerate(variants(key), 1):
                    name = f'{key}_{tier}_{v}'
                    it = fn()
                    it.id = f'casque3d_{name}'
                    raretes.aura(it, tier)
                    it.save()
                    prev = fn()                  # aperçu : le casque posé sur une tête
                    raretes.aura(prev, tier)
                    prev.box((4, 4, 4), (12, 12, 12), 'skin')
                    prev.box((5, 7, 3.98), (6.6, 8, 4), 'slit')
                    prev.box((9.4, 7, 3.98), (11, 8, 4), 'slit')
                    pimg, pels = prev.build()
                    d = {'gui': {'rotation': [15, 160, 0], 'translation': [0, -2, 0], 'scale': [0.5] * 3}}
                    tiles[name] = render(pimg, pels, d, 200)
                    with open(os.path.join(pack_oraxen, 'items', f'{name}_helmet.json'), 'w') as f:
                        json.dump({'model': {'type': 'minecraft:model', 'model': f'evo:item/casque3d_{name}'}}, f,
                                  separators=(',', ':'))
    for key in CASQUES:
        with open(os.path.join(pack_oraxen, 'items', f'{key}_helmet.json'), 'w') as f:
            json.dump({'model': {'type': 'minecraft:model', 'model': f'evo:item/casque3d_{key}_rare_2'}}, f,
                      separators=(',', ':'))
    # une planche par classe : lignes = paliers, colonnes = variantes
    out = preview_dir or HERE
    for key in CASQUES:
        sheet = Image.new('RGBA', (VARIANTS * 200 + 110, len(raretes.TIERS) * 200), (56, 58, 66, 255))
        d = ImageDraw.Draw(sheet)
        for r, tier in enumerate(raretes.TIERS):
            d.text((8, r * 200 + 95), tier, fill=(230, 230, 230, 255))
            for v in range(VARIANTS):
                sheet.alpha_composite(tiles[f'{key}_{tier}_{v + 1}'], (110 + v * 200, r * 200))
        sheet.save(os.path.join(out, f'casques_{key}.png'))
    return tiles

if __name__ == '__main__':
    build(os.path.join(HERE, '..', '..', 'pack', 'assets', 'oraxen'))
