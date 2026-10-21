"""Armes des monstres (butin MythicMobs) et meubles de planque, objets Oraxen.

Mêmes modèles 3D que catalog.py (namespace evo). Côté serveur, les objets Oraxen pointent dessus avec
components.item_model: evo:<id> (voir src/items/oraxen/items/*.yml, recopiés dans plugins/Oraxen/items/).
"""
from kit import Item, Mat, MATS, BOW, OBJECT, grain
from catalog import SWORD, tip

MATS.update({
    'rust': Mat((128, 84, 58), 18, 0.72),
    'rust_steel': Mat((120, 112, 104), 16, 0.72),
    'bone_dark': Mat((168, 156, 128), 10, 0.78),
    'ice': Mat((170, 220, 245), 10, 0.85, 0.1, light=6, hi=(240, 255, 255)),
    'frost_glow': Mat((150, 235, 255), 6, 0.95, light=14, hi=(255, 255, 255)),
    'cult_steel': Mat((60, 48, 80), 8, 0.75, hi=(140, 110, 190)),
    'void_glow': Mat((190, 80, 255), 8, 0.95, light=12),
    'club_wood': Mat((96, 70, 44), 12, 0.78, pattern=grain),
    'forge_iron': Mat((70, 66, 64), 10, 0.72),
    'wax': Mat((236, 226, 196), 6, 0.9),
    'flame': Mat((255, 196, 80), 6, 1.0, light=15),
    'glass': Mat((200, 228, 240), 4, 0.95),
    'lit_glass': Mat((255, 190, 90), 6, 1.0, light=15, pattern=lambda c, p, face, px, py, w, hgt: (
        (255, 246, 200) if abs(px - (w - 1) / 2) <= w * 0.18 and hgt * 0.35 <= py <= hgt * 0.75
        else (255, 214, 120) if abs(px - (w - 1) / 2) <= w * 0.34 and hgt * 0.15 <= py <= hgt * 0.9 else c)),
    'plank': Mat((150, 108, 64), 8, 0.85, pattern=grain),
    'plank_dark': Mat((98, 66, 40), 8, 0.85, pattern=grain),
    'cushion': Mat((140, 36, 40), 8, 0.85),
})

# Meubles : posés par Oraxen sur une entité d'affichage, en transformation « fixed » (taille réelle).
FURNITURE = dict(OBJECT)
FURNITURE.update({
    'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
    'gui': {'rotation': [25, 145, 0], 'translation': [0, -1, 0], 'scale': [0.6] * 3},
    'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.35] * 3},
    'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.3] * 3},
    'thirdperson_lefthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.3] * 3},
    'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.35] * 3},
    'firstperson_lefthand': {'rotation': [0, 225, 0], 'translation': [0, 0, 0], 'scale': [0.35] * 3},
})


# =====================================================================================
#  Armes des monstres
# =====================================================================================

def mob_dague_rouillee():
    """Gobelin pillard : lame courte ébréchée, manche ficelé."""
    it = Item('mob_dague_rouillee', tilt=SWORD)
    it.col(-1.6, -0.6, 1.6, 1.6, 'rust')
    it.col(-0.6, 4.0, 1.2, 1.2, 'leather_dark')
    it.box((5.6, 4.0, 7.4), (10.4, 4.9, 8.6), 'rust')
    it.col(4.9, 11.0, 2.0, 0.8, 'rust_steel')
    it.box((8.6, 6.4, 7.5), (9.1, 7.4, 8.5), 'rust')      # encoche
    it.box((6.9, 8.6, 7.5), (7.4, 9.6, 8.5), 'rust')
    it.col(11.0, 12.2, 1.3, 0.7, 'rust_steel')
    it.col(12.2, 13.0, 0.6, 0.6, 'rust_steel')
    return it


def mob_arc_os():
    """Squelette errant : arc en os et tendons."""
    def bow(pull):
        it = Item('mob_arc_os', tilt=45, display=BOW)
        limb = [(8.0, 11.0, 9.2, 10.4), (11.0, 14.0, 8.4, 9.6), (14.0, 16.4, 7.4, 8.6), (16.4, 18.4, 6.2, 7.4)]
        for n, (y0, y1, x0, x1) in enumerate(limb):
            mat = 'bone' if n % 2 == 0 else 'bone_dark'
            it.box((x0, y0, 7.5), (x1, y1, 8.5), mat)
            it.box((x0, 16 - y1, 7.5), (x1, 16 - y0, 8.5), mat)
        for (y, x0, x1) in ((11.0, 8.2, 10.6), (14.0, 7.2, 9.8), (16.4, 6.0, 8.8)):
            it.box((x0, y - 0.3, 7.35), (x1, y + 0.3, 8.65), 'bone_dark')
            it.box((x0, 16 - y - 0.3, 7.35), (x1, 16 - y + 0.3, 8.65), 'bone_dark')
        it.box((5.4, 18.4, 7.6), (6.6, 19.4, 8.4), 'bone')
        it.box((5.4, -3.4, 7.6), (6.6, -2.4, 8.4), 'bone')
        it.box((9.0, 6.0, 7.3), (10.8, 10.0, 8.7), 'leather_dark')
        sx, steps = 5.9, 4
        for half in (1, -1):
            for k in range(steps):
                t0, t1 = k / steps, (k + 1) / steps
                x = sx - pull * (1 - (t0 + t1) / 2)
                ya, yb = 8 + half * 11 * t0, 8 + half * 11 * t1
                it.box((x - 0.15, min(ya, yb), 7.9), (x + 0.15, max(ya, yb), 8.1), 'string')
        if pull:
            x0 = sx - pull
            it.box((x0, 7.85, 7.85), (x0 + 11.5, 8.15, 8.15), 'bone_dark')
            it.box((x0 + 11.5, 7.5, 7.8), (x0 + 12.7, 8.5, 8.2), 'rust_steel')
            it.box((x0 + 0.2, 7.3, 7.95), (x0 + 2.0, 8.7, 8.05), 'feather')
        return it

    base = bow(0)
    base.variants = {f'_pulling_{i}': bow(p) for i, p in enumerate((1.4, 2.6, 3.6))}
    return base


def mob_lame_chevalier():
    """Chevalier squelette : épée longue d'acier noirci, garde en croix usée."""
    it = Item('mob_lame_chevalier', tilt=SWORD)
    it.col(-3.0, -1.8, 1.9, 1.9, 'steel_dark')
    it.col(-1.8, 3.4, 1.3, 1.3, 'leather_dark')
    it.box((3.6, 3.4, 7.3), (12.4, 4.6, 8.7), 'steel_dark')
    it.box((3.0, 3.0, 7.4), (4.0, 5.0, 8.6), 'iron')
    it.box((12.0, 3.0, 7.4), (13.0, 5.0, 8.6), 'iron')
    it.col(4.6, 16.4, 1.8, 0.9, 'iron')
    it.box((7.65, 5.2, 7.4), (8.35, 15.0, 8.6), 'steel_dark')
    it.box((8.9, 9.0, 7.5), (9.3, 10.0, 8.5), 'steel_dark')  # entaille
    tip(it, 16.4, 2.5, 0.9, 'iron')
    return it


def mob_hachoir_orc():
    """Orc brute : hachoir massif, fer brut et manche épais."""
    it = Item('mob_hachoir_orc', tilt=SWORD)
    it.col(-3.0, 15.0, 1.8, 1.8, 'club_wood')
    it.col(-2.6, 2.0, 2.0, 2.0, 'leather_dark')
    it.box((8.9, 9.0, 7.4), (15.6, 16.6, 8.6), 'rust_steel')
    it.box((15.0, 8.4, 7.5), (16.0, 17.2, 8.5), 'iron')
    it.col(15.0, 16.0, 2.4, 2.4, 'rust')
    for y in (10.4, 13.0, 15.4):
        it.box((9.2, y, 8.6), (10.0, y + 0.8, 8.8), 'rust')
    it.col(16.0, 17.6, 1.0, 1.0, 'rust_steel')
    return it


def mob_dague_culte():
    """Cultiste de l'Ombre : dague rituelle ondulée, gemme du vide."""
    it = Item('mob_dague_culte', tilt=SWORD)
    it.col(-1.4, -0.4, 1.4, 1.4, 'void_glow')
    it.col(-0.4, 3.8, 1.2, 1.2, 'leather_dark')
    it.box((5.0, 3.8, 7.4), (11.0, 4.6, 8.6), 'cult_steel')
    it.box((4.6, 4.6, 7.5), (5.4, 5.8, 8.5), 'cult_steel')
    it.box((10.6, 4.6, 7.5), (11.4, 5.8, 8.5), 'cult_steel')
    it.col(4.4, 5.4, 1.4, 1.4, 'void_glow')
    for n, y in enumerate(range(5, 13)):
        dx = 0.5 if n % 2 == 0 else -0.5
        it.box((7.1 + dx, y, 7.6), (8.9 + dx, y + 1, 8.4), 'cult_steel')
    it.box((7.8, 5.4, 8.4), (8.2, 12.0, 8.5), 'void_glow')
    it.col(13.0, 14.2, 0.9, 0.6, 'cult_steel')
    return it


def mob_massue_troll():
    """Troll des marais : gourdin noueux hérissé de pointes."""
    it = Item('mob_massue_troll', tilt=SWORD)
    it.col(-3.0, 6.0, 1.6, 1.6, 'club_wood')
    it.col(-2.4, 1.0, 1.9, 1.9, 'leather_dark')
    it.col(6.0, 9.0, 2.6, 2.6, 'club_wood')
    it.col(9.0, 11.0, 3.6, 3.6, 'club_wood')
    it.col(11.0, 17.0, 5.0, 5.0, 'club_wood')
    it.col(17.0, 18.6, 3.6, 3.6, 'club_wood')
    it.col(12.4, 13.6, 5.2, 5.2, 'moss')
    it.box((5.4, 15.0, 5.4), (7.0, 16.4, 7.0), 'moss')
    for (x, y, z) in ((5.1, 12.0, 8), (10.9, 15.0, 8), (8, 16.0, 5.1), (8, 14.6, 10.9), (5.1, 16.0, 8),
                      (10.9, 11.6, 8), (8, 11.8, 5.1), (8, 17.2, 10.9)):
        it.box((x - 0.5, y - 0.5, z - 0.5), (x + 0.5, y + 0.5, z + 0.5), 'bone')
    return it


def mob_hache_chef():
    """Chef de guerre orc : grande hache à double tranchant, chiffon rouge."""
    it = Item('mob_hache_chef', tilt=SWORD)
    it.col(-3.4, -2.4, 2.0, 2.0, 'bronze')
    it.col(-2.4, 18.0, 1.4, 1.4, 'wood_dark')
    it.col(-1.6, 3.0, 1.7, 1.7, 'leather')
    it.col(11.0, 16.6, 2.2, 2.2, 'bronze')
    for side in (1, -1):
        x0, x1 = (9.1, 13.6) if side > 0 else (2.4, 6.9)
        it.box((x0, 11.6, 7.4), (x1, 16.0, 8.6), 'iron')
        ex = (13.4, 14.6) if side > 0 else (1.4, 2.6)
        it.box((ex[0], 10.4, 7.5), (ex[1], 17.2, 8.5), 'edge')
    it.box((9.0, 9.4, 7.2), (10.6, 11.0, 8.8), 'cloth_red')
    it.box((9.6, 7.0, 7.4), (10.4, 9.4, 8.6), 'cloth_red')
    it.col(18.0, 19.4, 0.8, 0.8, 'bronze')
    return it


def mob_baton_givre():
    """Liche mineure : bâton de bois pâle coiffé d'un cristal de glace."""
    it = Item('mob_baton_givre', tilt=SWORD)
    it.col(-3.4, 13.0, 1.2, 1.2, 'wood_pale')
    it.col(-3.6, -2.6, 1.6, 1.6, 'silver')
    it.col(3.0, 5.0, 1.5, 1.5, 'leather_dark')
    it.col(12.6, 13.6, 2.2, 2.2, 'silver')
    for (x, z) in ((6.6, 8), (9.4, 8), (8, 6.6), (8, 9.4)):
        it.box((x - 0.35, 13.4, z - 0.35), (x + 0.35, 15.6, z + 0.35), 'silver')
    it.col(14.0, 17.6, 1.8, 1.8, 'ice')
    it.col(14.6, 17.0, 1.0, 1.0, 'frost_glow')
    it.col(17.6, 18.8, 1.0, 1.0, 'ice')
    return it


def mob_lame_roi_liche():
    """Morvhal le Roi-Liche : espadon d'os et de glace, gemme d'améthyste."""
    it = Item('mob_lame_roi_liche', tilt=SWORD)
    it.col(-3.6, -2.4, 2.0, 2.0, 'amethyst')
    it.col(-2.4, 3.0, 1.4, 1.4, 'bone_dark')
    it.box((2.4, 3.0, 7.3), (13.6, 4.4, 8.7), 'bone')
    it.box((1.6, 3.4, 7.5), (2.6, 5.6, 8.5), 'bone')
    it.box((13.4, 3.4, 7.5), (14.4, 5.6, 8.5), 'bone')
    it.col(3.4, 4.4, 1.8, 1.8, 'amethyst')
    it.col(4.4, 17.4, 2.4, 1.0, 'ice')
    it.box((7.6, 5.0, 7.45), (8.4, 16.0, 8.55), 'frost_glow')
    for y in (6.0, 9.0, 12.0):
        it.box((6.2, y, 7.6), (6.8, y + 1.4, 8.4), 'bone')
        it.box((9.2, y + 1.4, 7.6), (9.8, y + 2.8, 8.4), 'bone')
    tip(it, 17.4, 3.0, 1.0, 'ice')
    return it


def mob_marteau_gardien():
    """Gardien de la Forge : marteau de forge, cœur de braise."""
    it = Item('mob_marteau_gardien', tilt=SWORD)
    it.col(-3.4, -2.4, 1.9, 1.9, 'forge_iron')
    it.col(-2.4, 12.6, 1.3, 1.3, 'wood_dark')
    it.col(-1.8, 3.0, 1.6, 1.6, 'leather_dark')
    it.box((3.6, 12.6, 6.0), (12.4, 17.8, 10.0), 'forge_iron')
    it.box((3.2, 12.2, 5.6), (4.2, 18.2, 10.4), 'bronze')
    it.box((11.8, 12.2, 5.6), (12.8, 18.2, 10.4), 'bronze')
    it.box((6.6, 14.0, 9.9), (9.4, 16.4, 10.3), 'ember')
    it.box((6.6, 14.0, 5.7), (9.4, 16.4, 6.1), 'ember')
    it.col(17.8, 18.6, 1.0, 1.0, 'bronze')
    return it


# =====================================================================================
#  Meubles de planque
# =====================================================================================

def furniture(id):
    return Item(id, density=2, display=FURNITURE)


def meuble_chaise():
    """Chaise de bois à coussin rouge (assise à 7 px du sol)."""
    it = furniture('meuble_chaise')
    for x in (3, 11.6):
        for z in (3, 11.6):
            it.box((x, 0, z), (x + 1.4, 7, z + 1.4), 'plank_dark')
    it.box((2.6, 7, 2.6), (13.4, 8.4, 13.4), 'plank')
    it.box((3.2, 8.4, 3.2), (12.8, 9.2, 11.6), 'cushion')
    for x in (3, 11.6):
        it.box((x, 8.4, 11.6), (x + 1.4, 20, 13.0), 'plank_dark')
    it.box((4.4, 13, 11.9), (11.6, 18.6, 12.7), 'plank')
    it.box((2.8, 19.4, 11.4), (13.2, 20.6, 13.2), 'plank_dark')
    it.box((3, 2.2, 4.4), (4.4, 3.0, 11.6), 'plank_dark')
    it.box((11.6, 2.2, 4.4), (13.0, 3.0, 11.6), 'plank_dark')
    return it


def meuble_etagere():
    """Étagère à trois planches, avec livres, bocaux et sacoche (fond du même côté que le dossier de la chaise)."""
    it = furniture('meuble_etagere')
    it.box((0.5, 0, 4), (1.7, 16, 12), 'plank_dark')
    it.box((14.3, 0, 4), (15.5, 16, 12), 'plank_dark')
    it.box((1.7, 0, 11.2), (14.3, 16, 12), 'plank_dark')
    for y in (0, 5.4, 10.8, 15):
        it.box((1.7, y, 4), (14.3, y + 1, 11.2), 'plank')
    # livres
    for n, x in enumerate((2.2, 3.7, 5.0, 6.6, 8.0)):
        mat = ('cloth_red', 'cloth_blue', 'cloth_green', 'leather', 'cloth_red')[n]
        it.box((x, 1, 5.2), (x + 1.3, 4.8 - (n % 2) * 0.7, 10.8), mat)
    it.box((10.0, 1, 5.4), (13.6, 2.6, 10.6), 'paper')
    # bocaux
    for x in (2.4, 6.2):
        it.box((x, 6.4, 5.6), (x + 3.0, 9.6, 9.4), 'glass')
        it.box((x + 0.5, 9.6, 6.0), (x + 2.5, 10.4, 9.0), 'wood')
    it.box((10.2, 6.4, 5.8), (13.4, 8.8, 9.6), 'emerald')
    it.box((2.4, 11.8, 6.0), (5.6, 13.8, 10.2), 'bone')
    it.box((7.6, 11.8, 5.6), (13.4, 14.6, 10.4), 'leather_bag')
    it.box((10.0, 12.6, 5.3), (11.0, 13.6, 5.6), 'gold')
    return it


def meuble_lanterne():
    """Lanterne de fer forgé à bougie, qui éclaire."""
    it = furniture('meuble_lanterne')
    it.box((4.5, 0, 4.5), (11.5, 1.2, 11.5), 'forge_iron')
    # vitres éclairées par la bougie (opaques : le rendu d'objet ne gère pas la transparence partielle ici)
    it.box((5, 1.2, 5), (11, 9.6, 11), 'lit_glass', faces={'up': 'forge_iron', 'down': 'forge_iron'})
    for x in (4.6, 10.6):
        for z in (4.6, 10.6):
            it.box((x, 1.2, z), (x + 0.8, 9.6, z + 0.8), 'forge_iron')
    it.box((7, 1.2, 7), (9, 5.2, 9), 'wax')
    it.box((7.4, 5.2, 7.4), (8.6, 7.0, 8.6), 'flame', light=15)
    it.box((4.5, 9.6, 4.5), (11.5, 10.8, 11.5), 'forge_iron')
    it.box((6, 10.8, 6), (10, 12.0, 10), 'forge_iron')
    it.box((7.4, 12.0, 7.6), (8.6, 14.2, 8.4), 'forge_iron')
    return it


MOB_WEAPONS = [mob_dague_rouillee, mob_arc_os, mob_lame_chevalier, mob_hachoir_orc, mob_dague_culte,
               mob_massue_troll, mob_hache_chef, mob_baton_givre, mob_lame_roi_liche, mob_marteau_gardien]
FURNITURE_ITEMS = [meuble_chaise, meuble_etagere, meuble_lanterne]
