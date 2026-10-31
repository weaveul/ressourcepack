"""Panoplies de classe en 3D pour BetterModel : modèle de joueur (dossier plugins/BetterModel/players) dont les
membres prennent le skin du joueur (os ph/pc/pw/phip/pra/prfa/pla/plfa/prl/prfl/pll/plfl, repris de steve.bbmodel)
et portent des pièces d'armure modelées (os enfants ar_*), avec animations idle / walk / attack.

Repère BetterModel : avant vers -z, droite du joueur vers +x, 0.9375 unité par pixel de skin (tête 22.5..30).
Le casque reprend heaumes.py (repère casque : tête 4..12), mis à l'échelle sur l'os de tête.
"""
import base64, copy, io, json, math, os, sys, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'items'))
sys.path.insert(0, HERE)
from PIL import Image  # noqa: E402
import heaumes  # noqa: E402
from heaumes import H, M, glow, R, plate, gold, engraved, cloth, horn, leather  # noqa: E402
from kit import MATS  # noqa: E402

STEVE = os.path.join(HERE, 'bm', 'steve.bbmodel')
OUT = '/mnt/project-files/models/players'
K = 0.9375                      # pixel de skin -> unité du modèle
HEAD_C = (0.0, 26.25, 0.0)      # centre de la tête

# os d'armure -> os du skin qui le porte
PARENT = {'ar_tete': 'hi_ph_head', 'ar_torse': 'pc_chest', 'ar_cape': 'pc_chest', 'ar_taille': 'pw_waist',
          'ar_hanches': 'phip_hip', 'ar_epaule_d': 'pra_right_arm', 'ar_epaule_g': 'pla_left_arm',
          'ar_avb_d': 'prfa_right_forearm', 'ar_avb_g': 'plfa_left_forearm', 'ar_cuisse_d': 'prl_right_leg',
          'ar_cuisse_g': 'pll_left_leg', 'ar_jambe_d': 'prfl_right_foreleg', 'ar_jambe_g': 'plfl_left_foreleg'}


def U():
    return str(uuid.uuid4())


# ==================================================================================================================
#  Pièces
# ==================================================================================================================

ARM_FIX = {'pra_right_arm': (-0.625, -0.5), 'pla_left_arm': (0.625, -0.5),
           'prfa_right_forearm': (-0.625, -0.375), 'plfa_left_forearm': (0.625, -0.375)}


def _shift(e, dx, dy):
    e['from'] = [e['from'][0] + dx, e['from'][1] + dy, e['from'][2]]
    e['to'] = [e['to'][0] + dx, e['to'][1] + dy, e['to'][2]]
    if e.get('origin'):
        e['origin'] = [e['origin'][0] + dx, e['origin'][1] + dy, e['origin'][2]]


def _eye_points():
    """Positions de la caméra FPS dans le repère de la tête (pivot du cou y 22.5). La tête suit le regard, donc dans
    son repère la caméra ne bouge qu'avec le tangage : debout l'oeil est 3.42 au-dessus du cou ; accroupi (pose
    « sneak ») il passe derrière le cou, 2.2 à 2.9 plus loin."""
    pts = []
    for p in range(-96, 97, 6):
        a = math.radians(p)
        pts.append((0.0, 22.5 + 3.42 * math.cos(a), 3.42 * math.sin(a)))
    for r in (2.2, 2.55, 2.9):
        for p in range(30, 131, 10):
            a = math.radians(p)
            for sg in (1, -1):
                pts.append((0.0, 22.5 + r * math.cos(a), sg * r * math.sin(a)))
    return pts


EYES = _eye_points()
# Coque du casque (autour de la tête) : presque tout l'hémisphère avant, pour les bords d'écran et le retard
# d'interpolation de BetterModel. Ornements extérieurs (cornes, ailes) : champ normal, sinon ils se creusent.
VIEW_COS_SHELL = math.cos(math.radians(88))
VIEW_COS = math.cos(math.radians(72))


FACE_N = {'north': (0, 0, -1), 'south': (0, 0, 1), 'east': (1, 0, 0), 'west': (-1, 0, 0), 'up': (0, 1, 0),
          'down': (0, -1, 0)}


def _rot(v, axis, ang, o=(0, 0, 0)):
    x, y, z = v[0] - o[0], v[1] - o[1], v[2] - o[2]
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    if axis == 0:
        y, z = y * c - z * s_, y * s_ + z * c
    elif axis == 1:
        x, z = x * c + z * s_, -x * s_ + z * c
    else:
        x, y = x * c - y * s_, x * s_ + y * c
    return (x + o[0], y + o[1], z + o[2])


def cull_for_camera(e):
    """Retire les faces qu'on verrait depuis la caméra FPS (celles tournées vers l'intérieur du casque) : de dedans,
    le casque devient invisible ; de dehors on ne voit que ses faces extérieures, donc rien ne change."""
    f, t = e['from'], e['to']
    c = [(f[i] + t[i]) / 2 for i in range(3)]
    h = [(t[i] - f[i]) / 2 for i in range(3)]
    shell = abs(c[0]) <= 4.8 and abs(c[2]) <= 4.8 and 21 <= c[1] <= 36
    cone = VIEW_COS_SHELL if shell else VIEW_COS
    rot = e.get('rotation') or [0, 0, 0]
    axis = next((i for i in range(3) if rot[i]), None)
    keep = {}
    for name, fd in e['faces'].items():
        n = FACE_N[name]
        fc = [c[i] + n[i] * h[i] for i in range(3)]
        # coins de la face
        ax = [i for i in range(3) if not n[i]]
        pts = [fc] + [[fc[i] + (sa * h[i] if i == ax[0] else sb * h[i] if i == ax[1] else 0) for i in range(3)]
                      for sa in (-1, 1) for sb in (-1, 1)]
        variants = [(pts, n)]
        if axis is not None:                      # même sens de rotation que le rendu (render.py) et le jeu
            variants = [([_rot(q, axis, rot[axis], e['origin']) for q in pts], _rot(n, axis, rot[axis]))]
        seen = False
        for qs, nn in variants:
            for ey in EYES:
                if sum((ey[i] - qs[0][i]) * nn[i] for i in range(3)) <= 1e-4:
                    continue                      # face tournée de l'autre côté : jamais vue de la caméra
                for q in qs:
                    d = [q[i] - ey[i] for i in range(3)]
                    ln = math.sqrt(sum(v * v for v in d)) or 1
                    if -d[2] / ln >= cone:    # dans le champ de vision (vers -z)
                        seen = True
                        break
                if seen:
                    break
            if seen:
                break
        keep[name] = fd if not seen else {'uv': [0, 0, 0, 0], 'texture': None}   # BetterModel exige 6 faces
    e['faces'] = keep
    return any(fd['texture'] is not None for fd in keep.values())


def helmet_into(x, item):
    """Recopie les éléments d'un casque heaumes (repère casque) dans l'os de tête du modèle."""
    def tp(p):
        return [(p[0] - 8) * K + HEAD_C[0], (p[1] - 8) * K + HEAD_C[1], (p[2] - 8) * K + HEAD_C[2]]
    for e in item.els:
        e2 = dict(e)
        e2['from'], e2['to'] = tp(e['from']), tp(e['to'])
        if e.get('rot'):
            r = dict(e['rot'])
            r['origin'] = tp(r['origin'])
            e2['rot'] = r
        e2['bone'] = 'ar_tete'
        x.it.els.append(e2)


def guerrier_legendaire():
    st = M('he_gu_steel', (66, 68, 80), engraved)
    st2 = M('he_gu_steel2', (104, 106, 118), plate)
    gd = M('he_gu_gold', (222, 168, 60), gold)
    rd = M('he_gu_red', (156, 26, 24), cloth, noise=8, edge=0.8, hi=False)
    lt = M('se_gu_leather', (70, 46, 30), leather, edge=0.8, hi=False)
    hn = M('he_gu_horn', (220, 196, 150), horn, edge=0.78)
    ey = glow('he_gu_eye', (255, 120, 40))
    x = H('set_guerrier_legendaire', cx=0, density=4)
    helmet_into(x, heaumes.guerrier())

    # --- torse : cuirasse en proue, gorgerin, gemme de braise, dossière
    x.bone = 'ar_torse'
    x.b((-4.05, 18.6, -2.25), (4.05, 22.6, 2.2), st)
    x.m((-4.1, 18.7, -2.75), (0.2, 22.5, -2.25), st2, R('y', 22.5, (0, 0, -2.25)))
    x.b((-0.55, 18.5, -3.2), (0.55, 22.7, -2.3), gd)
    x.m((-4.15, 22.0, -2.85), (-0.4, 22.5, -2.2), gd, R('y', 22.5, (0, 0, -2.25)))
    x.b((-0.8, 20.0, -3.45), (0.8, 21.5, -3.15), ey)
    x.b((-3.0, 22.4, -2.4), (3.0, 23.3, 2.4), gd)                            # gorgerin
    x.b((-3.9, 18.8, 2.2), (3.9, 22.5, 2.6), st2)
    x.b((-0.45, 18.8, 2.6), (0.45, 22.5, 2.85), gd)
    # --- cape rouge
    x.bone = 'ar_cape'
    x.b((-4.3, 4.0, 2.9), (4.3, 22.6, 3.3), rd)
    x.b((-4.4, 21.8, 2.7), (4.4, 22.8, 3.5), gd)
    x.b((-4.3, 4.0, 2.85), (4.3, 4.5, 3.35), gd)
    # --- taille : plaques de ventre, ceinture, boucle
    x.bone = 'ar_taille'
    x.b((-3.95, 15.8, -2.15), (3.95, 18.55, 2.1), st)
    x.b((-4.0, 17.1, -2.25), (4.0, 17.5, 2.2), gd)
    x.b((-4.1, 14.9, -2.3), (4.1, 15.9, 2.3), lt)
    x.b((-0.9, 14.7, -2.65), (0.9, 16.1, -2.25), gd)
    # --- hanches : tassettes, tabard rouge
    x.bone = 'ar_hanches'
    x.b((-3.9, 13.1, -2.5), (3.9, 14.9, -2.05), st2)
    x.b((-3.6, 11.6, -2.7), (3.6, 13.3, -2.25), st)
    x.b((-1.6, 5.4, -3.0), (1.6, 14.6, -2.65), rd)
    x.b((-1.8, 5.0, -3.1), (1.8, 5.5, -2.6), gd)
    x.b((-1.6, 6.0, 2.2), (1.6, 14.6, 2.55), rd)
    x.m((-4.3, 10.4, -2.1), (-3.6, 14.8, 2.1), st2, R('z', -22.5, (-3.9, 14.8, 0)))
    x.m((-4.35, 10.2, -2.15), (-3.55, 10.6, 2.15), gd, R('z', -22.5, (-3.9, 14.8, 0)))

    for s in (1, -1):
        d = 'd' if s > 0 else 'g'
        X = lambda a, b: (min(a * s, b * s), max(a * s, b * s))  # noqa: E731

        def bx(xa, y0, z0, xb, y1, z1, mat, rot=None):
            lo, hi = X(xa, xb)
            x.b((lo, y0, z0), (hi, y1, z1), mat, rot)

        # --- épaulière : dôme, lames étagées, liserés d'or, pointes
        x.bone = f'ar_epaule_{d}'
        bx(2.8, 20.6, -3.2, 9.2, 24.4, 3.2, st)
        bx(3.4, 24.4, -2.6, 8.4, 25.4, 2.6, st2)
        bx(4.2, 25.4, -1.8, 7.6, 25.9, 1.8, gd)
        x.b((min(5.9 * s, 9.6 * s), 20.6, -3.21), (max(5.9 * s, 9.6 * s), 24.4, 3.21), st2,
            R('z', -22.5 * s, (9.2 * s, 24.4, 0)))                               # pan extérieur incliné
        bx(3.0, 19.4, -3.0, 9.6, 20.8, 3.0, st2)
        bx(3.4, 18.2, -2.8, 9.4, 19.6, 2.8, st)
        bx(2.8, 20.5, -3.4, 9.7, 20.9, 3.4, gd)
        bx(3.0, 19.3, -3.1, 9.7, 19.5, 3.1, gd)
        bx(5.8, 21.4, -3.45, 7.2, 22.8, -3.2, ey)                                # gemme de braise
        for z in (-2.0, 0.0, 2.0):
            x.limb((6.6 * s, 25.2, z), [(1.8, -22.5 * s, 1.1), (1.6, -22.5 * s, 0.8), (1.2, 0, 0.45)], [gd, hn, hn],
                   plane='xy', depth=1.0)
        bx(3.55, 17.3, -2.1, 7.75, 18.4, 2.1, st)                                # brassard
        # --- canon d'avant-bras, gantelet évasé, ailerons
        x.bone = f'ar_avb_{d}'
        bx(3.5, 12.4, -2.1, 7.75, 16.2, 2.1, st)
        bx(3.45, 15.6, -2.2, 7.8, 16.0, 2.2, gd)
        bx(3.3, 11.1, -2.4, 7.95, 12.5, 2.4, st2)
        bx(3.25, 12.4, -2.45, 8.0, 12.75, 2.45, gd)
        x.limb((7.75 * s, 13.2, 0), [(1.2, -45 * s, 0.9), (1.0, -22.5 * s, 0.5)], [st2, gd], plane='xy', depth=0.4)
        # --- cuissard, genouillère à pointe, grève, soleret
        x.bone = f'ar_cuisse_{d}'
        bx(-0.1, 6.4, -2.2, 3.95, 11.0, 2.05, st)
        bx(-0.15, 9.7, -2.3, 4.0, 10.1, 2.1, gd)
        x.bone = f'ar_jambe_{d}'
        bx(-0.1, 4.6, -2.6, 3.95, 6.4, -1.9, st2)
        x.limb((1.9 * s, 5.5, -2.6), [(0.9, -90, 0.7), (0.5, -90, 0.35)], [gd], plane='zy')
        bx(-0.1, 1.3, -2.15, 3.95, 4.9, 2.05, st)
        bx(-0.15, 4.5, -2.25, 4.0, 4.9, 2.1, gd)
        bx(-0.2, 0.0, -3.1, 4.05, 1.4, 2.15, st2)
        bx(0.6, 0.0, -3.4, 3.2, 1.0, -3.05, gd)
    return x.it


SETS = {'guerrier_legendaire': guerrier_legendaire}


# ==================================================================================================================
#  Animations
# ==================================================================================================================

def _kf(ch, t, v):
    return {'channel': ch, 'data_points': [{'x': str(v[0]), 'y': str(v[1]), 'z': str(v[2])}], 'uuid': U(),
            'time': round(t, 4), 'color': -1, 'interpolation': 'catmullrom'}


def _anim(name, loop, length, tracks, gid, pos=None, scale=None, override=False):
    animators = {}
    for b, pts in tracks.items():
        animators[gid[b]] = {'name': b, 'type': 'bone', 'rotation_global': False, 'quaternion_interpolation': False,
                             'keyframes': [_kf('rotation', t, v) for t, v in pts]}
    for b, pts in (pos or {}).items():
        an = animators.setdefault(gid[b], {'name': b, 'type': 'bone', 'rotation_global': False,
                                           'quaternion_interpolation': False, 'keyframes': []})
        an['keyframes'] += [_kf('position', t, v) for t, v in pts]
    for b, pts in (scale or {}).items():
        an = animators.setdefault(gid[b], {'name': b, 'type': 'bone', 'rotation_global': False,
                                           'quaternion_interpolation': False, 'keyframes': []})
        an['keyframes'] += [_kf('scale', t, v) for t, v in pts]
    return {'uuid': U(), 'name': name, 'loop': loop, 'override': override, 'length': length, 'snapping': 24,
            'selected': False, 'group_name': '', 'anim_time_update': '', 'blend_weight': '', 'start_delay': '',
            'loop_delay': '', 'animators': animators}


def wave(L, n, f):
    """Échantillonne f(phase 0..1) en n+1 clés sur une boucle de L secondes."""
    return [(L * i / n, f(i / n)) for i in range(n + 1)]


def animations(gid):
    L = 0.9                                         # un pas complet (gauche + droite)
    c = lambda p: math.cos(2 * math.pi * p)         # noqa: E731
    sn = lambda p: math.sin(2 * math.pi * p)        # noqa: E731
    kn = lambda p: max(0.0, sn(p)) ** 1.5           # noqa: E731  genou : se plie quand la jambe revient
    walk = _anim('walk', 'loop', L, {
        'prl_right_leg': wave(L, 8, lambda p: (-32 * c(p), 0, 0)),
        'pll_left_leg': wave(L, 8, lambda p: (32 * c(p), 0, 0)),
        'prfl_right_foreleg': wave(L, 8, lambda p: (6 + 42 * kn(p + 0.0), 0, 0)),
        'plfl_left_foreleg': wave(L, 8, lambda p: (6 + 42 * kn(p + 0.5), 0, 0)),
        'pra_right_arm': wave(L, 8, lambda p: (26 * c(p), 0, 3)),
        'pla_left_arm': wave(L, 8, lambda p: (-26 * c(p), 0, -3)),
        'prfa_right_forearm': wave(L, 8, lambda p: (-12 - 16 * max(0.0, -c(p)), 0, 0)),
        'plfa_left_forearm': wave(L, 8, lambda p: (-12 - 16 * max(0.0, c(p)), 0, 0)),
        'pc_chest': wave(L, 8, lambda p: (-3, 6 * c(p), 0)),
        'phip_hip': wave(L, 8, lambda p: (0, -5 * c(p), 0)),
        'ar_cape': wave(L, 8, lambda p: (14 + 5 * sn(2 * p), 0, 0)),
    }, gid, pos={'player_root': wave(L, 8, lambda p: (0, 0.55 * abs(sn(p)), 0))})
    idle = _anim('idle', 'loop', 3.0, {
        'pc_chest': wave(3.0, 6, lambda p: (-1.8 * (1 - c(p)) / 2, 0, 0)),
        'pra_right_arm': wave(3.0, 6, lambda p: (-2, 0, 3 + 2 * (1 - c(p)) / 2)),
        'pla_left_arm': wave(3.0, 6, lambda p: (-2, 0, -3 - 2 * (1 - c(p)) / 2)),
        'prfa_right_forearm': [(0, (-6, 0, 0)), (3.0, (-6, 0, 0))],
        'plfa_left_forearm': [(0, (-6, 0, 0)), (3.0, (-6, 0, 0))],
        'ar_cape': wave(3.0, 6, lambda p: (4 + 2 * sn(p), 0, 0)),
    }, gid, pos={'player_root': wave(3.0, 6, lambda p: (0, -0.15 * (1 - c(p)) / 2, 0))})
    attack = _anim('attack', 'once', 0.45, {
        'pra_right_arm': [(0, (0, 0, 0)), (0.1, (-130, -10, 12)), (0.22, (20, 15, -8)), (0.45, (0, 0, 0))],
        'prfa_right_forearm': [(0, (0, 0, 0)), (0.1, (-25, 0, 0)), (0.22, (-5, 0, 0)), (0.45, (0, 0, 0))],
        'pc_chest': [(0, (0, 0, 0)), (0.1, (-4, 14, 0)), (0.22, (8, -18, 0)), (0.45, (0, 0, 0))],
        'pla_left_arm': [(0, (0, 0, 0)), (0.1, (-20, 0, -10)), (0.22, (15, 0, -5)), (0.45, (0, 0, 0))],
    }, gid)
    jump = _anim('jump', 'once', 0.5, {
        'prl_right_leg': [(0, (0, 0, 0)), (0.15, (-25, 0, 0)), (0.5, (0, 0, 0))],
        'pll_left_leg': [(0, (0, 0, 0)), (0.15, (10, 0, 0)), (0.5, (0, 0, 0))],
        'prfl_right_foreleg': [(0, (0, 0, 0)), (0.15, (40, 0, 0)), (0.5, (0, 0, 0))],
        'plfl_left_foreleg': [(0, (0, 0, 0)), (0.15, (30, 0, 0)), (0.5, (0, 0, 0))],
        'pra_right_arm': [(0, (0, 0, 0)), (0.15, (-30, 0, 15)), (0.5, (0, 0, 0))],
        'pla_left_arm': [(0, (0, 0, 0)), (0.15, (-30, 0, -15)), (0.5, (0, 0, 0))],
        'ar_cape': [(0, (5, 0, 0)), (0.2, (35, 0, 0)), (0.5, (8, 0, 0))],
    }, gid)
    # Accroupi (joué par EvoPerso tant que le joueur est accroupi) : le corps descend comme la caméra, sinon en FPS
    # elle passe dans l'armure. override : remplace marche/repos pendant l'accroupissement.
    hold = lambda v: [(0, v), (1.0, v)]  # noqa: E731
    sneak = _anim('sneak', 'loop', 1.0, {
        'prl_right_leg': hold((-42, 0, 0)), 'pll_left_leg': hold((-42, 0, 0)),
        'prfl_right_foreleg': hold((84, 0, 0)), 'plfl_left_foreleg': hold((84, 0, 0)),
        'pw_waist': hold((-16, 0, 0)), 'pc_chest': hold((-6, 0, 0)),
        'pra_right_arm': hold((-18, 0, 4)), 'pla_left_arm': hold((-18, 0, -4)),
        'prfa_right_forearm': hold((-14, 0, 0)), 'plfa_left_forearm': hold((-14, 0, 0)),
        'ar_cape': hold((24, 0, 0)),
    }, gid, pos={'player_root': hold((0, -2.9, 0))}, override=True)
    return [idle, walk, attack, jump, sneak]


# ==================================================================================================================
#  Écriture du .bbmodel
# ==================================================================================================================

def build(key):
    item = SETS[key]()
    img, els = item.build()
    W = img.width
    d = json.load(open(STEVE))
    d['name'] = f'evo_{key}'
    for g in d['groups']:
        if g['name'] == 'h_ph_head':
            g['name'] = 'hi_ph_head'       # hi_ : l'os ET ses enfants (casque) suivent le regard ; h_ = l'os seul
    # La cape du skin (os cape_cape) ferait doublon avec la cape de la panoplie.
    cape = [g for g in d['groups'] if g['name'] == 'cape_cape']
    if cape:
        d['groups'].remove(cape[0])

        def drop(lst):
            for c in list(lst):
                if isinstance(c, dict):
                    if c['uuid'] == cape[0]['uuid']:
                        lst.remove(c)
                    else:
                        drop(c['children'])
        drop(d['outliner'])
    # BetterModel dessine le skin des bras centré sur le pivot de l'os (bras : x 5, haut à y 22 ; avant-bras : haut à
    # 16.5), alors que les cubes de steve.bbmodel sont décalés de 0.625 vers l'extérieur et 0.5 / 0.375 vers le haut.
    # On recale les cubes du skin (pour l'aperçu) et l'armure des bras sur ce que le jeu affiche vraiment.
    uuid_bone = {}

    def own(lst, gname=None):
        for c in lst:
            if isinstance(c, dict):
                own(c['children'], {g['uuid']: g['name'] for g in d['groups']}[c['uuid']])
            else:
                uuid_bone[c] = gname
    own(d['outliner'])
    for e in d['elements']:
        dx, dy = ARM_FIX.get(uuid_bone.get(e['uuid']), (0, 0))
        if dx or dy:
            _shift(e, dx, dy)
    groups = {g['name']: g for g in d['groups']}
    gid = {n: g['uuid'] for n, g in groups.items()}
    # noeuds de l'outliner par uuid de groupe
    nodes = {}

    def index(lst):
        for c in lst:
            if isinstance(c, dict):
                nodes[c['uuid']] = c
                index(c['children'])
    index(d['outliner'])
    # os d'armure
    ar_nodes = {}
    for bone, parent in PARENT.items():
        pg = groups[parent]
        g = copy.deepcopy(pg)
        g.update({'uuid': U(), 'name': bone, 'rotation': [0, 0, 0], 'children': []})
        if bone == 'ar_cape':
            g['origin'] = [0, 22.6, 3.1]   # la cape pivote depuis les épaules
        d['groups'].append(g)
        gid[bone] = g['uuid']
        node = {'uuid': g['uuid'], 'isOpen': True, 'children': []}
        nodes[pg['uuid']]['children'].append(node)
        ar_nodes[bone] = node
    # texture de l'armure (index 1)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    tex = copy.deepcopy(d['textures'][0])
    tex.update({'name': f'evo_{key}.png', 'id': '1', 'width': W, 'height': W, 'uv_width': W, 'uv_height': W,
                'uuid': U(), 'source': 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()})
    d['textures'].append(tex)
    face_map = {'north': 'north', 'south': 'south', 'east': 'east', 'west': 'west', 'up': 'up', 'down': 'down'}
    n = 0
    for src, el in zip(item.els, els):
        bone = src.get('bone')
        if bone not in ar_nodes:
            continue
        faces = {}
        for f, fd in el['faces'].items():
            u0, v0, u1, v1 = [c * W / 16 for c in fd['uv']]
            faces[face_map[f]] = {'uv': [u0, v0, u1, v1], 'texture': 1}
        e = {'name': 'armure', 'box_uv': False, 'render_order': 'default', 'locked': False,
             'allow_mirror_modeling': True, 'from': el['from'], 'to': el['to'], 'autouv': 0, 'color': 0,
             'origin': [(el['from'][i] + el['to'][i]) / 2 for i in range(3)], 'faces': faces, 'type': 'cube',
             'uuid': U()}
        if el.get('rotation'):
            r = el['rotation']
            e['origin'] = r['origin']
            e['rotation'] = [r['angle'] if r['axis'] == a else 0 for a in 'xyz']
        if el.get('light_emission'):
            e['light_emission'] = el['light_emission']
        if bone == 'ar_tete' and not cull_for_camera(e):
            continue
        dx, dy = ARM_FIX.get(PARENT[bone], (0, 0))
        if dx or dy:
            _shift(e, dx, dy)
        d['elements'].append(e)
        ar_nodes[bone]['children'].append(e['uuid'])
        n += 1
    d['animations'] = animations(gid)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f'evo_{key}.bbmodel')
    json.dump(d, open(path, 'w'))
    return path, n, W


if __name__ == '__main__':
    for key in (sys.argv[1:] or SETS):
        print(build(key))


def preview(key, path):
    """Planche face / profil / dos, pose de repos, skin neutre."""
    from render import render
    from kit import Mat
    MATS['se_skin'] = Mat((150, 120, 100), 4, 0.9)
    item = SETS[key]()
    d = json.load(open(STEVE))
    names = {g['uuid']: g['name'] for g in d['groups']}
    owner = {}

    def own(lst, gname=None):
        for c in lst:
            if isinstance(c, dict):
                own(c['children'], names[c['uuid']])
            else:
                owner[c] = gname
    own(d['outliner'])
    for e in d['elements']:
        if e['name'] == 'skin':
            dx, dy = ARM_FIX.get(owner[e['uuid']], (0, 0))   # skin là où BetterModel le dessine
            item.box((e['from'][0] + dx, e['from'][1] + dy, e['from'][2]),
                     (e['to'][0] + dx, e['to'][1] + dy, e['to'][2]), 'se_skin')
    img, els = item.build()
    for src, e in zip(item.els, els):
        dx, dy = ARM_FIX.get(PARENT.get(src.get('bone')), (0, 0))
        if dx or dy:
            e['from'] = [e['from'][0] + dx, e['from'][1] + dy, e['from'][2]]
            e['to'] = [e['to'][0] + dx, e['to'][1] + dy, e['to'][2]]
            if e.get('rotation'):
                o = e['rotation']['origin']
                e['rotation'] = dict(e['rotation'], origin=[o[0] + dx, o[1] + dy, o[2]])
    for e in els:                                   # recentre la figure sur le repère du rendu
        for k in ('from', 'to'):
            e[k] = [e[k][0] + 8, e[k][1] - 9, e[k][2] + 8]
        if e.get('rotation'):
            o = e['rotation']['origin']
            e['rotation'] = dict(e['rotation'], origin=[o[0] + 8, o[1] - 9, o[2] + 8])
    tiles = []
    for yaw in (200, 135, 20):
        disp = {'gui': {'rotation': [12, yaw, 0], 'translation': [0, 0, 0], 'scale': [0.34] * 3}}
        tiles.append(render(img, els, disp, 420))
    sheet = Image.new('RGBA', (420 * 3, 420), (40, 42, 48, 255))
    for i, t in enumerate(tiles):
        sheet.alpha_composite(t, (i * 420, 0))
    sheet.save(path)
