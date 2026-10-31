"""Heaumes épiques : casques de classe sculptés pièce par pièce, dans l'esprit des MMORPG (plaques étagées, cimiers,
cornes et ailes, filigrane d'or, regards lumineux).

Repère casques3d : la tête occupe 4..12 sur les trois axes, l'avant est côté z bas, coque S..E (3.4..12.6).
Règle anti-scintillement : aucune face extérieure entre 3.5 et 4.0 ni entre 12.0 et 12.5 (calque « chapeau » du skin).

Outils :
  H.b(a, b, mat, rot)        pavé, rotation facultative R(axe, angle, origine)
  H.m(a, b, mat, rot)        pavé + son miroir gauche/droite (x -> 16 - x)
  H.limb(base, segs, ...)    pièce courbe (corne, aile, plume) : suite de segments orientés tous les 22.5°
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'items'))
sys.path.insert(0, HERE)
from PIL import Image, ImageDraw  # noqa: E402
from kit import Item, Mat, MATS, h, mix  # noqa: E402
from render import render  # noqa: E402
from casques3d import HELMET, S, E, hammered, brushed, filigree, cloth_folds, leather, fur, feathers, bark_grain, \
    leaves, horn_rings, starry  # noqa: E402


# ==================================================================================================================
#  Motifs
# ==================================================================================================================

def plate(c, p, face, px, py, w, hgt):
    """Plaque forgée : reflet en haut de la pièce, ombre en bas, martelage fin."""
    t = py / max(1, hgt - 1) if face not in ('up', 'down') else 0.4
    k = 1.12 - 0.3 * t
    k *= 0.94 + 0.1 * h(int(p[0] * 3), int(p[1] * 3), int(p[2] * 3))
    if face == 'up':
        k *= 1.12
    return tuple(v * k for v in c)


def gold(c, p, face, px, py, w, hgt):
    """Or ciselé : volutes sombres, éclats clairs."""
    s = math.sin(p[0] * 3.1 + math.sin(p[1] * 2.7) * 1.6) + math.sin(p[2] * 3.1 + p[1] * 1.7)
    if abs(s) < 0.2:
        return tuple(v * 0.62 for v in c)
    if h(int(p[0] * 4), int(p[1] * 4), int(p[2] * 4)) > 0.93:
        return mix(c, (255, 250, 220), 0.6)
    t = py / max(1, hgt - 1) if face not in ('up', 'down') else 0.3
    return tuple(v * (1.1 - 0.22 * t) for v in c)


def engraved(c, p, face, px, py, w, hgt):
    """Acier gravé : entrelacs fins plus sombres sur une plaque forgée."""
    c = plate(c, p, face, px, py, w, hgt)
    s = math.sin((p[0] + p[2]) * 2.2) * math.cos(p[1] * 2.2)
    return tuple(v * 0.7 for v in c) if abs(s) < 0.08 else c


def runes(col):
    def f(c, p, face, px, py, w, hgt):
        c = plate(c, p, face, px, py, w, hgt)
        gx, gy = int((p[0] + p[2]) * 2.5) % 6, int(p[1] * 2.5) % 5
        cell = h(int((p[0] + p[2]) * 2.5) // 6, int(p[1] * 2.5) // 5, 3)
        if cell > 0.55 and ((gx == 2 and gy < 4) or (gy == 1 and 1 <= gx <= 3) or (gy == 3 and gx in (1, 3))):
            return col
        return c
    return f


def feather_vanes(c, p, face, px, py, w, hgt):
    """Plume : rachis central clair, barbes obliques."""
    u = (px + 0.5) / w
    if abs(u - 0.5) < 0.08:
        return mix(c, (255, 255, 255), 0.4)
    k = 0.86 + 0.16 * (((py + int(abs(u - 0.5) * 8)) % 3) == 0)
    return tuple(v * k * (1.05 - 0.25 * abs(u - 0.5)) for v in c)


def horn(c, p, face, px, py, w, hgt):
    """Corne annelée, plus sombre vers la pointe."""
    k = 0.85 + 0.2 * (int((p[0] + p[1] * 1.3 + p[2]) * 1.6) % 2)
    return tuple(v * k for v in c)


def crystal(c, p, face, px, py, w, hgt):
    t = (px + py) / max(1, w + hgt - 2)
    if abs(px - py) <= 0 or (px + py) == max(w, hgt) - 1:
        return mix(c, (255, 255, 255), 0.55)
    return tuple(min(255, v * (1.25 - 0.45 * t)) for v in c)


def cloth(c, p, face, px, py, w, hgt):
    c = cloth_folds(c, p, face, px, py, w, hgt)
    t = py / max(1, hgt - 1) if face not in ('up', 'down') else 0.2
    return tuple(v * (1.08 - 0.22 * t) for v in c)


def stars(c, p, face, px, py, w, hgt):
    c = cloth(c, p, face, px, py, w, hgt)
    if h(int(p[0] * 5), int(p[1] * 5), int(p[2] * 5)) > 0.975:
        return (255, 236, 170)
    return c


def bone(c, p, face, px, py, w, hgt):
    k = 0.9 + 0.12 * h(int(p[0] * 4), int(p[1] * 4), int(p[2] * 4))
    if h(int(p[0] * 6), int(p[1] * 2), int(p[2] * 6)) > 0.95:
        k *= 0.7
    return tuple(v * k for v in c)


def mail(c, p, face, px, py, w, hgt):
    x, y = int((p[0] + p[2]) * 4), int(p[1] * 4)
    ring = (x + (y // 2) % 2) % 2 == 0 and y % 2 == 0
    return tuple(v * (1.15 if ring else 0.72) for v in c)


def M(name, rgb, pattern=None, noise=5, edge=0.68, light=0, hi=True):
    MATS[name] = Mat(rgb, noise, edge, pattern=pattern, light=light,
                     hi=tuple(min(255, int(v * 1.3 + 40)) for v in rgb) if hi else None)
    return name


def glow(name, rgb, level=15):
    MATS[name] = Mat(rgb, 3, 0.95, light=level, hi=(255, 255, 255))
    return name


# ==================================================================================================================
#  Outils de modelage
# ==================================================================================================================

def R(axis, angle, origin):
    return {'axis': axis, 'angle': angle, 'origin': list(origin)}


def _rot(axis, deg, v):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    x, y, z = v
    if axis == 'x':
        return (x, c * y - s * z, s * y + c * z)
    if axis == 'y':
        return (c * x + s * z, y, -s * x + c * z)
    return (c * x - s * y, s * x + c * y, z)


# plan de courbure -> (axe de rotation, direction à 0°)
PLANES = {'xy': ('z', (0, 1, 0)), 'zy': ('x', (0, 1, 0)), 'xz': ('y', (0, 0, 1))}


class H:
    def __init__(self, id, cx=8, density=4):
        self.it = Item(id, density=density, display=HELMET)
        self.cx = cx        # axe du miroir gauche/droite
        self.bone = None    # os courant (modèles BetterModel)

    def b(self, a, b, mat, rot=None, faces=None, light=None):
        a, b = [min(a[i], b[i]) for i in range(3)], [max(a[i], b[i]) for i in range(3)]
        self.it.box(tuple(a), tuple(b), mat, faces=faces, light=light)
        self.it.els[-1]['bone'] = self.bone
        if rot and rot['angle']:
            self.it.els[-1]['rot'] = rot
        return self

    def m(self, a, b, mat, rot=None, **kw):
        self.b(a, b, mat, rot, **kw)
        c2 = 2 * self.cx
        ma, mb = (c2 - b[0], a[1], a[2]), (c2 - a[0], b[1], b[2])
        mr = None
        if rot:
            o = rot['origin']
            mr = R(rot['axis'], rot['angle'] if rot['axis'] == 'x' else -rot['angle'], (c2 - o[0], o[1], o[2]))
        return self.b(ma, mb, mat, mr, **kw)

    def limb(self, base, segs, mats, plane='xy', mirror=False, depth=None):
        """segs : [(longueur, angle, largeur), ...]. L'angle (multiple de 22.5) se mesure depuis la verticale ;
        positif = vers -x (plan xy), vers +z (plan zy) ou vers +x (plan xz). depth : épaisseur hors du plan
        (par défaut = largeur). Renvoie la pointe."""
        axis, up = PLANES[plane]
        q = _rot(axis, 90, up)
        bases = [(0, up), (90, q), (180, tuple(-v for v in up)), (-90, tuple(-v for v in q))]
        p = list(base)
        n = len(segs)
        for i, (L, ang, w) in enumerate(segs):
            mat = mats[min(len(mats) - 1, int(i * len(mats) / n))]
            ba, bv = min(bases, key=lambda t: abs(((ang - t[0] + 180) % 360) - 180))
            res = ((ang - ba + 180) % 360) - 180
            d = w if depth is None else depth * (w / segs[0][2])
            ext = L + w * 0.35
            lo, hi = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
            for k in range(3):
                if bv[k] > 0.5:
                    lo[k], hi[k] = p[k] - w * 0.2, p[k] + ext
                elif bv[k] < -0.5:
                    lo[k], hi[k] = p[k] - ext, p[k] + w * 0.2
                elif k == 'xyz'.index(axis):
                    lo[k], hi[k] = p[k] - d / 2, p[k] + d / 2
                else:
                    lo[k], hi[k] = p[k] - w / 2, p[k] + w / 2
            rot = R(axis, res, p) if res else None
            self.b(lo, hi, mat, rot)
            if mirror:
                c2 = 2 * self.cx
                ma, mb = (c2 - hi[0], lo[1], lo[2]), (c2 - lo[0], hi[1], hi[2])
                mr = R(axis, res if axis == 'x' else -res, (c2 - p[0], p[1], p[2])) if res else None
                self.b(ma, mb, mat, mr)
            dv = _rot(axis, ang, up)
            p = [p[k] + dv[k] * L for k in range(3)]
        return p

    def limbs(self, base, segs, mats, plane='xy', depth=None):
        return self.limb(base, segs, mats, plane, mirror=True, depth=depth)


# ==================================================================================================================
#  Pièces communes
# ==================================================================================================================

def helm_shell(x, m, s=2.9, top=13.8, ch=1.8, cv=1.2, y0=3.0, trim=None, trim_v=None):
    """Coque de heaume plus large que la tête, arêtes du dessus et coins verticaux chanfreinés (fini le cube).
    s : demi-largeur extérieure depuis 8 (bord à 8-s.. non : bord x = s .. 16-s)."""
    a, b = s, 16 - s
    t = 0.5
    if cv:                                                                   # corps en croix (coins chanfreinés)
        x.b((a + cv, y0, a), (b - cv, top - ch, b), m)
        x.b((a, y0, a + cv), (b, top - ch, b - cv), m)
    else:
        x.b((a, y0, a), (b, top - ch, b), m)
    x.b((a + ch, top - ch, a + ch), (b - ch, top, b - ch), m)                # dessus
    L = ch * math.sqrt(2) + 0.4
    ym = top - ch / 2
    # chanfreins du dessus : avant, arrière, gauche, droite
    x.b((a + 0.2, ym - L / 2, a + ch / 2 - t / 2), (b - 0.2, ym + L / 2, a + ch / 2 + t / 2), trim or m, R('x', 45, (8, ym, a + ch / 2)))
    x.b((a + 0.2, ym - L / 2, b - ch / 2 - t / 2), (b - 0.2, ym + L / 2, b - ch / 2 + t / 2), trim or m, R('x', -45, (8, ym, b - ch / 2)))
    x.b((a + ch / 2 - t / 2, ym - L / 2, a + 0.2), (a + ch / 2 + t / 2, ym + L / 2, b - 0.2), trim or m, R('z', -45, (a + ch / 2, ym, 8)))
    x.b((b - ch / 2 - t / 2, ym - L / 2, a + 0.2), (b - ch / 2 + t / 2, ym + L / 2, b - 0.2), trim or m, R('z', 45, (b - ch / 2, ym, 8)))
    # coins verticaux
    if cv:
        Lv = cv * math.sqrt(2) + 0.3
        for (cx, cz, ang) in ((a + cv / 2, a + cv / 2, -45), (b - cv / 2, a + cv / 2, 45),
                              (a + cv / 2, b - cv / 2, 45), (b - cv / 2, b - cv / 2, -45)):
            x.b((cx - t / 2, y0, cz - Lv / 2), (cx + t / 2, top - ch + 0.2, cz + Lv / 2), trim or m, R('y', ang, (cx, 0, cz)))
    return top


def octo(x, cx, cz, y0, y1, r, m, rot_mat=None):
    """Prisme octogonal (hors de la tête) : carré + carré tourné de 45°."""
    x.b((cx - r, y0, cz - r), (cx + r, y1, cz + r), m)
    k = r * 0.94
    x.b((cx - k, y0 + 0.01, cz - k), (cx + k, y1 - 0.01, cz + k), rot_mat or m, R('y', 45, (cx, 0, cz)))


def mantle(x, m, m2=None, y0=2.6, y1=4.3):
    """Col / pèlerine posé sur les épaules, évasé."""
    x.b((1.6, y0, 2.4), (14.4, y1, 13.8), m)
    x.b((2.4, y1, 3.0), (13.6, y1 + 0.6, 13.2), m2 or m)


def band(x, y0, y1, m, s=3.1):
    x.b((s, y0, s), (16 - s, y1, 16 - s), m)


# ==================================================================================================================
#  Les neuf heaumes légendaires
# ==================================================================================================================

def guerrier():
    """Seigneur de guerre : heaume noir à proue, cornes de bélier immenses, crinière rouge, regard de braise."""
    st = M('he_gu_steel', (66, 68, 80), engraved)
    st2 = M('he_gu_steel2', (104, 106, 118), plate)
    gd = M('he_gu_gold', (222, 168, 60), gold)
    rd = M('he_gu_red', (156, 26, 24), cloth, noise=8, edge=0.8, hi=False)
    hn = M('he_gu_horn', (220, 196, 150), horn, edge=0.78)
    hn2 = M('he_gu_horn2', (110, 86, 62), horn, edge=0.8)
    ey = glow('he_gu_eye', (255, 120, 40))
    sl = M('he_gu_slit', (12, 8, 10), None, 2, 1, hi=False)
    x = H('casque3d_proto_guerrier')
    top = helm_shell(x, st, s=2.9, top=13.8, ch=1.8, cv=1.2, trim=st2)
    # proue en V devant le visage, arête d'or, fentes rougeoyantes
    x.m((3.2, 3.0, 2.3), (8.2, 9.4, 2.9), st2, R('y', 22.5, (8, 0, 2.3)))
    x.m((3.9, 7.6, 2.0), (7.4, 8.5, 2.4), sl, R('y', 22.5, (8, 0, 2.3)))
    x.m((4.4, 7.8, 1.9), (7.0, 8.3, 2.1), ey, R('y', 22.5, (8, 0, 2.3)))
    x.b((7.3, 2.8, 1.2), (8.7, 10.0, 2.3), gd)
    for yy in (4.0, 5.2, 6.4):                                              # grille de souffle
        x.m((4.6, yy, 2.0), (7.2, yy + 0.4, 2.3), sl, R('y', 22.5, (8, 0, 2.3)))
    # front lourd en V
    x.m((2.6, 9.2, 1.8), (8.4, 10.8, 3.2), gd, R('z', -22.5, (8, 9.6, 2.5)))
    # protège-joues évasés, rivets
    x.m((2.2, 2.6, 4.2), (2.9, 8.6, 10.4), st2)
    x.m((2.0, 2.6, 4.2), (2.3, 8.6, 4.8), gd)
    x.m((2.0, 2.6, 4.2), (2.3, 3.0, 10.4), gd)
    for yy in (4.0, 6.0, 8.0):
        x.m((1.9, yy, 7.0), (2.2, yy + 0.5, 7.5), gd)
    # garde-nuque étagé
    for i, y in enumerate((2.6, 4.0, 5.4)):
        x.b((3.1, y, 13.1), (12.9, y + 1.6, 13.9 - i * 0.25), st2 if i % 2 else st)
        x.b((3.1, y, 13.9 - i * 0.25), (12.9, y + 0.3, 14.1 - i * 0.25), gd)
    band(x, 10.8, 11.5, gd, s=2.6)
    for (cx, cz) in ((4.0, 4.0), (12.0, 4.0), (4.0, 12.0), (12.0, 12.0)):     # bossettes aux coins du dessus
        x.b((cx - 0.6, 11.7, cz - 0.6), (cx + 0.6, 12.9, cz + 0.6), gd, R('y', 45, (cx, 0, cz)))
    # crête dentelée
    for i, hgt in enumerate((1.4, 2.4, 3.0, 2.6, 1.8, 1.0)):
        z = 4.8 + i * 1.15
        x.b((7.5, top - 0.3, z), (8.5, top + hgt, z + 0.9), gd if i % 2 == 0 else st2)
    # crinière rouge
    x.limb((8, top + 0.8, 10.0), [(2.0, 112.5, 1.8), (2.4, 135, 1.6), (2.6, 157.5, 1.4), (2.6, 180, 1.1)],
           [rd], plane='zy', depth=2.6)
    # cornes de bélier
    for mir in (False, True):
        sx = 1 if not mir else -1
        b = (2.6, 10.6, 8.0) if not mir else (13.4, 10.6, 8.0)
        segs = [(1.7, 90, 2.4), (1.7, 67.5, 2.2), (1.7, 45, 1.9), (1.7, 22.5, 1.6), (1.5, 0, 1.3), (1.3, -22.5, 1.0),
                (1.1, -45, 0.7)]
        if mir:
            segs = [(L, -a, w) for L, a, w in segs]
        x.limb(b, segs, [hn, hn, hn, hn, hn2], plane='xy')
        x.b((b[0] - 0.7 * sx, 9.6, 6.6), (b[0] + 0.4 * sx, 11.6, 9.4), gd)
    return x.it


def paladin():
    """Croisé céleste : argent blanc et or, grandes ailes, couronne solaire, fente bleue en croix."""
    sv = M('he_pa_silver', (214, 218, 230), plate)
    sv2 = M('he_pa_silver2', (186, 192, 208), engraved)
    gd = M('he_pa_gold', (236, 186, 70), gold)
    wh = M('he_pa_wing', (248, 246, 238), feather_vanes, noise=4, edge=0.84, hi=False)
    wh2 = M('he_pa_wing2', (218, 224, 240), feather_vanes, noise=4, edge=0.84, hi=False)
    bl = glow('he_pa_eye', (140, 210, 255))
    hl = glow('he_pa_holy', (255, 232, 140), 13)
    gm = glow('he_pa_gem', (90, 160, 255), 12)
    sl = M('he_pa_slit', (20, 22, 34), None, 2, 1, hi=False)
    x = H('casque3d_proto_paladin')
    top = helm_shell(x, sv, s=2.9, top=14.0, ch=2.0, cv=1.2, trim=sv2, trim_v=gd)
    # masque bombé en V, croix lumineuse
    x.m((3.2, 3.0, 2.3), (8.2, 10.4, 2.9), sv2, R('y', 22.5, (8, 0, 2.3)))
    x.m((3.8, 7.9, 2.0), (7.8, 8.6, 2.2), bl, R('y', 22.5, (8, 0, 2.3)))
    x.b((7.5, 4.0, 1.4), (8.5, 9.6, 2.3), sv2)
    x.b((7.6, 4.4, 1.2), (8.4, 9.2, 1.4), bl)
    x.b((7.3, 9.6, 1.4), (8.7, 12.8, 2.6), gd)                              # arête d'or montante
    x.m((2.8, 9.8, 1.9), (7.4, 10.6, 2.9), gd, R('z', 22.5, (7.4, 10.2, 2.4)))
    x.b((7.1, 11.0, 1.0), (8.9, 12.6, 1.4), gm)
    band(x, 2.8, 3.4, gd, s=2.6)
    # couronne solaire
    for ang in (-45, -22.5, 0, 22.5, 45):
        L = 3.8 if ang == 0 else (3.0 if abs(ang) < 30 else 2.4)
        x.limb((8, top - 0.2, 10.4), [(L, ang, 0.9)], [gd], plane='xy', depth=0.5)
    x.b((6.8, top - 0.2, 10.0), (9.2, top + 0.8, 10.8), hl)
    # ailes : pennes serrées qui forment une vraie surface
    for mir in (False, True):
        bx = 2.6 if not mir else 13.4
        x.b((bx - 0.8, 7.0, 6.0) if not mir else (bx, 7.0, 6.0), (bx, 11.4, 10.6) if not mir else (bx + 0.8, 11.4, 10.6), gd)
        tiers = ((10.6, [(2.2, 45, 1.5), (2.4, 22.5, 1.3), (2.6, 0, 1.1), (1.8, -22.5, 0.7)], wh),
                 (9.4, [(2.0, 67.5, 1.4), (2.2, 45, 1.2), (2.2, 22.5, 1.0), (1.4, 0, 0.6)], wh2),
                 (8.2, [(1.8, 90, 1.3), (2.0, 67.5, 1.0), (1.6, 45, 0.7)], wh))
        for k, (y, segs, mat) in enumerate(tiers):
            for j in range(6):
                dz = 6.4 + j * 0.75 + k * 0.2
                sc = 1.0 - 0.07 * j
                segs2 = [(L * sc, a if not mir else -a, w) for L, a, w in segs]
                x.limb((bx + (-0.3 if not mir else 0.3), y, dz), segs2, [mat], plane='xy', depth=0.55)
    return x.it


def mage():
    """Archimage : grand chapeau à bord rond, cône tordu, bande d'or, cristal et plume."""
    cl = M('he_ma_cloth', (58, 52, 156), stars, noise=6, edge=0.82, hi=False)
    cl2 = M('he_ma_cloth2', (36, 32, 104), cloth, noise=6, edge=0.82, hi=False)
    gd = M('he_ma_gold', (230, 180, 74), gold)
    gm = glow('he_ma_gem', (110, 210, 255), 14)
    ft = M('he_ma_feather', (230, 90, 70), feather_vanes, noise=4, edge=0.86, hi=False)
    x = H('casque3d_proto_mage')
    # coiffe sous le chapeau, voile de nuque, visage libre
    x.b((S, 9.0, S + 1.2), (E, 12.6, E), cl2)
    x.b((S, 3.6, 7.0), (E, 9.0, E), cl2)
    x.m((S, 3.6, S), (S + 0.6, 9.0, 7.0), cl2)
    mantle(x, cl2, gd, y0=2.8, y1=3.6)
    # bord rond (octogone) légèrement relevé derrière
    octo(x, 8, 8.4, 12.6, 13.1, 8.4, cl2)
    octo(x, 8, 8.4, 13.1, 13.4, 7.0, cl)
    # bande d'or + boucle
    octo(x, 8, 8.6, 13.4, 14.6, 4.6, gd)
    x.b((6.6, 13.2, 3.4), (9.4, 14.9, 3.9), gd)
    x.b((7.3, 13.6, 3.2), (8.7, 14.5, 3.4), gm)
    # cône : octogones qui se resserrent, puis pointe pliée vers l'arrière
    y = 14.6
    for r, hgt in ((4.2, 1.3), (3.6, 1.3), (3.0, 1.3), (2.4, 1.2)):
        octo(x, 8, 9.0, y, y + hgt, r, cl)
        y += hgt
    tip = x.limb((8, y - 0.3, 9.2), [(1.6, 22.5, 3.0), (1.6, 45, 2.3), (1.6, 90, 1.7), (1.4, 135, 1.1)],
                 [cl, cl, cl2], plane='zy')
    x.b((tip[0] - 0.5, tip[1] - 0.5, tip[2] - 0.5), (tip[0] + 0.5, tip[1] + 0.5, tip[2] + 0.5), gm)
    # plume
    x.limb((12.0, 14.2, 7.0), [(1.8, -22.5, 1.2), (2.0, -22.5, 1.1), (2.0, -45, 0.9), (1.4, -67.5, 0.5)],
           [ft], plane='xy', depth=0.4)
    for (cx, cy, cz, s) in ((0.8, 16.0, 6.0, 0.7), (15.2, 17.0, 10.0, 0.6), (5.0, 18.4, 15.0, 0.5)):
        x.b((cx - s, cy - s * 1.6, cz - s), (cx + s, cy + s * 1.6, cz + s), gm, R('y', 45, (cx, cy, cz)))
    return x.it


def _hood(x, m, m2, sh, s=3.0, top=13.6):
    """Capuche fermée (coque chanfreinée), ouverture sombre sur le visage, rebord épais, pointe avant."""
    helm_shell(x, m, s=s, top=top, ch=1.8, cv=1.2)
    x.b((4.2, 3.2, s - 0.1), (11.8, 10.6, s), sh)                            # ombre du visage
    x.b((3.2, 10.4, s - 0.9), (12.8, 11.6, s), m2)                           # rebord du haut
    x.m((3.2, 3.0, s - 0.9), (4.4, 11.6, s), m2)                             # rebords latéraux
    x.limb((8, 11.0, s - 0.5), [(1.4, -22.5, 3.2), (1.2, -45, 1.8)], [m2], plane='zy', depth=6.0)  # pointe avant
    x.limb((8, top - 0.6, 12.0), [(1.8, 135, 3.4), (2.0, 157.5, 2.4), (1.8, 180, 1.4)], [m, m2], plane='zy')


def rodeur():
    """Assassin : capuche profonde, masque de crâne, regard vert, pèlerine et dagues de dos."""
    hd = M('he_ro_hood', (46, 58, 46), cloth, noise=6, edge=0.82, hi=False)
    hd2 = M('he_ro_hood2', (30, 38, 32), cloth, noise=6, edge=0.82, hi=False)
    bn = M('he_ro_bone', (228, 216, 188), bone, edge=0.74)
    lt = M('he_ro_leather', (104, 66, 40), leather, edge=0.78, hi=False)
    sv = M('he_ro_steel', (176, 182, 194), plate)
    ey = glow('he_ro_eye', (120, 255, 140))
    sh = M('he_ro_shadow', (8, 10, 8), None, 2, 1, hi=False)
    x = H('casque3d_proto_rodeur')
    _hood(x, hd, hd2, sh)
    mantle(x, hd2, lt)
    # masque de crâne
    x.b((4.6, 3.2, 2.4), (11.4, 7.6, 3.0), bn)
    x.b((5.2, 7.6, 2.6), (10.8, 8.0, 3.0), bn)
    for i in range(6):
        xx = 5.1 + i * 1.0
        x.b((xx, 3.4, 2.3), (xx + 0.45, 4.6, 2.4), sh)
    x.b((7.5, 5.4, 2.3), (8.5, 6.6, 2.4), sh)
    x.m((5.2, 5.0, 2.3), (6.6, 6.6, 2.4), sh)                               # orbites basses du crâne
    x.m((5.4, 8.6, 2.85), (7.0, 9.3, 2.95), ey)                               # regard dans l'ombre
    # sangle, boucle, dagues croisées
    x.b((2.8, 7.6, 2.8), (13.2, 8.2, 13.2), lt)
    x.m((2.6, 7.4, 7.2), (2.8, 8.4, 8.6), sv)
    for mir in (False, True):
        segs = [(4.0, -45, 0.7), (2.4, -45, 0.4)] if not mir else [(4.0, 45, 0.7), (2.4, 45, 0.4)]
        b = (5.6, 7.6, 13.6) if not mir else (10.4, 7.6, 13.6)
        x.limb(b, segs, [lt, sv], plane='xy', depth=0.3)
    return x.it


def druide():
    """Gardien sylvestre : masque de cerf en écorce, bois ramifiés, couronne de feuilles, yeux d'ambre."""
    wd = M('he_dr_wood', (104, 74, 46), bark_grain, edge=0.76, hi=False)
    wd2 = M('he_dr_wood2', (76, 52, 32), bark_grain, edge=0.76, hi=False)
    an = M('he_dr_antler', (228, 212, 178), horn, edge=0.78)
    lf = M('he_dr_leaf', (84, 164, 70), leaves, noise=10, edge=0.8, hi=False)
    lf2 = M('he_dr_leaf2', (56, 120, 52), leaves, noise=10, edge=0.8, hi=False)
    ms = M('he_dr_moss', (98, 126, 62), fur, noise=12, edge=0.86, hi=False)
    fl = glow('he_dr_flower', (250, 160, 210), 6)
    ey = glow('he_dr_eye', (255, 196, 70))
    sh = M('he_dr_shadow', (14, 12, 8), None, 2, 1, hi=False)
    x = H('casque3d_proto_druide')
    top = helm_shell(x, wd, s=3.0, top=13.6, ch=1.8, cv=1.2, trim=wd2)
    # museau de cerf qui avance, arcades, yeux
    x.b((5.6, 3.0, 1.8), (10.4, 7.8, 3.0), wd2)
    x.b((6.4, 2.8, 0.6), (9.6, 5.8, 1.8), wd2)
    x.b((7.0, 4.6, 0.4), (9.0, 5.6, 0.6), sh)
    x.m((2.9, 8.4, 2.0), (7.6, 9.8, 3.0), wd2, R('z', 22.5, (7.6, 9.2, 2.5)))
    x.m((4.4, 7.4, 2.8), (6.8, 8.4, 3.0), sh)
    x.m((4.8, 7.6, 2.75), (6.4, 8.2, 2.85), ey)
    # couronne de feuilles + fleurs
    for i in range(11):
        a = i / 10 * math.pi
        cx, cz = 8 - 5.8 * math.cos(a), 8.2 - 5.8 * math.sin(a)
        x.b((cx - 1.0, 11.0, cz - 1.0), (cx + 1.0, 12.8 + (i % 2) * 0.7, cz + 1.0), lf if i % 2 else lf2,
            R('y', 45, (cx, 11, cz)))
    for (cx, cz) in ((3.4, 5.2), (12.6, 5.2), (8.0, 2.4), (5.4, 3.0), (10.6, 3.0)):
        x.b((cx - 0.5, 12.6, cz - 0.5), (cx + 0.5, 13.4, cz + 0.5), fl)
    x.b((4.8, top - 0.1, 4.8), (11.2, top + 0.5, 11.2), ms)
    x.b((2.7, 2.8, 12.6), (13.3, 9.2, 13.4), ms)
    x.m((2.4, 4.0, 6.0), (2.9, 10.6, 11.4), lf2)
    # bois de cerf
    for mir in (False, True):
        sgn = 1 if not mir else -1
        bx = 5.2 if not mir else 10.8
        main = [(1.8, 22.5, 1.2), (1.8, 22.5, 1.1), (2.0, 0, 1.0), (2.0, -22.5, 0.8), (1.6, 0, 0.6)]
        x.limb((bx, top - 0.2, 8.6), [(L, a * sgn, w) for L, a, w in main], [an], plane='xy')
        for (yy, segs) in ((top + 2.2, [(1.8, 67.5, 0.65), (1.4, 22.5, 0.45)]),
                           (top + 4.0, [(1.6, 45, 0.55), (1.2, 0, 0.4)]),
                           (top + 3.2, [(1.6, -22.5, 0.5), (1.0, 0, 0.35)])):
            t = (yy - top) / 7.0
            x.limb((bx - sgn * (0.6 + 2.2 * t), yy, 8.6), [(L, a * sgn, w) for L, a, w in segs], [an], plane='xy')
        x.limb((bx - sgn * 0.6, top + 1.2, 8.8), [(1.6, 22.5, 0.5), (1.2, 45, 0.35)], [an], plane='zy')
    return x.it


def lamerunique():
    """Chevalier runique : acier noir à arêtes vives, runes violettes, lames de cimier, éclats en orbite."""
    st = M('he_lr_steel', (46, 44, 58), runes((200, 120, 255)))
    st2 = M('he_lr_steel2', (78, 76, 96), plate)
    sv = M('he_lr_silver', (188, 188, 206), plate)
    gl = glow('he_lr_glow', (196, 110, 255))
    sl = M('he_lr_slit', (10, 8, 16), None, 2, 1, hi=False)
    x = H('casque3d_proto_lamerunique')
    top = helm_shell(x, st, s=2.9, top=13.6, ch=1.8, cv=1.2, trim=sv)
    # visière en bec
    x.m((3.2, 3.6, 2.2), (8.2, 9.4, 2.9), st2, R('y', 22.5, (8, 0, 2.2)))
    x.b((7.6, 3.2, 0.8), (8.4, 9.8, 2.2), sv)
    x.m((3.8, 7.7, 1.9), (7.4, 8.4, 2.2), sl, R('y', 22.5, (8, 0, 2.2)))
    x.m((4.4, 7.9, 1.8), (7.0, 8.2, 1.95), gl, R('y', 22.5, (8, 0, 2.2)))
    x.m((2.8, 9.2, 1.8), (8.4, 9.9, 3.0), sv, R('z', -22.5, (8, 9.5, 2.4)))
    # lames de cimier
    x.limb((8, top - 0.2, 6.0), [(2.6, 22.5, 1.8), (2.6, 45, 1.5), (2.8, 67.5, 1.1), (2.4, 90, 0.6)],
           [sv, sv, gl], plane='zy', depth=0.6)
    for mir in (False, True):
        sg = 1 if not mir else -1
        bx = 2.8 if not mir else 13.2
        bx = 2.5 if not mir else 13.5
        x.limb((bx, 10.4, 5.0), [(2.4, 45, 1.8), (2.6, 67.5, 1.4), (2.4, 90, 0.9), (1.4, 112.5, 0.5)],
               [st2, sv, sv, gl], plane='zy', depth=0.4)
        x.limb((bx, 8.0, 7.0), [(2.2, 67.5, 1.4), (2.2, 90, 1.0), (1.4, 112.5, 0.5)], [st2, sv], plane='zy', depth=0.4)
    for i, y in enumerate((2.6, 4.2)):
        x.b((3.1, y, 13.1), (12.9, y + 1.8, 13.9 - i * 0.3), st2)
    x.m((2.55, 6.0, 6.4), (2.7, 9.6, 6.9), gl)
    x.m((2.55, 7.6, 5.6), (2.7, 8.1, 7.7), gl)
    for (cx, cy, cz, s) in ((0.2, 13.6, 5.0, 0.5), (15.8, 12.2, 9.0, 0.6), (8.0, 19.4, 13.6, 0.4)):
        x.b((cx - s, cy - s * 1.8, cz - s), (cx + s, cy + s * 1.8, cz + s), gl, R('y', 45, (cx, cy, cz)))
    return x.it


def gardeserment():
    """Garde du serment : grand heaume en tonneau, couronne d'or, cimier écarlate, grille lumineuse."""
    st = M('he_gs_steel', (150, 156, 170), engraved)
    st2 = M('he_gs_steel2', (122, 128, 144), plate)
    gd = M('he_gs_gold', (232, 180, 64), gold)
    rd = M('he_gs_red', (176, 30, 34), feather_vanes, noise=5, edge=0.84, hi=False)
    bl = M('he_gs_blue', (34, 58, 140), cloth, noise=6, edge=0.82, hi=False)
    ey = glow('he_gs_eye', (255, 220, 120))
    sl = M('he_gs_slit', (16, 14, 18), None, 2, 1, hi=False)
    x = H('casque3d_proto_gardeserment')
    top = helm_shell(x, st, s=2.6, top=13.6, ch=1.4, cv=1.6, trim=gd)
    x.b((3.4, 3.2, 1.9), (12.6, 11.2, 2.6), st2)                            # plaque faciale
    x.b((4.0, 8.2, 1.7), (12.0, 8.9, 1.9), ey)
    x.b((7.5, 3.4, 1.3), (8.5, 11.4, 1.9), gd)
    for (xx, yy) in ((4.8, 4.6), (4.8, 6.0), (10.6, 4.6), (10.6, 6.0), (5.9, 5.3), (9.5, 5.3)):
        x.b((xx, yy, 1.8), (xx + 0.6, yy + 0.6, 1.9), sl)
    band(x, 9.4, 10.2, gd, s=2.3)
    band(x, 2.8, 3.4, gd, s=2.3)
    # couronne d'or à fleurons
    octo(x, 8, 8, top - 0.6, top + 0.6, 4.6, gd)
    for i in range(8):
        a = i / 8 * 2 * math.pi
        cx, cz = 8 + 4.4 * math.sin(a), 8 - 4.4 * math.cos(a)
        hh = 1.8 if i % 2 == 0 else 1.2
        x.b((cx - 0.5, top + 0.6, cz - 0.3), (cx + 0.5, top + 0.6 + hh, cz + 0.3), gd, R('y', 45 if i % 2 else 0, (cx, 0, cz)))
        if i % 2 == 0:
            x.b((cx - 0.35, top + 2.4, cz - 0.35), (cx + 0.35, top + 3.1, cz + 0.35), ey, R('y', 45, (cx, 0, cz)))
    # cimier en éventail et lambrequin
    for i, ang in enumerate((-22.5, 0, 22.5, 45, 67.5, 90)):
        L = (5.0, 5.6, 5.4, 4.8, 4.0, 3.0)[i]
        x.limb((8, top + 0.4, 7.4 + i * 0.4), [(L * 0.6, ang, 1.5), (L * 0.4, ang + 22.5, 1.1)], [rd],
               plane='zy', depth=0.9)
    x.limb((8, 12.0, 13.6), [(2.0, 157.5, 4.6), (2.6, 180, 4.0), (2.0, -157.5, 3.0)], [bl], plane='zy', depth=1.0)
    # épaulières de joue et rosaces
    x.m((1.8, 3.0, 4.0), (2.6, 9.0, 10.4), st2)
    x.m((1.4, 5.8, 6.2), (1.8, 8.2, 8.6), gd, R('x', 45, (1.6, 7.0, 7.4)))
    return x.it


def sentinelle():
    """Sentinelle elfique : heaume ajouré argent et vert, ailerons en feuilles, diadème et ambre."""
    sv = M('he_sn_silver', (210, 218, 214), plate)
    gr = M('he_sn_green', (46, 116, 78), engraved)
    gd = M('he_sn_gold', (226, 190, 96), gold)
    lf = M('he_sn_leaf', (80, 176, 100), leaves, noise=8, edge=0.8, hi=False)
    am = glow('he_sn_amber', (255, 176, 60), 13)
    hd = M('he_sn_hood', (40, 74, 52), cloth, noise=6, edge=0.82, hi=False)
    x = H('casque3d_proto_sentinelle')
    # calotte ouverte sur le visage, sommet chanfreiné
    x.b((S, 6.0, S + 1.2), (E, 12.6, E), gr)
    x.b((S, 3.6, 8.0), (E, 6.0, E), gr)
    x.m((S, 6.0, S), (S + 0.6, 12.6, S + 1.2), gr)
    x.b((S + 0.6, 10.6, S), (E - 0.6, 12.6, S + 1.2), gr)
    x.b((4.6, 12.6, 4.6), (11.4, 14.0, 11.4), gr)
    x.b((S, 12.4, 5.0), (E, 13.2, 11.0), gr, R('z', 0, (8, 0, 8)))
    for (ang, cx) in ((-45, 4.0), (45, 12.0)):
        x.b((cx - 0.3, 12.0, S + 0.4), (cx + 0.3, 14.2, E - 0.4), sv, R('z', ang, (cx, 13.1, 8)))
    x.b((S + 0.4, 12.0, 3.7), (E - 0.4, 14.2, 4.3), sv, R('x', 45, (8, 13.1, 4.0)))
    x.b((S + 0.4, 12.0, 11.7), (E - 0.4, 14.2, 12.3), sv, R('x', -45, (8, 13.1, 12.0)))
    x.m((2.8, 4.0, 3.0), (3.4, 10.6, 8.0), sv)
    x.m((2.8, 3.2, 3.2), (3.4, 4.0, 5.4), sv)
    # diadème en pointe
    x.b((3.0, 10.4, 2.8), (13.0, 11.0, 3.4), gd)
    x.limb((8, 11.0, 2.9), [(1.4, 0, 1.4), (1.2, 0, 0.8), (0.8, 0, 0.4)], [gd], plane='xy', depth=0.4)
    x.b((7.4, 10.6, 2.4), (8.6, 11.8, 2.8), am)
    x.m((4.0, 11.0, 2.9), (5.6, 11.6, 3.3), gd, R('z', -22.5, (5.6, 11.0, 3)))
    # ailerons en feuilles
    for mir in (False, True):
        sg = 1 if not mir else -1
        bx = 3.0 if not mir else 13.0
        for k, (y, segs) in enumerate(((10.0, [(2.2, 67.5, 1.5), (2.6, 45, 1.3), (2.6, 22.5, 1.0), (1.8, 0, 0.5)]),
                                       (8.6, [(2.2, 90, 1.3), (2.4, 67.5, 1.1), (2.2, 45, 0.7)]),
                                       (7.2, [(2.0, 112.5, 1.1), (2.0, 90, 0.9), (1.6, 67.5, 0.5)]))):
            for j in range(3):
                x.limb((bx, y, 8.2 + k * 0.6 + j * 0.7), [(L * (1 - 0.1 * j), a * sg, w) for L, a, w in segs],
                       [sv, sv, lf], plane='xy', depth=0.5)
    x.b((S - 0.3, 3.0, E - 0.2), (E + 0.3, 8.0, E + 0.5), hd)
    x.limb((8, 12.0, 12.8), [(2.0, 157.5, 3.6), (2.0, 180, 2.8)], [hd], plane='zy', depth=1.0)
    return x.it


def arcaniste():
    """Arcaniste : capuche de nuit étoilée, masque d'argent, cornes de cristal, halo runique flottant."""
    hd = M('he_ar_hood', (66, 40, 116), stars, noise=6, edge=0.82, hi=False)
    hd2 = M('he_ar_hood2', (42, 24, 76), cloth, noise=6, edge=0.82, hi=False)
    sv = M('he_ar_silver', (200, 202, 218), engraved)
    gd = M('he_ar_gold', (226, 184, 80), gold)
    cr = M('he_ar_crystal', (110, 220, 255), crystal, noise=3, edge=0.9, light=12, hi=False)
    gl = glow('he_ar_glow', (110, 230, 255))
    sh = M('he_ar_shadow', (6, 4, 12), None, 2, 1, hi=False)
    x = H('casque3d_proto_arcaniste')
    _hood(x, hd, hd2, sh)
    mantle(x, hd2, gd)
    x.b((4.8, 3.4, 2.4), (11.2, 10.0, 3.0), sv)                             # masque d'argent
    x.b((7.6, 3.4, 2.2), (8.4, 10.0, 2.4), gd)
    x.m((5.3, 7.8, 2.25), (7.0, 8.5, 2.4), gl)
    x.m((5.6, 5.0, 2.25), (6.0, 7.0, 2.4), gl)
    for mir in (False, True):
        sg = 1 if not mir else -1
        bx = 5.0 if not mir else 11.0
        x.limb((bx, 13.2, 6.6), [(1.6, 22.5 * sg, 1.5), (1.8, 0, 1.2), (1.8, -22.5 * sg, 0.9), (1.2, -45 * sg, 0.5)],
               [cr], plane='xy')
    cx, cy, cz, r = 8, 14.0, 15.0, 4.8
    for i in range(12):
        a = i / 12 * 2 * math.pi
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        x.b((px - 0.55, py - 0.55, cz - 0.25), (px + 0.55, py + 0.55, cz + 0.25), gl if i % 3 == 0 else gd,
            R('z', 45 if i % 2 else 22.5, (px, py, cz)))
    x.b((7.2, 13.2, cz - 0.2), (8.8, 14.8, cz + 0.2), cr, R('z', 45, (8, 14.0, cz)))
    return x.it


PROTOS = [('guerrier', guerrier), ('paladin', paladin), ('mage', mage), ('rodeur', rodeur), ('druide', druide),
          ('lamerunique', lamerunique), ('gardeserment', gardeserment), ('sentinelle', sentinelle),
          ('arcaniste', arcaniste)]
NOMS = {'guerrier': 'Guerrier', 'paladin': 'Paladin', 'mage': 'Mage', 'rodeur': 'Rôdeur', 'druide': 'Druide',
        'lamerunique': 'Lame runique', 'gardeserment': 'Garde-serment', 'sentinelle': 'Sentinelle',
        'arcaniste': 'Arcaniste'}


def check(it):
    """Vérifie les contraintes du format (bornes, angles) et la règle anti-scintillement."""
    bad = []
    for e in it.els:
        for v in e['from'] + e['to']:
            if v < -16 or v > 32:
                bad.append(('borne', e['from'], e['to']))
        r = e.get('rot')
        if r and r['angle'] not in (-45, -22.5, 0, 22.5, 45):
            bad.append(('angle', r))
    return bad


MATS['he_skin'] = Mat((196, 148, 118), 4, 0.95)
MATS['he_hair'] = Mat((70, 46, 30), 6, 0.9)
MATS['he_eyes'] = Mat((40, 30, 60), 2, 1)


def preview(it, views=((18, 200), (18, 140), (10, 90), (18, 20))):
    it.box((4, 4, 4), (12, 12, 12), 'he_skin')
    it.box((5, 7, 3.98), (6.6, 8, 4), 'he_eyes')
    it.box((9.4, 7, 3.98), (11, 8, 4), 'he_eyes')
    img, els = it.build()
    tiles = []
    for rx, ry in views:
        d = {'gui': {'rotation': [rx, ry, 0], 'translation': [0, -3.5, 0], 'scale': [0.42] * 3}}
        tiles.append(render(img, els, d, 230))
    return tiles


if __name__ == '__main__':
    out = os.path.join(HERE, 'apercus')
    which = sys.argv[1:] or [k for k, _ in PROTOS]
    rows = []
    for key, fn in PROTOS:
        if key not in which:
            continue
        it = fn()
        bad = check(it)
        if bad:
            print(key, 'PROBLÈMES', bad[:5])
        rows.append((key, preview(it)))
    W, Hh = 230, 230
    sheet = Image.new('RGBA', (150 + 4 * W, len(rows) * Hh), (40, 42, 48, 255))
    d = ImageDraw.Draw(sheet)
    for r, (key, tiles) in enumerate(rows):
        d.text((10, r * Hh + Hh // 2), NOMS[key], fill=(235, 225, 200, 255))
        for c, t in enumerate(tiles):
            sheet.alpha_composite(t, (150 + c * W, r * Hh))
    name = 'heaumes_proto.png' if len(rows) > 1 else f'heaume_{rows[0][0]}.png'
    sheet.save(os.path.join(out, name))
    print('ok', name)
