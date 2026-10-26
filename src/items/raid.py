"""Clé de raid (ressource EvoExtract cle_raid) et coffre de boss (EvoPerso BossChest, entité d'affichage FIXED)."""
import consommables  # noqa: F401  (matériaux c_*)
from kit import Item, Mat, MATS, OBJECT
from mobs import FURNITURE

MATS.update({
    'r_iron': Mat((70, 72, 82), 8, 0.72, hi=(140, 144, 160)),
    'r_wood': Mat((86, 46, 30), 8, 0.8),
    'r_inside': Mat((40, 20, 14), 6, 0.9),
    'r_velvet': Mat((120, 20, 40), 8, 0.85),
})


def cle_raid():
    """Grande clé d'or : anneau à rune lumineuse, tige torsadée, panneton à dents."""
    it = Item('cle_raid', density=4, display=OBJECT)
    # anneau
    it.box((5.0, 9.0, 7.4), (11.0, 10.2, 8.6), 'gold')
    it.box((5.0, 14.6, 7.4), (11.0, 15.8, 8.6), 'gold')
    it.box((4.0, 10.0, 7.4), (5.4, 14.8, 8.6), 'gold')
    it.box((10.6, 10.0, 7.4), (12.0, 14.8, 8.6), 'gold')
    it.box((6.6, 11.2, 7.6), (9.4, 13.6, 8.4), 'b_gold_rune')
    it.box((7.4, 15.8, 7.6), (8.6, 16.8, 8.4), 'ruby')
    # tige
    it.col(1.8, 9.0, 1.4, 1.4, 'gold')
    for y in (3.0, 5.2, 7.4):
        it.col(y, y + 0.6, 1.8, 1.8, 'gold_dark')
    # panneton
    it.box((8.7, 1.4, 7.5), (11.4, 2.8, 8.5), 'gold')
    it.box((9.4, 2.8, 7.5), (10.4, 4.0, 8.5), 'gold')
    it.box((10.6, 2.8, 7.5), (11.4, 3.6, 8.5), 'gold')
    it.box((8.7, 4.0, 7.5), (10.6, 4.8, 8.5), 'gold')
    return it


def _coffre(id, ouvert):
    it = Item(id, density=4, display=FURNITURE)
    # caisse
    it.box((1.0, 0.0, 3.0), (15.0, 8.0, 13.0), 'r_wood')
    for x in (1.0, 14.0):
        it.box((x - 0.2, 0.0, 2.8), (x + 1.2, 8.2, 13.2), 'r_iron')
    it.box((0.8, 0.0, 2.8), (15.2, 1.0, 13.2), 'r_iron')
    it.box((6.8, 1.0, 2.8), (9.2, 8.0, 3.0), 'gold')
    # serrure dorée et rune
    it.box((6.6, 4.0, 2.4), (9.4, 7.6, 2.8), 'gold')
    it.box((7.6, 4.6, 2.2), (8.4, 6.2, 2.4), 'b_black')
    it.box((2.6, 2.6, 2.9), (5.4, 5.4, 3.0), 'b_gold_rune')
    it.box((10.6, 2.6, 2.9), (13.4, 5.4, 3.0), 'b_gold_rune')
    if not ouvert:
        it.box((1.0, 8.0, 3.0), (15.0, 11.0, 13.0), 'r_wood')
        it.box((2.0, 11.0, 4.0), (14.0, 12.4, 12.0), 'r_wood')
        for x in (1.0, 14.0):
            it.box((x - 0.2, 8.0, 2.8), (x + 1.2, 11.2, 13.2), 'r_iron')
        it.box((1.8, 11.0, 7.0), (14.2, 12.6, 9.0), 'gold')
        it.box((6.6, 7.6, 2.4), (9.4, 10.0, 2.8), 'gold')
    else:
        # intérieur, trésor qui brille, couvercle relevé à l'arrière
        it.box((2.2, 6.0, 4.2), (13.8, 7.8, 11.8), 'b_sun', light=12)
        it.box((3.4, 7.8, 5.4), (6.0, 8.8, 8.0), 'gold')
        it.box((9.0, 7.8, 6.6), (11.4, 9.0, 9.4), 'ruby')
        it.box((6.6, 7.8, 8.6), (8.6, 8.6, 10.6), 'sapphire')
        it.box((1.0, 8.0, 12.0), (15.0, 18.0, 15.0), 'r_wood')
        for x in (1.0, 14.0):
            it.box((x - 0.2, 8.0, 11.8), (x + 1.2, 18.2, 15.2), 'r_iron')
        it.box((1.0, 8.0, 11.6), (15.0, 18.0, 12.0), 'r_velvet')
    return it


def coffre_raid():
    return _coffre('coffre_raid', False)


def coffre_raid_ouvert():
    return _coffre('coffre_raid_ouvert', True)


RAID = [cle_raid, coffre_raid, coffre_raid_ouvert]
