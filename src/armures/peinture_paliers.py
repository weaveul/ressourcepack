"""Plastrons, jambières et bottes par palier de rareté : un dessin propre à chaque classe et à chaque palier.

Le palier rare garde le peintre de peinture_hd.py. Les autres sont décrits par une « tenue » (Outfit) : matériaux du
corps, des épaules, des manches, des jambes et des bottes, plus des détails peints sur l'avant et le dos. Les calques
d'armure collent au corps du joueur : la forme change par le dessin (plaques, capes, fourrures, robes), pas en volume.
"""
import math

from kit import Mat, MATS, h, mix
from casques3d import hammered, brushed, filigree, cloth_folds, starry, fur, bark_grain, leaves, feathers
from peinture_hd import chain, scales_hd, leather_soft, vines


def quilted(c, p, face, px, py, w, hgt):
    """Gambison matelassé : losanges cousus."""
    x, y = p[0] * 4, p[1] * 4
    if int(x + y) % 4 == 0 or int(x - y) % 4 == 0:
        return tuple(v * 0.78 for v in c)
    return c


def studded(c, p, face, px, py, w, hgt):
    if px % 3 == 1 and py % 3 == 1:
        return (200, 196, 186)
    return leather_soft(c, p, face, px, py, w, hgt)


def cracks(c, p, face, px, py, w, hgt):
    """Plaque noire fendue de lumière violette."""
    x, y = p[0] * 4, p[1] * 4
    if abs(math.sin(x * 0.9 + y * 0.35) + math.sin(y * 0.7 - x * 0.2)) < 0.12:
        return (200, 110, 255)
    return c


def veins(c, p, face, px, py, w, hgt):
    """Bois vivant parcouru de sève lumineuse."""
    x, y = p[0] * 4, p[1] * 4
    if abs(x % 6 - 3 - 1.5 * math.sin(y / 2.5)) < 0.45:
        return (120, 255, 130)
    return bark_grain(c, p, face, px, py, w, hgt)


def stars_lines(c, p, face, px, py, w, hgt):
    """Robe céleste : étoiles et traits de constellation."""
    x, y = int(p[0] * 4), int(p[1] * 4)
    if h(x, y, 7) > 0.965:
        return (255, 240, 180)
    if abs((x - y * 0.6) % 9 - 4.5) < 0.3 and h(x // 9, y // 5, 3) > 0.5:
        return (150, 190, 255)
    return c


def circuits(c, p, face, px, py, w, hgt):
    x, y = int(p[0] * 4), int(p[1] * 4)
    if (x % 5 == 2 and h(x // 5, y // 4, 11) > 0.45) or (y % 6 == 3 and h(x // 4, y // 6, 13) > 0.6):
        return (90, 220, 255)
    return c


MATS.update({
    # matériaux simples (commun)
    'pc_gambeson': Mat((170, 150, 116), 6, 0.86, pattern=quilted),
    'pc_gambeson_d': Mat((126, 108, 82), 6, 0.86, pattern=quilted),
    'pc_linen': Mat((176, 162, 130), 8, 0.86, pattern=cloth_folds),
    'pc_linen_d': Mat((132, 118, 92), 8, 0.86, pattern=cloth_folds),
    'pc_rope': Mat((150, 120, 76), 6, 0.8),
    'pc_robe_brown': Mat((98, 72, 52), 6, 0.86, pattern=cloth_folds),
    'pc_robe_violet': Mat((70, 52, 96), 6, 0.86, pattern=cloth_folds),
    'pc_robe_green': Mat((70, 92, 58), 6, 0.86, pattern=cloth_folds),
    'pc_leather': Mat((104, 70, 42), 6, 0.78, pattern=leather_soft),
    'pc_leather_d': Mat((70, 48, 30), 6, 0.78, pattern=leather_soft),
    'pc_studded': Mat((60, 44, 32), 6, 0.78, pattern=studded),
    'pc_iron': Mat((120, 124, 134), 8, 0.72, pattern=hammered, hi=(180, 184, 194)),
    'pc_chain': Mat((120, 124, 134), 6, 0.85, pattern=chain),
    'pc_white': Mat((222, 218, 206), 6, 0.86, pattern=cloth_folds),
    # épique
    'pe_scale': Mat((150, 120, 70), 6, 0.8, pattern=scales_hd),
    'pe_fur': Mat((120, 96, 70), 14, 0.9, pattern=fur),
    'pe_fur_l': Mat((200, 190, 170), 12, 0.9, pattern=fur),
    'pe_silver': Mat((206, 210, 222), 5, 0.74, pattern=brushed, hi=(255, 255, 255)),
    'pe_gold': Mat((226, 182, 74), 6, 0.74, pattern=filigree, hi=(255, 236, 150)),
    'pe_blue': Mat((40, 64, 148), 6, 0.84, pattern=cloth_folds),
    'pe_crimson': Mat((128, 26, 40), 6, 0.86, pattern=cloth_folds),
    'pe_crimson_d': Mat((84, 18, 28), 6, 0.86, pattern=cloth_folds),
    'pe_rune_band': Mat((214, 170, 70), 6, 0.8, pattern=filigree),
    'pe_black_leather': Mat((44, 38, 36), 6, 0.78, pattern=leather_soft),
    'pe_bark': Mat((100, 72, 44), 6, 0.78, pattern=bark_grain),
    'pe_moss': Mat((86, 126, 58), 12, 0.85, pattern=fur),
    'pe_steel_dark': Mat((62, 60, 74), 6, 0.76, pattern=hammered, hi=(120, 118, 140)),
    'pe_owl': Mat((150, 118, 80), 8, 0.86, pattern=feathers),
    'pe_owl_l': Mat((222, 206, 172), 8, 0.86, pattern=feathers),
    'pe_crystal': Mat((120, 220, 255), 6, 0.9, light=12, hi=(230, 250, 255)),
    # légendaire
    'pl_dragon': Mat((70, 26, 26), 6, 0.78, pattern=scales_hd),
    'pl_dragon_plate': Mat((44, 36, 40), 6, 0.74, pattern=hammered, hi=(110, 70, 70)),
    'pl_ember': Mat((255, 110, 40), 6, 0.95, light=15, hi=(255, 210, 140)),
    'pl_white_gold': Mat((236, 232, 220), 5, 0.74, pattern=brushed, hi=(255, 255, 255)),
    'pl_gold': Mat((240, 192, 70), 6, 0.74, pattern=filigree, hi=(255, 244, 170)),
    'pl_holy': Mat((255, 236, 150), 4, 0.95, light=14, hi=(255, 255, 230)),
    'pl_celestial': Mat((26, 24, 64), 6, 0.9, pattern=stars_lines),
    'pl_wolf': Mat((116, 112, 106), 14, 0.9, pattern=fur),
    'pl_wolf_l': Mat((196, 190, 180), 12, 0.9, pattern=fur),
    'pl_amber': Mat((255, 180, 40), 4, 0.95, light=13, hi=(255, 240, 160)),
    'pl_livewood': Mat((96, 70, 44), 6, 0.78, pattern=veins),
    'pl_leaf_gold': Mat((220, 180, 60), 8, 0.84, light=4, pattern=leaves),
    'pl_void_plate': Mat((30, 26, 40), 6, 0.78, pattern=cracks),
    'pl_void_glow': Mat((200, 110, 255), 4, 0.95, light=15, hi=(240, 210, 255)),
    'pl_lion_gold': Mat((222, 170, 60), 6, 0.74, pattern=filigree, hi=(255, 236, 150)),
    'pl_mane': Mat((206, 146, 58), 14, 0.88, pattern=fur),
    'pl_feather': Mat((140, 110, 76), 8, 0.86, pattern=feathers),
    'pl_feather_l': Mat((226, 212, 180), 8, 0.86, pattern=feathers),
    'pl_circuit': Mat((26, 24, 40), 6, 0.86, pattern=circuits),
    'pl_azure': Mat((90, 220, 255), 4, 0.95, light=14, hi=(220, 250, 255)),
})


class Outfit:
    """Tenue : un matériau par zone, des rangées en option et des détails peints (fonctions F -> None)."""

    def __init__(self, body, belt, skirt, arm, leg, boot, collar=None, shoulder=None, cuff=None, sleeveless=False,
                 knee=None, boot_top=None, boot_from=14, toe=None, waist=None, front=None, back=None, side=None,
                 arm_detail=None, leg_detail=None, boot_detail=None, belt_rows=(15, 17), shoulder_rows=8, cap=None):
        self.__dict__.update(locals())
        del self.__dict__['self']


def painter(o):
    def paint(F):
        p, W, H = F.part, F.w, F.h
        if p == 'body':
            if F.cap:
                F.rows(0, H, o.cap or o.body); return
            F.rows(0, o.belt_rows[0], o.body)
            F.rows(o.belt_rows[1], 24, o.skirt)
            F.rows(o.belt_rows[0], o.belt_rows[1], o.belt)
            if o.collar:
                F.rows(0, 2, o.collar)
            if F.front and o.front:
                o.front(F)
            if F.back and o.back:
                o.back(F)
            if F.side and o.side:
                o.side(F)
        elif p == 'arm':
            if o.sleeveless:
                from PIL import Image
                F.img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                if F.cap:
                    return
                F.rows(14, 23, o.cuff or o.arm)
                F.rows(14, 15, o.belt, bevel=False)
                if o.shoulder:
                    F.rows(0, 3, o.shoulder)
                if o.arm_detail:
                    o.arm_detail(F)
                return
            if F.face == 'bottom':
                F.rows(0, H, o.arm); return
            F.rows(0, 24, o.arm)
            if o.shoulder:
                F.rows(0, o.shoulder_rows, o.shoulder)
            if o.cuff:
                F.rows(18, 24, o.cuff)
            if o.arm_detail and not F.cap:
                o.arm_detail(F)
        elif p == 'boot':
            if F.cap:
                F.rows(0, H, o.boot); return
            F.rows(o.boot_from, 24, o.boot)
            if o.boot_top:
                F.rows(o.boot_from, o.boot_from + 2, o.boot_top)
            if o.toe and F.front:
                F.rect(1, 21, W - 1, 24, o.toe)
            if o.boot_detail:
                o.boot_detail(F)
            F.clear(0, 0, W, o.boot_from)
        elif p == 'leg':
            F.rows(0, 18, o.leg)
            if o.knee and (F.front or F.side):
                F.rect(0, 9, W, 14, o.knee)
            if o.leg_detail:
                o.leg_detail(F)
            F.clear(0, 18, W, H)
        elif p == 'waist':
            F.rows(18, 24, o.waist or o.leg)
            F.rows(18, 20, o.belt)
            F.clear(0, 0, W, 18)
    return paint


# --- petits motifs réutilisés --------------------------------------------------------------------------------------

def emblem_diamond(mat, inner, cy=8, r=3):
    def f(F):
        cx = F.w // 2
        for dy in range(-r, r + 1):
            k = r - abs(dy)
            F.rect(cx - k - 1, cy + dy, cx + k + 1, cy + dy + 1, mat, bevel=False)
        F.rect(cx - 1, cy - 1, cx + 1, cy + 1, inner, bevel=False)
    return f


def diagonal(mat, y0=1, n=14, flip=False):
    def f(F):
        for i in range(n):
            x = (F.w - 3 - i) if flip else (2 + i)
            F.rect(x, y0 + i, x + 2, y0 + 2 + i, mat, bevel=False)
    return f


def cape(mat, edge=None, y0=2):
    def f(F):
        F.rect(1, y0, F.w - 1, 24, mat)
        if edge:
            F.rect(1, 22, F.w - 1, 24, edge, bevel=False)
    return f


def both(*fs):
    def f(F):
        for g in fs:
            g(F)
    return f


def plates(mat, rows=(5, 9, 13), x0=1):
    def f(F):
        for y in rows:
            F.rect(x0, y, F.w - x0, y + 1, mat, bevel=False)
    return f


def vertical(mat, w=2, y0=2, y1=15):
    def f(F):
        F.rect(F.w // 2 - w // 2, y0, F.w // 2 + (w - w // 2), y1, mat)
    return f


def dots(color, rows, xs=None):
    def f(F):
        for y in rows:
            for x in (xs or (2, F.w - 3)):
                F.px(x, y, color)
    return f


def stripe(mat, y0, y1):
    def f(F):
        if not F.cap:
            F.rows(y0, y1, mat, bevel=False)
    return f


def ribs(mat):
    """Côtes de plates en chevrons."""
    def f(F):
        cx = F.w // 2
        for y in (4, 7, 10, 13):
            for i in range(cx - 1):
                F.px(cx - 1 - i, y + i // 3, (0, 0, 0)) if False else None
                F.rect(cx - 1 - i, y + i // 3, cx - i, y + 1 + i // 3, mat, bevel=False)
                F.rect(cx + i, y + i // 3, cx + i + 1, y + 1 + i // 3, mat, bevel=False)
    return f


# ==================================================================================================================
#  Tenues
# ==================================================================================================================

OUTFITS = {
    # --- Guerrier --------------------------------------------------------------------------------------------------
    ('guerrier', 'commun'): Outfit(
        body='pc_gambeson', belt='pc_leather_d', skirt='pc_gambeson_d', arm='pc_gambeson', cuff='pc_leather',
        leg='pc_linen_d', knee='pc_leather', boot='pc_leather', boot_top='pc_leather_d', boot_from=15,
        front=vertical('pc_rope', 1, 2, 15)),
    ('guerrier', 'epique'): Outfit(
        body='pe_scale', belt='pc_leather_d', skirt='pe_crimson', arm='pe_scale', collar='pe_fur',
        shoulder='gu_bronze', shoulder_rows=9, cuff='gu_plate_d', leg='pe_scale', knee='gu_bronze',
        boot='gu_plate', boot_top='gu_bronze', toe='gu_bronze',
        front=both(diagonal('pe_crimson', 2, 13), emblem_diamond('gu_bronze', 'gu_plate', 9, 2)),
        back=cape('pe_crimson', 'gu_bronze'),
        arm_detail=both(stripe('gu_plate', 3, 4), stripe('gu_plate', 6, 7))),
    ('guerrier', 'legendaire'): Outfit(
        body='pl_dragon_plate', belt='pl_gold', skirt='pl_dragon', arm='pl_dragon', collar='pl_gold',
        shoulder='pl_dragon_plate', shoulder_rows=10, cuff='pl_dragon_plate', leg='pl_dragon', knee='pl_dragon_plate',
        boot='pl_dragon_plate', boot_top='pl_gold', toe='pl_gold',
        front=both(ribs('pl_gold'), lambda F: F.rect(F.w // 2 - 1, 7, F.w // 2 + 1, 10, 'pl_ember')),
        back=both(cape('pe_crimson_d', 'pl_gold'), dots((255, 120, 50), (6, 10, 14), (4, 11))),
        arm_detail=both(stripe('pl_gold', 0, 1), lambda F: [F.px(x, 2, (240, 230, 210)) for x in range(1, F.w - 1, 2)],
                        lambda F: F.rect(F.w // 2 - 1, 20, F.w // 2 + 1, 22, 'pl_ember')),
        leg_detail=lambda F: F.rect(F.w // 2 - 1, 10, F.w // 2 + 1, 13, 'pl_ember') if F.front else None),

    # --- Paladin ---------------------------------------------------------------------------------------------------
    ('paladin', 'commun'): Outfit(
        body='pc_chain', belt='pc_leather_d', skirt='pc_chain', arm='pc_chain', leg='pc_chain', boot='pc_leather',
        boot_top='pc_leather_d',
        front=both(lambda F: F.rect(3, 2, F.w - 3, 24, 'pc_white'),
                   lambda F: F.rect(F.w // 2 - 1, 5, F.w // 2 + 1, 14, 'pe_crimson'),
                   lambda F: F.rect(F.w // 2 - 3, 7, F.w // 2 + 3, 9, 'pe_crimson')),
        back=lambda F: F.rect(3, 2, F.w - 3, 24, 'pc_white')),
    ('paladin', 'epique'): Outfit(
        body='pe_silver', belt='pe_gold', skirt='pe_silver', arm='pe_silver', collar='pe_gold', shoulder='pe_silver',
        shoulder_rows=10, cuff='pe_gold', leg='pa_plate_d', knee='pe_silver', boot='pe_silver', boot_top='pe_gold',
        toe='pe_gold',
        front=both(plates('pa_plate_d', (12,)), emblem_diamond('pe_gold', 'pa_holy', 7, 3),
                   lambda F: [F.rect(3, y, F.w - 3, y + 1, 'pe_gold', bevel=False) for y in (17, 20)]),
        back=cape('pe_blue', 'pe_gold'),
        arm_detail=both(stripe('pe_gold', 0, 1), stripe('pe_gold', 9, 10))),
    ('paladin', 'legendaire'): Outfit(
        body='pl_white_gold', belt='pl_gold', skirt='pl_white_gold', arm='pl_white_gold', collar='pl_gold',
        shoulder='pl_gold', shoulder_rows=9, cuff='pl_gold', leg='pl_white_gold', knee='pl_gold', boot='pl_white_gold',
        boot_top='pl_gold', toe='pl_gold',
        front=both(lambda F: [F.rect(2 + i, 4 + i, 4 + i, 5 + i, 'pl_gold', bevel=False) for i in range(5)],   # ailes
                   lambda F: [F.rect(F.w - 4 - i, 4 + i, F.w - 2 - i, 5 + i, 'pl_gold', bevel=False) for i in range(5)],
                   lambda F: F.rect(F.w // 2 - 1, 3, F.w // 2 + 1, 14, 'pl_holy'),
                   lambda F: F.rect(F.w // 2 - 3, 6, F.w // 2 + 3, 8, 'pl_holy')),
        back=both(cape('pl_white_gold', 'pl_gold'),
                  lambda F: [F.px(F.w // 2 + int(3 * math.cos(a / 4)), 8 + int(3 * math.sin(a / 4)), (255, 236, 150))
                             for a in range(26)]),
        arm_detail=lambda F: F.rect(F.w // 2 - 1, 3, F.w // 2 + 1, 6, 'pl_holy'),
        leg_detail=lambda F: F.rect(F.w // 2 - 1, 2, F.w // 2 + 1, 8, 'pl_gold') if F.front else None),

    # --- Mage ------------------------------------------------------------------------------------------------------
    ('mage', 'commun'): Outfit(
        body='pc_robe_brown', belt='pc_rope', skirt='pc_robe_brown', arm='pc_robe_brown', cuff='pc_linen_d',
        leg='pc_robe_brown', boot='pc_leather_d', boot_from=17, belt_rows=(14, 15)),
    ('mage', 'epique'): Outfit(
        body='pe_crimson', belt='pe_rune_band', skirt='pe_crimson', arm='pe_crimson', collar='pe_rune_band',
        shoulder='pe_crimson_d', shoulder_rows=5, cuff='pe_rune_band', leg='pe_crimson', boot='pe_crimson_d',
        boot_top='pe_rune_band', boot_from=16, waist='pe_crimson',
        front=both(lambda F: F.rect(F.w // 2 - 2, 0, F.w // 2 + 2, 24, 'pe_crimson_d'),                 # robe croisée
                   lambda F: F.rect(F.w // 2 - 1, 2, F.w // 2, 24, 'pe_rune_band', bevel=False),
                   lambda F: F.rect(F.w // 2 - 1, 15, F.w // 2 + 1, 17, 'ma_gem')),
        back=both(lambda F: F.rect(2, 0, F.w - 2, 4, 'pe_crimson_d'), emblem_diamond('pe_rune_band', 'ma_gem', 9, 3)),
        leg_detail=stripe('pe_rune_band', 15, 17)),
    ('mage', 'legendaire'): Outfit(
        body='pl_celestial', belt='pl_gold', skirt='pl_celestial', arm='pl_celestial', collar='pl_gold',
        shoulder='pl_gold', shoulder_rows=4, cuff='pl_gold', leg='pl_celestial', boot='pl_celestial',
        boot_top='pl_gold', boot_from=16, waist='pl_celestial',
        front=both(lambda F: F.rect(3, 2, F.w - 3, 6, 'pl_gold'),                                         # mantelet
                   lambda F: F.rect(4, 3, F.w - 4, 5, 'pl_celestial', bevel=False),
                   lambda F: F.rect(F.w // 2 - 1, 8, F.w // 2 + 1, 11, 'pe_crystal')),
        back=both(lambda F: F.rect(3, 2, F.w - 3, 6, 'pl_gold'),
                  lambda F: [F.px(F.w // 2 + int(4 * math.cos(a / 4)), 13 + int(4 * math.sin(a / 4)), (150, 190, 255))
                             for a in range(26)]),
        arm_detail=lambda F: F.rect(F.w // 2 - 1, 10, F.w // 2 + 1, 12, 'pe_crystal'),
        leg_detail=stripe('pl_gold', 16, 18)),

    # --- Rôdeur ----------------------------------------------------------------------------------------------------
    ('rodeur', 'commun'): Outfit(
        body='pc_linen', belt='pc_leather_d', skirt='pc_linen', arm='pc_linen', sleeveless=True, cuff='pc_leather',
        leg='pc_linen_d', boot='pc_leather', boot_from=14,
        front=lambda F: F.rect(3, 2, F.w - 3, 15, 'pc_leather'),
        back=lambda F: F.rect(3, 2, F.w - 3, 15, 'pc_leather')),
    ('rodeur', 'epique'): Outfit(
        body='pe_black_leather', belt='belt', skirt='ro_tunic_d', arm='pe_black_leather', shoulder='pe_fur',
        shoulder_rows=6, cuff='leather_hd', leg='ro_tunic_d', knee='pe_black_leather', boot='pe_black_leather',
        boot_top='pe_fur', collar='pe_fur',
        front=both(diagonal('belt', 1, 15), diagonal('belt', 1, 15, flip=True),
                   lambda F: F.rect(F.w // 2 - 1, 7, F.w // 2 + 1, 9, 'steel_buckle')),
        back=both(diagonal('belt', 1, 15),
                  lambda F: [F.rect(F.w - 6, y, F.w - 3, y + 1, 'ro_feather', bevel=False) for y in (1, 2)])),
    ('rodeur', 'legendaire'): Outfit(
        body='pc_studded', belt='pl_amber', skirt='pl_wolf', arm='pc_studded', sleeveless=True, shoulder='pl_wolf',
        cuff='pc_studded', leg='pe_black_leather', knee='pc_studded', boot='pe_black_leather', boot_top='pl_wolf',
        collar='pl_wolf_l',
        front=both(lambda F: F.rect(0, 0, F.w, 5, 'pl_wolf'),                                              # pelisse
                   lambda F: F.rect(F.w // 2 - 1, 5, F.w // 2 + 1, 7, 'pl_amber')),
        back=both(cape('pl_wolf'), lambda F: F.rect(2, 2, F.w - 2, 5, 'pl_wolf_l')),
        side=lambda F: F.rect(0, 0, F.w, 6, 'pl_wolf')),

    # --- Druide ----------------------------------------------------------------------------------------------------
    ('druide', 'commun'): Outfit(
        body='pc_robe_green', belt='pc_rope', skirt='pc_robe_green', arm='pc_robe_green', sleeveless=True,
        cuff='pc_rope', leg='pc_robe_green', boot='pc_linen_d', boot_from=17, belt_rows=(14, 15)),
    ('druide', 'epique'): Outfit(
        body='dr_vine_cloth', belt='pe_bark', skirt='pe_moss', arm='pe_moss', shoulder='dr_leafy', shoulder_rows=5,
        cuff='pe_bark', leg='dr_vine_cloth', knee='pe_bark', boot='pe_bark', boot_top='pe_moss',
        front=both(lambda F: [F.rect(x0, y0, x1, y1, 'pe_bark') for (x0, y0, x1, y1) in
                              ((1, 2, 7, 9), (F.w - 7, 2, F.w - 1, 9), (2, 9, F.w - 2, 15))],
                   lambda F: F.rect(F.w // 2 - 1, 5, F.w // 2 + 1, 7, 'dr_amber')),
        back=both(lambda F: F.rect(1, 2, F.w - 1, 15, 'pe_bark'), lambda F: F.rect(1, 0, F.w - 1, 3, 'dr_leafy'))),
    ('druide', 'legendaire'): Outfit(
        body='pl_livewood', belt='pl_leaf_gold', skirt='dr_leafy', arm='pl_livewood', shoulder='pl_leaf_gold',
        shoulder_rows=4, cuff='pl_livewood', leg='pl_livewood', knee='pl_leaf_gold', boot='pl_livewood',
        boot_top='pl_leaf_gold', collar='pl_leaf_gold',
        front=both(emblem_diamond('pl_leaf_gold', 'dr_amber', 8, 3)),
        back=lambda F: [F.rect(F.w // 2 - 1 - i, 4 + 3 * i, F.w // 2 + 1 + i, 5 + 3 * i, 'pl_leaf_gold', bevel=False)
                        for i in range(4)]),

    # --- Lame-runique ----------------------------------------------------------------------------------------------
    ('lamerunique', 'commun'): Outfit(
        body='pc_leather_d', belt='pc_leather', skirt='lr_scale', arm='pc_leather_d', cuff='lr_plate_d',
        leg='pc_leather_d', boot='lr_plate_d', boot_top='lr_silver',
        front=lambda F: F.rect(F.w // 2 - 1, 5, F.w // 2 + 1, 10, 'lr_silver')),
    ('lamerunique', 'epique'): Outfit(
        body='lr_plate', belt='lr_silver', skirt='lr_scale', arm='lr_scale', shoulder='lr_plate', shoulder_rows=10,
        cuff='lr_plate_d', leg='lr_scale', knee='lr_plate', boot='lr_plate', boot_top='lr_silver', toe='lr_silver',
        collar='lr_silver',
        front=both(lambda F: [F.rect(x, 3, x + 1, 14, 'lr_glow', bevel=False) for x in (3, F.w // 2, F.w - 4)],
                   lambda F: [F.rect(x - 1, y, x + 2, y + 1, 'lr_glow', bevel=False)
                              for x in (3, F.w // 2, F.w - 4) for y in (5, 9, 12)]),
        back=both(lambda F: F.rect(F.w // 2 - 1, 1, F.w // 2 + 1, 22, 'lr_silver'),
                  lambda F: F.rect(F.w // 2 - 3, 4, F.w // 2 + 3, 5, 'lr_silver', bevel=False)),
        arm_detail=lambda F: [F.rect(x, 3, x + 2, 5, 'lr_silver') for x in range(1, F.w - 1, 3)]),
    ('lamerunique', 'legendaire'): Outfit(
        body='pl_void_plate', belt='pl_void_glow', skirt='pl_void_plate', arm='pl_void_plate', shoulder='pl_void_plate',
        shoulder_rows=10, cuff='pl_void_plate', leg='pl_void_plate', knee='lr_silver', boot='pl_void_plate',
        boot_top='pl_void_glow', toe='lr_silver', collar='lr_silver',
        front=both(emblem_diamond('lr_silver', 'pl_void_glow', 7, 3),
                   lambda F: F.rect(F.w // 2 - 1, 11, F.w // 2 + 1, 15, 'pl_void_glow')),
        back=both(cape('ar_robe', 'pl_void_glow'), lambda F: F.rect(F.w // 2 - 1, 4, F.w // 2 + 1, 12, 'pl_void_glow')),
        arm_detail=both(lambda F: [F.rect(x, 1, x + 2, 4, 'lr_silver') for x in range(1, F.w - 1, 3)],
                        lambda F: F.rect(F.w // 2 - 1, 18, F.w // 2 + 1, 23, 'pl_void_glow'))),

    # --- Garde-serment ---------------------------------------------------------------------------------------------
    ('gardeserment', 'commun'): Outfit(
        body='pc_studded', belt='pc_leather_d', skirt='pc_chain', arm='pc_chain', cuff='pc_leather', leg='pc_chain',
        boot='pc_leather', boot_top='pc_leather_d',
        front=lambda F: F.rect(3, 2, F.w - 3, 15, 'gs_blue'),
        back=lambda F: F.rect(3, 2, F.w - 3, 15, 'gs_blue')),
    ('gardeserment', 'epique'): Outfit(
        body='gs_steel', belt='gs_gold', skirt='gs_red', arm='gs_steel', shoulder='gs_steel', shoulder_rows=10,
        cuff='gs_gold', leg='gs_steel_d', knee='gs_steel', boot='gs_steel', boot_top='gs_gold', toe='gs_gold',
        collar='gs_gold',
        front=both(lambda F: F.rect(2, 3, F.w - 2, 15, 'gs_blue'),
                   lambda F: F.rect(2, 3, 3, 15, 'gs_gold', bevel=False),
                   lambda F: F.rect(F.w - 3, 3, F.w - 2, 15, 'gs_gold', bevel=False),
                   emblem_diamond('gs_gold', 'gs_red', 8, 3)),
        back=cape('gs_red', 'gs_gold'),
        arm_detail=both(stripe('gs_gold', 3, 4), stripe('gs_gold', 7, 8))),
    ('gardeserment', 'legendaire'): Outfit(
        body='pl_lion_gold', belt='pl_gold', skirt='gs_red', arm='gs_steel', shoulder='pl_lion_gold', shoulder_rows=10,
        cuff='pl_lion_gold', leg='gs_steel', knee='pl_lion_gold', boot='gs_steel', boot_top='pl_lion_gold',
        toe='pl_lion_gold', collar='pl_mane',
        front=both(lambda F: F.rect(0, 0, F.w, 4, 'pl_mane'),                                           # crinière
                   lambda F: F.rect(F.w // 2 - 3, 5, F.w // 2 + 3, 12, 'gs_steel'),                        # mufle de lion
                   lambda F: F.rect(F.w // 2 - 2, 6, F.w // 2 + 2, 11, 'pl_lion_gold'),
                   lambda F: [F.px(x, 8, (255, 180, 40)) for x in (F.w // 2 - 2, F.w // 2 + 1)],
                   lambda F: F.rect(F.w // 2 - 1, 10, F.w // 2 + 1, 11, 'ro_shadow', bevel=False)),
        back=both(cape('gs_red', 'pl_gold'), lambda F: F.rect(0, 0, F.w, 4, 'pl_mane')),
        side=lambda F: F.rect(0, 0, F.w, 4, 'pl_mane')),

    # --- Sentinelle ------------------------------------------------------------------------------------------------
    ('sentinelle', 'commun'): Outfit(
        body='ro_tunic', belt='pc_rope', skirt='ro_tunic', arm='ro_tunic', cuff='pc_leather', leg='ro_tunic_d',
        boot='pc_leather', boot_from=15),
    ('sentinelle', 'epique'): Outfit(
        body='sn_leather', belt='belt', skirt='sn_cloak', arm='sn_cloak', shoulder='pe_owl', shoulder_rows=6,
        cuff='dr_bark', leg='sn_cloak_d', knee='sn_leather', boot='sn_leather', boot_top='pe_owl', collar='pe_owl_l',
        front=both(lambda F: F.rect(0, 0, F.w, 5, 'pe_owl'),
                   lambda F: F.rect(F.w // 2 - 1, 5, F.w // 2 + 1, 7, 'dr_amber'),
                   lambda F: [F.rect(x, 7, x + 3, 13, 'dr_bark') for x in (3, F.w - 6)]),
        back=both(cape('sn_cloak_d'), lambda F: F.rect(1, 0, F.w - 1, 6, 'pe_owl'))),
    ('sentinelle', 'legendaire'): Outfit(
        body='pl_feather', belt='pl_amber', skirt='pl_feather', arm='pl_feather', shoulder='pl_feather_l',
        shoulder_rows=8, cuff='dr_bark', leg='pl_feather', knee='dr_bark', boot='dr_bark', boot_top='pl_feather_l',
        collar='pl_feather_l',
        front=both(lambda F: [F.rect(3, 3, F.w // 2 - 1, 8, 'pl_feather_l'), F.rect(F.w // 2 + 1, 3, F.w - 3, 8, 'pl_feather_l')],
                   lambda F: [F.px(x, 5, (255, 180, 40)) for x in (5, F.w - 6)],                          # yeux de hibou
                   lambda F: F.rect(F.w // 2 - 1, 7, F.w // 2 + 1, 10, 'cp_beak' if 'cp_beak' in MATS else 'dr_bark')),
        back=lambda F: [F.rect(1 + i, 3 + 3 * i, F.w - 1 - i, 5 + 3 * i, 'pl_feather_l' if i % 2 else 'pl_feather')
                        for i in range(6)]),

    # --- Arcaniste -------------------------------------------------------------------------------------------------
    ('arcaniste', 'commun'): Outfit(
        body='pc_robe_violet', belt='pc_rope', skirt='pc_robe_violet', arm='pc_robe_violet', cuff='lr_plate_d',
        leg='pc_robe_violet', boot='lr_plate_d', boot_from=16, belt_rows=(14, 15)),
    ('arcaniste', 'epique'): Outfit(
        body='ar_robe', belt='ma_sash', skirt='ar_robe_l', arm='ar_robe', shoulder='lr_plate', shoulder_rows=8,
        cuff='lr_silver', leg='ar_robe', knee='lr_plate', boot='lr_plate_d', boot_top='lr_silver', collar='lr_silver',
        front=both(lambda F: F.rect(2, 2, F.w - 2, 10, 'lr_plate'),
                   lambda F: [F.rect(x, 15, x + 2, 17, 'pe_crystal') for x in (3, F.w // 2 - 1, F.w - 5)]),
        back=both(lambda F: F.rect(2, 2, F.w - 2, 10, 'lr_plate'), lambda F: F.rect(F.w // 2 - 1, 4, F.w // 2 + 1, 8, 'ar_rune')),
        arm_detail=lambda F: F.rect(F.w // 2 - 1, 3, F.w // 2 + 1, 5, 'pe_crystal')),
    ('arcaniste', 'legendaire'): Outfit(
        body='pl_circuit', belt='pl_azure', skirt='pl_circuit', arm='pl_circuit', shoulder='lr_plate', shoulder_rows=9,
        cuff='pl_azure', leg='pl_circuit', knee='lr_plate', boot='lr_plate', boot_top='pl_azure', toe='lr_silver',
        collar='lr_silver',
        front=both(emblem_diamond('lr_silver', 'pl_azure', 8, 4)),
        back=both(cape('pl_circuit', 'pl_azure'), emblem_diamond('lr_silver', 'pl_azure', 9, 3)),
        arm_detail=lambda F: [F.rect(x, 1, x + 2, 3, 'pl_azure') for x in range(1, F.w - 1, 3)]),
}

PAINTERS = {k: painter(o) for k, o in OUTFITS.items()}
