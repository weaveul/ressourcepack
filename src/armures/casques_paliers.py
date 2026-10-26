"""Casques par palier de rareté : une silhouette propre à chaque classe et à chaque palier.

Le palier rare garde le casque de casques3d.py. Commun : forme simple et usée (calotte, capuche, bandeau).
Épique : forme plus travaillée (cimier, cornes, masque). Légendaire : silhouette spectaculaire (crâne de dragon,
ailes, halo, tête de loup, crâne de cerf...). Même repère que casques3d : tête 4..12, avant côté z bas.
"""
import math

from kit import Item, Mat, MATS
from casques3d import (HELMET, S, E, shell, curve, hammered, brushed, filigree, cloth_folds, leather, fur,
                       feathers, bark_grain, leaves, horn_rings, starry)

MATS.update({
    'cp_chain': Mat((128, 132, 142), 6, 0.85),
    'cp_rust': Mat((112, 96, 84), 10, 0.75, pattern=hammered),
    'cp_iron': Mat((120, 124, 134), 8, 0.72, pattern=hammered, hi=(180, 184, 194)),
    'cp_strap': Mat((86, 56, 34), 6, 0.78, pattern=leather),
    'cp_cloth': Mat((120, 104, 86), 8, 0.86, pattern=cloth_folds),
    'cp_bone': Mat((226, 214, 186), 6, 0.8, grad=-0.2, pattern=horn_rings),
    'cp_bone_d': Mat((170, 154, 124), 6, 0.8),
    'cp_teeth': Mat((240, 236, 220), 3, 0.85),
    'cp_eye_red': Mat((255, 70, 40), 4, 0.95, light=15, hi=(255, 200, 150)),
    'cp_eye_amber': Mat((255, 180, 40), 4, 0.95, light=14, hi=(255, 240, 160)),
    'cp_eye_green': Mat((120, 255, 120), 4, 0.95, light=14),
    'cp_eye_violet': Mat((200, 120, 255), 4, 0.95, light=15),
    'cp_halo': Mat((255, 230, 140), 4, 0.95, light=15, hi=(255, 255, 220)),
    'cp_wolf': Mat((120, 116, 110), 14, 0.9, pattern=fur),
    'cp_wolf_d': Mat((80, 76, 72), 14, 0.9, pattern=fur),
    'cp_wolf_l': Mat((190, 184, 172), 12, 0.9, pattern=fur),
    'cp_owl': Mat((150, 118, 80), 8, 0.86, pattern=feathers),
    'cp_owl_l': Mat((222, 206, 172), 8, 0.86, pattern=feathers),
    'cp_beak': Mat((90, 80, 70), 4, 0.8),
    'cp_plume_red': Mat((170, 34, 34), 8, 0.84, pattern=feathers),
    'cp_plume_blue': Mat((40, 70, 160), 8, 0.84, pattern=feathers),
    'cp_plume_white': Mat((236, 234, 226), 6, 0.86, pattern=feathers),
    'cp_mane': Mat((210, 150, 60), 14, 0.88, pattern=fur),
    'cp_crystal': Mat((120, 220, 255), 6, 0.9, light=13, hi=(230, 250, 255)),
    'cp_crystal_v': Mat((190, 120, 255), 6, 0.9, light=13, hi=(240, 220, 255)),
    'cp_void': Mat((24, 18, 36), 4, 0.95),
    'cp_bark': Mat((92, 66, 42), 6, 0.78, pattern=bark_grain),
    'cp_moss': Mat((90, 130, 60), 12, 0.85, pattern=fur),
    'cp_leaf_gold': Mat((220, 180, 60), 8, 0.84, light=4, pattern=leaves),
})


def it_for(name):
    return Item('casque3d_' + name, density=4, display=HELMET)


def dome(it, mat, y0=7.6, top=12.4, steps=3):
    """Calotte arrondie : coque jusqu'en y0, puis paliers qui rétrécissent."""
    it.box((S, y0, S), (E, top, E), mat)
    for i in range(1, steps + 1):
        d = 0.7 * i
        it.box((S + d, top + (i - 1) * 0.5, S + d), (E - d, top + i * 0.5, E - d), mat)


def band(it, y0, y1, mat, out=0.3):
    it.box((S - out, y0, S - out), (E + out, y1, E + out), mat)


def hood(it, mat, mat_d, rim=None, top=12.6):
    """Capuche creuse, visage ouvert (même découpe que le rôdeur)."""
    it.box((S, 3.6, E - 0.8), (E, top, E), mat)
    it.box((S, 3.6, S), (S + 0.6, top, E - 0.8), mat)
    it.box((E - 0.6, 3.6, S), (E, top, E - 0.8), mat)
    it.box((S + 0.6, top - 0.6, S), (E - 0.6, top, E - 0.8), mat)
    it.box((S + 0.6, 10.4, S), (E - 0.6, top - 0.6, S + 0.8), rim or mat)
    it.box((S + 0.6, 3.6, S), (5.0, 10.4, S + 0.8), rim or mat)
    it.box((11.0, 3.6, S), (E - 0.6, 10.4, S + 0.8), rim or mat)
    it.box((S + 0.6, top, S + 0.6), (E - 0.6, top + 0.8, E - 0.2), mat)
    it.box((5.0, 9.8, S + 0.8), (11.0, 10.4, S + 1.0), 'ro_shadow')
    it.box((2.6, 2.8, 2.6), (13.4, 4.0, 13.4), mat_d)


def halo(it, y, r, mat, z=8.6, t=0.45):
    """Anneau flottant (carré à coins coupés) au-dessus ou derrière la tête."""
    c = 8
    it.box((c - r + 0.8, y, z - r), (c + r - 0.8, y + t, z - r + t), mat)
    it.box((c - r + 0.8, y, z + r - t), (c + r - 0.8, y + t, z + r), mat)
    it.box((c - r, y, z - r + 0.8), (c - r + t, y + t, z + r - 0.8), mat)
    it.box((c + r - t, y, z - r + 0.8), (c + r, y + t, z + r - 0.8), mat)
    for sx in (-1, 1):
        for sz in (-1, 1):
            x0 = c + sx * (r - 0.8)
            z0 = z + sz * (r - 0.8)
            it.box((min(x0, x0 + sx * 0.6), y, min(z0, z0 + sz * 0.6)),
                   (max(x0, x0 + sx * 0.6), y + t, max(z0, z0 + sz * 0.6)), mat)


def halo_v(it, cy, r, mat, z=13.6, t=0.45, n=16):
    """Halo vertical derrière la tête (anneau de pavés dans le plan x-y)."""
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = 8 + r * math.cos(a), cy + r * math.sin(a)
        it.box((x - 0.45, y - 0.45, z), (x + 0.45, y + 0.45, z + t), mat)


def spikes(it, xs, y, z0, z1, h, mat, tip=None):
    for i, x in enumerate(xs):
        hh = h[i] if isinstance(h, (list, tuple)) else h
        it.box((x, y, z0), (x + 1.0, y + hh, z1), mat)
        if tip:
            it.box((x + 0.25, y + hh, z0 + 0.2), (x + 0.75, y + hh + 0.6, z1 - 0.2), tip)


def eyes(it, mat, y=7.6, z=S - 0.06, w=2.0, gap=1.8):
    for x0 in (8 - gap / 2 - w, 8 + gap / 2):
        it.box((x0, y, z), (x0 + w, y + 0.8, z + 0.06), mat)


# ==================================================================================================================
#  Guerrier
# ==================================================================================================================

def guerrier_commun():
    it = it_for('guerrier_commun')
    dome(it, 'cp_rust', 8.0)                                         # calotte à nasal
    band(it, 7.6, 8.6, 'cp_strap', 0.2)
    it.box((7.4, 4.8, S - 0.5), (8.6, 8.6, S), 'cp_rust')            # nasal
    for side in (-1, 1):                                             # mentonnière de cuir
        x0 = S - 0.3 if side < 0 else E
        it.box((x0, 4.0, 6.0), (x0 + 0.3, 7.6, 7.2), 'cp_strap')
    it.box((S, 3.6, 10.8), (E, 8.0, E), 'cp_chain')                  # maille sur la nuque
    for x in (S + 0.4, E - 1.0):
        it.box((x, 10.4, S - 0.2), (x + 0.6, 11.0, S), 'cp_iron')
    return it


def guerrier_epique():
    it = it_for('guerrier_epique')
    shell(it, 'gu_steel')
    it.box((S, 3.4, S - 0.8), (E, 7.4, S), 'gu_steel_l')             # mâchoire saillante
    for x in (4.4, 5.6, 6.8, 8.6, 9.8, 11.0):
        it.box((x, 4.4, S - 0.86), (x + 0.5, 6.6, S - 0.8), 'slit')
    eyes(it, 'slit', 8.0, S - 0.06, 2.4, 1.0)
    it.box((S - 0.4, 7.4, S - 0.4), (E + 0.4, 8.0, S + 0.4), 'gu_bronze')
    # crête de pointes de l'avant vers l'arrière
    for i in range(6):
        z = S + 0.6 + i * 1.4
        ht = 3.2 - abs(i - 2) * 0.5
        it.box((7.4, 12.6, z), (8.6, 12.6 + ht, z + 1.0), 'gu_bronze')
        it.box((7.7, 12.6 + ht, z + 0.2), (8.3, 13.2 + ht, z + 0.8), 'gu_steel_l')
    # cornes de bélier enroulées
    for side in (-1, 1):
        x0 = S if side < 0 else E
        n = 14
        for i in range(n):
            t = i / (n - 1)
            a = t * math.pi * 1.6
            dx = 1.2 + 2.4 * math.sin(a) + t * 0.6
            y = 10.2 + 2.6 * (1 - math.cos(a)) - t * 3.2
            z = 9.0 - 2.6 * math.sin(a * 0.9)
            w = 1.3 - t * 0.7
            cx = x0 + side * dx
            it.box((cx - w, y - w, z - w), (cx + w, y + w, z + w), 'gu_horn' if i < n - 2 else 'gu_horn_tip')
    return it


def guerrier_legendaire():
    it = it_for('guerrier_legendaire')
    # crâne de dragon : museau qui avance au-dessus du visage, mâchoire en bas, cornes et collerette
    shell(it, 'gu_steel', 6.8, 12.4)
    it.box((S - 0.2, 10.2, S - 2.6), (E + 0.2, 12.2, S), 'gu_steel')          # museau
    it.box((S + 0.8, 12.2, S - 2.2), (E - 0.8, 12.8, S + 1.0), 'gu_steel_l')
    it.box((S + 0.6, 9.6, S - 2.6), (E - 0.6, 10.2, S - 2.0), 'cp_teeth')      # dents du haut
    for x in (S + 1.0, 5.6, 7.2, 8.8, 10.4, E - 1.6):
        it.box((x, 9.0, S - 2.5), (x + 0.6, 9.6, S - 2.1), 'cp_teeth')
    it.box((S - 0.2, 3.4, S - 1.8), (E + 0.2, 4.8, S + 1.0), 'gu_steel')       # mâchoire
    for x in (S + 1.0, 6.0, 9.4, E - 1.6):
        it.box((x, 4.8, S - 1.7), (x + 0.6, 5.6, S - 1.3), 'cp_teeth')
    it.box((S - 0.2, 4.8, S + 0.4), (S + 0.6, 10.2, E), 'gu_steel_l')          # joues
    it.box((E - 0.6, 4.8, S + 0.4), (E + 0.2, 10.2, E), 'gu_steel_l')
    for x0 in (4.6, 9.6):                                                       # yeux ardents
        it.box((x0, 10.6, S - 2.66), (x0 + 1.8, 11.4, S - 2.6), 'cp_eye_red')
    it.box((5.2, 7.2, S - 0.06), (10.8, 8.2, S), 'slit')
    # collerette d'écailles et crinière rouge
    for i in range(7):
        x = S + i * 1.32
        it.box((x, 12.4, E - 0.2), (x + 1.2, 13.6 + (1.4 if i % 2 else 0.6), E + 1.2), 'gu_bronze')
    for i in range(6):
        z = 7 + i * 1.2
        it.box((7.3, 12.8 - i * 0.4, z), (8.7, 15.4 - i * 0.7, z + 1.3), 'gu_red')
    # grandes cornes en arrière
    for side in (-1, 1):
        curve(it, S if side < 0 else E, side, 14,
              lambda t: (0.6 + 2.2 * t, 11.4 + 5.4 * math.sin(t * math.pi * 0.55), 7.4 + 7.4 * t, 1.5 - 1.0 * t),
              ('gu_bronze', 'cp_bone', 'gu_horn_tip'))
    return it


# ==================================================================================================================
#  Paladin
# ==================================================================================================================

def paladin_commun():
    it = it_for('paladin_commun')
    # bassinet ouvert sur une coiffe de mailles
    it.box((S, 3.0, 10.4), (E, 10.4, E), 'cp_chain')
    it.box((S, 3.0, S), (S + 0.6, 10.4, 10.4), 'cp_chain')
    it.box((E - 0.6, 3.0, S), (E, 10.4, 10.4), 'cp_chain')
    it.box((S + 0.6, 3.0, S), (E - 0.6, 5.0, S + 0.6), 'cp_chain')            # camail sous le menton
    dome(it, 'cp_iron', 10.0, 12.4, 4)
    band(it, 10.0, 10.6, 'cp_strap', 0.2)
    it.box((7.6, 10.6, S - 0.3), (8.4, 12.0, S), 'pa_gold')                    # petite croix
    it.box((7.0, 11.0, S - 0.3), (9.0, 11.6, S), 'pa_gold')
    return it


def paladin_epique():
    it = it_for('paladin_epique')
    # salade à visière, crête en soleil derrière la tête
    shell(it, 'pa_silver', 3.6, 12.0)
    it.box((S - 0.2, 7.0, S - 0.8), (E + 0.2, 10.4, S), 'pa_silver')           # visière bombée
    it.box((4.4, 8.4, S - 0.86), (11.6, 9.0, S - 0.8), 'slit')
    it.box((S - 0.2, 10.4, S - 0.8), (E + 0.2, 11.0, S), 'pa_gold')
    for x in (5.0, 6.6, 9.0, 10.6):
        it.box((x, 7.4, S - 0.86), (x + 0.6, 8.0, S - 0.8), 'slit')
    it.box((S + 0.6, 12.0, S + 0.6), (E - 0.6, 12.8, E + 1.4), 'pa_silver')   # queue de la salade
    it.box((S + 0.2, 6.0, E), (E - 0.2, 12.0, E + 1.6), 'pa_silver')
    # soleil : rayons dorés en éventail
    for i in range(9):
        a = math.pi * (0.1 + 0.8 * i / 8)
        ln = 5.4 if i % 2 == 0 else 3.6
        for k in range(4):
            r = 2.0 + k * ln / 4
            x, y = 8 + r * math.cos(a), 12.6 + r * math.sin(a)
            it.box((x - 0.4, y - 0.4, 12.2), (x + 0.4, y + 0.4, 12.8), 'pa_gold' if k < 3 else 'pa_holy')
    it.box((7.3, 13.0, 11.8), (8.7, 14.4, 12.9), 'pa_holy')
    return it


def paladin_legendaire():
    it = it_for('paladin_legendaire')
    shell(it, 'pa_silver')
    it.box((4.4, 7.8, S - 0.05), (11.6, 8.6, S), 'slit')
    it.box((7.6, 4.6, S - 0.05), (8.4, 7.8, S), 'slit')
    band(it, 3.4, 4.2, 'pa_gold')
    # couronne
    band(it, 12.0, 13.0, 'pa_gold', 0.4)
    for i, x in enumerate((S - 0.2, 5.4, 7.4, 9.4, E - 1.2)):
        ht = 2.2 if i == 2 else 1.4
        it.box((x, 13.0, S - 0.4), (x + 1.2, 13.0 + ht, S + 0.4), 'pa_gold')
        it.box((x + 0.3, 13.0 + ht, S - 0.3), (x + 0.9, 13.6 + ht, S + 0.3), 'pa_holy')
    # grandes ailes d'ange vers l'arrière et le haut
    for side in (-1, 1):
        x0 = S if side < 0 else E
        for j in range(7):
            y = 8.0 + j * 1.4
            ln = 4.0 + j * 0.9
            x1 = x0 + side * (0.4 + j * 0.45)
            a, b = sorted((x1, x1 + side * 0.9))
            it.box((a, y, 7.4 + j * 0.3), (b, y + 1.3, 7.4 + j * 0.3 + ln), 'pa_white' if j < 6 else 'pa_gold')
    halo(it, 17.2, 3.4, 'cp_halo')                                             # halo flottant
    return it


# ==================================================================================================================
#  Mage
# ==================================================================================================================

def mage_commun():
    it = it_for('mage_commun')
    hood(it, 'cp_cloth', 'cp_cloth')
    for i in range(4):                                                         # pointe molle qui retombe
        it.box((6.8 + i * 0.2, 13.0 + i * 0.5, 9 + i * 1.1), (9.2 - i * 0.2, 13.8 + i * 0.4, 10.8 + i * 1.1), 'cp_cloth')
    it.box((S - 0.1, 10.6, S - 0.1), (E + 0.1, 11.2, S + 0.9), 'cp_strap')
    return it


def mage_epique():
    it = it_for('mage_epique')
    # chapeau tordu à bord immense, plume et orbes en orbite
    it.box((-0.6, 11.0, 0.0), (16.6, 11.8, 16.0), 'ma_cloth_d')
    it.box((S, 10.8, S), (E, 12.6, E), 'ma_cloth')
    band(it, 12.0, 13.2, 'ma_gold', 0.2)
    n = 14
    for i in range(n):
        t = i / (n - 1)
        w = 4.4 * (1 - t) ** 1.1 + 0.4
        cx = 8 + 3.0 * math.sin(t * 2.6)
        cz = 8 + 3.8 * t
        y = 13.2 + i * 0.95
        it.box((cx - w, y, cz - w), (cx + w, y + 1.05, cz + w), 'ma_cloth')
    for i in range(6):                                                         # plume sur le côté
        it.box((E + 0.2, 12.4 + i * 1.0, 7.0 + i * 0.6), (E + 0.8, 13.4 + i * 1.0, 9.0 + i * 0.5), 'cp_plume_white')
    for (x, y, z) in ((1.6, 13.0, 3.0), (14.0, 14.4, 6.0), (2.4, 15.2, 12.6)):
        it.box((x - 0.6, y - 0.6, z - 0.6), (x + 0.6, y + 0.6, z + 0.6), 'ma_gem')
    it.box((7.2, 12.2, S - 0.6), (8.8, 13.4, S - 0.2), 'ma_star')
    return it


def mage_legendaire():
    it = it_for('mage_legendaire')
    # couronne arcanique : voile, diadème d'or, flèche de cristaux flottants, œil central
    hood(it, 'ma_cloth', 'ma_cloth_d', rim='ma_gold')
    band(it, 11.0, 12.0, 'ma_gold', 0.4)
    for i, x in enumerate((S + 0.2, 5.8, 9.2, E - 1.4)):
        it.box((x, 12.0, S - 0.3), (x + 1.2, 14.0 + (0.8 if i in (1, 2) else 0), S + 0.5), 'ma_gold')
    it.box((7.1, 11.2, S - 0.9), (8.9, 13.0, S - 0.3), 'ma_gem')               # œil
    for k in range(6):                                                         # flèche de cristaux
        w = 1.0 - k * 0.12
        y = 14.6 + k * 1.6
        it.box((8 - w, y, 8 - w), (8 + w, y + 1.2, 8 + w), 'cp_crystal' if k % 2 == 0 else 'ma_gem')
    for i in range(6):                                                         # orbite de petits cristaux
        a = 2 * math.pi * i / 6
        x, z = 8 + 6.0 * math.cos(a), 8 + 6.0 * math.sin(a)
        it.box((x - 0.5, 14.0 + (i % 2) * 0.8, z - 0.5), (x + 0.5, 15.0 + (i % 2) * 0.8, z + 0.5), 'ma_star')
    return it


# ==================================================================================================================
#  Rôdeur
# ==================================================================================================================

def rodeur_commun():
    it = it_for('rodeur_commun')
    dome(it, 'ro_leather', 9.0, 12.4, 3)                                       # bonnet de cuir
    it.box((S, 6.0, 10.6), (E, 9.0, E), 'ro_leather')
    it.box((S, 7.0, S + 0.6), (S + 0.6, 9.0, 10.6), 'ro_leather')
    it.box((E - 0.6, 7.0, S + 0.6), (E, 9.0, 10.6), 'ro_leather')
    band(it, 9.0, 9.8, 'cp_strap', 0.2)
    return it


def rodeur_epique():
    it = it_for('rodeur_epique')
    hood(it, 'ro_cloth', 'ro_cloth_d')
    it.box((S + 0.4, 3.6, S - 0.4), (E - 0.4, 7.6, S + 0.4), 'ro_cloth_d')     # masque de tissu
    it.box((S + 0.4, 7.4, S - 0.45), (E - 0.4, 7.7, S - 0.35), 'ro_leather')
    it.box((1.8, 2.6, 2.0), (14.2, 4.6, 14.0), 'ro_fur')                       # col de fourrure
    for side in (-1, 1):                                                       # oreilles de loup sur la capuche
        x0 = 5.0 if side < 0 else 9.8
        it.box((x0, 13.2, 7.6), (x0 + 1.2, 15.0, 8.8), 'cp_wolf')
        it.box((x0 + 0.3, 15.0, 7.9), (x0 + 0.9, 15.8, 8.5), 'cp_wolf_d')
    for i in range(3):                                                         # deux plumes croisées
        it.box((E + 0.2, 10.4 + i * 1.0, 9.0 + i * 0.6), (E + 0.8, 11.4 + i * 1.0, 10.8 + i * 0.5), 'ro_feather')
        it.box((E + 0.3, 10.0 + i * 1.1, 10.6 + i * 0.8), (E + 0.9, 11.0 + i * 1.1, 12.0 + i * 0.7), 'cp_owl_l')
    return it


def rodeur_legendaire():
    it = it_for('rodeur_legendaire')
    # dépouille de grand loup : tête au-dessus du front, peau qui tombe dans le dos
    it.box((S - 0.2, 9.8, S - 0.2), (E + 0.2, 13.6, E + 0.2), 'cp_wolf')       # crâne du loup
    it.box((S - 0.2, 3.6, 10.0), (E + 0.2, 9.8, E + 0.2), 'cp_wolf')
    it.box((S - 0.2, 4.6, S + 0.6), (S + 0.6, 9.8, 10.0), 'cp_wolf_d')
    it.box((E - 0.6, 4.6, S + 0.6), (E + 0.2, 9.8, 10.0), 'cp_wolf_d')
    it.box((5.2, 10.4, S - 3.4), (10.8, 13.2, S), 'cp_wolf')                   # museau
    it.box((5.8, 10.0, S - 3.4), (10.2, 10.6, S - 0.4), 'cp_wolf_l')
    it.box((7.0, 12.4, S - 3.8), (9.0, 13.4, S - 3.2), 'ro_shadow')            # truffe
    for x in (5.6, 6.8, 8.6, 9.8):
        it.box((x, 9.4, S - 3.2), (x + 0.5, 10.0, S - 2.8), 'cp_teeth')        # crocs
    for x0 in (4.4, 10.0):
        it.box((x0, 12.0, S - 0.06), (x0 + 1.6, 12.8, S), 'cp_eye_amber')      # yeux
    for side in (-1, 1):                                                       # oreilles
        x0 = 4.0 if side < 0 else 10.6
        it.box((x0, 13.6, 6.4), (x0 + 1.4, 15.8, 7.8), 'cp_wolf')
        it.box((x0 + 0.3, 15.8, 6.7), (x0 + 1.1, 16.6, 7.5), 'cp_wolf_d')
    for i in range(5):                                                         # peau dans le dos
        it.box((S + 0.4 + i * 0.1, 2.6 - i * 0.6, E + 0.2 + i * 0.3), (E - 0.4 - i * 0.1, 3.8 - i * 0.6, E + 1.2 + i * 0.3), 'cp_wolf')
    for side in (-1, 1):                                                       # pattes sur les épaules
        x0 = 1.6 if side < 0 else 12.0
        it.box((x0, 2.8, 4.0), (x0 + 2.4, 4.0, 9.0), 'cp_wolf_l')
    return it


# ==================================================================================================================
#  Druide
# ==================================================================================================================

def druide_commun():
    it = it_for('druide_commun')
    band(it, 10.6, 11.6, 'cp_bark', 0.2)                                       # bandeau de liane
    for (x, z) in ((S - 0.6, 6.0), (5.0, S - 0.6), (9.6, S - 0.6), (E, 9.0)):
        it.box((x, 11.0, z), (x + 1.4, 12.6, z + 1.0), 'dr_leaf')
    it.box((S + 0.4, 12.0, S + 0.4), (E - 0.4, 12.4, E - 0.4), 'cp_moss')
    return it


def druide_epique():
    it = it_for('druide_epique')
    # couronne d'arbre : tronc tressé, branches qui montent, feuillage, fleurs, masque de mousse
    band(it, 10.0, 12.2, 'dr_wood', 0.3)
    it.box((S, 6.0, 10.6), (E, 10.0, E), 'dr_moss')
    it.box((S + 0.2, 6.8, S - 0.5), (E - 0.2, 7.4, S - 0.2), 'dr_wood')        # arcade de bois sur les yeux
    for side in (-1, 1):
        for k, (x0, z0, lean) in enumerate(((5.0, 6.0, 1.0), (6.8, 10.0, 0.4))):
            x = x0 if side < 0 else 16 - x0 - 1.0
            for i in range(6):
                it.box((x + side * i * 0.45 * lean, 12.2 + i * 1.0, z0 - i * 0.2),
                       (x + 1.0 + side * i * 0.45 * lean, 13.2 + i * 1.0, z0 + 1.0 - i * 0.2), 'dr_wood')
    for (x, y, z, w) in ((3.0, 17.0, 5.0, 1.8), (11.0, 17.4, 5.2, 1.8), (5.4, 18.0, 9.0, 1.6), (10.0, 18.2, 9.4, 1.6),
                         (8.0, 18.8, 7.0, 2.0)):
        it.box((x - w, y - w * 0.6, z - w), (x + w, y + w * 0.6, z + w), 'dr_leaf' if x < 8 else 'dr_leaf_d')
    for (x, y, z) in ((2.4, 16.8, 3.6), (12.6, 17.0, 3.8), (8.0, 19.6, 6.0), (S - 0.4, 11.6, 6.0)):
        it.box((x - 0.4, y - 0.4, z - 0.4), (x + 0.4, y + 0.4, z + 0.4), 'dr_flower')
    return it


def druide_legendaire():
    it = it_for('druide_legendaire')
    # crâne de cerf en masque, bois immenses et lumineux, feuilles d'or flottantes
    it.box((S + 0.4, 8.0, S - 1.6), (E - 0.4, 12.4, S + 0.4), 'cp_bone')       # front du crâne
    it.box((5.8, 4.6, S - 2.6), (10.2, 8.4, S - 0.4), 'cp_bone')               # museau
    it.box((6.4, 4.2, S - 2.7), (9.6, 4.8, S - 1.0), 'cp_bone_d')
    for x0 in (4.6, 9.8):
        it.box((x0, 8.8, S - 1.66), (x0 + 1.6, 10.0, S - 1.6), 'cp_eye_green')
    it.box((S, 7.0, S + 0.4), (E, 12.4, E), 'dr_moss')
    for side in (-1, 1):
        x0 = 5.0 if side < 0 else 11.0
        curve(it, x0, side, 12, lambda t: (4.0 * t, 12.4 + 8.6 * t, 7.6 - 1.4 * t, 0.9 - 0.45 * t),
              ('cp_bone', 'dr_antler', 'cp_eye_green'))
        for (t0, ln, up) in ((0.25, 2.6, 1.0), (0.5, 2.8, 1.6), (0.75, 2.2, 1.8)):
            bx, by = x0 + side * 4.0 * t0, 12.4 + 8.6 * t0
            for j in range(4):
                u = j / 3
                cx = bx + side * (0.4 + u * ln * 0.5)
                it.box((cx - 0.35, by + u * up * 2, 7.6 - 1.4 * t0 - u * ln - 0.35),
                       (cx + 0.35, by + u * up * 2 + 0.7, 7.6 - 1.4 * t0 - u * ln + 0.35),
                       'cp_eye_green' if j == 3 else 'dr_antler')
    for (x, y, z) in ((1.0, 15.0, 10.0), (15.0, 16.0, 9.0), (3.0, 20.0, 6.0), (13.0, 21.0, 7.0), (8.0, 15.4, 13.4)):
        it.box((x - 0.7, y - 0.3, z - 0.7), (x + 0.7, y + 0.3, z + 0.7), 'cp_leaf_gold')
    return it


# ==================================================================================================================
#  Lame-runique
# ==================================================================================================================

def lamerunique_commun():
    it = it_for('lamerunique_commun')
    dome(it, 'lr_steel_l', 7.0, 12.4, 3)
    it.box((4.6, 7.6, S - 0.05), (11.4, 8.2, S), 'slit')
    it.box((S, 3.6, 10.4), (E, 7.0, E), 'lr_steel_l')
    it.box((7.6, 9.6, S - 0.3), (8.4, 11.0, S), 'lr_silver')                   # rune éteinte
    band(it, 7.0, 7.6, 'lr_silver', 0.2)
    return it


def lamerunique_epique():
    it = it_for('lamerunique_epique')
    # heaume en pointe, visière en bec, longue lame dorsale, runes
    shell(it, 'lr_steel', 3.6, 11.6, top=False)
    for i in range(5):                                                         # sommet pointu
        d = 0.8 * i
        it.box((S + d, 11.6 + i * 0.9, S + d), (E - d, 12.5 + i * 0.9, E - d), 'lr_steel')
    for i in range(4):                                                         # visière en bec
        it.box((S + 0.6 + i * 0.6, 5.0 + i * 0.3, S - 0.6 - (3 - i) * 0.5), (E - 0.6 - i * 0.6, 7.6 - i * 0.2, S), 'lr_steel_l')
    eyes(it, 'lr_glow', 8.0, S - 0.06, 2.2, 1.6)
    for i in range(9):                                                         # lame dorsale
        z = 9.0 + i * 0.7
        it.box((7.6, 15.0 - i * 1.0, z), (8.4, 16.4 - i * 0.9, z + 0.8), 'lr_silver')
    for (y, z) in ((10.0, S - 0.06), (9.0, S - 0.06)):
        pass
    for side in (-1, 1):
        x0 = S - 0.06 if side < 0 else E
        for y in (6.0, 8.0, 10.0):
            it.box((x0, y, 6.6), (x0 + 0.06, y + 0.8, 8.4), 'lr_glow')
    return it


def lamerunique_legendaire():
    it = it_for('lamerunique_legendaire')
    # chevalier démoniaque : cornes avant énormes, masque de crocs, halo d'éclats runiques
    shell(it, 'lr_steel')
    it.box((S - 0.2, 3.4, S - 1.0), (E + 0.2, 7.0, S), 'lr_steel_l')
    for x in (4.4, 5.6, 6.8, 8.6, 9.8, 11.0):
        it.box((x, 3.4, S - 1.1), (x + 0.6, 4.6 + (0.6 if x in (5.6, 9.8) else 0), S - 0.9), 'cp_teeth')
    eyes(it, 'cp_eye_violet', 7.6, S - 0.06, 2.2, 1.4)
    it.box((7.2, 9.2, S - 0.6), (8.8, 11.6, S), 'lr_glow')
    for side in (-1, 1):
        curve(it, S if side < 0 else E, side, 12,
              lambda t: (0.6 + 3.4 * math.sin(t * math.pi * 0.6), 10.0 + 5.0 * t, 8.0 - 8.0 * t ** 1.3, 1.6 - 1.1 * t),
              ('lr_silver', 'lr_steel_l', 'lr_glow'))
    halo_v(it, 14.0, 5.6, 'lr_glow', z=13.4, n=14)
    for i in range(5):                                                         # éclats flottants
        a = math.pi * (0.15 + 0.7 * i / 4)
        x, y = 8 + 7.2 * math.cos(a), 14.0 + 7.2 * math.sin(a)
        it.box((x - 0.4, y - 0.9, 13.0), (x + 0.4, y + 0.9, 13.8), 'lr_silver')
    return it


# ==================================================================================================================
#  Multiclasses
# ==================================================================================================================

def gardeserment_commun():
    it = it_for('gardeserment_commun')
    # chapel de fer : calotte et large bord
    dome(it, 'cp_iron', 9.4, 12.4, 3)
    it.box((1.6, 9.4, 1.6), (14.4, 10.0, 14.4), 'cp_iron')
    it.box((S, 3.6, 10.8), (E, 9.4, E), 'cp_chain')
    band(it, 10.0, 10.6, 'cp_strap', 0.1)
    return it


def gardeserment_epique():
    it = it_for('gardeserment_epique')
    # heaume à bouche de grenouille et grand panache
    shell(it, 'gs_helm', 3.6, 12.4)
    for i in range(4):
        it.box((S - 0.2 - i * 0.1, 8.6 + i * 0.4, S - 0.6 - i * 0.6), (E + 0.2 + i * 0.1, 9.0 + i * 0.4, S - i * 0.6), 'gs_helm')
    it.box((S - 0.4, 8.0, S - 2.6), (E + 0.4, 8.6, S - 2.0), 'slit')          # fente sous le rebord
    it.box((S - 0.4, 3.4, S - 1.2), (E + 0.4, 8.0, S), 'gs_helm')              # bavière
    band(it, 3.4, 4.0, 'gs_gold')
    for i in range(8):                                                         # panache
        t = i / 7
        it.box((7.0 - t, 13.0 + 4.0 * math.sin(t * 2.0), 8.0 + 5.0 * t), (9.0 + t, 14.6 + 4.0 * math.sin(t * 2.0), 9.6 + 5.0 * t),
               'cp_plume_red' if i % 2 == 0 else 'cp_plume_blue')
    it.box((7.0, 12.4, 7.4), (9.0, 13.4, 9.4), 'gs_gold')
    return it


def gardeserment_legendaire():
    it = it_for('gardeserment_legendaire')
    # heaume au lion : mufle doré sur l'avant, crinière tout autour
    shell(it, 'gs_helm')
    for i in range(10):                                                        # crinière
        a = 2 * math.pi * i / 10
        x, z = 8 + 5.6 * math.cos(a), 8.4 + 5.6 * math.sin(a)
        it.box((x - 1.0, 6.0, z - 1.0), (x + 1.0, 14.0 + (i % 2) * 0.8, z + 1.0), 'cp_mane')
    it.box((S + 0.2, 12.4, S + 0.2), (E - 0.2, 14.4, E - 0.2), 'cp_mane')
    it.box((5.0, 8.4, S - 1.2), (11.0, 12.6, S), 'gs_gold')                    # mufle
    it.box((6.4, 6.4, S - 2.2), (9.6, 9.4, S - 1.0), 'gs_gold')                # museau
    it.box((7.2, 8.6, S - 2.5), (8.8, 9.4, S - 2.1), 'ro_shadow')              # truffe
    for x0 in (5.4, 9.2):
        it.box((x0, 10.6, S - 1.26), (x0 + 1.4, 11.4, S - 1.2), 'cp_eye_amber')
    it.box((5.2, 6.0, S - 0.06), (10.8, 6.6, S), 'slit')
    for side in (-1, 1):
        x0 = 4.6 if side < 0 else 10.2
        it.box((x0, 12.6, S - 0.8), (x0 + 1.2, 13.8, S + 0.2), 'gs_gold')     # oreilles
    band(it, 3.4, 4.2, 'gs_gold')
    return it


def sentinelle_commun():
    it = it_for('sentinelle_commun')
    # bandana de toile et couronne de deux feuilles
    dome(it, 'sn_hood', 9.6, 12.4, 2)
    band(it, 9.6, 10.6, 'sn_hood_d', 0.2)
    for i in range(3):                                                         # nœud qui pend dans le dos
        it.box((7.2 + i * 0.2, 9.0 - i * 1.0, E + 0.2), (8.8 - i * 0.2, 10.0 - i * 1.0, E + 0.8), 'sn_hood_d')
    it.box((E - 0.4, 10.0, 5.0), (E + 0.4, 11.6, 6.4), 'dr_leaf')
    return it


def sentinelle_epique():
    it = it_for('sentinelle_epique')
    hood(it, 'sn_hood', 'sn_hood_d')
    it.box((S + 0.6, 7.0, S - 0.5), (E - 0.6, 10.0, S + 0.2), 'cp_bark')       # masque de bois
    eyes(it, 'slit', 8.2, S - 0.56, 1.8, 1.6)
    it.box((7.6, 7.0, S - 0.8), (8.4, 9.0, S - 0.5), 'cp_bark')
    for i in range(7):                                                         # mantelet de plumes de hibou
        a = math.pi * (i / 6)
        x, z = 8 + 6.6 * math.cos(a), 10.2 + 3.0 * math.sin(a)
        it.box((x - 1.0, 2.6, z - 1.2), (x + 1.0, 5.4, z + 1.2), 'cp_owl' if i % 2 else 'cp_owl_l')
    for side in (-1, 1):                                                       # aigrettes
        x0 = 5.6 if side < 0 else 9.6
        it.box((x0, 13.2, 6.0), (x0 + 0.8, 15.4, 7.0), 'cp_owl')
    return it


def sentinelle_legendaire():
    it = it_for('sentinelle_legendaire')
    # grand-duc : tête de hibou au-dessus du front, ailes repliées sur les côtés, yeux d'ambre
    it.box((S - 0.4, 9.6, S - 0.6), (E + 0.4, 14.4, E + 0.4), 'cp_owl')
    it.box((S - 0.4, 3.6, 10.2), (E + 0.4, 9.6, E + 0.4), 'cp_owl')
    for x0 in (4.0, 9.0):                                                      # disques faciaux
        it.box((x0, 10.0, S - 0.9), (x0 + 3.0, 13.6, S - 0.5), 'cp_owl_l')
        it.box((x0 + 0.8, 11.2, S - 1.0), (x0 + 2.2, 12.4, S - 0.86), 'cp_eye_amber')
    it.box((7.4, 9.4, S - 1.6), (8.6, 11.4, S - 0.5), 'cp_beak')
    for side in (-1, 1):                                                       # aigrettes
        x0 = 3.6 if side < 0 else 11.0
        it.box((x0, 14.4, 6.0), (x0 + 1.4, 17.0, 7.4), 'cp_owl')
        it.box((x0 + 0.3, 17.0, 6.3), (x0 + 1.1, 17.8, 7.1), 'cp_owl_l')
    for side in (-1, 1):                                                       # ailes repliées
        x0 = S - 0.4 if side < 0 else E + 0.4
        for j in range(6):
            a, b = sorted((x0, x0 + side * (0.8 + j * 0.3)))
            it.box((a, 3.0 + j * 1.6, 6.0 + j * 0.4), (b, 5.0 + j * 1.6, 14.0 + j * 0.3), 'cp_owl' if j % 2 else 'cp_owl_l')
    return it


def arcaniste_commun():
    it = it_for('arcaniste_commun')
    hood(it, 'ar_hood', 'ar_hood_d')
    band(it, 10.6, 11.2, 'lr_steel_l', 0.15)
    it.box((7.4, 10.6, S - 0.4), (8.6, 11.6, S - 0.1), 'cp_crystal')
    return it


def arcaniste_epique():
    it = it_for('arcaniste_epique')
    hood(it, 'ar_hood', 'ar_hood_d', rim='ar_hood_d')
    it.box((S - 0.1, 3.6, S - 0.4), (E + 0.1, 7.0, S + 0.6), 'lr_steel_l')
    for side in (-1, 1):                                                       # cornes de métal
        curve(it, 5.6 if side < 0 else 10.4, side, 9,
              lambda t: (2.6 * t, 13.0 + 4.0 * t, 8.0 + 3.0 * t, 0.7 - 0.35 * t),
              ('lr_steel_l', 'lr_silver', 'ar_rune'))
    for i in range(8):                                                         # anneau de cristaux en orbite
        a = 2 * math.pi * i / 8
        x, z = 8 + 6.4 * math.cos(a), 8 + 6.4 * math.sin(a)
        it.box((x - 0.4, 12.0 - 0.6 * (i % 2), z - 0.4), (x + 0.4, 13.4 - 0.6 * (i % 2), z + 0.4),
               'cp_crystal' if i % 2 else 'cp_crystal_v')
    return it


def arcaniste_legendaire():
    it = it_for('arcaniste_legendaire')
    # masque d'acier plein aux yeux d'azur, haute capuche, couronne d'éclats en halo
    hood(it, 'ar_hood', 'ar_hood_d', top=13.6)
    it.box((S + 0.4, 3.6, S - 0.6), (E - 0.4, 10.4, S + 0.2), 'lr_steel')
    eyes(it, 'ar_rune', 7.8, S - 0.66, 2.0, 1.6)
    for x in (5.2, 7.6, 10.0):
        it.box((x, 4.4, S - 0.66), (x + 0.8, 6.2, S - 0.6), 'ar_rune')
    it.box((S + 0.4, 10.4, S - 0.6), (E - 0.4, 11.0, S + 0.2), 'lr_silver')
    for i in range(7):                                                         # couronne d'éclats
        a = math.pi * (0.05 + 0.9 * i / 6)
        x, y = 8 + 6.4 * math.cos(a), 13.4 + 6.4 * math.sin(a)
        it.box((x - 0.5, y - 1.2, 11.2), (x + 0.5, y + 1.2, 12.2), 'cp_crystal' if i % 2 else 'cp_crystal_v')
    it.box((7.2, 20.0, 11.0), (8.8, 22.4, 12.4), 'cp_crystal')
    return it


PALIERS = {}
for _k, _fn in list(globals().items()):
    for _t in ('commun', 'epique', 'legendaire'):
        if _k.endswith('_' + _t) and callable(_fn) and not _k.startswith('_'):
            PALIERS[(_k[:-len(_t) - 1], _t)] = _fn
