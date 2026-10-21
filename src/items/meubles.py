"""Meubles de planque par style (Elfe, Nain, Sorcier, Orc) et portes de style.

Convention (comme la chaise de mobs.py, vérifiée en jeu) : le modèle remplit le bloc 16x16x16 posé, le dos du
meuble est du côté z haut, l'avant côté z bas. Les objets Oraxen sont dans src/items/oraxen/items/evo_meubles_styles.yml
(générés par oraxen_meubles() plus bas).
"""
import math, os
from PIL import Image
from kit import Item, Mat, MATS, h, mix, clamp, grain
from mobs import FURNITURE  # importe aussi les matériaux des meubles (wax, flame...)

HERE = os.path.dirname(__file__)


def bark(c, p, face, px, py, w, hgt):
    """Écorce : sillons verticaux."""
    k = 0.75 if (int(p[0] * 2 + p[2] * 2 + h(int(p[1]), 3) * 2) % 3 == 0) else 1.0
    return tuple(v * k for v in c)


def stars(c, p, face, px, py, w, hgt):
    return (255, 236, 160) if h(p[0] * 2, p[1] * 2, p[2] * 2) > 0.95 else c


def leafy(c, p, face, px, py, w, hgt):
    return mix(c, (150, 210, 110), 0.5) if h(p[0] * 2, p[1] * 2, p[2] * 2) > 0.8 else c


def bricks(c, p, face, px, py, w, hgt):
    row = int(p[1] / 2)
    off = (row % 2) * 2
    joint = (p[1] % 2) < 0.5 or ((p[0] + p[2] + off) % 4) < 0.5
    return tuple(v * 0.7 for v in c) if joint else c


MATS.update({
    # Elfe : bois pâle, feuilles, argent lunaire
    'elf_wood': Mat((222, 206, 168), 7, 0.85, pattern=grain),
    'elf_wood_dark': Mat((168, 142, 100), 7, 0.85, pattern=grain),
    'elf_leaf': Mat((96, 166, 84), 14, 0.82, pattern=leafy),
    'elf_cloth': Mat((70, 130, 110), 8, 0.85),
    'moonstone': Mat((196, 228, 255), 8, 0.9, light=10, hi=(255, 255, 255)),
    'elf_silver': Mat((214, 222, 232), 6, 0.8, hi=(255, 255, 255)),
    'water': Mat((90, 170, 230), 8, 0.95, light=6),
    # Nain : chêne sombre, pierre, fer, runes d'or
    'dw_wood': Mat((92, 60, 38), 8, 0.8, pattern=grain),
    'dw_stone': Mat((112, 110, 116), 12, 0.78, pattern=bricks),
    'dw_iron': Mat((84, 86, 94), 8, 0.72, hi=(160, 165, 175)),
    'dw_gold': Mat((222, 168, 54), 8, 0.75, hi=(255, 230, 140)),
    'rune_gold': Mat((255, 196, 70), 6, 0.95, light=12),
    'dw_red': Mat((128, 34, 30), 8, 0.82),
    'coal_glow': Mat((255, 110, 30), 14, 0.9, light=15),
    # Sorcier : bois violet, étoffe étoilée, arcane
    'wiz_wood': Mat((70, 46, 88), 8, 0.8, pattern=grain),
    'wiz_cloth': Mat((52, 38, 120), 8, 0.85, pattern=stars),
    'wiz_gold': Mat((214, 176, 80), 8, 0.78),
    'potion_green': Mat((90, 230, 120), 8, 0.95, light=10),
    'potion_pink': Mat((240, 90, 200), 8, 0.95, light=10),
    'brew': Mat((120, 240, 110), 10, 0.95, light=14, pattern=stars),
    'cauldron': Mat((44, 42, 48), 8, 0.72),
    # Orc : rondins, peaux, os, peinture de guerre
    'orc_log': Mat((104, 74, 46), 10, 0.78, pattern=bark),
    'orc_hide': Mat((150, 112, 72), 12, 0.8),
    'orc_fur': Mat((96, 80, 64), 18, 0.85),
    'war_red': Mat((150, 28, 26), 8, 0.8),
    'orc_iron': Mat((92, 84, 80), 14, 0.7),
})

# Assise : décalage vertical du siège Oraxen (validé en jeu pour un coussin à 9.2 px : -1.3).
def seat(y_px):
    return round(-1.3 + (y_px - 9.2) / 16, 2)


def F(id):
    return Item(id, density=2, display=FURNITURE)


# =====================================================================================
#  Briques communes
# =====================================================================================

def legs(it, y1, mat, inset=2.6, size=1.4, x0=None, x1=None, z0=None, z1=None):
    x0 = inset if x0 is None else x0
    x1 = 16 - inset - size if x1 is None else x1
    z0 = inset if z0 is None else z0
    z1 = 16 - inset - size if z1 is None else z1
    for x in (x0, x1):
        for z in (z0, z1):
            it.box((x, 0, z), (x + size, y1, z + size), mat)


# =====================================================================================
#  ELFE
# =====================================================================================

def elfe_chaise():
    it = F('elfe_chaise')
    for x in (3, 11.6):
        it.box((x, 0, 3), (x + 1.4, 7, 4.4), 'elf_wood_dark')
        it.box((x + 0.2, 0, 11.4), (x + 1.2, 7, 12.6), 'elf_wood_dark')
    it.box((2.6, 7, 2.6), (13.4, 8.2, 13.2), 'elf_wood')
    it.box((3.2, 8.2, 3.2), (12.8, 8.8, 12.0), 'elf_cloth')
    # dossier en arc de branches
    for x in (3, 11.6):
        it.box((x, 8.2, 11.6), (x + 1.4, 17, 13), 'elf_wood_dark')
    for i, (x0, x1, y) in enumerate(((4.4, 11.6, 17), (5.4, 10.6, 18.2), (6.6, 9.4, 19.2))):
        it.box((x0, y - 1.2, 11.8), (x1, y, 12.8), 'elf_wood')
    it.box((7.4, 9.6, 12.0), (8.6, 16, 12.6), 'elf_wood')
    it.box((6.2, 12.4, 11.9), (9.8, 13.4, 12.7), 'elf_leaf')
    it.box((7.5, 19.2, 11.9), (8.5, 20.4, 12.7), 'moonstone')
    return it


def elfe_table():
    it = F('elfe_table')
    it.col(0, 1.2, 7, 7, 'elf_wood_dark')
    it.col(1.2, 11, 2.2, 2.2, 'elf_wood')
    for a in range(4):
        dx, dz = [(3, 0), (-3, 0), (0, 3), (0, -3)][a]
        it.box((8 + dx * 0.7 - 0.6, 9, 8 + dz * 0.7 - 0.6), (8 + dx * 0.7 + 0.6, 12, 8 + dz * 0.7 + 0.6), 'elf_wood')
    it.box((1, 12, 2.5), (15, 13.2, 13.5), 'elf_wood')
    it.box((2.5, 12, 1), (13.5, 13.2, 15), 'elf_wood')
    it.box((2, 13.2, 3.5), (14, 13.5, 12.5), 'elf_leaf')
    it.box((6.5, 13.5, 6.5), (9.5, 14.2, 9.5), 'elf_silver')
    it.box((7.2, 14.2, 7.2), (8.8, 16.6, 8.8), 'moonstone')
    return it


def elfe_lit():
    """Lit sur deux blocs : tête côté z haut (contre le mur), pied vers z négatif."""
    it = F('elfe_lit')
    it.box((1, 3, -14), (15, 6, 15), 'elf_wood')
    it.box((1.6, 6, -13.4), (14.4, 8, 12), 'elf_cloth')
    it.box((2.4, 6, 11), (13.6, 9, 14.4), 'elf_silver')   # oreiller
    it.box((1.4, 8, -13.4), (14.6, 8.6, 4), 'elf_leaf')   # couverture
    legs(it, 3, 'elf_wood_dark', x0=1, x1=13.6, z0=-14, z1=13.6)
    # tête de lit en arche feuillue
    it.box((0.6, 0, 14.4), (2, 20, 15.8), 'elf_wood_dark')
    it.box((14, 0, 14.4), (15.4, 20, 15.8), 'elf_wood_dark')
    it.box((2, 13, 14.6), (14, 15, 15.6), 'elf_wood')
    it.box((3.5, 15, 14.6), (12.5, 18, 15.6), 'elf_wood')
    it.box((5.5, 18, 14.6), (10.5, 20, 15.6), 'elf_wood')
    it.box((2, 15, 14.2), (5, 17, 14.6), 'elf_leaf')
    it.box((11, 15, 14.2), (14, 17, 14.6), 'elf_leaf')
    it.box((7.3, 16, 14.2), (8.7, 17.4, 14.6), 'moonstone')
    # pied de lit
    it.box((0.6, 0, -15.6), (15.4, 9, -14), 'elf_wood_dark')
    return it


def elfe_armoire():
    it = F('elfe_armoire')
    it.box((1, 0, 5), (15, 22, 15), 'elf_wood')
    it.box((1.6, 1, 4.6), (7.8, 21, 5), 'elf_wood_dark')
    it.box((8.2, 1, 4.6), (14.4, 21, 5), 'elf_wood_dark')
    for x in (2.6, 9.2):
        it.box((x, 12, 4.3), (x + 4.2, 17, 4.6), 'elf_leaf')
        it.box((x + 1.6, 6, 4.3), (x + 2.6, 11, 4.6), 'elf_leaf')
    it.box((7.2, 9, 4.2), (7.8, 12, 4.6), 'elf_silver')
    it.box((8.2, 9, 4.2), (8.8, 12, 4.6), 'elf_silver')
    it.box((0.4, 22, 4.4), (15.6, 23.2, 15.6), 'elf_wood_dark')
    it.box((5, 23.2, 9), (11, 25, 11), 'elf_wood')
    it.box((7.2, 25, 9.4), (8.8, 26.6, 10.6), 'moonstone')
    return it


def elfe_lampe():
    """Lampe-arbre : un tronc fin et des feuilles qui tiennent une pierre de lune."""
    it = F('elfe_lampe')
    it.col(0, 1, 6, 6, 'elf_wood_dark')
    it.col(1, 12, 1.4, 1.4, 'elf_wood')
    it.box((5.6, 11, 7.4), (10.4, 12, 8.6), 'elf_wood')
    it.box((5.6, 12, 7.4), (6.6, 15, 8.6), 'elf_wood')
    it.box((9.4, 12, 7.4), (10.4, 15, 8.6), 'elf_wood')
    it.col(12.2, 14.8, 2.6, 2.6, 'moonstone')
    it.box((4.6, 14.6, 6.6), (7, 15.6, 9.4), 'elf_leaf')
    it.box((9, 14.6, 6.6), (11.4, 15.6, 9.4), 'elf_leaf')
    return it


def elfe_coffre():
    it = F('elfe_coffre')
    it.box((2, 0, 4), (14, 8, 12), 'elf_wood')
    it.box((1.6, 8, 3.6), (14.4, 10.4, 12.4), 'elf_wood_dark')
    it.box((2.4, 10.4, 4.4), (13.6, 11.2, 11.6), 'elf_wood_dark')
    for x in (2.6, 12.4):
        it.box((x, 0, 3.7), (x + 1, 10.6, 12.3), 'elf_silver')
    it.box((6.4, 3, 3.6), (9.6, 8.8, 4), 'elf_leaf')
    it.box((7.3, 7, 3.4), (8.7, 8.6, 3.7), 'moonstone')
    return it


def elfe_vasque():
    """Vasque lunaire : coupe d'eau lumineuse sur pied ouvragé."""
    it = F('elfe_vasque')
    it.col(0, 1.2, 8, 8, 'elf_silver')
    it.col(1.2, 8, 2.4, 2.4, 'elf_wood')
    for a in range(4):
        dx, dz = [(1, 0), (-1, 0), (0, 1), (0, -1)][a]
        it.box((8 + dx * 2 - 0.5, 1.2, 8 + dz * 2 - 0.5), (8 + dx * 2 + 0.5, 6, 8 + dz * 2 + 0.5), 'elf_leaf')
    it.col(8, 9.4, 9, 9, 'elf_silver')
    it.box((2.5, 9.4, 3.5), (13.5, 11.4, 4.5), 'elf_silver')
    it.box((2.5, 9.4, 11.5), (13.5, 11.4, 12.5), 'elf_silver')
    it.box((2.5, 9.4, 4.5), (3.5, 11.4, 11.5), 'elf_silver')
    it.box((12.5, 9.4, 4.5), (13.5, 11.4, 11.5), 'elf_silver')
    it.box((3.5, 9.4, 4.5), (12.5, 10.8, 11.5), 'water')
    it.box((7.4, 10.8, 7.4), (8.6, 12, 8.6), 'moonstone')
    return it


# =====================================================================================
#  NAIN
# =====================================================================================

def nain_chaise():
    """Tabouret-trône trapu, cerclé de fer."""
    it = F('nain_chaise')
    it.box((2.6, 0, 2.6), (13.4, 7, 13.4), 'dw_wood')
    for y in (1, 5.4):
        it.box((2.4, y, 2.4), (13.6, y + 0.8, 13.6), 'dw_iron')
    it.box((2.2, 7, 2.2), (13.8, 8.6, 13.8), 'dw_wood')
    it.box((3, 8.6, 3), (13, 9.2, 11.4), 'dw_red')
    it.box((2.2, 8.6, 11.4), (13.8, 17, 13.8), 'dw_wood')
    it.box((2, 15.6, 11.2), (14, 17.6, 14), 'dw_iron')
    it.box((6.6, 11, 11.1), (9.4, 14, 11.4), 'dw_gold')
    it.box((7.4, 11.8, 10.9), (8.6, 13.2, 11.1), 'rune_gold')
    for x in (2.2, 12.2):
        it.box((x, 8.6, 3), (x + 1.6, 12, 11.4), 'dw_wood')
    return it


def nain_table():
    it = F('nain_table')
    it.box((3, 0, 3), (13, 2, 13), 'dw_stone')
    it.box((5, 2, 5), (11, 11, 11), 'dw_stone')
    it.box((0.5, 11, 0.5), (15.5, 13.6, 15.5), 'dw_wood')
    it.box((0.3, 11.6, 0.3), (15.7, 12.6, 15.7), 'dw_iron')
    it.box((3, 13.6, 4), (6.5, 16.6, 7.5), 'dw_iron')        # chope
    it.box((3.4, 16.4, 4.4), (6.1, 17, 7.1), 'paper')
    it.box((9, 13.6, 8.5), (13, 14.2, 12.5), 'dw_gold')       # pièces
    it.box((10, 14.2, 9.5), (12, 14.8, 11.5), 'dw_gold')
    return it


def nain_lit():
    it = F('nain_lit')
    it.box((1, 0, -15), (15, 6, 15), 'dw_wood')
    for z in (-14, -1, 12):
        it.box((0.8, 1, z), (15.2, 2, z + 1.4), 'dw_iron')
    it.box((1.6, 6, -14.4), (14.4, 8.6, 12.4), 'orc_fur')
    it.box((2.6, 6, 11.4), (13.4, 9.4, 14.4), 'dw_red')
    it.box((0, 0, 14.6), (16, 16, 16), 'dw_stone')            # tête de lit en pierre
    it.box((0, 16, 14.2), (16, 17.4, 16), 'dw_iron')
    it.box((5, 9, 14.3), (11, 14, 14.6), 'dw_gold')
    it.box((7, 10, 14.1), (9, 13, 14.3), 'rune_gold')
    it.box((0, 0, -16), (16, 9, -14.6), 'dw_wood')
    return it


def nain_armoire():
    """Râtelier-armoire de forge : portes bardées de fer et marteau accroché."""
    it = F('nain_armoire')
    it.box((0.5, 0, 5), (15.5, 20, 15), 'dw_wood')
    for y in (2, 9.5, 17):
        it.box((0.3, y, 4.6), (15.7, y + 1.2, 15.4), 'dw_iron')
    it.box((7.6, 1, 4.6), (8.4, 19, 5), 'dw_iron')
    it.box((6.4, 10.8, 4.2), (7.4, 13, 4.6), 'dw_gold')
    it.box((8.6, 10.8, 4.2), (9.6, 13, 4.6), 'dw_gold')
    it.box((0, 20, 4.4), (16, 22, 15.6), 'dw_stone')
    it.box((3, 4, 4.3), (5, 8, 4.6), 'rune_gold')
    it.box((11, 4, 4.3), (13, 8, 4.6), 'rune_gold')
    return it


def nain_lampe():
    """Brasero de fer sur trépied, braises vives."""
    it = F('nain_lampe')
    for (x, z) in ((4, 4), (10.6, 4), (7.3, 11)):
        it.box((x, 0, z), (x + 1.4, 7, z + 1.4), 'dw_iron')
    it.box((3.5, 7, 3.5), (12.5, 8, 12.5), 'dw_iron')
    it.box((3, 8, 3), (13, 11, 4), 'dw_iron')
    it.box((3, 8, 12), (13, 11, 13), 'dw_iron')
    it.box((3, 8, 4), (4, 11, 12), 'dw_iron')
    it.box((12, 8, 4), (13, 11, 12), 'dw_iron')
    it.box((4, 8, 4), (12, 10.4, 12), 'coal_glow')
    it.box((5.5, 10.4, 6), (8, 12.4, 8.5), 'coal_glow')
    it.box((8.5, 10.4, 8), (10.5, 11.8, 10), 'flame')
    return it


def nain_coffre():
    it = F('nain_coffre')
    it.box((1.5, 0, 3.5), (14.5, 9, 12.5), 'dw_wood')
    it.box((1.2, 9, 3.2), (14.8, 12, 12.8), 'dw_wood')
    for x in (2.8, 7.4, 12.0):
        it.box((x, 0, 3.0), (x + 1.2, 12.2, 13.0), 'dw_iron')
    it.box((6, 6, 2.8), (10, 10, 3.2), 'dw_gold')
    it.box((7.2, 7, 2.6), (8.8, 8.6, 2.8), 'rune_gold')
    return it


def nain_enclume():
    it = F('nain_enclume')
    it.box((3, 0, 3), (13, 2, 13), 'dw_stone')
    it.box((4, 2, 4), (12, 7, 12), 'orc_log')
    it.box((5, 7, 4.5), (11, 9, 11.5), 'dw_iron')
    it.box((6.2, 9, 5.5), (9.8, 11, 10.5), 'dw_iron')
    it.box((2, 11, 4), (14, 14, 12), 'dw_iron')
    it.box((-1, 11.8, 6.5), (2, 13.6, 9.5), 'dw_iron')        # bigorne
    it.box((14, 12, 5), (15.6, 14, 11), 'dw_iron')
    it.box((5, 14, 9), (12, 15, 10), 'wood_dark')            # marteau
    it.box((10.5, 14, 7.6), (13, 16.4, 11.4), 'dw_iron')
    it.box((3, 14, 5), (6, 14.4, 7), 'coal_glow')            # lame rougie
    return it


# =====================================================================================
#  SORCIER
# =====================================================================================

def sorcier_chaise():
    """Fauteuil à haut dossier pointu, étoffe étoilée."""
    it = F('sorcier_chaise')
    legs(it, 7, 'wiz_wood', inset=2.6)
    it.box((2.4, 7, 2.4), (13.6, 8.4, 13.6), 'wiz_wood')
    it.box((3, 8.4, 3), (13, 9.4, 11.6), 'wiz_cloth')
    it.box((2.4, 8.4, 11.6), (13.6, 20, 13.4), 'wiz_wood')
    it.box((3.4, 9.4, 11.2), (12.6, 19, 11.6), 'wiz_cloth')
    it.box((4.6, 20, 11.8), (11.4, 22.4, 13.2), 'wiz_wood')
    it.box((6.6, 22.4, 12), (9.4, 24.4, 13), 'wiz_wood')
    it.box((7.4, 24.4, 12.1), (8.6, 25.6, 12.9), 'arcane')
    for x in (2.2, 12.2):
        it.box((x, 8.4, 3), (x + 1.6, 12.4, 11.6), 'wiz_wood')
        it.box((x, 12.4, 3), (x + 1.6, 13.2, 11.6), 'wiz_gold')
    return it


def sorcier_table():
    """Pupitre à grimoire : livre ouvert et bougies."""
    it = F('sorcier_table')
    it.col(0, 1.4, 8, 6, 'wiz_wood')
    it.col(1.4, 11, 2, 2, 'wiz_wood')
    it.box((2, 11, 3), (14, 12.4, 13), 'wiz_wood')
    it.box((1.6, 11.4, 2.6), (14.4, 12, 13.4), 'wiz_gold')
    it.box((3.5, 12.4, 5), (7.9, 13.2, 11), 'paper')           # grimoire ouvert
    it.box((8.1, 12.4, 5), (12.5, 13.2, 11), 'paper')
    it.box((3.2, 12.2, 4.7), (12.8, 12.6, 11.3), 'wiz_cloth')
    it.box((5, 13.2, 7), (6.6, 13.3, 9), 'arcane')
    it.box((2.2, 12.4, 11.6), (3.8, 15.6, 13), 'wax')
    it.box((2.6, 15.6, 12), (3.4, 16.8, 12.6), 'flame')
    it.box((12.4, 12.4, 2.8), (13.6, 14.8, 4), 'potion_green')
    return it


def sorcier_lit():
    it = F('sorcier_lit')
    it.box((1, 3, -14), (15, 6, 15), 'wiz_wood')
    it.box((1.6, 6, -13.4), (14.4, 8, 12), 'wiz_cloth')
    it.box((2.4, 6, 11), (13.6, 9, 14.4), 'paper')
    it.box((1.4, 8, -13.4), (14.6, 8.6, 5), 'wiz_cloth')
    legs(it, 3, 'wiz_wood', x0=1, x1=13.6, z0=-14, z1=13.6)
    # baldaquin
    for x in (0.6, 14):
        for z in (-15.6, 14.4):
            it.box((x, 0, z), (x + 1.4, 26, z + 1.4), 'wiz_wood')
    it.box((0.6, 26, -15.6), (15.4, 27.4, 15.8), 'wiz_wood')
    it.box((1, 24, 14.6), (15, 26, 15.6), 'wiz_cloth')
    it.box((1, 24, -15.4), (15, 26, -14.4), 'wiz_cloth')
    it.box((7, 26.2, -1), (9, 28, 1), 'arcane')
    return it


def sorcier_armoire():
    """Bibliothèque d'arcanes : grimoires, fioles et crâne."""
    it = F('sorcier_armoire')
    it.box((0.5, 0, 11), (15.5, 24, 16), 'wiz_wood')
    it.box((0.5, 0, 4), (1.7, 24, 11), 'wiz_wood')
    it.box((14.3, 0, 4), (15.5, 24, 11), 'wiz_wood')
    for y in (0, 7.6, 15.2, 22.8):
        it.box((1.7, y, 4), (14.3, y + 1.2, 11), 'wiz_wood')
    books = ('wiz_cloth', 'cloth_red', 'cloth_green', 'wiz_gold', 'cloth_blue', 'leather_dark')
    x = 2
    for n in range(7):
        w = 1.2 + (n % 3) * 0.3
        it.box((x, 1.2, 5), (x + w, 6.2 - (n % 2), 10.6), books[n % len(books)])
        x += w + 0.15
    it.box((10.6, 1.2, 5.2), (13.8, 3.4, 10.4), 'paper')
    for n, mat in enumerate(('potion_green', 'potion_pink', 'arcane')):
        x0 = 2.6 + n * 3.6
        it.box((x0, 8.8, 6.2), (x0 + 2.2, 11.6, 8.8), mat)
        it.box((x0 + 0.6, 11.6, 6.8), (x0 + 1.6, 12.6, 8.2), 'wood')
    it.box((2.6, 16.4, 5.6), (6.4, 19.6, 9.6), 'bone')        # crâne
    it.box((3.2, 17.6, 5.4), (4.2, 18.6, 5.6), 'leather_dark')
    it.box((4.8, 17.6, 5.4), (5.8, 18.6, 5.6), 'leather_dark')
    x = 8
    for n in range(4):
        it.box((x, 16.4, 5), (x + 1.4, 21, 10.6), books[(n + 2) % len(books)])
        x += 1.55
    it.box((5, 24, 7), (11, 25, 11), 'wiz_gold')
    it.box((7.2, 25, 8.2), (8.8, 26.6, 9.8), 'arcane')
    return it


def sorcier_lampe():
    """Orbe flottant sur un pied en spirale."""
    it = F('sorcier_lampe')
    it.col(0, 1, 6, 6, 'wiz_wood')
    for i in range(8):
        a = i * math.pi / 4
        x, z = 8 + 1.2 * math.cos(a), 8 + 1.2 * math.sin(a)
        it.box((x - 0.6, 1 + i * 1.2, z - 0.6), (x + 0.6, 2.4 + i * 1.2, z + 0.6), 'wiz_gold')
    it.col(10.6, 11.4, 4, 4, 'wiz_wood')
    it.col(12, 15, 3, 3, 'arcane')
    it.col(12.6, 14.4, 3.6, 1.4, 'arcane')
    return it


def sorcier_coffre():
    it = F('sorcier_coffre')
    it.box((2, 0, 4), (14, 8, 12), 'wiz_wood')
    it.box((1.6, 8, 3.6), (14.4, 10, 12.4), 'wiz_cloth')
    it.box((2.6, 10, 4.6), (13.4, 11, 11.4), 'wiz_wood')
    for x in (2.2, 12.8):
        it.box((x, 0, 3.7), (x + 1, 10.2, 12.3), 'wiz_gold')
    it.box((6.6, 4, 3.6), (9.4, 7.4, 3.9), 'wiz_gold')
    it.box((7.3, 4.8, 3.4), (8.7, 6.6, 3.6), 'arcane')
    return it


def sorcier_chaudron():
    it = F('sorcier_chaudron')
    for (x, z) in ((3, 3), (11.6, 3), (3, 11.6), (11.6, 11.6)):
        it.box((x, 0, z), (x + 1.4, 2, z + 1.4), 'cauldron')
    it.box((2.5, 2, 2.5), (13.5, 3.2, 13.5), 'cauldron')
    it.box((1.5, 3.2, 1.5), (14.5, 11, 2.5), 'cauldron')
    it.box((1.5, 3.2, 13.5), (14.5, 11, 14.5), 'cauldron')
    it.box((1.5, 3.2, 2.5), (2.5, 11, 13.5), 'cauldron')
    it.box((13.5, 3.2, 2.5), (14.5, 11, 13.5), 'cauldron')
    it.box((1, 10.2, 1), (15, 11.2, 15), 'cauldron')
    it.box((2.5, 3.2, 2.5), (13.5, 9.8, 13.5), 'brew')
    it.box((5, 9.8, 6), (7, 11.8, 8), 'brew')
    it.box((9, 9.8, 9), (10.4, 12.8, 10.4), 'brew')
    it.box((10, 9.8, 4), (11, 18, 5), 'wood')                 # louche
    return it


# =====================================================================================
#  ORC
# =====================================================================================

def orc_chaise():
    """Trône de rondins couvert d'une peau, crâne au sommet."""
    it = F('orc_chaise')
    it.box((2, 0, 2.5), (14, 7.6, 13.5), 'orc_log')
    it.box((1.6, 7.6, 2), (14.4, 9, 12), 'orc_fur')
    it.box((1.6, 7.6, 11.4), (14.4, 19, 14), 'orc_log')
    it.box((2, 9, 11), (14, 17, 11.6), 'orc_hide')
    it.box((4, 12, 10.8), (12, 13.2, 11), 'war_red')
    it.box((5.6, 19, 11.6), (10.4, 23, 14.4), 'bone')
    it.box((6.4, 20.6, 11.4), (7.6, 21.8, 11.6), 'leather_dark')
    it.box((8.4, 20.6, 11.4), (9.6, 21.8, 11.6), 'leather_dark')
    for x in (1, 13):
        it.box((x, 7.6, 3), (x + 2, 12, 11.4), 'orc_log')
        it.box((x + 0.4, 12, 3.5), (x + 1.6, 14, 4.7), 'bone')
    it.box((0.6, 17, 12.4), (1.6, 22, 13.4), 'bone')
    it.box((14.4, 17, 12.4), (15.4, 22, 13.4), 'bone')
    return it


def orc_table():
    """Table de festin : demi-rondin sur tréteaux, gigot et os."""
    it = F('orc_table')
    for x in (2, 12.4):
        it.box((x, 0, 3), (x + 1.6, 10, 4.6), 'orc_log')
        it.box((x, 0, 11.4), (x + 1.6, 10, 13), 'orc_log')
        it.box((x, 6, 4.6), (x + 1.6, 7, 11.4), 'orc_log')
    it.box((0.5, 10, 1.5), (15.5, 13, 14.5), 'orc_log')
    it.box((0.6, 12.6, 1.6), (15.4, 13.2, 14.4), 'orc_hide')
    it.box((4, 13.2, 5), (9, 15.6, 9), 'cloth_red')            # gigot
    it.box((9, 13.8, 6.4), (11.6, 14.8, 7.6), 'bone')
    it.box((10, 13.2, 10), (13, 13.8, 11), 'bone')
    it.box((2.5, 13.2, 10.5), (5, 16, 13), 'orc_iron')         # chope
    return it


def orc_lit():
    it = F('orc_lit')
    it.box((0.6, 0, -15), (15.4, 3, 15), 'orc_log')
    it.box((1, 3, -14.6), (15, 6, 14.6), 'orc_fur')
    it.box((2, 6, 9.6), (14, 8.4, 14), 'orc_hide')
    it.box((1.6, 6, -12), (14.4, 6.8, 6), 'orc_hide')
    for x in (0, 14.4):
        it.box((x, 0, 14.4), (x + 1.6, 18, 16), 'orc_log')
    it.box((1.6, 9, 14.6), (14.4, 15, 15.6), 'orc_hide')
    it.box((5, 15, 14.6), (11, 19, 15.8), 'bone')
    it.box((3, 12, 14.4), (13, 13, 14.6), 'war_red')
    return it


def orc_armoire():
    """Râtelier d'armes : haches et lances sur fond de rondins."""
    it = F('orc_armoire')
    for x in (0.5, 4.4, 8.2, 12):
        it.box((x, 0, 13), (x + 3.5, 22, 16), 'orc_log')
    for y in (3, 15):
        it.box((0, y, 11.4), (16, y + 1.6, 13), 'orc_log')
    # hache
    it.box((3.4, 2, 10.4), (4.6, 18, 11.4), 'wood_dark')
    it.box((1, 13, 10.2), (3.4, 18, 11.6), 'orc_iron')
    it.box((4.6, 13, 10.2), (7, 18, 11.6), 'orc_iron')
    # lance
    it.box((11.4, 1, 10.4), (12.6, 20, 11.4), 'wood_dark')
    it.box((11, 20, 10.2), (13, 23, 11.6), 'orc_iron')
    it.box((10.6, 17, 10.2), (13.4, 18, 11.6), 'war_red')
    it.box((6.6, 19, 12.6), (9.4, 22, 13), 'bone')
    return it


def orc_lampe():
    """Torchère : crâne sur pieu, flamme dans le crâne."""
    it = F('orc_lampe')
    it.col(0, 1.4, 5, 5, 'orc_log')
    it.col(1.4, 11, 1.4, 1.4, 'orc_log')
    it.col(5, 6, 1.8, 1.8, 'war_red')
    it.box((5.6, 11, 5.6), (10.4, 15, 10.4), 'bone')
    it.box((6.4, 12.4, 5.4), (7.6, 13.6, 5.6), 'flame')
    it.box((8.4, 12.4, 5.4), (9.6, 13.6, 5.6), 'flame')
    it.box((6.6, 15, 6.6), (9.4, 17, 9.4), 'flame')
    it.box((7.3, 17, 7.3), (8.7, 18.4, 8.7), 'ember')
    return it


def orc_coffre():
    it = F('orc_coffre')
    it.box((1.5, 0, 3.5), (14.5, 8, 12.5), 'orc_log')
    it.box((1.2, 8, 3.2), (14.8, 10.6, 12.8), 'orc_hide')
    it.box((1, 1, 3), (15, 2, 13), 'orc_iron')
    it.box((1, 6, 3), (15, 7, 13), 'orc_iron')
    it.box((6.6, 3, 2.8), (9.4, 6, 3.2), 'bone')
    for x in (2, 13):
        it.box((x, 10.6, 7.4), (x + 1, 12.6, 8.6), 'bone')
    return it


def orc_trophee():
    """Totem de guerre : crânes empilés et cornes, bannière rouge."""
    it = F('orc_trophee')
    it.col(0, 1.6, 8, 8, 'orc_log')
    it.col(1.6, 22, 2.4, 2.4, 'orc_log')
    it.box((4.6, 6, 5.6), (11.4, 10.4, 10.4), 'bone')
    it.box((5.2, 13, 5.8), (10.8, 17, 10.2), 'bone')
    for (y, z) in ((7.6, 5.4), (14.4, 5.6)):
        it.box((5.8, y, z), (7, y + 1.2, z + 0.2), 'leather_dark')
        it.box((9, y, z), (10.2, y + 1.2, z + 0.2), 'leather_dark')
    it.box((1.4, 15, 7.4), (5.2, 16.2, 8.6), 'bone')
    it.box((0.6, 16.2, 7.4), (1.8, 19, 8.6), 'bone')
    it.box((10.8, 15, 7.4), (14.6, 16.2, 8.6), 'bone')
    it.box((14.2, 16.2, 7.4), (15.4, 19, 8.6), 'bone')
    it.box((9.2, 18, 8.6), (14, 22, 9.0), 'war_red')
    it.box((7.4, 22, 7.4), (8.6, 24, 8.6), 'orc_iron')
    return it


# =====================================================================================
#  Catalogue
# =====================================================================================

STYLES = {
    'elfe': ('Elfe', '#9ad18a', [elfe_chaise, elfe_table, elfe_lit, elfe_armoire, elfe_lampe, elfe_coffre, elfe_vasque]),
    'nain': ('Nain', '#e0a84a', [nain_chaise, nain_table, nain_lit, nain_armoire, nain_lampe, nain_coffre, nain_enclume]),
    'sorcier': ('Sorcier', '#a98cff', [sorcier_chaise, sorcier_table, sorcier_lit, sorcier_armoire, sorcier_lampe,
                                       sorcier_coffre, sorcier_chaudron]),
    'orc': ('Orc', '#d0584a', [orc_chaise, orc_table, orc_lit, orc_armoire, orc_lampe, orc_coffre, orc_trophee]),
}


def unfight(it, eps=0.1):
    """Évite le scintillement : quand deux pavés de matériaux différents ont une face visible dans le même plan,
    le plus petit dépasse de eps vers l'extérieur (les faces du dessous posées au sol ne comptent pas)."""
    E = it.els
    for i, a in enumerate(E):
        for b in E[i + 1:]:
            if a['mat'] == b['mat']:
                continue
            for ax in range(3):
                o = [k for k in range(3) if k != ax]
                if not all(min(a['to'][k], b['to'][k]) - max(a['from'][k], b['from'][k]) > 0.01 for k in o):
                    continue
                for side, key in ((1, 'to'), (-1, 'from')):
                    if abs(a[key][ax] - b[key][ax]) > 1e-6 or (ax == 1 and side == -1 and a[key][ax] <= 0):
                        continue
                    area = lambda e: (e['to'][o[0]] - e['from'][o[0]]) * (e['to'][o[1]] - e['from'][o[1]])
                    small = a if area(a) <= area(b) else b
                    small[key] = list(small[key])
                    small[key][ax] = round(small[key][ax] + side * eps, 3)
    return it


def fitted(fn):
    """Réduit l'icône (inventaire, main, sol) des meubles plus grands qu'un bloc ; la pose reste à l'échelle 1."""
    def make():
        it = unfight(fn())
        lo = [min(e['from'][k] for e in it.els) for k in range(3)]
        hi = [max(e['to'][k] for e in it.els) for k in range(3)]
        k = min(1.0, 16 / max(hi[i] - lo[i] for i in range(3)))
        if k < 1:
            cy = (lo[1] + hi[1]) / 2 - 8
            cz = (lo[2] + hi[2]) / 2 - 8
            d = {}
            for slot, t in FURNITURE.items():
                t = dict(t)
                if slot != 'fixed':
                    t['scale'] = [round(v * k, 3) for v in t['scale']]
                    if slot == 'gui':
                        t['translation'] = [0, round(-1 - cy * 0.6 * k, 2), 0]
                d[slot] = t
            it.display = d
        return it
    make.__name__ = fn.__name__
    return make


# Couvercle des coffres : hauteur de la charnière (le couvercle pivote autour de l'arête arrière, côté z haut).
LIDS = {'elfe_coffre': 8, 'nain_coffre': 9, 'sorcier_coffre': 8, 'orc_coffre': 8}


def opened(fn, lid_y, angle, suffix):
    """Variante du coffre au couvercle soulevé de angle degrés (images de l'animation d'ouverture Oraxen)."""
    def make():
        it = fitted(fn)()
        it.id += suffix
        els = []
        for e in it.els:
            if e['from'][1] < lid_y < e['to'][1]:
                low, high = dict(e), dict(e)
                low['to'] = [e['to'][0], lid_y, e['to'][2]]
                high['from'] = [e['from'][0], lid_y, e['from'][2]]
                els += [low, high]
            else:
                els.append(e)
        lid = [e for e in els if e['from'][1] >= lid_y]
        back = max(e['to'][2] for e in lid)
        for e in lid:
            e['rot'] = {'angle': angle, 'axis': 'x', 'origin': [8, lid_y, back]}
        it.els = els
        return it
    make.__name__ = fn.__name__ + suffix
    return make


STYLE_ITEMS = [fitted(fn) for _, (_, _, fns) in STYLES.items() for fn in fns]
_by_name = {fn.__name__: fn for _, (_, _, fns) in STYLES.items() for fn in fns}
OPEN_ITEMS = [opened(_by_name[k], y, a, s) for k, y in LIDS.items() for a, s in ((22.5, '_ouvert1'), (45, '_ouvert'))]

# nom affiché, type (pour le comportement Oraxen), hauteur d'assise en px
NAMES = {
    'elfe_chaise': ('Chaise sylvestre', 'seat', 8.8), 'elfe_table': ('Table de lune', 'solid', 0),
    'elfe_lit': ('Lit de feuillage', 'bed', 0), 'elfe_armoire': ('Armoire elfique', 'tall', 0),
    'elfe_lampe': ('Lampe-arbre', 'lamp', 0), 'elfe_coffre': ('Coffret elfique', 'solid', 0),
    'elfe_vasque': ('Vasque lunaire', 'lamp_solid', 0),
    'nain_chaise': ('Siège du clan', 'seat', 9.2), 'nain_table': ('Table de pierre', 'solid', 0),
    'nain_lit': ('Couche de fourrure', 'bed', 0), 'nain_armoire': ('Armoire de forge', 'tall', 0),
    'nain_lampe': ('Brasero naine', 'lamp_solid', 0), 'nain_coffre': ('Coffre cerclé', 'solid', 0),
    'nain_enclume': ('Enclume runique', 'solid', 0),
    'sorcier_chaise': ('Fauteuil arcanique', 'seat', 9.4), 'sorcier_table': ('Pupitre à grimoire', 'solid', 0),
    'sorcier_lit': ('Lit à baldaquin étoilé', 'bed', 0), 'sorcier_armoire': ("Bibliothèque d'arcanes", 'tall', 0),
    'sorcier_lampe': ('Orbe flottant', 'lamp', 0), 'sorcier_coffre': ('Malle du sorcier', 'solid', 0),
    'sorcier_chaudron': ('Chaudron bouillonnant', 'lamp_solid', 0),
    'orc_chaise': ('Trône de rondins', 'seat', 9.0), 'orc_table': ('Table de festin', 'solid', 0),
    'orc_lit': ('Couche de peaux', 'bed', 0), 'orc_armoire': ("Râtelier d'armes", 'tall', 0),
    'orc_lampe': ('Torchère à crâne', 'lamp', 0), 'orc_coffre': ('Coffre de butin', 'solid', 0),
    'orc_trophee': ('Totem de guerre', 'tall', 0),
}


def oraxen_meubles():
    """YAML Oraxen des meubles de style."""
    out = ['# Généré par src/items/meubles.py (dépôt ressourcepack). Ne pas éditer à la main.',
           '# Meubles de style, modèles evo:<id> ; même réglage que evo_meubles.yml (entité d\'affichage sans transformation).', '']
    for key, (label, color, fns) in STYLES.items():
        for fn in fns:
            iid = fn.__name__
            name, kind, seat_y = NAMES[iid]
            out += [f'{iid}:', f'  itemname: "<{color}>{name}"', '  material: PAPER', '  lore:',
                    f'    - "<gray>Style : <white>{label}"', '  components:', f'    item_model: evo:{iid}',
                    '  mechanics:', '    furniture:', '      type: DISPLAY_ENTITY', '      properties:',
                    '        display_transform: NONE']
            if kind.startswith('lamp'):
                out += ['        brightness:', '          block_light: 15', '          sky_light: 15']
            if kind in ('seat', 'solid', 'lamp_solid'):
                out += ['      barrier: true']
            elif kind == 'tall':
                out += ['      barriers:', '        - origin', '        - y: 1']
            elif kind == 'bed':
                out += ['      barriers:', '        - origin', '        - z: -1']
            else:
                out += ['      hitboxes:', '        - 0,0,0 0.6,1.0']
            out += ['      limited_placing:', '        roof: false', '        floor: true', '        wall: false']
            if kind == 'seat':
                out += ['      seats:', f'        - 0,{seat(seat_y)},0']
            if kind == 'bed':
                out += ['      seats:', f'        - 0,{seat(7.0)},0']
            if kind.startswith('lamp'):
                out += ['      lights:', '        - 0,1,0 13' if kind == 'lamp_solid' else '        - 0,0,0 13']
            if iid.endswith(('_coffre', '_armoire')):
                rows = 3 if iid.endswith('_coffre') else 6
                out += ['      storage:', '        type: STORAGE', f'        rows: {rows}', f'        title: "{name}"']
                if iid in LIDS:
                    # images de l'animation, jouées par le correctif Oraxen « model: » (StorageMechanic)
                    out += [f'        open_animation: "model:evo:{iid}_ouvert1,evo:{iid}_ouvert"',
                            f'        close_animation: "model:evo:{iid}_ouvert1,evo:{iid}"']
            out += ['      drop:', '        silktouch: false', '        loots:',
                    f'          - {{ oraxen_item: {iid}, probability: 1.0 }}', '']
    path = os.path.join(HERE, 'oraxen', 'items', 'evo_meubles_styles.yml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    return path
