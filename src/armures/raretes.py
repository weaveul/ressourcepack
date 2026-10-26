"""Variantes de rareté des armures : commune, rare (le look de base), épique, légendaire.

Chaque palier repeint les mêmes formes avec des matériaux transformés (usure, saturation, reflets dorés) et ajoute
ses ornements : liseré violet et gemme pour l'épique, liseré d'or, gemme ardente et runes pour la légendaire.
EvoPerso choisit le palier : oraxen:<set> pour rare, oraxen:<set>_<palier> pour les autres.
"""
import colorsys
from contextlib import contextmanager

from kit import Mat, MATS, h, clamp

TIERS = ['commun', 'rare', 'epique', 'legendaire']
SUFFIX = {'commun': '_commun', 'rare': '', 'epique': '_epique', 'legendaire': '_legendaire'}

# Ornements, ajoutés à MATS une fois pour toutes (non transformés).
MATS.update({
    'ep_trim': Mat((150, 110, 220), 5, 0.8, hi=(220, 190, 255)),
    'ep_gem': Mat((180, 90, 255), 6, 0.9, light=11, hi=(240, 210, 255)),
    'lg_trim': Mat((236, 186, 72), 6, 0.76, hi=(255, 240, 170)),
    'lg_gem': Mat((255, 120, 40), 8, 0.9, light=15, hi=(255, 220, 150)),
    'lg_rune': Mat((255, 210, 110), 4, 0.95, light=13),
})
ORNAMENTS = {'ep_trim', 'ep_gem', 'lg_trim', 'lg_gem', 'lg_rune', 'skin', 'slit'}


def _sat(c, k, v=1.0):
    r, g, b = (x / 255 for x in c[:3])
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, min(1, l * v), min(1, s * k))
    return (r * 255, g * 255, b * 255)


def shade(c, tier, p):
    """Couleur d'un texel une fois passée au palier."""
    if tier == 'commun':
        c = _sat(c, 0.5, 0.86)
        if h(int(p[0] * 3) + 17, int(p[1] * 3), int(p[2] * 3)) > 0.9:      # éraflures et taches d'usure
            c = tuple(v * 0.62 for v in c)
    elif tier == 'epique':
        c = _sat(c, 1.18, 1.03)
    elif tier == 'legendaire':
        c = _sat(c, 1.22, 1.04)
        lum = sum(c) / 3
        if lum > 150:                                                       # reflets dorés
            k = min(0.4, (lum - 150) / 160)
            c = (c[0] + (255 - c[0]) * k * 0.5, c[1] + (220 - c[1]) * k * 0.3, c[2] * (1 - k * 0.5))
    return c


class TierMat:
    def __init__(self, base, tier):
        self.base, self.tier = base, tier
        self.light = 0 if tier == 'commun' else (min(15, base.light + 2) if base.light else 0)

    def color(self, p, face, px, py, w, hgt):
        c = self.base.color(p, face, px, py, w, hgt)
        return tuple(clamp(v) for v in shade(c, self.tier, p)) + (c[3],)


@contextmanager
def palier(tier):
    """Le temps du bloc, MATS rend les matériaux du palier (les ornements restent tels quels)."""
    if tier == 'rare':
        yield
        return
    saved = dict(MATS)
    for k, m in saved.items():
        if k not in ORNAMENTS:
            MATS[k] = TierMat(m, tier)
    try:
        yield
    finally:
        MATS.clear()
        MATS.update(saved)


def trim_face(F, tier):
    """Ornements peints sur une face de calque (peinture_hd.Face), après le peintre de la classe."""
    if tier not in ('epique', 'legendaire') or F.cap:
        return
    trim = 'ep_trim' if tier == 'epique' else 'lg_trim'
    a = F.img.split()[3].load()
    m = MATS[trim]
    # liseré le long des arêtes verticales, là où la face est peinte
    for y in range(F.h):
        for x in (0, F.w - 1):
            if a[x, y]:
                F.img.putpixel((x, y), m.color((x * 0.25, y * 0.25, 1), F.face, 1, y, 3, F.h))
    if F.part == 'body' and F.front:
        g = 'ep_gem' if tier == 'epique' else 'lg_gem'
        cx = F.w // 2
        F.rect(cx - 2, 5, cx + 2, 9, trim)
        F.rect(cx - 1, 6, cx + 1, 8, g, bevel=False)
    if tier == 'legendaire':
        if F.part in ('arm', 'boot', 'leg') and (F.front or F.side):
            for y in range(3, F.h - 2, 6):                 # runes ardentes
                if a[F.w // 2, y]:
                    F.px(F.w // 2, y, (255, 214, 120))
                    F.px(F.w // 2 - 1, y + 1, (255, 170, 70))
                    F.px(F.w // 2, y + 2, (255, 214, 120))
        if F.part == 'body' and F.back:
            cx = F.w // 2
            for (dx, dy) in ((0, 4), (-1, 5), (1, 5), (0, 6), (0, 8), (-2, 7), (2, 7)):
                F.px(cx + dx, dy + 2, (255, 210, 110))


# Point d'accroche de la gemme de front sur chaque casque (x, y, z de la face avant), z bas = avant.
GEM = {
    'guerrier': (8.0, 10.6, 3.4), 'paladin': (8.0, 12.2, 3.4), 'mage': (8.0, 12.8, 3.2),
    'rodeur': (8.0, 11.1, 3.2), 'druide': (8.0, 11.1, 3.4), 'lamerunique': (8.0, 12.2, 3.4),
    'gardeserment': (8.0, 11.0, 3.4), 'sentinelle': (8.0, 11.0, 3.2), 'arcaniste': (8.0, 11.6, 3.2),
}


def adorn_helmet(it, key, tier):
    """Gemme (épique), gemme ardente sertie d'or et deux pointes dorées (légendaire)."""
    if tier not in ('epique', 'legendaire'):
        return
    x, y, z = GEM[key]
    if tier == 'epique':
        it.box((x - 0.7, y - 0.7, z - 0.7), (x + 0.7, y + 0.7, z - 0.1), 'ep_trim')
        it.box((x - 0.45, y - 0.45, z - 1.0), (x + 0.45, y + 0.45, z - 0.6), 'ep_gem')
    else:
        it.box((x - 1.1, y - 0.9, z - 0.7), (x + 1.1, y + 0.9, z - 0.1), 'lg_trim')
        it.box((x - 0.6, y - 0.6, z - 1.1), (x + 0.6, y + 0.6, z - 0.6), 'lg_gem')
        for side in (-1, 1):                               # rayons dorés de part et d'autre
            a, b = sorted((x + side * 1.1, x + side * 2.0))
            it.box((a, y - 0.25, z - 0.5), (b, y + 0.25, z - 0.1), 'lg_trim')
            it.box((x + side * 2.3 - 0.25, y - 0.25, z - 0.65), (x + side * 2.3 + 0.25, y + 0.25, z - 0.35), 'lg_rune')
