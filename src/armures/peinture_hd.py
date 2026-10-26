"""Calques d'armure en double résolution (128x64) peints en détail : plastron, bras, jambières, bottes.

Même disposition que les calques vanilla 64x32, chaque texel coupé en 2x2. Chaque face est peinte par la fonction
de sa classe à coups de pavés de matériaux (kit.Mat : bruit, liseré sombre aux bords du pavé, reflet clair), ce qui
donne des plaques biseautées, des rivets, des coutures, du tissu plissé, des runes. Le casque n'est pas peint ici :
il est modelé en 3D (casques3d.py).
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'items'))
sys.path.insert(0, HERE)
from PIL import Image  # noqa: E402
from kit import Mat, MATS, h, mix  # noqa: E402
import raretes  # noqa: E402
import casques3d  # noqa: E402,F401  (matériaux des casques, réutilisés pour assortir)
from casques3d import hammered, brushed, filigree, runes_glow, cloth_folds, starry, leather, fur, bark_grain, leaves  # noqa: E402

K = 2  # facteur de résolution


def chain(c, p, face, px, py, w, hgt):
    """Cotte de mailles : anneaux en quinconce."""
    x, y = int(p[0] * 4), int(p[1] * 4)
    ring = (x + (y // 2) % 2) % 2 == 0 and y % 2 == 0
    return tuple(v * (1.12 if ring else 0.78) for v in c)


def scales_hd(c, p, face, px, py, w, hgt):
    x, y = p[0] * 4, p[1] * 4
    row = int(y / 2)
    u = (x + row % 2) % 2
    return tuple(v * (0.75 if (y % 2) < 0.6 and abs(u - 1) < 0.6 else 1.0) for v in c)


def leather_soft(c, p, face, px, py, w, hgt):
    """Cuir : grain et couture discrète un point sur trois le long des bords."""
    k = 0.9 + 0.14 * h(int(p[0] * 3), int(p[1] * 3), int(p[2] * 3))
    if (px == 1 or py == 1 or px == w - 2 or py == hgt - 2) and w > 5 and hgt > 5 and (px + py) % 3 == 0:
        return mix(c, (200, 170, 120), 0.55)
    return tuple(v * k for v in c)


def vines(c, p, face, px, py, w, hgt):
    x, y = p[0] * 4, p[1] * 4
    if abs(x - 3 - 2.2 * math.sin(y / 3)) < 0.7:
        return (70, 130, 56)
    if abs(x - 3 - 2.2 * math.sin(y / 3)) < 2.2 and int(y) % 5 == 0:
        return (110, 170, 80)
    return c


MATS.update({
    'chain': Mat((128, 132, 142), 6, 0.85, pattern=chain),
    'chain_d': Mat((90, 94, 104), 6, 0.85, pattern=chain),
    'leather_hd': Mat((112, 72, 42), 6, 0.78, pattern=leather_soft),
    'leather_hd_d': Mat((74, 48, 30), 6, 0.78, pattern=leather_soft),
    'belt': Mat((70, 44, 26), 5, 0.75, pattern=leather_soft),
    'steel_buckle': Mat((196, 198, 206), 4, 0.7, hi=(250, 250, 255)),
    'cloth_white': Mat((226, 222, 210), 6, 0.86, pattern=cloth_folds),
    'gu_cloth_red': Mat((142, 30, 30), 6, 0.84, pattern=cloth_folds),
    'pa_tabard': Mat((40, 62, 140), 6, 0.84, pattern=cloth_folds),
    'ma_robe': Mat((52, 46, 128), 6, 0.86, pattern=starry),
    'ma_robe_d': Mat((34, 30, 92), 6, 0.86, pattern=cloth_folds),
    'ma_sash': Mat((140, 40, 90), 6, 0.84, pattern=cloth_folds),
    'ro_tunic': Mat((60, 90, 50), 6, 0.86, pattern=cloth_folds),
    'ro_tunic_d': Mat((42, 64, 36), 6, 0.86, pattern=cloth_folds),
    'ro_fur': Mat((150, 128, 100), 14, 0.9, pattern=fur),
    'ro_pouch': Mat((96, 62, 36), 6, 0.78, pattern=leather_soft),
    'dr_bark': Mat((104, 74, 46), 6, 0.78, pattern=bark_grain),
    'dr_bark_l': Mat((140, 104, 66), 6, 0.8, pattern=bark_grain),
    'dr_vine_cloth': Mat((86, 70, 50), 6, 0.86, pattern=vines),
    'dr_leafy': Mat((76, 140, 60), 10, 0.84, pattern=leaves),
    'dr_amber': Mat((240, 170, 50), 4, 0.9, light=8, hi=(255, 230, 150)),
    'lr_plate': Mat((50, 48, 62), 6, 0.76, pattern=hammered, hi=(108, 106, 128)),
    'lr_plate_d': Mat((34, 32, 44), 6, 0.78, pattern=brushed),
    'lr_scale': Mat((46, 44, 58), 6, 0.8, pattern=scales_hd),
    'gu_plate': Mat((146, 152, 164), 6, 0.72, pattern=hammered, hi=(222, 228, 238)),
    'gu_plate_d': Mat((110, 116, 128), 6, 0.74, pattern=hammered),
    'pa_plate': Mat((212, 216, 226), 5, 0.74, pattern=brushed, hi=(255, 255, 255)),
    'pa_plate_d': Mat((168, 174, 188), 5, 0.76, pattern=brushed),
})


class Face:
    """Toile d'une face (coordonnées en texels HD, origine en haut à gauche)."""

    def __init__(self, part, face, w, hh, seed):
        self.part, self.face, self.w, self.h, self.seed = part, face, w, hh, seed
        self.img = Image.new('RGBA', (w, hh), (0, 0, 0, 0))
        self.front = face == 'front'
        self.back = face == 'back'
        self.side = face in ('left', 'right')
        self.cap = face in ('top', 'bottom')

    def rect(self, x0, y0, x1, y1, mat, bevel=True):
        m = MATS[mat]
        x0, y0 = max(0, int(x0)), max(0, int(y0))
        x1, y1 = min(self.w, int(x1)), min(self.h, int(y1))
        for y in range(y0, y1):
            for x in range(x0, x1):
                p = (x * 0.25 + self.seed * 3.1, y * 0.25, self.seed)
                if bevel:
                    c = m.color(p, self.face, x - x0, y - y0, x1 - x0, y1 - y0)
                else:
                    c = m.color(p, self.face, 1, 1, 9, 9)
                self.img.putpixel((x, y), c)

    def rows(self, y0, y1, mat, bevel=True):
        self.rect(0, y0, self.w, y1, mat, bevel)

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((int(x), int(y)), tuple(int(v) for v in color) + (255,))

    def rivet(self, x, y, light=(236, 236, 240), dark=(60, 60, 66)):
        self.px(x, y, light)
        self.px(x + 1, y + 1, dark)

    def clear(self, x0, y0, x1, y1):
        for y in range(max(0, y0), min(self.h, y1)):
            for x in range(max(0, x0), min(self.w, x1)):
                self.img.putpixel((x, y), (0, 0, 0, 0))


# =====================================================================================================
#  Classes. part : body (plastron), arm, boot (calque 1, bas de jambe), leg (calque 2), waist (calque 2, bas du corps)
#  Hauteurs HD : corps et membres 24, largeurs : corps 16 (face) / 8 (côté), membres 8.
# =====================================================================================================

def guerrier(F):
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'gu_plate'); return
        F.rows(0, 15, 'gu_plate')                       # cuirasse
        F.rows(15, 17, 'belt')
        F.rows(17, 24, 'chain')                         # maille sous la cuirasse
        if F.front or F.back:
            F.rect(0, 0, W, 2, 'gu_bronze')             # col
            F.rect(W // 2 - 1, 2, W // 2 + 1, 15, 'gu_bronze') if F.front else None
            for y in (5, 9, 13):                        # lames de la cuirasse
                F.rect(1, y, W - 1, y + 1, 'gu_plate_d', bevel=False)
            if F.front:
                F.rect(2, 3, W // 2 - 1, 8, 'gu_plate')   # pectoraux
                F.rect(W // 2 + 1, 3, W - 2, 8, 'gu_plate')
                F.rect(W // 2 - 2, 15, W // 2 + 2, 17, 'steel_buckle')
                F.rect(4, 17, W - 4, 24, 'gu_cloth_red')  # tabard
                F.rect(4, 22, W - 4, 24, 'gu_bronze')
            for x in (1, W - 2):
                for y in (3, 7, 11):
                    F.rivet(x, y)
        else:
            for y in (5, 9, 13):
                F.rect(0, y, W, y + 1, 'gu_plate_d', bevel=False)
    elif p == 'arm':
        if F.face == 'bottom':
            F.rows(0, H, 'gu_plate'); return
        F.rows(0, 8, 'gu_plate')                        # épaulière
        F.rows(0, 2, 'gu_bronze')
        F.rows(6, 8, 'gu_plate_d')
        F.rows(8, 15, 'chain')
        F.rows(15, 24, 'gu_plate_d')                    # canon d'avant-bras
        F.rows(15, 16, 'gu_bronze', bevel=False)
        F.rows(22, 24, 'leather_hd_d')
        if not F.cap:
            F.rivet(2, 4); F.rivet(W - 3, 4); F.rivet(W // 2, 18)
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'gu_plate'); return
        F.rows(14, 24, 'gu_plate')
        F.rows(14, 15, 'gu_bronze', bevel=False)
        F.rows(19, 20, 'gu_plate_d', bevel=False)
        if F.front:
            F.rect(1, 21, W - 1, 24, 'gu_bronze')       # embout
        F.clear(0, 0, W, 14)
    elif p == 'leg':
        F.rows(0, 18, 'chain')
        F.rows(0, 2, 'belt')
        if F.front or F.side:
            F.rect(0, 9, W, 14, 'gu_plate')             # genouillère
            F.rect(1, 10, W - 1, 11, 'gu_bronze', bevel=False)
            F.rivet(W // 2, 12)
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'chain')
        F.rows(18, 20, 'belt')
        if F.front:
            F.rect(W // 2 - 2, 18, W // 2 + 2, 20, 'steel_buckle')
        F.clear(0, 0, W, 18)


def paladin(F):
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'pa_plate'); return
        F.rows(0, 16, 'pa_plate')
        F.rows(16, 18, 'pa_gold')
        F.rows(18, 24, 'pa_plate_d')
        if F.front or F.back:
            F.rect(0, 0, W, 2, 'pa_gold')
            F.rect(3, 4, W - 3, 24, 'pa_tabard')        # tabard bleu
            F.rect(3, 4, 4, 24, 'pa_gold', bevel=False)
            F.rect(W - 4, 4, W - 3, 24, 'pa_gold', bevel=False)
            F.rect(W // 2 - 1, 6, W // 2 + 1, 15, 'pa_gold')   # croix
            F.rect(W // 2 - 3, 8, W // 2 + 3, 10, 'pa_gold')
            if F.front:
                F.rect(W // 2 - 1, 8, W // 2 + 1, 10, 'pa_holy')
            F.rect(3, 16, W - 3, 18, 'pa_gold')
        else:
            for y in (5, 10):
                F.rect(0, y, W, y + 1, 'pa_plate_d', bevel=False)
    elif p == 'arm':
        if F.face == 'bottom':
            F.rows(0, H, 'pa_plate'); return
        F.rows(0, 9, 'pa_plate')                        # grande épaulière
        F.rows(0, 2, 'pa_gold')
        F.rows(7, 9, 'pa_gold')
        F.rows(9, 15, 'pa_plate_d')
        F.rows(15, 24, 'pa_plate')
        F.rows(15, 16, 'pa_gold', bevel=False)
        F.rows(21, 24, 'pa_gold')
        if F.front or F.side:
            F.rect(W // 2 - 1, 3, W // 2 + 1, 6, 'pa_holy')
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'pa_plate'); return
        F.rows(14, 24, 'pa_plate')
        F.rows(14, 16, 'pa_gold')
        F.rows(22, 24, 'pa_gold')
        F.clear(0, 0, W, 14)
    elif p == 'leg':
        F.rows(0, 18, 'pa_plate_d')
        F.rows(0, 2, 'pa_gold')
        if F.front or F.side:
            F.rect(0, 8, W, 14, 'pa_plate')
            F.rect(W // 2 - 1, 9, W // 2 + 1, 13, 'pa_gold')
        if F.front:
            F.rect(1, 2, W - 1, 8, 'pa_tabard')         # pan du tabard
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'pa_plate_d')
        F.rows(18, 20, 'pa_gold')
        F.clear(0, 0, W, 18)


def mage(F):
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'ma_robe'); return
        F.rows(0, 24, 'ma_robe', bevel=False)
        F.rows(0, 2, 'ma_gold')
        F.rows(14, 17, 'ma_sash')                       # ceinture d'étoffe
        if F.front:
            F.rect(W // 2 - 1, 2, W // 2 + 1, 24, 'ma_gold')     # ouverture brodée
            F.rect(W // 2 - 2, 14, W // 2 + 2, 17, 'ma_gold')
            F.rect(W // 2 - 1, 15, W // 2 + 1, 16, 'ma_gem')
            for y in range(4, 13, 3):
                F.px(W // 2 - 3, y, (255, 230, 140)); F.px(W // 2 + 2, y, (255, 230, 140))
            F.rect(2, 3, 5, 6, 'ma_robe_d')             # pochette à parchemin
        if F.back:
            F.rect(W // 2 - 3, 5, W // 2 + 3, 11, 'ma_gold')     # sceau arcanique
            F.rect(W // 2 - 2, 6, W // 2 + 2, 10, 'ma_robe_d')
            F.rect(W // 2 - 1, 7, W // 2 + 1, 9, 'ma_gem')
    elif p == 'arm':
        if F.face == 'bottom':
            F.rows(0, H, 'ma_robe_d'); return
        F.rows(0, 24, 'ma_robe', bevel=False)
        F.rows(0, 3, 'ma_robe_d')                       # épaule
        F.rows(18, 22, 'ma_robe_d')                     # manche évasée
        F.rows(22, 24, 'ma_gold')
        if not F.cap:
            F.rect(W // 2 - 1, 10, W // 2 + 1, 12, 'ma_gem')
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'ma_robe_d'); return
        F.rows(16, 24, 'ma_robe_d')
        F.rows(16, 17, 'ma_gold', bevel=False)
        F.rows(22, 24, 'leather_hd_d', bevel=False)
        if F.front:
            F.rect(W // 2 - 1, 20, W // 2 + 1, 22, 'ma_gold')
        F.clear(0, 0, W, 16)
    elif p == 'leg':
        F.rows(0, 18, 'ma_robe', bevel=False)          # bas de la robe
        F.rows(15, 18, 'ma_gold')
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'ma_robe', bevel=False)
        F.rows(18, 20, 'ma_sash')
        F.clear(0, 0, W, 18)


def rodeur(F):
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'ro_tunic'); return
        F.rows(0, 24, 'ro_tunic', bevel=False)
        F.rows(0, 2, 'ro_fur')                          # col fourré
        if F.front or F.back:
            F.rect(2, 2, W - 2, 16, 'leather_hd')        # jerkin de cuir
            F.rect(W // 2, 2, W // 2 + 1, 16, 'leather_hd_d', bevel=False)
            for y in range(4, 16, 3):                    # laçage
                F.px(W // 2 - 1, y, (220, 200, 150)); F.px(W // 2 + 1, y + 1, (220, 200, 150))
        if F.front or F.back:
            for i in range(14):                          # baudrier en diagonale
                x = (2 + i) if F.front else (W - 3 - i)
                F.rect(x, 1 + i, x + 2, 3 + i, 'belt', bevel=False)
            if F.front:
                F.rect(9, 7, 12, 10, 'steel_buckle')
        F.rows(16, 18, 'belt')
        if F.front:
            F.rect(W // 2 - 1, 16, W // 2 + 1, 18, 'steel_buckle')
            F.rect(1, 18, 5, 22, 'ro_pouch')             # bourses
            F.rect(W - 5, 18, W - 1, 22, 'ro_pouch')
    elif p == 'arm':
        F.img = Image.new('RGBA', (W, H), (0, 0, 0, 0))  # sans manches : brassards seuls
        if F.cap:
            return
        F.rows(14, 23, 'leather_hd')
        F.rows(14, 15, 'leather_hd_d', bevel=False)
        F.rows(18, 19, 'belt', bevel=False)
        F.rows(22, 23, 'leather_hd_d', bevel=False)
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'leather_hd_d'); return
        F.rows(13, 24, 'leather_hd')
        F.rows(12, 15, 'ro_fur')                         # revers fourré
        F.rows(19, 20, 'belt', bevel=False)
        F.rows(22, 24, 'leather_hd_d')
        F.clear(0, 0, W, 12)
    elif p == 'leg':
        F.rows(0, 18, 'ro_tunic_d', bevel=False)
        if F.front or F.side:
            F.rect(1, 6, W - 1, 12, 'leather_hd')        # renfort de cuisse
            F.rect(1, 8, W - 1, 9, 'belt', bevel=False)
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'ro_tunic_d', bevel=False)
        F.rows(18, 20, 'belt')
        F.clear(0, 0, W, 18)


def druide(F):
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'dr_leafy'); return
        F.rows(0, 24, 'dr_vine_cloth', bevel=False)
        F.rows(0, 4, 'dr_leafy')                         # mantelet de feuilles
        if F.front or F.back:
            for (x0, y0, x1, y1) in ((2, 4, 7, 10), (W - 7, 4, W - 2, 10), (3, 10, W - 3, 15)):
                F.rect(x0, y0, x1, y1, 'dr_bark')        # plaques d'écorce
            if F.front:
                F.rect(W // 2 - 1, 7, W // 2 + 1, 9, 'dr_amber')
            F.rect(0, 15, W, 17, 'dr_bark_l')
            F.rect(2, 4, 3, 15, 'dr_leafy', bevel=False)
        F.rows(15, 17, 'dr_bark_l')
        F.rows(21, 24, 'dr_leafy')
    elif p == 'arm':
        F.img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        if F.cap:
            return
        F.rows(0, 3, 'dr_leafy')                         # feuilles à l'épaule
        F.rows(13, 22, 'dr_bark')                        # brassard d'écorce
        F.rows(16, 17, 'dr_leafy', bevel=False)
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'dr_bark'); return
        F.rows(14, 24, 'dr_vine_cloth', bevel=False)
        F.rows(14, 16, 'dr_leafy')
        F.rows(20, 24, 'dr_bark')
        F.clear(0, 0, W, 14)
    elif p == 'leg':
        F.rows(0, 18, 'dr_vine_cloth', bevel=False)
        if F.front or F.side:
            F.rect(0, 8, W, 13, 'dr_bark')
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'dr_vine_cloth', bevel=False)
        F.rows(18, 20, 'dr_bark_l')
        F.clear(0, 0, W, 18)


def lamerunique(F):
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'lr_plate'); return
        F.rows(0, 16, 'lr_plate')
        F.rows(16, 18, 'lr_silver')
        F.rows(18, 24, 'lr_scale', bevel=False)
        F.rows(0, 2, 'lr_silver')
        if F.front or F.back:
            F.rect(W // 2 - 1, 2, W // 2 + 1, 16, 'lr_plate_d')
            if F.front:
                c0 = W // 2 - 3                                   # rune centrale (ᚱ)
                F.rect(c0, 3, c0 + 2, 14, 'lr_glow', bevel=False)
                for i in range(4):
                    F.rect(c0 + 2 + i, 3 + i, c0 + 4 + i, 4 + i, 'lr_glow', bevel=False)
                    F.rect(c0 + 5 - i, 7 + i, c0 + 7 - i, 8 + i, 'lr_glow', bevel=False)
                for i in range(3):
                    F.rect(c0 + 2 + i, 10 + i, c0 + 4 + i, 11 + i, 'lr_glow', bevel=False)
            for y in (5, 10):
                F.rect(1, y, 4, y + 1, 'lr_silver', bevel=False)
                F.rect(W - 4, y, W - 1, y + 1, 'lr_silver', bevel=False)
            F.rect(W // 2 - 2, 16, W // 2 + 2, 18, 'lr_glow')
    elif p == 'arm':
        if F.face == 'bottom':
            F.rows(0, H, 'lr_plate'); return
        F.rows(0, 9, 'lr_plate')                         # épaulière à pointes
        F.rows(0, 2, 'lr_silver')
        if not F.cap:
            for x in range(1, W - 1, 3):
                F.rect(x, 2, x + 2, 4, 'lr_silver')
        F.rows(7, 9, 'lr_silver')
        F.rows(9, 15, 'lr_scale', bevel=False)
        F.rows(15, 24, 'lr_plate_d')
        F.rows(15, 16, 'lr_silver', bevel=False)
        if not F.cap:
            F.rect(W // 2 - 1, 18, W // 2 + 1, 22, 'lr_glow')
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'lr_plate'); return
        F.rows(14, 24, 'lr_plate')
        F.rows(14, 15, 'lr_silver', bevel=False)
        if F.front:
            F.rect(W // 2 - 1, 16, W // 2 + 1, 20, 'lr_glow')
        F.rows(22, 24, 'lr_silver')
        F.clear(0, 0, W, 14)
    elif p == 'leg':
        F.rows(0, 18, 'lr_scale', bevel=False)
        F.rows(0, 2, 'lr_silver')
        if F.front or F.side:
            F.rect(0, 8, W, 14, 'lr_plate')
            F.rect(W // 2 - 1, 9, W // 2 + 1, 13, 'lr_glow')
            F.rect(W // 2 - 2, 10, W // 2 + 2, 11, 'lr_glow', bevel=False)
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'lr_scale', bevel=False)
        F.rows(18, 20, 'lr_silver')
        F.clear(0, 0, W, 18)


# --- Panoplies multiclasses -------------------------------------------------------------------------------------
MATS.update({
    'gs_steel': Mat((96, 102, 116), 6, 0.72, pattern=hammered, hi=(170, 178, 196)),
    'gs_steel_d': Mat((66, 70, 82), 6, 0.74, pattern=brushed),
    'gs_gold': Mat((214, 168, 70), 6, 0.74, pattern=filigree, hi=(255, 230, 150)),
    'gs_red': Mat((128, 28, 34), 6, 0.84, pattern=cloth_folds),
    'gs_blue': Mat((36, 56, 124), 6, 0.84, pattern=cloth_folds),
    'sn_cloak': Mat((46, 72, 50), 6, 0.86, pattern=cloth_folds),
    'sn_cloak_d': Mat((32, 50, 36), 6, 0.86, pattern=cloth_folds),
    'sn_leather': Mat((92, 62, 38), 6, 0.78, pattern=leather_soft),
    'ar_robe': Mat((44, 30, 70), 6, 0.86, pattern=cloth_folds),
    'ar_robe_l': Mat((70, 48, 110), 6, 0.86, pattern=starry),
    'ar_rune': Mat((90, 220, 255), 4, 0.95, light=13, hi=(220, 250, 255)),
})


def gardeserment(F):
    """Garde-serment (Guerrier, Paladin) : acier bruni, or, tabard écartelé rouge et bleu."""
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'gs_steel'); return
        F.rows(0, 15, 'gs_steel')
        F.rows(0, 2, 'gs_gold')
        F.rows(15, 17, 'gs_gold')
        F.rows(17, 24, 'chain_d')
        if F.front or F.back:
            half = W // 2
            F.rect(2, 3, half, 9, 'gs_red'); F.rect(half, 3, W - 2, 9, 'gs_blue')       # écartelé
            F.rect(2, 9, half, 15, 'gs_blue'); F.rect(half, 9, W - 2, 15, 'gs_red')
            F.rect(2, 8, W - 2, 10, 'gs_gold', bevel=False)
            F.rect(half - 1, 3, half + 1, 15, 'gs_gold', bevel=False)
            if F.front:
                F.rect(half - 2, 7, half + 2, 11, 'gs_gold')                           # écu au centre
                F.rect(half - 1, 8, half + 1, 10, 'pa_holy')
                F.rect(3, 17, W - 3, 24, 'gs_blue')
                F.rect(3, 22, W - 3, 24, 'gs_gold')
        else:
            for y in (5, 10):
                F.rect(0, y, W, y + 1, 'gs_steel_d', bevel=False)
            F.rivet(W // 2, 3)
    elif p == 'arm':
        if F.face == 'bottom':
            F.rows(0, H, 'gs_steel'); return
        F.rows(0, 9, 'gs_steel')                         # épaulière à trois lames
        for y in (0, 3, 6):
            F.rows(y, y + 1, 'gs_gold', bevel=False)
        F.rows(9, 15, 'chain_d')
        F.rows(15, 24, 'gs_steel_d')
        F.rows(15, 16, 'gs_gold', bevel=False)
        F.rows(22, 24, 'gs_gold')
        if not F.cap:
            F.rivet(2, 11); F.rivet(W - 3, 11)
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'gs_steel'); return
        F.rows(14, 24, 'gs_steel')
        F.rows(14, 16, 'gs_gold')
        F.rows(19, 20, 'gs_steel_d', bevel=False)
        if F.front:
            F.rect(1, 21, W - 1, 24, 'gs_gold')
        F.clear(0, 0, W, 14)
    elif p == 'leg':
        F.rows(0, 18, 'chain_d')
        F.rows(0, 2, 'belt')
        if F.front or F.side:
            F.rect(0, 3, W, 8, 'gs_steel')               # tassette
            F.rect(0, 9, W, 14, 'gs_steel')              # genouillère
            F.rect(W // 2 - 1, 10, W // 2 + 1, 13, 'gs_gold')
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'chain_d')
        F.rows(18, 20, 'gs_gold')
        F.clear(0, 0, W, 18)


def sentinelle(F):
    """Sentinelle des bois (Rôdeur, Druide) : cuir, mantelet de feuilles, écorce, fermoir d'ambre."""
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'dr_leafy'); return
        F.rows(0, 24, 'sn_cloak', bevel=False)
        F.rows(0, 3, 'dr_leafy')
        if F.front:
            F.rect(3, 3, W - 3, 16, 'sn_leather')         # justaucorps de cuir
            F.rect(W // 2, 3, W // 2 + 1, 16, 'leather_hd_d', bevel=False)
            for y in range(5, 16, 3):
                F.px(W // 2 - 1, y, (210, 190, 130)); F.px(W // 2 + 1, y, (210, 190, 130))
            F.rect(W // 2 - 2, 3, W // 2 + 2, 6, 'dr_amber')   # fermoir d'ambre
            F.rect(4, 7, 7, 13, 'dr_bark')                 # plastron d'écorce
            F.rect(W - 7, 7, W - 4, 13, 'dr_bark')
        if F.back:
            F.rect(2, 3, W - 2, 22, 'sn_cloak_d')          # cape
            for y in range(6, 22, 5):
                F.rect(2, y, W - 2, y + 1, 'dr_leafy', bevel=False)
        F.rows(16, 18, 'belt')
        if F.front:
            F.rect(W // 2 - 1, 16, W // 2 + 1, 18, 'dr_amber')
            F.rect(1, 18, 5, 22, 'ro_pouch')
    elif p == 'arm':
        if F.face == 'bottom':
            F.rows(0, H, 'sn_leather'); return
        F.rows(0, 24, 'sn_cloak', bevel=False)
        F.rows(0, 5, 'dr_leafy')                          # feuilles à l'épaule
        F.rows(13, 22, 'dr_bark')                         # brassard d'écorce lacé
        F.rows(15, 16, 'belt', bevel=False)
        F.rows(19, 20, 'belt', bevel=False)
        F.rows(22, 24, 'sn_leather')
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'sn_leather'); return
        F.rows(13, 24, 'sn_leather')
        F.rows(12, 15, 'ro_fur')
        F.rows(18, 21, 'dr_bark')
        F.rows(22, 24, 'leather_hd_d')
        F.clear(0, 0, W, 12)
    elif p == 'leg':
        F.rows(0, 18, 'sn_cloak_d', bevel=False)
        if F.front or F.side:
            F.rect(1, 5, W - 1, 12, 'sn_leather')
            F.rect(1, 7, W - 1, 8, 'dr_leafy', bevel=False)
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'sn_cloak_d', bevel=False)
        F.rows(18, 20, 'belt')
        F.clear(0, 0, W, 18)


def arcaniste(F):
    """Arcaniste de guerre (Mage, Lame-runique) : robe violette, plaques d'acier sombre, runes d'azur."""
    p, W, H = F.part, F.w, F.h
    if p == 'body':
        if F.cap:
            F.rows(0, H, 'lr_plate'); return
        F.rows(0, 24, 'ar_robe', bevel=False)
        F.rows(0, 2, 'lr_silver')
        if F.front or F.back:
            F.rect(2, 2, W - 2, 12, 'lr_plate')           # plastron d'acier sombre
            F.rect(2, 12, W - 2, 13, 'lr_silver', bevel=False)
            if F.front:
                cx = W // 2                                # cercle runique
                for (dx, dy) in ((-2, 0), (-1, -1), (0, -2), (1, -2), (2, -1), (3, 0), (3, 1), (2, 2), (1, 3),
                                 (0, 3), (-1, 2), (-2, 1)):
                    F.px(cx + dx - 1, 7 + dy - 1, (110, 230, 255))
                F.rect(cx - 1, 6, cx + 1, 8, 'ar_rune')
                F.rect(cx - 1, 13, cx + 1, 24, 'ar_robe_l')   # ouverture de la robe
            else:
                F.rect(W // 2 - 1, 4, W // 2 + 1, 10, 'ar_rune', bevel=False)
        F.rows(14, 16, 'ma_sash')
    elif p == 'arm':
        if F.face == 'bottom':
            F.rows(0, H, 'ar_robe'); return
        F.rows(0, 24, 'ar_robe', bevel=False)
        F.rows(0, 7, 'lr_plate')                          # spalière
        F.rows(6, 7, 'lr_silver', bevel=False)
        F.rows(17, 22, 'ar_robe_l')
        F.rows(22, 24, 'lr_silver')
        if not F.cap:
            F.rect(W // 2 - 1, 2, W // 2 + 1, 5, 'ar_rune')
            F.rect(W // 2 - 1, 19, W // 2 + 1, 20, 'ar_rune', bevel=False)
    elif p == 'boot':
        if F.cap:
            F.rows(0, H, 'lr_plate'); return
        F.rows(14, 24, 'lr_plate_d')
        F.rows(14, 15, 'lr_silver', bevel=False)
        if F.front:
            F.rect(W // 2 - 1, 17, W // 2 + 1, 20, 'ar_rune')
        F.rows(22, 24, 'lr_silver')
        F.clear(0, 0, W, 14)
    elif p == 'leg':
        F.rows(0, 18, 'ar_robe', bevel=False)
        F.rows(14, 17, 'ar_robe_l')
        F.rows(17, 18, 'lr_silver', bevel=False)
        if F.front or F.side:
            F.rect(1, 6, W - 1, 11, 'lr_plate')
            F.rect(W // 2 - 1, 7, W // 2 + 1, 10, 'ar_rune')
        F.clear(0, 18, W, H)
    elif p == 'waist':
        F.rows(18, 24, 'ar_robe', bevel=False)
        F.rows(18, 20, 'ma_sash')
        F.clear(0, 0, W, 18)


PAINTERS = {'guerrier': guerrier, 'paladin': paladin, 'mage': mage, 'rodeur': rodeur, 'druide': druide,
            'lamerunique': lamerunique, 'gardeserment': gardeserment, 'sentinelle': sentinelle, 'arcaniste': arcaniste}


def faces(u, v, w, hh, d):
    return {'top': (u + d, v, w, d), 'bottom': (u + d + w, v, w, d), 'right': (u, v + d, d, hh),
            'front': (u + d, v + d, w, hh), 'left': (u + d + w, v + d, d, hh), 'back': (u + 2 * d + w, v + d, w, hh)}


BODY, ARM, LEG = (16, 16, 8, 12, 4), (40, 16, 4, 12, 4), (0, 16, 4, 12, 4)


def paint_box(layer, key, box, part, seed, skip=(), tier='rare'):
    for name, (x, y, w, hh) in faces(*box).items():
        if name in skip:
            continue
        F = Face(part, name, w * K, hh * K, seed)
        PAINTERS[key](F)
        raretes.trim_face(F, tier)
        layer.alpha_composite(F.img, (x * K, y * K))


def layers_hd(key, tier='rare'):
    """Calques 1 et 2 de la panoplie, au palier de rareté donné (raretes.TIERS)."""
    with raretes.palier(tier):
        return _layers_hd(key, tier)


def _layers_hd(key, tier):
    l1 = Image.new('RGBA', (64 * K, 32 * K), (0, 0, 0, 0))
    paint_box(l1, key, BODY, 'body', 2, tier=tier)
    paint_box(l1, key, ARM, 'arm', 3, tier=tier)
    paint_box(l1, key, LEG, 'boot', 4, skip=('top',), tier=tier)
    l2 = Image.new('RGBA', (64 * K, 32 * K), (0, 0, 0, 0))
    paint_box(l2, key, BODY, 'waist', 5, skip=('top', 'bottom'), tier=tier)
    paint_box(l2, key, LEG, 'leg', 6, skip=('top', 'bottom'), tier=tier)
    return l1, l2


def preview(keys, tier='rare'):
    """Mannequins de face et de dos (casque 3D non représenté)."""
    S = 6
    sheet = Image.new('RGBA', (len(keys) * 2 * 18 * K * S // 2 + 20, 36 * K * S // 2 + 20), (40, 42, 48, 255))
    for n, key in enumerate(keys):
        l1, l2 = layers_hd(key, tier)
        for v, side in enumerate(('front', 'back')):
            fig = Image.new('RGBA', (16 * K, 32 * K), (0, 0, 0, 0))
            for (x, y, w, hh) in ((4, 0, 8, 8), (4, 8, 8, 12), (0, 8, 4, 12), (12, 8, 4, 12), (4, 20, 4, 12), (8, 20, 4, 12)):
                fig.paste((150, 120, 100, 255) if y == 0 else (90, 90, 96, 255), (x * K, y * K, (x + w) * K, (y + hh) * K))

            def put(layer, box, dst):
                fx, fy, w, hh = faces(*box)[side]
                fig.alpha_composite(layer.crop((fx * K, fy * K, (fx + w) * K, (fy + hh) * K)), (dst[0] * K, dst[1] * K))
            put(l2, BODY, (4, 8)); put(l2, LEG, (4, 20)); put(l2, LEG, (8, 20))
            put(l1, BODY, (4, 8)); put(l1, ARM, (0, 8)); put(l1, ARM, (12, 8))
            put(l1, LEG, (4, 20)); put(l1, LEG, (8, 20))
            big = fig.resize((16 * K * S // 2, 32 * K * S // 2), Image.NEAREST)
            sheet.alpha_composite(big, (10 + (n * 2 + v) * 18 * K * S // 2, 10))
    return sheet


if __name__ == '__main__':
    preview(list(PAINTERS)).save(os.path.join(HERE, 'armures_hd_apercu.png'))


def _front(layer, box):
    fx, fy, w, hh = faces(*box)['front']
    return layer.crop((fx * K, fy * K, (fx + w) * K, (fy + hh) * K))


def _outline(img):
    """Contour sombre d'un pixel autour de la silhouette, pour la lisibilité dans l'inventaire."""
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    a = img.split()[3].load()
    W, H = img.size
    for y in range(H):
        for x in range(W):
            if a[x, y]:
                continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and a[x + dx, y + dy]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out.putpixel((x, y), (22, 20, 26, 255))
    out.alpha_composite(img)
    return out


def icons_hd(key, tier='rare', layers=None):
    """Icônes 32x32 tirées des calques peints : plastron, jambières, bottes (le casque est modelé en 3D)."""
    l1, l2 = layers or layers_hd(key, tier)
    chest = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    arm = _front(l1, ARM).crop((0, 0, 8, 18))
    chest.alpha_composite(arm, (1, 4))
    chest.alpha_composite(arm.transpose(Image.FLIP_LEFT_RIGHT), (23, 4))
    chest.alpha_composite(_front(l1, BODY).crop((0, 0, 16, 24)), (8, 4))
    for y in range(4, 7):                                  # encolure
        for x in range(13 + (y - 4), 19 - (y - 4)):
            chest.putpixel((x, y), (0, 0, 0, 0))
    legs = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    legs.alpha_composite(_front(l2, BODY).crop((0, 18, 16, 24)), (8, 3))
    leg = _front(l2, LEG).crop((0, 0, 8, 18))
    legs.alpha_composite(leg, (7, 9))
    legs.alpha_composite(leg.transpose(Image.FLIP_LEFT_RIGHT), (17, 9))
    boots = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    boot = _front(l1, LEG).crop((0, 12, 8, 24))
    for i, x in enumerate((5, 19)):
        b = boot if i == 0 else boot.transpose(Image.FLIP_LEFT_RIGHT)
        boots.alpha_composite(b, (x, 9))
        boots.alpha_composite(b.crop((0, 8, 8, 12)), (x - 2 if i == 0 else x + 2, 17))   # pied qui dépasse vers l'avant
    return {'chestplate': _outline(chest), 'leggings': _outline(legs), 'boots': _outline(boots)}
