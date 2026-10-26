"""Kit d'armures : 16 panoplies par classe (4 raretés x 4 variantes), toutes différentes.

Chaque panoplie est une ligne de TABLE : coque du casque, visage, sommet, côtés, palette de couleurs, coupe de la
tenue, motif du torse et dos. Les pièces du kit sont posées sur la tête (repère casques3d : tête 4..12, avant côté
z bas), sans rien qui flotte. La palette porte la rareté : fer, cuir et toile pour le commun ; acier, drap et bronze
pour le rare ; métaux teintés et étoffes riches pour l'épique ; or, argent blanc, métaux sombres et lueurs pour le
légendaire.
"""
import math

from kit import Item, Mat, MATS, h, mix
from casques3d import (HELMET, S, E, hammered, brushed, filigree, cloth_folds, leather, fur, feathers, bark_grain,
                       leaves, horn_rings, starry)
from peinture_hd import chain, scales_hd, leather_soft
import casques_paliers  # noqa: F401  (matériaux cp_*)


def quilted(c, p, face, px, py, w, hgt):
    x, y = p[0] * 4, p[1] * 4
    return tuple(v * 0.8 for v in c) if int(x + y) % 4 == 0 or int(x - y) % 4 == 0 else c


def studded(c, p, face, px, py, w, hgt):
    if px % 3 == 1 and py % 3 == 1:
        return mix(c, (225, 220, 205), 0.7)
    return leather_soft(c, p, face, px, py, w, hgt)


KINDS = {
    # nature du matériau -> (bruit, liseré, motif, reflet clair ?)
    'metal': (6, 0.72, hammered, True), 'lisse': (5, 0.75, brushed, True), 'orne': (6, 0.74, filigree, True),
    'drap': (6, 0.85, cloth_folds, False), 'etoile': (6, 0.86, starry, False), 'cuir': (6, 0.78, leather_soft, False),
    'fourrure': (14, 0.9, fur, False), 'ecorce': (6, 0.78, bark_grain, False), 'feuille': (10, 0.84, leaves, False),
    'plume': (8, 0.86, feathers, False), 'os': (6, 0.8, horn_rings, False), 'maille': (6, 0.85, chain, False),
    'ecaille': (6, 0.8, scales_hd, False), 'matelasse': (6, 0.86, quilted, False), 'clous': (6, 0.78, studded, False),
    'lueur': (4, 0.95, None, True), 'uni': (4, 0.8, None, False),
}


def mat(name, rgb, kind):
    noise, edge, pattern, hi = KINDS[kind]
    MATS[name] = Mat(rgb, noise, edge, pattern=pattern, light=14 if kind == 'lueur' else 0,
                     hi=tuple(min(255, int(v * 1.35 + 30)) for v in rgb) if hi else None)
    return name


# rôles : m coque/torse, l pièce secondaire, t liseré et bandes, d sombre/doublure, a accent (plumet, étoffe), g lueur
P = {
    # --- commun : matériaux pauvres
    'fer': {'m': ((118, 120, 126), 'metal'), 'l': ((96, 98, 104), 'maille'), 't': ((86, 58, 36), 'cuir'),
            'd': ((70, 60, 52), 'drap'), 'a': ((150, 132, 104), 'drap')},
    'fer_rouille': {'m': ((122, 104, 90), 'metal'), 'l': ((100, 92, 86), 'maille'), 't': ((74, 50, 32), 'cuir'),
                    'd': ((62, 52, 44), 'drap'), 'a': ((120, 60, 44), 'drap')},
    'cuir': {'m': ((108, 74, 46), 'cuir'), 'l': ((84, 58, 36), 'cuir'), 't': ((60, 42, 28), 'cuir'),
             'd': ((150, 132, 104), 'drap'), 'a': ((140, 110, 80), 'drap')},
    'toile': {'m': ((164, 148, 116), 'drap'), 'l': ((132, 116, 90), 'matelasse'), 't': ((90, 62, 38), 'cuir'),
              'd': ((110, 96, 74), 'drap'), 'a': ((150, 120, 76), 'cuir')},
    'bure': {'m': ((104, 78, 56), 'drap'), 'l': ((84, 62, 44), 'drap'), 't': ((150, 120, 76), 'uni'),
             'd': ((70, 52, 38), 'drap'), 'a': ((130, 100, 66), 'drap')},
    'lin_vert': {'m': ((92, 110, 70), 'drap'), 'l': ((70, 88, 54), 'drap'), 't': ((120, 90, 56), 'cuir'),
                 'd': ((58, 72, 44), 'drap'), 'a': ((80, 140, 60), 'feuille')},
    'drap_gris': {'m': ((92, 84, 104), 'drap'), 'l': ((70, 64, 82), 'drap'), 't': ((110, 112, 120), 'metal'),
                  'd': ((54, 50, 64), 'drap'), 'a': ((120, 200, 230), 'uni')},
    'peau': {'m': ((128, 112, 92), 'fourrure'), 'l': ((96, 70, 44), 'cuir'), 't': ((70, 50, 32), 'cuir'),
             'd': ((86, 74, 62), 'fourrure'), 'a': ((180, 160, 130), 'os')},
    # --- rare : matériaux de soldat
    'acier': {'m': ((150, 156, 168), 'metal'), 'l': ((120, 124, 136), 'maille'), 't': ((196, 132, 70), 'orne'),
              'd': ((110, 116, 128), 'lisse'), 'a': ((150, 32, 30), 'drap')},
    'acier_bleu': {'m': ((150, 158, 172), 'lisse'), 'l': ((118, 122, 134), 'maille'), 't': ((214, 176, 80), 'orne'),
                   'd': ((40, 62, 140), 'drap'), 'a': ((40, 62, 140), 'drap')},
    'cuir_vert': {'m': ((112, 76, 46), 'cuir'), 'l': ((62, 92, 52), 'drap'), 't': ((70, 46, 28), 'cuir'),
                  'd': ((42, 62, 36), 'drap'), 'a': ((200, 70, 50), 'plume')},
    'drap_bleu': {'m': ((50, 52, 136), 'etoile'), 'l': ((34, 34, 96), 'drap'), 't': ((220, 178, 80), 'orne'),
                  'd': ((30, 30, 80), 'drap'), 'a': ((90, 190, 255), 'lueur')},
    'bois': {'m': ((110, 78, 48), 'ecorce'), 'l': ((80, 140, 60), 'feuille'), 't': ((140, 104, 66), 'ecorce'),
             'd': ((86, 70, 50), 'drap'), 'a': ((240, 150, 200), 'uni')},
    'runique': {'m': ((56, 54, 68), 'metal'), 'l': ((46, 44, 58), 'ecaille'), 't': ((170, 170, 186), 'lisse'),
                'd': ((36, 34, 46), 'lisse'), 'a': ((190, 100, 255), 'lueur')},
    'bronze': {'m': ((176, 120, 66), 'metal'), 'l': ((130, 96, 60), 'maille'), 't': ((226, 182, 90), 'orne'),
               'd': ((96, 64, 36), 'cuir'), 'a': ((36, 56, 124), 'drap')},
    'cuir_noir': {'m': ((60, 50, 44), 'clous'), 'l': ((44, 38, 36), 'cuir'), 't': ((150, 150, 158), 'lisse'),
                  'd': ((34, 30, 30), 'drap'), 'a': ((120, 30, 30), 'drap')},
    'violet': {'m': ((60, 42, 92), 'drap'), 'l': ((84, 82, 100), 'lisse'), 't': ((170, 170, 186), 'lisse'),
               'd': ((40, 28, 64), 'drap'), 'a': ((90, 220, 255), 'lueur')},
    # --- épique : teintes riches
    'acier_noirci': {'m': ((76, 80, 92), 'metal'), 'l': ((60, 62, 72), 'maille'), 't': ((200, 60, 50), 'orne'),
                     'd': ((44, 46, 54), 'lisse'), 'a': ((150, 24, 30), 'drap'), 'g': ((255, 90, 50), 'lueur')},
    'argent_azur': {'m': ((208, 214, 226), 'lisse'), 'l': ((170, 176, 190), 'maille'), 't': ((90, 150, 230), 'orne'),
                    'd': ((40, 70, 150), 'drap'), 'a': ((236, 234, 226), 'plume'), 'g': ((140, 200, 255), 'lueur')},
    'pourpre': {'m': ((128, 26, 40), 'drap'), 'l': ((84, 18, 28), 'drap'), 't': ((214, 170, 70), 'orne'),
                'd': ((70, 14, 24), 'drap'), 'a': ((236, 234, 226), 'plume'), 'g': ((255, 170, 60), 'lueur')},
    'ombre': {'m': ((40, 46, 40), 'cuir'), 'l': ((30, 36, 30), 'drap'), 't': ((150, 140, 120), 'lisse'),
              'd': ((22, 26, 22), 'drap'), 'a': ((120, 116, 110), 'fourrure'), 'g': ((150, 255, 140), 'lueur')},
    'chene': {'m': ((92, 66, 42), 'ecorce'), 'l': ((60, 120, 50), 'feuille'), 't': ((170, 140, 90), 'ecorce'),
              'd': ((86, 120, 60), 'fourrure'), 'a': ((250, 200, 90), 'uni'), 'g': ((255, 200, 80), 'lueur')},
    'emeraude': {'m': ((40, 110, 80), 'lisse'), 'l': ((30, 80, 60), 'ecaille'), 't': ((200, 210, 200), 'lisse'),
                 'd': ((24, 60, 44), 'drap'), 'a': ((60, 220, 140), 'lueur'), 'g': ((80, 255, 160), 'lueur')},
    'cuivre': {'m': ((190, 110, 70), 'metal'), 'l': ((140, 84, 56), 'ecaille'), 't': ((90, 190, 170), 'lisse'),
               'd': ((80, 50, 34), 'cuir'), 'a': ((60, 140, 130), 'drap'), 'g': ((120, 255, 220), 'lueur')},
    'nuit': {'m': ((32, 30, 70), 'etoile'), 'l': ((24, 22, 54), 'drap'), 't': ((180, 190, 230), 'lisse'),
             'd': ((18, 16, 40), 'drap'), 'a': ((150, 120, 255), 'lueur'), 'g': ((170, 140, 255), 'lueur')},
    # --- légendaire : métaux précieux, lueurs
    'or': {'m': ((232, 186, 70), 'orne'), 'l': ((200, 150, 56), 'ecaille'), 't': ((250, 236, 190), 'lisse'),
           'd': ((150, 30, 30), 'drap'), 'a': ((236, 234, 226), 'plume'), 'g': ((255, 240, 170), 'lueur')},
    'blanc_or': {'m': ((236, 232, 220), 'lisse'), 'l': ((210, 206, 196), 'maille'), 't': ((240, 192, 70), 'orne'),
                 'd': ((200, 190, 160), 'drap'), 'a': ((255, 255, 250), 'plume'), 'g': ((255, 236, 150), 'lueur')},
    'dragon': {'m': ((52, 40, 44), 'metal'), 'l': ((80, 26, 26), 'ecaille'), 't': ((230, 170, 60), 'orne'),
               'd': ((30, 22, 26), 'lisse'), 'a': ((160, 30, 30), 'fourrure'), 'g': ((255, 100, 40), 'lueur')},
    'neant': {'m': ((34, 28, 46), 'metal'), 'l': ((26, 22, 36), 'ecaille'), 't': ((190, 180, 210), 'lisse'),
              'd': ((18, 14, 26), 'lisse'), 'a': ((90, 50, 140), 'drap'), 'g': ((200, 110, 255), 'lueur')},
    'givre': {'m': ((200, 226, 240), 'lisse'), 'l': ((150, 190, 220), 'ecaille'), 't': ((240, 250, 255), 'orne'),
              'd': ((60, 100, 150), 'drap'), 'a': ((230, 240, 250), 'fourrure'), 'g': ((150, 230, 255), 'lueur')},
    'solaire': {'m': ((250, 210, 110), 'orne'), 'l': ((236, 120, 40), 'drap'), 't': ((255, 250, 220), 'lisse'),
                'd': ((170, 60, 30), 'drap'), 'a': ((255, 140, 40), 'plume'), 'g': ((255, 220, 120), 'lueur')},
    'sylve': {'m': ((236, 226, 196), 'os'), 'l': ((90, 150, 70), 'feuille'), 't': ((220, 180, 60), 'orne'),
              'd': ((70, 110, 50), 'fourrure'), 'a': ((220, 180, 60), 'feuille'), 'g': ((120, 255, 130), 'lueur')},
    'loup_blanc': {'m': ((200, 196, 186), 'fourrure'), 'l': ((60, 50, 44), 'clous'), 't': ((230, 200, 140), 'orne'),
                   'd': ((150, 144, 136), 'fourrure'), 'a': ((236, 234, 226), 'os'), 'g': ((255, 180, 40), 'lueur')},
    'azur': {'m': ((30, 28, 46), 'lisse'), 'l': ((60, 56, 80), 'metal'), 't': ((200, 210, 230), 'lisse'),
             'd': ((40, 30, 70), 'drap'), 'a': ((90, 220, 255), 'lueur'), 'g': ((90, 220, 255), 'lueur')},
    'crepuscule': {'m': ((90, 40, 110), 'drap'), 'l': ((60, 26, 80), 'etoile'), 't': ((236, 186, 72), 'orne'),
                   'd': ((40, 20, 56), 'drap'), 'a': ((255, 150, 220), 'lueur'), 'g': ((255, 170, 230), 'lueur')},
}


def palette(name):
    """Matériaux de la palette (créés une fois) : rôle -> nom dans MATS."""
    out = {}
    pal = P[name]
    for role in 'mltdag':
        spec = pal.get(role) or pal['t']
        out[role] = mat(f'k_{name}_{role}', spec[0], spec[1])
    out['slit'] = 'slit'
    return out


# ==================================================================================================================
#  Casques : coques
# ==================================================================================================================

def _shell(it, m, y0=3.6, y1=12.4, front=True):
    it.box((S, y0, S + (0 if front else 0.6)), (E, y1, E), m)
    if not front:
        it.box((S, y0, S), (S + 0.6, y1, S + 0.6), m)
    it.box((S + 0.6, y1, S + 0.6), (E - 0.6, y1 + 0.8, E - 0.6), m)


def _dome(it, m, y0, top=12.4, steps=3):
    it.box((S, y0, S), (E, top, E), m)
    for i in range(1, steps + 1):
        d = 0.7 * i
        it.box((S + d, top + (i - 1) * 0.5, S + d), (E - d, top + i * 0.5, E - d), m)


def _hood(it, m, d, top=12.6, rim=None):
    it.box((S, 3.6, E - 0.8), (E, top, E), m)
    it.box((S, 3.6, S), (S + 0.6, top, E - 0.8), m)
    it.box((E - 0.6, 3.6, S), (E, top, E - 0.8), m)
    it.box((S + 0.6, top - 0.6, S), (E - 0.6, top, E - 0.8), m)
    it.box((S + 0.6, 10.4, S), (E - 0.6, top - 0.6, S + 0.8), rim or m)
    it.box((S + 0.6, 3.6, S), (5.0, 10.4, S + 0.8), rim or m)
    it.box((11.0, 3.6, S), (E - 0.6, 10.4, S + 0.8), rim or m)
    it.box((S + 0.6, top, S + 0.6), (E - 0.6, top + 0.8, E - 0.2), m)
    it.box((5.0, 9.8, S + 0.8), (11.0, 10.4, S + 1.0), 'ro_shadow')


def base_calotte(it, c):
    _dome(it, c['m'], 8.0)
    it.box((S - 0.2, 7.6, S - 0.2), (E + 0.2, 8.4, E + 0.2), c['t'])
    it.box((S, 3.6, 10.8), (E, 8.0, E), c['l'])                                   # nuque


def base_heaume(it, c):
    _shell(it, c['m'])
    it.box((S - 0.3, 3.4, S - 0.3), (E + 0.3, 4.2, E + 0.3), c['t'])


def base_heaume_ouvert(it, c):
    _shell(it, c['m'], front=False)
    it.box((S + 0.6, 10.4, S), (E - 0.6, 12.4, S + 0.6), c['m'])                 # front
    it.box((S + 0.6, 3.6, S), (5.2, 10.4, S + 0.6), c['m'])                      # joues
    it.box((10.8, 3.6, S), (E - 0.6, 10.4, S + 0.6), c['m'])
    it.box((S - 0.3, 10.4, S - 0.3), (E + 0.3, 11.0, S + 0.3), c['t'])


def base_salade(it, c):
    _shell(it, c['m'], 6.4, 12.0)
    it.box((S - 0.2, 7.0, S - 0.8), (E + 0.2, 10.4, S), c['m'])                  # visière bombée
    it.box((S - 0.2, 10.4, S - 0.8), (E + 0.2, 11.0, S), c['t'])
    it.box((S + 0.4, 5.6, E), (E - 0.4, 11.4, E + 1.8), c['m'])                  # queue
    it.box((S, 3.6, S + 0.6), (E, 6.4, E), c['l'])                               # gorgerin


def base_barbute(it, c):
    _shell(it, c['m'])
    it.box((5.6, 7.4, S - 0.06), (10.4, 8.6, S), 'slit')
    it.box((7.2, 3.6, S - 0.06), (8.8, 7.4, S), 'slit')
    it.box((7.4, 8.6, S - 0.6), (8.6, 12.4, S), c['t'])                          # arête


def base_bassinet(it, c):
    _shell(it, c['m'])
    for i in range(4):                                                            # visière en museau de chien
        it.box((S + 0.6 + i * 0.7, 4.6 + i * 0.4, S - 0.6 - (3 - i) * 0.6), (E - 0.6 - i * 0.7, 9.6 - i * 0.3, S), c['d'])
    it.box((S - 0.3, 9.6, S - 0.3), (E + 0.3, 10.2, S + 0.3), c['t'])


def base_chapel(it, c):
    _dome(it, c['m'], 9.4, 12.4, 3)
    it.box((1.6, 9.4, 1.6), (14.4, 10.0, 14.4), c['m'])                          # bord
    it.box((1.4, 9.2, 1.4), (14.6, 9.4, 14.6), c['t'])
    it.box((S, 3.6, 10.8), (E, 9.4, E), c['l'])


def base_capuche(it, c):
    _hood(it, c['m'], c['d'], rim=c['l'])
    it.box((2.6, 2.8, 2.6), (13.4, 4.0, 13.4), c['d'])


def base_capuche_pointe(it, c):
    _hood(it, c['m'], c['d'])
    for i in range(5):
        it.box((6.6 + i * 0.3, 12.8 - i * 1.1, E - 0.2 + i * 0.5), (9.4 - i * 0.3, 13.6 - i * 1.0, E + 0.8 + i * 0.5), c['m'])
    it.box((2.4, 2.8, 2.4), (13.6, 4.2, 13.6), c['l'])                            # pèlerine


def base_masque(it, c):
    _shell(it, c['m'])
    it.box((S + 0.4, 3.6, S - 0.6), (E - 0.4, 11.0, S), c['l'])                  # masque plein
    for x0 in (5.0, 9.2):
        it.box((x0, 7.8, S - 0.66), (x0 + 1.8, 8.8, S - 0.6), c['g'] if 'g' in c else 'slit')
    it.box((7.6, 4.4, S - 0.66), (8.4, 7.0, S - 0.6), c['d'])


def base_cercle(it, c):
    it.box((S - 0.2, 10.4, S - 0.2), (E + 0.2, 11.6, E + 0.2), c['t'])
    it.box((S + 0.2, 11.6, S + 0.2), (E - 0.2, 12.2, E - 0.2), c['m'])


def base_chapeau(it, c):
    it.box((1.0, 11.2, 1.0), (15.0, 12.0, 15.0), c['d'])
    it.box((S, 11.0, S), (E, 12.6, E), c['m'])
    it.box((S - 0.2, 12.2, S - 0.2), (E + 0.2, 13.2, E + 0.2), c['t'])
    for i in range(10):
        t = i / 9
        w = 4.4 * (1 - t) ** 1.2 + 0.6
        cz = 8 + 3.6 * t * t
        it.box((8 - w, 13.2 + i * 0.95, cz - w), (8 + w, 14.25 + i * 0.95, cz + w), c['m'])


def base_coiffe(it, c):
    _dome(it, c['m'], 9.0, 12.4, 3)
    it.box((S, 5.4, 10.6), (E, 9.0, E), c['m'])                                  # rabat sur la nuque
    it.box((S, 6.8, S + 0.6), (S + 0.6, 9.0, 10.6), c['m'])
    it.box((E - 0.6, 6.8, S + 0.6), (E, 9.0, 10.6), c['m'])
    it.box((S - 0.2, 9.0, S - 0.2), (E + 0.2, 9.8, E + 0.2), c['t'])


def base_bete(it, c):
    it.box((S - 0.2, 9.8, S - 0.2), (E + 0.2, 13.6, E + 0.2), c['m'])            # crâne de la bête
    it.box((S - 0.2, 3.6, 10.0), (E + 0.2, 9.8, E + 0.2), c['m'])
    it.box((S - 0.2, 4.6, S + 0.6), (S + 0.6, 9.8, 10.0), c['d'])
    it.box((E - 0.6, 4.6, S + 0.6), (E + 0.2, 9.8, 10.0), c['d'])
    it.box((5.2, 10.4, S - 3.0), (10.8, 13.0, S), c['m'])                        # museau
    it.box((5.8, 10.0, S - 3.0), (10.2, 10.6, S - 0.4), c['a'])
    for x0 in (4.4, 10.0):
        it.box((x0, 12.0, S - 0.26), (x0 + 1.6, 12.8, S - 0.2), c['g'] if 'g' in c else 'slit')


def base_turban(it, c):
    for i in range(4):
        d = 0.35 * i
        it.box((S - 0.4 + d, 9.4 + i * 0.9, S - 0.4 + d), (E + 0.4 - d, 10.4 + i * 0.9, E + 0.4 - d),
               c['m'] if i % 2 == 0 else c['l'])
    it.box((7.2, 11.0, S - 0.8), (8.8, 12.6, S - 0.3), c['t'])
    it.box((S, 4.0, 10.6), (E, 9.4, E), c['l'])                                  # voile sur la nuque


BASES = {k[5:]: v for k, v in globals().items() if k.startswith('base_')}


# ==================================================================================================================
#  Casques : visages (sur les coques fermées)
# ==================================================================================================================

def face(it, kind, c):
    z = S - 0.06
    if kind == 'fente':
        for x0 in (4.6, 9.0):
            it.box((x0, 7.6, z), (x0 + 2.4, 8.4, S), 'slit')
    elif kind == 'croix':
        it.box((4.4, 7.8, z), (11.6, 8.6, S), 'slit')
        it.box((7.6, 4.6, z), (8.4, 7.8, S), 'slit')
    elif kind == 'grille':
        it.box((4.6, 7.6, z), (11.4, 8.4, S), 'slit')
        for x in (5.0, 6.4, 7.8, 9.2, 10.6):
            it.box((x, 4.4, z), (x + 0.5, 7.4, S), 'slit')
    elif kind == 'yeux':
        for x0 in (5.0, 9.4):
            it.box((x0, 7.4, z), (x0 + 1.6, 8.8, S), c['g'] if 'g' in c else 'slit')
    elif kind == 'nasal':
        it.box((7.4, 4.8, S - 0.5), (8.6, 8.6, S), c['t'])
    elif kind == 'mentonniere':
        it.box((S - 0.1, 3.6, S - 0.4), (E + 0.1, 7.0, S + 0.6), c['l'])
        it.box((S - 0.1, 6.8, S - 0.5), (E + 0.1, 7.4, S + 0.6), c['t'])
    elif kind == 'voile':
        it.box((S + 0.4, 3.6, S - 0.4), (E - 0.4, 7.6, S + 0.4), c['d'])
        it.box((S + 0.4, 7.4, S - 0.45), (E - 0.4, 7.7, S - 0.35), c['t'])
    elif kind == 'crocs':
        it.box((S - 0.2, 3.4, S - 1.0), (E + 0.2, 6.6, S), c['l'])
        for x in (4.4, 5.8, 9.6, 11.0):
            it.box((x, 6.6, S - 0.9), (x + 0.6, 7.4, S - 0.5), 'cp_teeth')
        for x0 in (4.8, 9.4):
            it.box((x0, 8.0, z), (x0 + 1.8, 8.8, S), c['g'] if 'g' in c else 'slit')


# ==================================================================================================================
#  Casques : sommets et côtés (tous attachés, épais d'au moins 0,8)
# ==================================================================================================================

def _curve(it, x0, side, n, f, mats):
    for i in range(n):
        t = i / (n - 1)
        dx, y, dz, w = f(t)
        cx = x0 + side * dx
        m = mats[0] if i == 0 else (mats[2] if i == n - 1 else mats[1])
        it.box((cx - w, y - w * 0.8, dz - w), (cx + w, y + w * 0.8, dz + w), m)


def top(it, kind, c, y=12.6):
    if kind == 'crete':
        it.box((7.3, y, S + 0.6), (8.7, y + 1.4, E - 0.4), c['t'])
    elif kind == 'cimier':
        for i in range(7):
            z = S + 0.4 + i * 1.2
            ht = 1.2 + 2.4 * math.sin((i + 0.5) / 7 * math.pi)
            it.box((7.4, y, z), (8.6, y + ht, z + 1.2), c['a'] if i % 2 == 0 else c['t'])
    elif kind == 'plumet':
        it.box((7.0, y, 7.4), (9.0, y + 0.8, 9.4), c['t'])
        for i in range(7):
            it.box((7.2, y + 0.6 + i * 0.7, 8.0 + i * 0.9), (8.8, y + 1.8 + i * 0.6, 9.6 + i * 0.9), c['a'])
    elif kind == 'crin':
        it.box((7.2, y, 6.0), (8.8, y + 1.2, E), c['t'])
        for i in range(6):
            it.box((7.0, y + 0.6 - i * 1.3, E - 0.2 + i * 0.25), (9.0, y + 1.8 - i * 1.2, E + 1.0 + i * 0.25), c['a'])
    elif kind == 'cornes':
        for side in (-1, 1):
            _curve(it, S if side < 0 else E, side, 10,
                   lambda t: (0.8 + 3.0 * math.sin(t * math.pi * 0.7), 9.6 + 5.6 * (1 - math.cos(t * math.pi * 0.7)),
                              8.4 - 2.4 * t ** 1.5, 1.4 - 0.8 * t), (c['t'], 'cp_bone', 'cp_bone_d'))
    elif kind == 'belier':
        for side in (-1, 1):
            x0 = S if side < 0 else E
            for i in range(13):
                t = i / 12
                a = t * math.pi * 1.6
                cx = x0 + side * (1.2 + 2.2 * math.sin(a) + t * 0.6)
                yy = 10.0 + 2.4 * (1 - math.cos(a)) - t * 3.0
                zz = 9.0 - 2.4 * math.sin(a * 0.9)
                w = 1.25 - t * 0.55
                it.box((cx - w, yy - w, zz - w), (cx + w, yy + w, zz + w), 'cp_bone' if i < 11 else 'cp_bone_d')
    elif kind == 'cornes_av':
        for side in (-1, 1):
            _curve(it, S if side < 0 else E, side, 9,
                   lambda t: (0.4 + 1.8 * t, 10.6 + 3.0 * t, 8.0 - 4.6 * t, 1.2 - 0.5 * t), (c['t'], c['l'], c['g'] if 'g' in c else c['t']))
    elif kind == 'ailes':
        for side in (-1, 1):
            x0 = S if side < 0 else E
            it.box((x0 + side * 0.1 - 0.5, 8.4, 6.6), (x0 + side * 0.1 + 0.5, 11.4, 9.6), c['t'])
            for j in range(6):
                yy = 9.2 + j * 1.25
                ln = 6.0 - j * 0.6
                x1 = x0 + side * (0.5 + j * 0.3)
                a, b = sorted((x1, x1 + side * 0.9))
                it.box((a, yy, 7.0 + j * 0.4), (b, yy + 1.2, 7.0 + j * 0.4 + ln), c['a'] if j < 5 else c['t'])
    elif kind == 'couronne':
        it.box((S - 0.3, y - 0.6, S - 0.3), (E + 0.3, y + 0.4, E + 0.3), c['t'])
        for i, x in enumerate((S, 6.2, 8.8, E - 1.4)):
            it.box((x, y + 0.4, S - 0.3), (x + 1.4, y + 1.6 + (0.6 if i in (1, 2) else 0), S + 0.5), c['t'])
        it.box((7.3, y - 0.4, S - 0.5), (8.7, y + 0.6, S - 0.2), c['g'] if 'g' in c else c['a'])
    elif kind == 'aileron':
        for i in range(8):
            z = 7.0 + i * 0.8
            it.box((7.5, y, z), (8.5, y + 3.2 - abs(i - 2.5) * 0.45, z + 0.9), c['t'])
    elif kind == 'bois':
        for side in (-1, 1):
            x0 = 5.0 if side < 0 else 11.0
            _curve(it, x0, side, 9, lambda t: (2.4 * t, y + 6.0 * t, 8.6 - 1.6 * t, 0.9 - 0.35 * t),
                   (c['t'], 'dr_antler', 'dr_antler'))
            for (t0, ln, up) in ((0.4, 2.2, 1.2), (0.7, 1.8, 1.4)):
                bx, by = x0 + side * 2.4 * t0, y + 6.0 * t0
                for j in range(3):
                    u = j / 2
                    cx = bx + side * (0.4 + u * ln * 0.3)
                    it.box((cx - 0.45, by + u * up * 2, 8.4 - 1.6 * t0 - u * ln - 0.45),
                           (cx + 0.45, by + u * up * 2 + 0.8, 8.4 - 1.6 * t0 - u * ln + 0.45), 'dr_antler')
    elif kind == 'feuilles':
        for (x, z) in ((S - 0.6, 6.0), (4.6, S - 0.6), (7.2, S - 0.8), (9.8, S - 0.6), (E, 9.0), (S - 0.6, 10.4)):
            it.box((x, y - 1.6, z), (x + 1.6, y + 0.4, z + 1.2), c['l'])
        it.box((S + 0.4, y - 0.6, S + 0.4), (E - 0.4, y, E - 0.4), c['d'])
    elif kind == 'oreilles':
        for side in (-1, 1):
            x0 = 4.2 if side < 0 else 10.4
            it.box((x0, y + 0.8, 6.6), (x0 + 1.4, y + 3.0, 8.0), c['m'])
            it.box((x0 + 0.3, y + 3.0, 6.9), (x0 + 1.1, y + 3.8, 7.7), c['d'])
    elif kind == 'gemme':
        it.box((6.9, 10.2, S - 0.7), (9.1, 12.0, S - 0.1), c['t'])
        it.box((7.3, 10.6, S - 1.0), (8.7, 11.6, S - 0.6), c['g'] if 'g' in c else c['a'])
    elif kind == 'rameaux':
        for side in (-1, 1):
            x0 = 5.6 if side < 0 else 10.4
            _curve(it, x0, side, 6, lambda t: (1.6 * t, y + 0.6 + 3.0 * t, 9.0 + 1.2 * t, 0.5 - 0.1 * t), (c['t'], c['t'], c['l']))
    elif kind == 'pointes':                                                       # pointes larges et basses
        for i, x in enumerate((S + 0.2, 6.0, 8.8, E - 1.6)):
            it.box((x, y, S + 0.2), (x + 1.4, y + (1.8 if i in (1, 2) else 1.2), S + 1.6), c['t'])
    elif kind == 'plumes':
        for side in (-1, 1):
            x0 = S - 0.6 if side < 0 else E
            for i in range(5):
                it.box((x0, y - 1.6 + i * 0.9, 7.6 + i * 0.6), (x0 + 0.6, y - 0.6 + i * 0.9, 9.2 + i * 0.5), c['a'])


def side(it, kind, c):
    if kind == 'joues':
        for s in (-1, 1):
            x0 = S - 0.5 if s < 0 else E
            it.box((x0, 3.4, 4.6), (x0 + 0.5, 8.6, 9.0), c['l'] if c['l'] != c['m'] else c['t'])
    elif kind == 'rosaces':
        for s in (-1, 1):
            x0 = S - 0.5 if s < 0 else E
            it.box((x0, 7.0, 7.0), (x0 + 0.5, 9.0, 9.0), c['t'])
    elif kind == 'ailettes':
        for s in (-1, 1):
            x0 = S if s < 0 else E
            for j in range(3):
                a, b = sorted((x0, x0 + s * (0.8 + j * 0.3)))
                it.box((a, 9.0 + j * 1.0, 7.4 + j * 0.3), (b, 10.0 + j * 1.0, 10.6 + j * 0.4), c['t'] if j == 2 else c['a'])
    elif kind == 'plume':
        for i in range(6):
            it.box((E + 0.2, 11.4 + i * 0.9, 7.6 + i * 0.6), (E + 0.8, 12.4 + i * 0.9, 9.4 + i * 0.5), c['a'])
    elif kind == 'fourrure':
        it.box((1.8, 2.6, 2.0), (14.2, 4.4, 14.0), c['a'] if P_KIND(c, 'a') == 'fourrure' else 'ro_fur')
    elif kind == 'camail':
        it.box((S - 0.1, 3.0, 9.6), (E + 0.1, 8.0, E + 0.1), 'cp_chain')
        it.box((S - 0.1, 3.0, S + 0.6), (S + 0.5, 8.0, 9.6), 'cp_chain')
        it.box((E - 0.5, 3.0, S + 0.6), (E + 0.1, 8.0, 9.6), 'cp_chain')
    elif kind == 'cape':
        it.box((2.4, 2.8, 2.4), (13.6, 4.2, 13.6), c['a'] if P_KIND(c, 'a') in ('drap', 'fourrure') else c['d'])
    elif kind == 'bandeau':
        it.box((S - 0.2, 10.6, S - 0.2), (E + 0.2, 11.4, E + 0.2), c['t'])
        it.box((E, 10.4, 6.0), (E + 0.4, 11.6, 7.4), c['g'] if 'g' in c else c['t'])


def P_KIND(c, role):
    name = c[role].split('_')[1:-1]
    pal = P['_'.join(name)]
    return (pal.get(role) or pal['t'])[1]


# ==================================================================================================================
#  Tenues (calques HD)
# ==================================================================================================================

def body_painter(spec, c, tier):
    """Peintre d'un calque HD pour la tenue : coupe, motif du torse, dos, plus les ornements du palier."""
    cut, chest, back = spec
    rich = {'commun': 0, 'rare': 1, 'epique': 2, 'legendaire': 3}[tier]
    m, l, t, d, a = c['m'], c['l'], c['t'], c['d'], c['a']
    g = c.get('g', a)
    robe = cut in ('robe', 'robe_longue')
    sleeveless = cut in ('cuir_nu', 'ecorce')

    def paint(F):
        p, W, H = F.part, F.w, F.h
        if p == 'body':
            if F.cap:
                F.rows(0, H, m); return
            if cut in ('plaque', 'ecailles'):
                F.rows(0, 15, m if cut == 'plaque' else l)
                F.rows(15, 17, t)
                F.rows(17, 24, l if cut == 'plaque' else m)
                if F.front or F.back:
                    for y in (5, 9, 13):
                        F.rect(1, y, W - 1, y + 1, d, bevel=False) if cut == 'plaque' else None
            elif cut == 'mailles':
                F.rows(0, 24, l)
                F.rows(15, 17, t)
            elif cut in ('brigandine', 'gambison', 'cuir', 'cuir_nu', 'fourrure'):
                F.rows(0, 24, m if cut != 'fourrure' else l)
                F.rows(15, 17, t)
                if cut == 'fourrure':
                    F.rows(0, 5, m)
            elif robe:
                F.rows(0, 24, m, bevel=False)
                F.rows(14, 16, t)
            elif cut == 'ecorce':
                F.rows(0, 24, d, bevel=False)
                if F.front or F.back:
                    for (x0, y0, x1, y1) in ((2, 3, 7, 9), (W - 7, 3, W - 2, 9), (3, 9, W - 3, 15)):
                        F.rect(x0, y0, x1, y1, m)
                F.rows(15, 17, t)
            if rich >= 1 and not robe:
                F.rows(0, 2, t)                                                   # col
            if F.front:
                chest_motif(F, chest, c, rich)
            if F.back:
                back_motif(F, back, c, rich)
        elif p == 'arm':
            if sleeveless:
                from PIL import Image
                F.img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                if F.cap:
                    return
                F.rows(14, 23, m if cut == 'ecorce' else l)
                F.rows(14, 15, t, bevel=False)
                if rich >= 2:
                    F.rows(0, 3, a if cut == 'fourrure' else t)
                return
            if F.face == 'bottom':
                F.rows(0, H, m); return
            base = l if cut in ('mailles', 'plaque', 'ecailles') else m
            F.rows(0, 24, base, bevel=not robe)
            if cut in ('plaque', 'ecailles', 'brigandine'):
                F.rows(0, 6 + 2 * rich, m)                                       # épaulière, plus grande si rare
                F.rows(15, 24, m)
                F.rows(15, 16, t, bevel=False)
            elif cut == 'fourrure':
                F.rows(0, 6, m)
            elif robe:
                F.rows(18, 22, d)
                F.rows(22, 24, t)
            else:
                F.rows(18, 24, l)
            if rich >= 2 and not F.cap:
                F.rows(0, 1, t, bevel=False)
            if rich >= 3 and not F.cap:
                F.rect(W // 2 - 1, 3, W // 2 + 1, 5, g)
        elif p == 'boot':
            if F.cap:
                F.rows(0, H, m if not robe else d); return
            top_y = 16 if robe else 14
            F.rows(top_y, 24, m if cut in ('plaque', 'ecailles') else (d if robe else l))
            F.rows(top_y, top_y + 2, t)
            if F.front and rich >= 1:
                F.rect(1, 21, W - 1, 24, t)
            if rich >= 3 and F.front:
                F.rect(W // 2 - 1, 17, W // 2 + 1, 19, g)
            F.clear(0, 0, W, top_y)
        elif p == 'leg':
            if robe:
                F.rows(0, 18, m, bevel=False)
                F.rows(15, 18, t)
            else:
                F.rows(0, 18, l if cut in ('mailles', 'plaque') else (d if cut != 'ecailles' else l))
                if F.front or F.side:
                    F.rect(0, 9, W, 14, m)                                        # genouillère
                    if rich >= 2:
                        F.rect(W // 2 - 1, 10, W // 2 + 1, 13, t)
                if F.front and chest == 'tabard':
                    F.rect(1, 0, W - 1, 8, a)
            F.clear(0, 18, W, H)
        elif p == 'waist':
            F.rows(18, 24, m if robe else l)
            F.rows(18, 20, t)
            F.clear(0, 0, W, 18)
    return paint


def chest_motif(F, kind, c, rich):
    W = F.w
    cx = W // 2
    t, a, d, m = c['t'], c['a'], c['d'], c['m']
    g = c.get('g', a)
    if kind == 'embleme':
        for dy in range(-3, 4):
            k = 3 - abs(dy)
            F.rect(cx - k - 1, 8 + dy, cx + k + 1, 9 + dy, t, bevel=False)
        F.rect(cx - 1, 7, cx + 1, 9, g if rich >= 2 else d, bevel=False)
    elif kind == 'croix':
        F.rect(3, 3, W - 3, 15, a)
        F.rect(cx - 1, 4, cx + 1, 14, t)
        F.rect(cx - 3, 6, cx + 3, 8, t)
    elif kind == 'soleil':
        for i in range(8):
            ang = 2 * math.pi * i / 8
            for r in range(2, 5):
                F.px(cx + round(r * math.cos(ang)) - 1, 8 + round(r * math.sin(ang)), (240, 200, 90))
        F.rect(cx - 2, 7, cx + 1, 10, g if rich >= 2 else t, bevel=False)
    elif kind == 'baudrier':
        for i in range(14):
            F.rect(2 + i, 1 + i, 4 + i, 3 + i, t, bevel=False)
    elif kind == 'croises':
        for i in range(14):
            F.rect(2 + i, 1 + i, 4 + i, 3 + i, t, bevel=False)
            F.rect(W - 4 - i, 1 + i, W - 2 - i, 3 + i, t, bevel=False)
    elif kind == 'tabard':
        F.rect(3, 2, W - 3, 24, a)
        F.rect(3, 2, 4, 24, t, bevel=False)
        F.rect(W - 4, 2, W - 3, 24, t, bevel=False)
    elif kind == 'ecartele':
        F.rect(2, 3, cx, 9, a); F.rect(cx, 3, W - 2, 9, d)
        F.rect(2, 9, cx, 15, d); F.rect(cx, 9, W - 2, 15, a)
        F.rect(cx - 1, 3, cx + 1, 15, t, bevel=False)
    elif kind == 'cotes':
        for y in (4, 7, 10, 13):
            for i in range(cx - 1):
                F.rect(cx - 1 - i, y + i // 3, cx - i, y + 1 + i // 3, t, bevel=False)
                F.rect(cx + i, y + i // 3, cx + i + 1, y + 1 + i // 3, t, bevel=False)
    elif kind == 'lacet':
        F.rect(cx - 1, 2, cx + 1, 15, d, bevel=False)
        for y in range(4, 15, 3):
            F.px(cx - 2, y, (220, 200, 150)); F.px(cx + 1, y, (220, 200, 150))
    elif kind == 'rune':
        F.rect(cx - 1, 3, cx + 1, 14, g, bevel=False)
        for y in (5, 9, 12):
            F.rect(cx - 3, y, cx + 3, y + 1, g, bevel=False)
    elif kind == 'plastron':
        F.rect(2, 2, W - 2, 12, m)
        F.rect(2, 12, W - 2, 13, t, bevel=False)
    elif kind == 'col':
        F.rect(0, 0, W, 5, c['a'])
        F.rect(cx - 1, 5, cx + 1, 7, g if rich >= 2 else t)
    elif kind == 'bourses':
        F.rect(1, 17, 5, 21, d)
        F.rect(W - 5, 17, W - 1, 21, d)
        F.rect(cx - 1, 15, cx + 1, 17, t)
    if rich >= 3 and kind not in ('rune', 'embleme', 'soleil'):
        F.rect(cx - 1, 8, cx + 1, 10, g)                                          # joyau central au légendaire


def back_motif(F, kind, c, rich):
    W = F.w
    t, a, d = c['t'], c['a'], c['d']
    if kind == 'cape':
        F.rect(1, 2, W - 1, 24, a if P_KIND(c, 'a') in ('drap', 'fourrure', 'etoile') else d)
        if rich >= 1:
            F.rect(1, 22, W - 1, 24, t, bevel=False)
    elif kind == 'embleme':
        cx = W // 2
        F.rect(cx - 3, 5, cx + 3, 11, t)
        F.rect(cx - 2, 6, cx + 2, 10, d)
        F.rect(cx - 1, 7, cx + 1, 9, c.get('g', a))
    elif kind == 'carquois':
        for i in range(14):
            F.rect(W - 3 - i, 1 + i, W - 1 - i, 3 + i, t, bevel=False)
        F.rect(W - 6, 1, W - 3, 3, a)
    elif kind == 'lames':
        F.rect(W // 2 - 1, 1, W // 2 + 1, 22, t)


# ==================================================================================================================
#  Les 144 panoplies : (coque, visage, sommet, côté, palette, coupe, torse, dos)
#  par classe : commun x4, rare x4, épique x4, légendaire x4
# ==================================================================================================================

TABLE = {
    'guerrier': [
        ('calotte', 'nasal', '-', 'camail', 'fer', 'gambison', 'lacet', '-'),
        ('chapel', '-', '-', '-', 'fer_rouille', 'mailles', 'baudrier', '-'),
        ('coiffe', '-', '-', 'fourrure', 'peau', 'cuir', 'col', '-'),
        ('heaume_ouvert', '-', 'crete', '-', 'cuir', 'brigandine', 'bourses', '-'),
        ('heaume', 'fente', 'cornes', '-', 'acier', 'plaque', 'embleme', '-'),
        ('salade', 'fente', 'plumet', '-', 'bronze', 'ecailles', 'tabard', 'cape'),
        ('barbute', '-', 'crin', 'rosaces', 'acier', 'mailles', 'ecartele', '-'),
        ('bassinet', '-', 'crete', 'camail', 'cuir_noir', 'brigandine', 'croises', 'lames'),
        ('heaume', 'grille', 'belier', '-', 'acier_noirci', 'plaque', 'cotes', 'cape'),
        ('masque', '-', 'aileron', 'joues', 'cuivre', 'ecailles', 'plastron', '-'),
        ('heaume_ouvert', 'mentonniere', 'cimier', 'fourrure', 'pourpre', 'fourrure', 'col', 'cape'),
        ('bete', '-', 'oreilles', 'fourrure', 'ombre', 'cuir', 'croises', '-'),
        ('heaume', 'crocs', 'cornes_av', '-', 'dragon', 'ecailles', 'cotes', 'cape'),
        ('salade', 'fente', 'couronne', '-', 'or', 'plaque', 'embleme', 'cape'),
        ('barbute', '-', 'ailes', 'rosaces', 'givre', 'plaque', 'soleil', '-'),
        ('masque', '-', 'belier', 'fourrure', 'neant', 'plaque', 'rune', 'lames'),
    ],
    'paladin': [
        ('calotte', '-', '-', 'camail', 'fer', 'mailles', 'croix', '-'),
        ('heaume_ouvert', '-', '-', '-', 'toile', 'gambison', 'tabard', '-'),
        ('chapel', '-', '-', 'camail', 'fer', 'brigandine', 'embleme', '-'),
        ('coiffe', '-', '-', '-', 'bure', 'robe', 'croix', '-'),
        ('heaume', 'croix', 'ailes', '-', 'acier_bleu', 'plaque', 'croix', '-'),
        ('salade', 'fente', 'plumet', '-', 'acier', 'plaque', 'tabard', 'cape'),
        ('bassinet', '-', 'crete', 'rosaces', 'bronze', 'mailles', 'soleil', 'embleme'),
        ('heaume_ouvert', 'mentonniere', 'gemme', 'camail', 'acier_bleu', 'brigandine', 'ecartele', 'cape'),
        ('heaume', 'croix', 'cimier', 'ailettes', 'argent_azur', 'plaque', 'embleme', 'cape'),
        ('barbute', '-', 'plumet', 'joues', 'pourpre', 'ecailles', 'croix', 'embleme'),
        ('salade', 'fente', 'couronne', '-', 'emeraude', 'plaque', 'soleil', '-'),
        ('masque', '-', 'crete', 'rosaces', 'cuivre', 'plaque', 'tabard', 'cape'),
        ('bassinet', '-', 'ailes', '-', 'blanc_or', 'plaque', 'soleil', 'cape'),
        ('heaume_ouvert', '-', 'couronne', 'ailettes', 'or', 'plaque', 'croix', 'embleme'),
        ('masque', '-', 'aileron', 'joues', 'solaire', 'ecailles', 'soleil', 'cape'),
        ('salade', 'fente', 'plumes', '-', 'givre', 'plaque', 'embleme', 'cape'),
    ],
    'mage': [
        ('capuche', '-', '-', '-', 'bure', 'robe', 'lacet', '-'),
        ('capuche_pointe', '-', '-', '-', 'drap_gris', 'robe', '-', '-'),
        ('coiffe', '-', '-', '-', 'toile', 'robe_longue', 'bourses', '-'),
        ('turban', '-', '-', '-', 'bure', 'robe', 'baudrier', '-'),
        ('chapeau', '-', '-', '-', 'drap_bleu', 'robe', 'embleme', 'embleme'),
        ('capuche', 'voile', 'gemme', '-', 'violet', 'robe_longue', 'rune', '-'),
        ('turban', '-', 'gemme', 'cape', 'pourpre', 'robe', 'lacet', 'cape'),
        ('cercle', '-', 'gemme', '-', 'drap_bleu', 'robe_longue', 'soleil', 'cape'),
        ('chapeau', '-', '-', 'plume', 'pourpre', 'robe', 'embleme', 'cape'),
        ('capuche_pointe', '-', 'couronne', '-', 'nuit', 'robe_longue', 'rune', 'embleme'),
        ('masque', '-', 'crete', 'cape', 'emeraude', 'robe', 'plastron', 'cape'),
        ('turban', '-', 'plumes', '-', 'cuivre', 'robe_longue', 'soleil', '-'),
        ('chapeau', '-', '-', 'bandeau', 'crepuscule', 'robe_longue', 'embleme', 'cape'),
        ('cercle', '-', 'couronne', 'cape', 'or', 'robe', 'soleil', 'cape'),
        ('capuche', 'voile', 'cornes_av', '-', 'neant', 'robe_longue', 'rune', 'embleme'),
        ('masque', '-', 'aileron', 'cape', 'givre', 'robe', 'embleme', 'cape'),
    ],
    'rodeur': [
        ('coiffe', '-', '-', '-', 'cuir', 'cuir', 'lacet', '-'),
        ('capuche', '-', '-', '-', 'lin_vert', 'cuir_nu', 'baudrier', 'carquois'),
        ('calotte', '-', '-', 'fourrure', 'peau', 'fourrure', 'col', '-'),
        ('turban', '-', '-', '-', 'toile', 'gambison', 'bourses', 'carquois'),
        ('capuche', '-', '-', 'plume', 'cuir_vert', 'cuir', 'croises', 'carquois'),
        ('capuche_pointe', 'voile', '-', '-', 'ombre', 'cuir', 'baudrier', '-'),
        ('coiffe', '-', 'plumes', 'bandeau', 'cuir_noir', 'brigandine', 'lacet', 'carquois'),
        ('bete', '-', 'oreilles', 'fourrure', 'peau', 'fourrure', 'col', 'cape'),
        ('capuche', 'voile', 'oreilles', 'fourrure', 'ombre', 'cuir', 'croises', 'cape'),
        ('heaume_ouvert', '-', 'plumes', 'bandeau', 'emeraude', 'ecailles', 'baudrier', 'carquois'),
        ('turban', 'voile', 'gemme', 'cape', 'cuivre', 'cuir_nu', 'bourses', 'carquois'),
        ('capuche_pointe', '-', 'rameaux', 'plume', 'chene', 'cuir', 'lacet', 'cape'),
        ('bete', '-', 'crin', 'fourrure', 'loup_blanc', 'fourrure', 'col', 'cape'),
        ('capuche', 'voile', 'couronne', 'cape', 'nuit', 'cuir', 'croises', 'carquois'),
        ('masque', '-', 'plumes', 'fourrure', 'or', 'ecailles', 'baudrier', 'cape'),
        ('capuche_pointe', 'voile', 'cornes_av', 'fourrure', 'dragon', 'cuir_nu', 'croises', 'carquois'),
    ],
    'druide': [
        ('cercle', '-', 'feuilles', '-', 'lin_vert', 'robe', 'lacet', '-'),
        ('capuche', '-', '-', '-', 'bure', 'robe_longue', '-', '-'),
        ('coiffe', '-', '-', 'fourrure', 'peau', 'fourrure', 'col', '-'),
        ('turban', '-', 'feuilles', '-', 'lin_vert', 'cuir_nu', 'baudrier', '-'),
        ('cercle', '-', 'bois', '-', 'bois', 'ecorce', 'embleme', '-'),
        ('capuche', '-', 'rameaux', 'cape', 'bois', 'robe', 'lacet', 'cape'),
        ('bete', '-', 'bois', 'fourrure', 'peau', 'fourrure', 'col', 'cape'),
        ('capuche_pointe', '-', 'feuilles', '-', 'cuir_vert', 'robe_longue', 'baudrier', 'cape'),
        ('cercle', '-', 'bois', 'cape', 'chene', 'ecorce', 'embleme', 'cape'),
        ('masque', '-', 'feuilles', 'fourrure', 'chene', 'ecorce', 'plastron', '-'),
        ('capuche', 'voile', 'rameaux', '-', 'emeraude', 'robe', 'soleil', 'cape'),
        ('turban', '-', 'oreilles', 'cape', 'ombre', 'fourrure', 'col', 'cape'),
        ('bete', '-', 'bois', 'cape', 'sylve', 'ecorce', 'embleme', 'cape'),
        ('cercle', '-', 'couronne', 'cape', 'or', 'robe_longue', 'soleil', 'cape'),
        ('capuche_pointe', '-', 'bois', 'fourrure', 'givre', 'fourrure', 'col', 'cape'),
        ('masque', '-', 'rameaux', 'cape', 'crepuscule', 'robe', 'rune', 'embleme'),
    ],
    'lamerunique': [
        ('calotte', '-', '-', '-', 'fer', 'cuir', 'rune', '-'),
        ('coiffe', '-', '-', '-', 'cuir', 'gambison', 'lacet', '-'),
        ('chapel', '-', '-', 'camail', 'fer_rouille', 'mailles', 'baudrier', '-'),
        ('capuche', '-', '-', '-', 'drap_gris', 'cuir', 'rune', '-'),
        ('heaume', 'fente', 'pointes', '-', 'runique', 'plaque', 'rune', '-'),
        ('bassinet', '-', 'aileron', '-', 'runique', 'ecailles', 'embleme', 'lames'),
        ('heaume_ouvert', 'mentonniere', 'crete', 'joues', 'acier', 'brigandine', 'rune', 'cape'),
        ('masque', '-', 'pointes', 'camail', 'cuir_noir', 'cuir', 'croises', 'lames'),
        ('barbute', '-', 'cornes_av', 'rosaces', 'acier_noirci', 'plaque', 'rune', 'cape'),
        ('heaume', 'yeux', 'aileron', 'joues', 'nuit', 'ecailles', 'cotes', 'lames'),
        ('salade', 'fente', 'crin', '-', 'emeraude', 'plaque', 'rune', '-'),
        ('capuche_pointe', 'mentonniere', 'gemme', 'cape', 'violet', 'robe', 'rune', 'embleme'),
        ('masque', '-', 'cornes_av', 'joues', 'neant', 'plaque', 'rune', 'cape'),
        ('heaume', 'crocs', 'pointes', 'rosaces', 'dragon', 'ecailles', 'embleme', 'lames'),
        ('bassinet', '-', 'couronne', '-', 'givre', 'plaque', 'rune', 'cape'),
        ('barbute', '-', 'aileron', 'ailettes', 'or', 'plaque', 'cotes', 'lames'),
    ],
    'gardeserment': [
        ('chapel', '-', '-', 'camail', 'fer', 'brigandine', 'tabard', '-'),
        ('calotte', 'nasal', '-', '-', 'fer_rouille', 'gambison', 'ecartele', '-'),
        ('heaume_ouvert', '-', '-', 'camail', 'fer', 'mailles', 'croix', '-'),
        ('coiffe', '-', '-', '-', 'cuir', 'brigandine', 'baudrier', '-'),
        ('heaume', 'fente', 'cimier', 'rosaces', 'acier_bleu', 'plaque', 'ecartele', '-'),
        ('salade', 'fente', 'crin', '-', 'bronze', 'plaque', 'tabard', 'cape'),
        ('bassinet', '-', 'plumet', 'camail', 'acier', 'mailles', 'embleme', 'cape'),
        ('barbute', '-', 'crete', 'joues', 'cuir_noir', 'brigandine', 'ecartele', 'lames'),
        ('heaume', 'grille', 'plumet', 'ailettes', 'pourpre', 'plaque', 'ecartele', 'cape'),
        ('masque', '-', 'cimier', 'rosaces', 'argent_azur', 'plaque', 'croix', 'embleme'),
        ('heaume_ouvert', 'mentonniere', 'couronne', 'camail', 'cuivre', 'ecailles', 'tabard', 'cape'),
        ('salade', 'fente', 'cornes', '-', 'acier_noirci', 'plaque', 'cotes', 'lames'),
        ('bete', '-', 'couronne', 'fourrure', 'or', 'plaque', 'embleme', 'cape'),
        ('heaume', 'croix', 'ailes', 'rosaces', 'blanc_or', 'plaque', 'ecartele', 'cape'),
        ('barbute', '-', 'cimier', 'joues', 'solaire', 'plaque', 'soleil', 'embleme'),
        ('masque', '-', 'cornes', 'fourrure', 'dragon', 'ecailles', 'cotes', 'cape'),
    ],
    'sentinelle': [
        ('coiffe', '-', '-', '-', 'lin_vert', 'gambison', 'lacet', '-'),
        ('capuche', '-', '-', '-', 'cuir', 'cuir_nu', 'baudrier', 'carquois'),
        ('turban', '-', '-', '-', 'toile', 'cuir', 'bourses', '-'),
        ('cercle', '-', 'feuilles', '-', 'lin_vert', 'robe', '-', '-'),
        ('capuche', '-', 'rameaux', '-', 'cuir_vert', 'cuir', 'croises', 'carquois'),
        ('coiffe', '-', 'plumes', 'fourrure', 'peau', 'fourrure', 'col', 'cape'),
        ('capuche_pointe', 'voile', 'feuilles', '-', 'bois', 'ecorce', 'lacet', 'cape'),
        ('heaume_ouvert', '-', 'plumes', 'bandeau', 'cuir_vert', 'brigandine', 'baudrier', 'carquois'),
        ('capuche', 'voile', 'oreilles', 'cape', 'chene', 'cuir', 'col', 'cape'),
        ('masque', '-', 'feuilles', 'plume', 'ombre', 'ecorce', 'plastron', 'carquois'),
        ('turban', 'voile', 'plumes', 'cape', 'emeraude', 'cuir_nu', 'croises', 'carquois'),
        ('bete', '-', 'oreilles', 'fourrure', 'peau', 'fourrure', 'croises', 'cape'),
        ('bete', '-', 'plumes', 'fourrure', 'loup_blanc', 'fourrure', 'col', 'cape'),
        ('capuche_pointe', '-', 'bois', 'cape', 'sylve', 'ecorce', 'embleme', 'cape'),
        ('masque', '-', 'oreilles', 'plume', 'or', 'cuir', 'croises', 'carquois'),
        ('capuche', 'voile', 'rameaux', 'fourrure', 'crepuscule', 'cuir', 'lacet', 'cape'),
    ],
    'arcaniste': [
        ('capuche', '-', '-', '-', 'drap_gris', 'robe', 'lacet', '-'),
        ('coiffe', '-', '-', '-', 'bure', 'gambison', 'rune', '-'),
        ('turban', '-', '-', '-', 'toile', 'robe_longue', 'bourses', '-'),
        ('calotte', '-', '-', '-', 'fer', 'cuir', 'rune', '-'),
        ('capuche', 'mentonniere', 'gemme', '-', 'violet', 'robe', 'plastron', '-'),
        ('cercle', '-', 'gemme', 'cape', 'drap_bleu', 'robe_longue', 'rune', 'cape'),
        ('heaume_ouvert', '-', 'pointes', 'joues', 'runique', 'ecailles', 'rune', '-'),
        ('turban', 'voile', 'gemme', '-', 'violet', 'robe', 'embleme', 'embleme'),
        ('capuche_pointe', 'mentonniere', 'cornes_av', '-', 'nuit', 'robe_longue', 'rune', 'cape'),
        ('masque', '-', 'gemme', 'cape', 'cuivre', 'plaque', 'embleme', 'cape'),
        ('chapeau', '-', '-', 'bandeau', 'emeraude', 'robe', 'rune', 'embleme'),
        ('heaume', 'yeux', 'pointes', 'joues', 'acier_noirci', 'ecailles', 'cotes', 'lames'),
        ('masque', '-', 'couronne', 'cape', 'azur', 'plaque', 'rune', 'cape'),
        ('capuche', 'voile', 'cornes_av', 'cape', 'neant', 'robe_longue', 'rune', 'embleme'),
        ('cercle', '-', 'couronne', 'cape', 'crepuscule', 'robe', 'soleil', 'cape'),
        ('heaume', 'yeux', 'aileron', 'rosaces', 'givre', 'plaque', 'embleme', 'cape'),
    ],
}

TIERS = ['commun', 'rare', 'epique', 'legendaire']


def spec(key, tier, variant):
    return TABLE[key][TIERS.index(tier) * 4 + variant - 1]


METALLIC = {'metal', 'lisse', 'orne', 'ecaille', 'maille'}
METAL_BASES = {'calotte', 'heaume', 'heaume_ouvert', 'salade', 'barbute', 'bassinet', 'chapel', 'masque'}
CLOTH_BASES = {'capuche', 'capuche_pointe', 'chapeau', 'turban'}
METAL_CUTS = {'plaque', 'ecailles'}
CLOTH_CUTS = {'robe', 'robe_longue'}


def _kind(pal, role):
    return (P[pal].get(role) or P[pal]['t'])[1]


def adapt(c, pal, metal):
    """Matière principale accordée à la forme : une coque ou une plaque en métal, une capuche ou une robe en étoffe."""
    c = dict(c)
    if metal and _kind(pal, 'm') not in METALLIC:
        c['m'] = c['t'] if _kind(pal, 't') in METALLIC else palette('acier')['m']
    elif metal is False and _kind(pal, 'm') in METALLIC:
        for role in ('d', 'a', 'l'):
            if _kind(pal, role) not in METALLIC and _kind(pal, role) != 'lueur':
                c['m'] = c[role]
                break
        else:
            c['m'] = palette('violet')['m']
    return c


def helmet(key, tier, variant):
    base, fc, tp, sd, pal = spec(key, tier, variant)[:5]
    c = adapt(palette(pal), pal, True if base in METAL_BASES else (False if base in CLOTH_BASES else None))
    it = Item(f'casque3d_{key}_{tier}_{variant}', density=4, display=HELMET)
    BASES[base](it, c)
    if fc != '-':
        face(it, fc, c)
    if sd != '-':
        side(it, sd, c)
    if tp != '-':
        y = {'chapel': 12.8, 'calotte': 13.4, 'coiffe': 13.4, 'cercle': 12.2, 'turban': 13.0, 'bete': 13.6}.get(base, 12.6)
        if base == 'chapeau' and tp not in ('gemme',):
            y = 13.2
        top(it, tp, c, y)
    return it


def body(key, tier, variant):
    s = spec(key, tier, variant)
    cut = s[5]
    c = adapt(palette(s[4]), s[4], True if cut in METAL_CUTS else (False if cut in CLOTH_CUTS else None))
    return body_painter(s[5:8], c, tier)


# ==================================================================================================================
#  Noms des pièces (écrits dans gear.yml, section « looks » de chaque set)
# ==================================================================================================================

N_CASQUE = {'calotte': 'Calotte', 'heaume': 'Heaume', 'heaume_ouvert': 'Heaume ouvert', 'salade': 'Salade',
            'barbute': 'Barbute', 'bassinet': 'Bassinet', 'chapel': 'Chapel', 'capuche': 'Capuche',
            'capuche_pointe': 'Capuche pointue', 'masque': 'Heaume à masque', 'cercle': 'Diadème',
            'chapeau': 'Chapeau', 'coiffe': 'Coiffe', 'bete': 'Dépouille', 'turban': 'Turban'}
N_CORPS = {'plaque': 'Cuirasse', 'ecailles': "Haubert d'écailles", 'mailles': 'Haubert de mailles',
           'brigandine': 'Brigandine', 'gambison': 'Gambison', 'cuir': 'Justaucorps', 'cuir_nu': 'Gilet de cuir',
           'fourrure': 'Pelisse', 'robe': 'Robe', 'robe_longue': 'Robe longue', 'ecorce': "Armure d'écorce"}
N_JAMBES = {'plaque': 'Jambières', 'ecailles': "Jambières d'écailles", 'mailles': 'Chausses de mailles',
            'brigandine': 'Jambières', 'gambison': 'Chausses matelassées', 'cuir': 'Braies de cuir',
            'cuir_nu': 'Braies de cuir', 'fourrure': 'Jambières fourrées', 'robe': 'Bas de robe',
            'robe_longue': 'Pans de robe', 'ecorce': "Jambières d'écorce"}
N_PIEDS = {'plaque': 'Solerets', 'ecailles': 'Solerets', 'mailles': 'Bottes ferrées', 'brigandine': 'Bottes ferrées',
           'gambison': 'Bottes', 'cuir': 'Bottes', 'cuir_nu': 'Bottes', 'fourrure': 'Bottes fourrées',
           'robe': 'Souliers', 'robe_longue': 'Souliers', 'ecorce': "Bottes d'écorce"}
N_LIGNEE = {'fer': 'du Soudard', 'fer_rouille': 'du Vagabond', 'cuir': 'du Coureur', 'toile': 'du Paysan',
            'bure': "de l'Ermite", 'lin_vert': 'du Bosquet', 'drap_gris': "de l'Apprenti", 'peau': 'du Trappeur',
            'acier': 'du Vétéran', 'acier_bleu': 'de la Garde', 'cuir_vert': 'du Forestier', 'drap_bleu': 'des Étoiles',
            'bois': 'du Sylvain', 'runique': 'des Runes', 'bronze': 'du Légionnaire', 'cuir_noir': 'du Spadassin',
            'violet': "de l'Arcane", 'acier_noirci': 'du Bourreau', 'argent_azur': 'du Ciel', 'pourpre': 'de la Pourpre',
            'ombre': "de l'Ombre", 'chene': 'du Vieux Chêne', 'emeraude': "d'Émeraude", 'cuivre': 'du Cuivre vert',
            'nuit': 'de la Nuit', 'or': "d'Or", 'blanc_or': 'du Séraphin', 'dragon': 'du Dragon', 'neant': 'du Néant',
            'givre': 'du Givre', 'solaire': "de l'Aube ardente", 'sylve': 'du Cerf blanc', 'loup_blanc': 'du Loup blanc',
            'azur': "de l'Azur", 'crepuscule': 'du Crépuscule'}


def names(key, tier, variant):
    s = spec(key, tier, variant)
    lin = N_LIGNEE[s[4]]
    return {'casque': f'{N_CASQUE[s[0]]} {lin}', 'plastron': f'{N_CORPS[s[5]]} {lin}',
            'jambieres': f'{N_JAMBES[s[5]]} {lin}', 'bottes': f'{N_PIEDS[s[5]]} {lin}'}


def gear_looks_yaml(key):
    """Bloc YAML « looks » d'un set : par rareté, les noms des 4 variantes."""
    q = lambda x: '"' + x.replace('"', '\\"') + '"'
    out = ['    looks:   # généré par src/armures/kit_armures.py (dépôt ressourcepack)']
    for tier in TIERS:
        out.append(f'      {tier}:')
        for v in range(1, 5):
            n = names(key, tier, v)
            out.append('        - {casque: %s, plastron: %s, jambieres: %s, bottes: %s}'
                       % (q(n['casque']), q(n['plastron']), q(n['jambieres']), q(n['bottes'])))
    return '\n'.join(out)
