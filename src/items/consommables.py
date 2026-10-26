"""Consommables de la boutique d'Aldric (potions, élixirs, vivres) et outils de réparation de Gorm, en 3D.

Potions : evo:conso_<article> (npcs.yml, item.item-model), une silhouette de flacon par tier (fiole, flasque,
carafe, cristal) et une forme propre à chaque élixir. Le verre est peint opaque : le liquide occupe le bas du
flacon, le verre vide le haut, avec un reflet.
Outils de réparation : evo:outil_reparation_<rareté> (resources.yml, modèle par défaut).
"""
import mobs  # noqa: F401  (glass, flame, wax)
import armes_butin  # noqa: F401  (b_* : cuivre, cuir, braise...)
from kit import Item, Mat, MATS, OBJECT


def liquid(rgb, light=6):
    r, g, b = rgb
    return Mat(rgb, 6, 0.8, 0.12, light=light, hi=(min(255, r + 90), min(255, g + 90), min(255, b + 90)))


MATS.update({
    'c_glass': Mat((206, 228, 236), 4, 0.9, hi=(255, 255, 255)),
    'c_shine': Mat((250, 255, 255), 2, 1.0),
    'c_cork': Mat((150, 108, 66), 10, 0.8),
    'c_wax_red': Mat((168, 28, 32), 8, 0.8),
    'c_label': Mat((232, 218, 180), 6, 0.85),
    'c_cloth': Mat((236, 230, 214), 8, 0.85),
    'c_bread': Mat((196, 140, 70), 14, 0.8, hi=(236, 190, 120)),
    'c_stone': Mat((120, 124, 132), 12, 0.75),
    'c_soin1': liquid((230, 70, 76)), 'c_soin2': liquid((200, 30, 44)), 'c_soin3': liquid((168, 14, 30), 8),
    'c_soin4': liquid((120, 0, 20), 10),
    'c_mana1': liquid((70, 130, 255)), 'c_mana2': liquid((40, 90, 220)), 'c_mana3': liquid((24, 60, 180), 8),
    'c_mana4': liquid((14, 34, 130), 10),
    'c_force': liquid((156, 42, 30)), 'c_celerite': liquid((124, 211, 242)), 'c_vision': liquid((31, 63, 160), 9),
    'c_fer': liquid((138, 143, 152), 3), 'c_feu': liquid((232, 144, 42), 9), 'c_heros': liquid((176, 95, 224), 11),
})


def obj(id):
    return Item(id, density=4, display=OBJECT)


def bottle(it, liq, y0, body_w, body_d, body_h, fill=0.65, neck_w=1.4, neck_h=1.6, glass='c_glass',
           stopper='c_cork', stopper_h=1.2):
    """Flacon simple : corps (liquide en bas, verre en haut), goulot, bouchon. Renvoie le haut du bouchon."""
    yl = y0 + body_h * fill
    it.col(y0, yl, body_w, body_d, liq)
    it.col(yl, y0 + body_h, body_w, body_d, glass)
    # reflet vertical sur la face avant
    it.box((8 - body_w / 2 + 0.6, y0 + 0.8, 8 + body_d / 2), (8 - body_w / 2 + 1.1, y0 + body_h - 0.6, 8 + body_d / 2 + 0.06),
           'c_shine')
    yn = y0 + body_h
    it.col(yn, yn + neck_h, neck_w, neck_w, glass)
    it.col(yn + neck_h, yn + neck_h + stopper_h, neck_w + 0.4, neck_w + 0.4, stopper)
    return yn + neck_h + stopper_h


# ------------------------------------------------------------------ potions de soin et de mana, par tier

def fiole(id, liq):
    it = obj(id)
    it.col(2.4, 3.0, 3.6, 3.6, liq)
    bottle(it, liq, 3.0, 4.6, 4.6, 4.2, fill=0.7)
    it.col(7.2, 7.6, 2.4, 2.4, 'c_glass')
    return it


def flasque(id, liq, ribbon):
    it = obj(id)
    top = bottle(it, liq, 2.0, 5.6, 3.2, 6.4, fill=0.7, neck_w=1.6, neck_h=2.0)
    it.col(8.4, 9.0, 3.0, 2.4, 'c_glass')
    # étiquette et cordon
    it.box((5.8, 3.4, 9.6), (10.2, 5.8, 9.7), 'c_label')
    it.col(10.2, 10.8, 2.0, 2.0, ribbon)
    return it


def carafe(id, liq, gem):
    it = obj(id)
    it.col(1.2, 2.0, 5.4, 5.4, 'gold')
    bottle(it, liq, 2.0, 6.4, 6.4, 5.6, fill=0.72, neck_w=2.0, neck_h=2.2, stopper='c_wax_red', stopper_h=1.4)
    it.col(7.6, 8.6, 4.6, 4.6, 'c_glass')
    it.col(8.6, 9.2, 2.6, 2.6, 'gold')
    it.box((7.3, 4.0, 11.2), (8.7, 5.4, 11.4), gem)
    return it


def supreme(id, liq, gem):
    it = obj(id)
    it.col(0.8, 1.6, 5.0, 5.0, 'gold')
    # flacon taillé en cristal : corps en gradins
    it.col(1.6, 2.6, 4.2, 4.2, liq)
    it.col(2.6, 6.6, 5.6, 5.6, liq)
    it.col(6.6, 7.8, 4.4, 4.4, 'c_glass')
    it.col(7.8, 8.6, 3.0, 3.0, 'c_glass')
    it.box((5.6, 3.0, 10.8), (6.2, 7.2, 10.86), 'c_shine')
    # cage d'or aux arêtes
    for (x, z) in ((5.0, 5.0), (11.0, 5.0), (5.0, 11.0), (11.0, 11.0)):
        it.box((x - 0.35, 1.6, z - 0.35), (x + 0.35, 7.0, z + 0.35), 'gold')
    it.col(6.6, 7.0, 6.4, 6.4, 'gold')
    it.col(8.6, 10.2, 1.6, 1.6, 'gold')
    it.col(10.2, 12.0, 2.0, 2.0, gem)
    return it


def conso_soin_mineure(): return fiole('conso_soin_mineure', 'c_soin1')
def conso_mana_mineure(): return fiole('conso_mana_mineure', 'c_mana1')
def conso_soin(): return flasque('conso_soin', 'c_soin2', 'cloth_red')
def conso_mana(): return flasque('conso_mana', 'c_mana2', 'cloth_blue')
def conso_grande_soin(): return carafe('conso_grande_soin', 'c_soin3', 'ruby')
def conso_grande_mana(): return carafe('conso_grande_mana', 'c_mana3', 'sapphire')
def conso_soin_supreme(): return supreme('conso_soin_supreme', 'c_soin4', 'ruby')
def conso_mana_supreme(): return supreme('conso_mana_supreme', 'c_mana4', 'sapphire')


# ------------------------------------------------------------------ élixirs : une forme chacun

def conso_force():
    """Fiole conique (erlenmeyer) sur socle de bronze, muscle gravé."""
    it = obj('conso_force')
    it.col(1.0, 1.8, 6.4, 6.4, 'bronze')
    it.col(1.8, 3.6, 6.0, 6.0, 'c_force')
    it.col(3.6, 5.2, 4.6, 4.6, 'c_force')
    it.col(5.2, 6.4, 3.2, 3.2, 'c_glass')
    it.col(6.4, 8.6, 1.6, 1.6, 'c_glass')
    it.col(8.6, 9.8, 2.0, 2.0, 'c_cork')
    it.box((6.6, 2.2, 11.0), (9.4, 3.4, 11.1), 'gold')
    it.box((5.4, 2.0, 11.0), (6.0, 3.0, 11.06), 'c_shine')
    return it


def conso_celerite():
    """Fiole longue et fine, plume nouée au goulot."""
    it = obj('conso_celerite')
    it.col(1.0, 1.6, 3.0, 3.0, 'silver')
    bottle(it, 'c_celerite', 1.6, 2.4, 2.4, 9.0, fill=0.75, neck_w=1.2, neck_h=1.2)
    it.col(10.4, 11.0, 1.8, 1.8, 'silver')
    it.box((9.6, 7.6, 7.8), (11.8, 11.4, 8.2), 'feather')
    it.box((9.0, 10.4, 7.7), (10.0, 11.0, 8.3), 'b_rope')
    return it


def conso_vision():
    """Flacon rond à l'œil doré."""
    it = obj('conso_vision')
    it.col(1.4, 2.2, 3.6, 3.6, 'c_vision')
    it.col(2.2, 6.6, 6.0, 4.2, 'c_vision')
    it.col(3.0, 5.8, 6.8, 3.4, 'c_vision')
    it.col(6.6, 7.6, 3.6, 3.0, 'c_glass')
    it.col(7.6, 9.2, 1.4, 1.4, 'c_glass')
    it.col(9.2, 10.4, 1.8, 1.8, 'c_cork')
    it.box((6.6, 3.6, 10.1), (9.4, 5.2, 10.2), 'gold')
    it.box((7.6, 4.0, 10.2), (8.4, 4.8, 10.3), 'b_black')
    return it


def conso_fer():
    """Bouteille carrée cerclée de fer et rivetée."""
    it = obj('conso_fer')
    bottle(it, 'c_fer', 1.6, 5.0, 5.0, 6.4, fill=0.7, neck_w=1.8, neck_h=1.4, stopper='iron', stopper_h=1.4)
    for y in (1.2, 4.4, 7.6):
        it.col(y, y + 0.6, 5.4, 5.4, 'iron')
    for (x, z) in ((5.4, 10.7), (10.6, 10.7), (5.4, 5.3), (10.6, 5.3)):
        it.box((x - 0.3, y - 0.1, z - 0.1), (x + 0.3, y + 0.7, z + 0.1), 'bronze')
    return it


def conso_feu():
    """Bouteille trapue, bouchon en forme de flamme."""
    it = obj('conso_feu')
    top = bottle(it, 'c_feu', 1.4, 5.2, 5.2, 5.0, fill=0.7, neck_w=1.8, neck_h=1.4, stopper='b_copper', stopper_h=0.8)
    it.col(top, top + 1.4, 1.6, 1.6, 'flame')
    it.col(top + 1.4, top + 2.4, 0.9, 0.9, 'flame')
    it.box((7.4, top + 0.4, 8.8), (8.4, top + 1.8, 9.2), 'ember')
    return it


def conso_elixir_heros():
    """Haute bouteille violette, couronne d'or en bouchon."""
    it = obj('conso_elixir_heros')
    it.col(0.8, 1.6, 4.6, 4.6, 'gold')
    bottle(it, 'c_heros', 1.6, 4.0, 4.0, 7.0, fill=0.75, neck_w=1.6, neck_h=1.4, stopper='gold', stopper_h=0.8)
    it.col(4.4, 5.0, 4.4, 4.4, 'gold')
    for (x, z) in ((7.0, 7.0), (9.0, 7.0), (7.0, 9.0), (9.0, 9.0)):
        it.box((x - 0.3, 10.8, z - 0.3), (x + 0.3, 11.8, z + 0.3), 'gold')
    it.col(10.8, 11.4, 1.0, 1.0, 'amethyst')
    return it


def conso_renaissance():
    """Fiole ardente dans une cage d'or en forme de phénix."""
    it = obj('conso_renaissance')
    it.col(0.8, 1.6, 4.4, 4.4, 'gold')
    bottle(it, 'ember', 1.6, 2.8, 2.8, 5.0, fill=0.8, neck_w=1.2, neck_h=1.0, stopper='gold', stopper_h=0.8)
    for (x, z) in ((5.8, 5.8), (10.2, 5.8), (5.8, 10.2), (10.2, 10.2)):
        it.box((x - 0.3, 1.6, z - 0.3), (x + 0.3, 7.0, z + 0.3), 'gold')
    it.col(7.0, 7.6, 4.6, 4.6, 'gold')
    for s in (1, -1):
        x = lambda v: 8 + s * v
        it.box((min(x(2.2), x(4.0)), 5.0, 7.6), (max(x(2.2), x(4.0)), 7.6, 8.4), 'ember')
        it.box((min(x(3.6), x(5.2)), 6.4, 7.7), (max(x(3.6), x(5.2)), 9.0, 8.3), 'flame')
    it.col(8.4, 9.4, 1.2, 1.2, 'flame')
    return it


# ------------------------------------------------------------------ vivres et soins

def conso_bandage():
    """Rouleau de bandage, croix rouge, bout déroulé."""
    it = obj('conso_bandage')
    it.box((3.6, 2.0, 5.4), (12.4, 7.2, 10.6), 'c_cloth')
    it.box((3.2, 2.4, 5.0), (12.8, 6.8, 11.0), 'c_cloth')
    it.box((3.0, 3.4, 7.2), (3.2, 5.8, 8.8), 'c_label')
    it.box((12.8, 3.4, 7.2), (13.0, 5.8, 8.8), 'c_label')
    it.box((7.2, 2.4, 11.0), (8.8, 6.8, 11.1), 'c_wax_red')
    it.box((5.8, 3.8, 11.0), (10.2, 5.4, 11.1), 'c_wax_red')
    it.box((5.0, 1.2, 10.4), (11.0, 2.0, 14.0), 'c_cloth')
    return it


def conso_ration():
    """Pain enveloppé dans un torchon noué."""
    it = obj('conso_ration')
    it.box((2.6, 1.2, 4.8), (13.4, 3.6, 11.2), 'c_cloth')
    it.box((3.4, 3.6, 5.4), (12.6, 6.4, 10.6), 'c_bread')
    it.box((4.4, 6.4, 6.2), (11.6, 7.4, 9.8), 'c_bread')
    for x in (5.6, 8.0, 10.4):
        it.box((x - 0.3, 6.6, 6.0), (x + 0.3, 7.5, 10.0), 'b_bark')
    it.box((7.4, 1.2, 4.6), (8.6, 5.0, 11.4), 'b_rope')
    it.box((2.0, 2.4, 6.8), (2.6, 4.4, 9.2), 'c_cloth')
    return it


# ------------------------------------------------------------------ outils de réparation de Gorm

def outil_reparation_commun():
    """Trousse de rémouleur : étui de cuir, lime et pierre qui dépassent."""
    it = obj('outil_reparation_commun')
    it.box((3.6, 1.0, 6.2), (12.4, 7.0, 9.8), 'leather')
    it.box((3.6, 5.2, 9.8), (12.4, 7.0, 10.2), 'leather_dark')
    it.box((7.4, 3.6, 9.8), (8.6, 5.2, 10.1), 'bronze')
    it.box((4.6, 7.0, 7.2), (5.8, 11.6, 8.4), 'iron')
    it.box((4.6, 7.0, 7.2), (5.8, 8.2, 8.4), 'wood')
    it.box((9.4, 7.0, 6.8), (11.6, 9.4, 9.0), 'c_stone')
    it.box((7.0, 7.0, 7.4), (7.8, 10.4, 8.2), 'steel')
    return it


def outil_reparation_peu_commun():
    """Pierre à aiguiser naine dans un cadre de bronze gravé."""
    it = obj('outil_reparation_peu_commun')
    it.box((2.4, 1.0, 5.4), (13.6, 2.2, 10.6), 'bronze')
    it.box((3.0, 2.2, 6.0), (13.0, 5.0, 10.0), 'c_stone')
    it.box((2.4, 2.2, 5.4), (3.4, 5.4, 10.6), 'bronze')
    it.box((12.6, 2.2, 5.4), (13.6, 5.4, 10.6), 'bronze')
    for x in (5.0, 8.0, 11.0):
        it.box((x - 0.4, 1.4, 10.6), (x + 0.4, 1.9, 10.7), 'gold')
    it.box((4.0, 5.0, 7.6), (12.0, 5.2, 8.4), 'c_shine')
    return it


def outil_reparation_rare():
    """Marteau de maître-forgeron, tête dorée sur manche de chêne."""
    it = obj('outil_reparation_rare')
    it.col(0.8, 1.6, 1.8, 1.8, 'gold_dark')
    it.col(1.6, 10.0, 1.2, 1.2, 'wood')
    it.col(1.8, 5.0, 1.5, 1.5, 'leather')
    it.box((4.0, 10.0, 6.6), (12.0, 12.8, 9.4), 'steel_dark')
    it.box((3.4, 9.8, 6.4), (4.4, 13.0, 9.6), 'gold')
    it.box((11.6, 9.8, 6.4), (12.6, 13.0, 9.6), 'gold')
    it.box((7.0, 10.4, 9.4), (9.0, 12.4, 9.6), 'gold')
    return it


def outil_reparation_epique():
    """Enclume runique portative."""
    it = obj('outil_reparation_epique')
    it.box((4.6, 0.8, 5.0), (11.4, 2.4, 11.0), 'b_black_steel')
    it.box((6.0, 2.4, 6.4), (10.0, 5.2, 9.6), 'b_black_steel')
    it.box((2.6, 5.2, 5.6), (13.4, 8.0, 10.4), 'b_black_steel')
    it.box((0.8, 5.8, 6.8), (2.6, 7.6, 9.2), 'b_black_steel')
    it.box((13.4, 6.4, 7.2), (14.6, 7.6, 8.8), 'b_black_steel')
    it.box((5.0, 5.8, 10.4), (11.0, 7.4, 10.5), 'rune_glow')
    it.box((5.0, 5.8, 5.5), (11.0, 7.4, 5.6), 'rune_glow')
    it.box((4.0, 8.0, 7.4), (12.0, 8.1, 8.6), 'arcane')
    return it


def outil_reparation_legendaire():
    """Feu de forge draconique : vasque d'écailles, braises et flamme."""
    it = obj('outil_reparation_legendaire')
    it.col(0.8, 2.0, 4.4, 4.4, 'b_black_steel')
    it.col(2.0, 3.6, 2.4, 2.4, 'b_black_steel')
    it.col(3.6, 5.0, 7.6, 7.6, 'b_dragon')
    it.col(5.0, 6.6, 9.4, 9.4, 'b_dragon')
    it.col(6.2, 7.0, 8.4, 8.4, 'b_dragon_glow')
    for (x, z) in ((3.2, 3.2), (12.8, 3.2), (3.2, 12.8), (12.8, 12.8)):
        it.box((x - 0.5, 5.0, z - 0.5), (x + 0.5, 8.0, z + 0.5), 'b_horn')
    it.col(7.0, 9.0, 4.0, 4.0, 'flame')
    it.col(9.0, 11.0, 2.4, 2.4, 'flame')
    it.col(11.0, 12.4, 1.0, 1.0, 'flame')
    it.box((5.4, 7.0, 7.4), (6.6, 9.4, 8.6), 'ember')
    it.box((9.4, 7.0, 7.4), (10.6, 8.6, 8.6), 'ember')
    return it


CONSOMMABLES = [
    conso_soin_mineure, conso_mana_mineure, conso_bandage, conso_ration,
    conso_soin, conso_mana, conso_force, conso_celerite, conso_vision,
    conso_grande_soin, conso_grande_mana, conso_fer, conso_feu,
    conso_soin_supreme, conso_mana_supreme, conso_elixir_heros, conso_renaissance,
]
OUTILS = [outil_reparation_commun, outil_reparation_peu_commun, outil_reparation_rare, outil_reparation_epique,
          outil_reparation_legendaire]
