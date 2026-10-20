"""Effets visuels HD des sorts : sprites (textures lisses 64-128 px, alpha progressif) posés sur des
quads plats, affichés en jeu par des item_display (EvoPerso, classe Vfx).

python3 src/vfx/generate.py  ->  pack/assets/evo/{items,models/item,textures/item}/vfx/...
Un modèle d'objet par sprite (ou par image d'une animation : EvoPerso change de modèle à chaque tick,
une animation .mcmeta ne repartirait pas de la première image)."""
import json, math, os
import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'pack', 'assets', 'evo')
rng = np.random.default_rng(7)


# ---------- bruit ----------
def value_noise(n, cells, seed):
    r = np.random.default_rng(seed)
    g = r.random((cells + 1, cells + 1))
    g[-1, :] = g[0, :]; g[:, -1] = g[:, 0]          # raccord
    t = np.linspace(0, cells, n, endpoint=False)
    i = t.astype(int); f = t - i; f = f * f * (3 - 2 * f)
    a = g[i][:, i]; b = g[i][:, i + 1]; c = g[i + 1][:, i]; d = g[i + 1][:, i + 1]
    fx = f[None, :]; fy = f[:, None]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def fbm(n, seed, octaves=4, base=4):
    out = np.zeros((n, n)); amp = 1; tot = 0
    for o in range(octaves):
        out += amp * value_noise(n, base * 2 ** o, seed + o * 17); tot += amp; amp *= 0.5
    return out / tot


def angular(th, seed, phase=0.0, kmin=2, kmax=13):
    """bruit périodique en angle (bords de flamme irréguliers), -1..1"""
    r = np.random.default_rng(seed); out = 0; tot = 0
    for k in range(kmin, kmax):
        amp = r.uniform(0.3, 1) / k ** 0.7
        out = out + amp * np.sin(k * th + r.uniform(0, 6.3) + phase * r.choice([-1, 1]) * r.uniform(0.5, 1.5))
        tot += amp
    return out / tot


def polar(n):
    y, x = np.mgrid[0:n, 0:n] + 0.5
    x = (x - n / 2) / (n / 2); y = (y - n / 2) / (n / 2)
    return np.sqrt(x * x + y * y), np.arctan2(y, x)


def ramp(t, stops):
    """t 0..1 -> RGB via des paliers [(pos, (r,g,b)), ...]"""
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,))
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (t >= p0) & (t <= p1)
        k = ((t - p0) / max(p1 - p0, 1e-6))[m][:, None]
        out[m] = np.array(c0) * (1 - k) + np.array(c1) * k
    return out


def save(img_rgb, alpha, path):
    a = np.clip(alpha, 0, 1)
    rgba = np.dstack([np.clip(img_rgb, 0, 255), a * 255]).astype(np.uint8)
    rgba[a < 1 / 255] = 0                                # pixels vides vraiment transparents
    full = os.path.join(ROOT, 'textures', 'item', 'vfx', path + '.png')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    Image.fromarray(rgba, 'RGBA').save(full)


FIRE = [(0, (255, 255, 235)), (0.18, (255, 236, 140)), (0.4, (255, 170, 40)), (0.65, (235, 80, 15)), (0.85, (150, 25, 10)), (1, (60, 10, 8))]
SMOKE = [(0, (90, 80, 76)), (1, (40, 36, 36))]


# ---------- sprites ----------
def fire_core(frames=8, n=64, name='fire_core', stops=None, seed=100):
    stops = stops or FIRE
    r, th = polar(n)
    for f in range(frames):
        ph = f / frames * 2 * math.pi
        noise = fbm(n, seed + f * 3, 4, 3)
        # langues de flamme qui tournent
        tongues = 0.5 + 0.5 * angular(th + noise * 0.6, 11, ph)
        edge = 0.58 + 0.3 * tongues + 0.14 * (noise - 0.5)
        heat = r / edge
        a = np.clip(1.25 - heat, 0, 1) ** 0.8
        col = ramp(heat * 0.95 + (noise - 0.5) * 0.25, stops)
        save(col, a, f'{name}_{f}')


def glow(name, n, color, power=2.2, maxa=0.55):
    r, _ = polar(n)
    a = np.clip(1 - r, 0, 1) ** power * maxa
    col = np.ones((n, n, 3)) * np.array(color)
    save(col, a, name)


def ember(n=32, name='ember', stops=None):
    stops = stops or FIRE
    r, _ = polar(n)
    core = np.clip(1 - r * 2.4, 0, 1)
    a = np.clip(np.clip(1 - r, 0, 1) ** 2.4 + core, 0, 1)
    col = ramp(0.75 - core * 0.75, stops)
    save(col, a, name)


def explosion(frames=8, n=128, name='explosion', stops=None, smoke_on=True, seed=300, cel=False):
    stops = stops or FIRE
    r, th = polar(n)
    for f in range(frames):
        t = (f + 1) / frames
        noise = fbm(n, seed + f, 5, 3)
        radius = 0.35 + 0.6 * t ** 0.6
        lumps = 0.14 * angular(th + noise * 0.8, 21, t * 2) + 0.28 * (noise - 0.5)
        d = r / (radius * (1 + lumps))
        # coeur brûlant qui refroidit, fumée sur le bord vers la fin
        heat = d * (0.55 + 0.9 * t) + (noise - 0.5) * 0.3
        fire = ramp(np.floor(np.clip(heat, 0, 1) * 5) / 5 + 0.1 if cel else heat, stops)
        smoke_amt = (1 if smoke_on else 0) * np.clip((d - 0.55) * 2 + t * 0.9 - 0.5, 0, 1) * np.clip(t * 1.6, 0, 1)
        smoke = ramp(noise, SMOKE)
        col = fire * (1 - smoke_amt[..., None]) + smoke * smoke_amt[..., None]
        a = (np.clip((1.15 - d) * 12, 0, 1) if cel else np.clip((1.15 - d) * 3, 0, 1)) * (1 - np.clip((t - 0.55) * 2.2, 0, 1) * (0.3 + 0.7 * noise))
        # anneau intérieur qui se creuse en fin d'explosion
        a *= np.clip(1 - np.clip(t - 0.6, 0, 1) * 2.5 * np.clip(1 - d * 1.4, 0, 1), 0, 1)
        save(col, a, f'{name}_{f}')


def shockwave(n=128, name='shockwave', stops=None):
    stops = stops or FIRE
    r, th = polar(n)
    noise = fbm(n, 900, 4, 4)
    band = np.exp(-((r - 0.82) / 0.07) ** 2) + 0.35 * np.exp(-((r - 0.7) / 0.12) ** 2) * noise
    a = np.clip(band, 0, 1) * np.clip((1 - r) * 12, 0, 1)
    col = ramp(1 - np.clip(band, 0, 1) * 0.8 + 0.25, stops)
    save(col, a, name)


def magic_circle(n=128, name='circle_fire', stops=FIRE):
    """Cercle runique : anneaux, runes, étoile à 6 branches ; dessiné en 4x puis réduit (anti-crénelage)."""
    from PIL import ImageDraw
    S = n * 4
    m = Image.new('L', (S, S), 0); d = ImageDraw.Draw(m)
    c = S / 2

    def ring(rad, w, v=255):
        d.ellipse([c - rad, c - rad, c + rad, c + rad], outline=v, width=w)

    ring(S * 0.48, 10); ring(S * 0.445, 4); ring(S * 0.33, 7); ring(S * 0.15, 5)
    # runes entre les deux anneaux extérieurs
    rr = np.random.default_rng(42)
    for k in range(18):
        a0 = k / 18 * 2 * math.pi
        x0, y0 = c + math.cos(a0) * S * 0.395, c + math.sin(a0) * S * 0.395
        for _ in range(3):
            p = [(x0 + rr.uniform(-1, 1) * S * 0.025, y0 + rr.uniform(-1, 1) * S * 0.025) for _ in range(2)]
            d.line(p, fill=255, width=6)
    # étoile à 6 branches (deux triangles)
    for off in (0, math.pi / 3):
        pts = [(c + math.cos(off + i * 2 * math.pi / 3 - math.pi / 2) * S * 0.33,
                c + math.sin(off + i * 2 * math.pi / 3 - math.pi / 2) * S * 0.33) for i in range(3)]
        d.polygon(pts, outline=255, width=6)
    # petits cercles aux pointes
    for i in range(6):
        a0 = i * math.pi / 3 - math.pi / 2
        x0, y0 = c + math.cos(a0) * S * 0.33, c + math.sin(a0) * S * 0.33
        d.ellipse([x0 - 18, y0 - 18, x0 + 18, y0 + 18], outline=255, width=5)
    lines = np.asarray(m.resize((n, n), Image.LANCZOS), dtype=float) / 255
    # halo doux autour des traits
    from PIL import ImageFilter
    halo = np.asarray(m.resize((n, n), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3)), dtype=float) / 255
    r, _ = polar(n)
    a = np.clip(lines + halo * 0.8, 0, 1) * np.clip((1 - r) * 20, 0, 1)
    col = ramp(0.55 - lines * 0.5 - halo * 0.1, stops)
    save(col, a, name)


ARCANE = [(0, (255, 245, 255)), (0.2, (245, 180, 255)), (0.45, (190, 90, 255)), (0.7, (110, 40, 210)), (0.88, (60, 20, 130)), (1, (25, 8, 60))]
FROST = [(0, (255, 255, 255)), (0.2, (210, 245, 255)), (0.45, (120, 210, 255)), (0.7, (50, 140, 230)), (0.88, (25, 70, 160)), (1, (10, 25, 70))]
STORM = [(0, (255, 255, 255)), (0.25, (220, 240, 255)), (0.5, (130, 190, 255)), (0.75, (70, 110, 255)), (1, (30, 30, 120))]


def star(name, n, stops, points=4, sharp=3.0):
    """étincelle en étoile (branches fines) + coeur rond"""
    r, th = polar(n)
    arms = np.abs(np.cos(th * points / 2)) ** (sharp * 6)
    a = np.clip(np.clip(1 - r, 0, 1) ** 2 * (0.25 + 0.75 * arms) * 1.6 + np.clip(1 - r * 3, 0, 1), 0, 1)
    col = ramp(r * 0.9, stops)
    save(col, a, name)


def frost_core(frames=6, n=64):
    """orbe de glace : coeur lumineux et 6 pointes cristallines qui tournent doucement"""
    r, th = polar(n)
    for f in range(frames):
        ph = f / frames * math.pi / 3
        noise = fbm(n, 500 + f, 4, 3)
        spikes = np.abs(np.cos((th + ph) * 3)) ** 8
        edge = 0.42 + 0.48 * spikes + 0.06 * (noise - 0.5)
        d = r / edge
        a = np.clip((1.1 - d) * 3, 0, 1)
        facet = 0.5 + 0.5 * np.sign(np.sin((th + ph) * 6))          # facettes claires/foncées
        col = ramp(d * 0.8 + facet * 0.12 + (noise - 0.5) * 0.15, FROST)
        save(col, a, f'frost_core_{f}')


def snowflake(name='snowflake', n=32):
    from PIL import ImageDraw, ImageFilter
    S = n * 4; m = Image.new('L', (S, S), 0); d = ImageDraw.Draw(m); c = S / 2
    for i in range(6):
        a0 = i * math.pi / 3
        x1, y1 = c + math.cos(a0) * S * 0.45, c + math.sin(a0) * S * 0.45
        d.line([(c, c), (x1, y1)], fill=255, width=7)
        for k in (0.5, 0.75):
            bx, by = c + math.cos(a0) * S * 0.45 * k, c + math.sin(a0) * S * 0.45 * k
            for sgn in (-1, 1):
                d.line([(bx, by), (bx + math.cos(a0 + sgn * 0.8) * S * 0.12, by + math.sin(a0 + sgn * 0.8) * S * 0.12)], fill=255, width=5)
    lines = np.asarray(m.resize((n, n), Image.LANCZOS), dtype=float) / 255
    halo = np.asarray(m.resize((n, n), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5)), dtype=float) / 255
    a = np.clip(lines + halo * 0.7, 0, 1)
    col = ramp(0.35 - lines * 0.35, FROST)
    save(col, a, name)


def shards(frames=6, n=128):
    """éclats de glace qui volent en étoile puis s'estompent"""
    from PIL import ImageDraw
    rr = np.random.default_rng(77)
    dirs = [(rr.uniform(0, 2 * math.pi), rr.uniform(0.6, 1.0), rr.uniform(0.05, 0.1)) for _ in range(14)]
    for f in range(frames):
        t = (f + 1) / frames
        S = n * 4; m = Image.new('L', (S, S), 0); d = ImageDraw.Draw(m); c = S / 2
        for ang, sp, w in dirs:
            dist = S * 0.45 * sp * (0.25 + 0.75 * t ** 0.6)
            tip = (c + math.cos(ang) * dist, c + math.sin(ang) * dist)
            back = (c + math.cos(ang) * dist * 0.55, c + math.sin(ang) * dist * 0.55)
            side = (math.cos(ang + math.pi / 2) * S * w * 0.5, math.sin(ang + math.pi / 2) * S * w * 0.5)
            mid = ((tip[0] + back[0]) / 2, (tip[1] + back[1]) / 2)
            d.polygon([tip, (mid[0] + side[0], mid[1] + side[1]), back, (mid[0] - side[0], mid[1] - side[1])], fill=255)
        lines = np.asarray(m.resize((n, n), Image.LANCZOS), dtype=float) / 255
        r, _ = polar(n)
        flash = np.clip(1 - r / (0.5 * (1 - t) + 0.05), 0, 1) ** 2
        a = np.clip(lines * (1.15 - t * 0.6) + flash * (1 - t), 0, 1)
        col = ramp(0.3 + r * 0.4 - flash * 0.3, FROST)
        save(col, a, f'shards_{f}')


def bolt(frames=4, w=128, h=32):
    """éclair horizontal (à étirer entre deux points) : coeur blanc, halo bleu, branches"""
    from PIL import ImageDraw, ImageFilter
    for f in range(frames):
        rr = np.random.default_rng(600 + f)
        S = 4; m = Image.new('L', (w * S, h * S), 0); d = ImageDraw.Draw(m)
        def path(x0, y0, x1, y1, amp, steps):
            pts = [(x0, y0)]
            for i in range(1, steps):
                k = i / steps
                pts.append((x0 + (x1 - x0) * k, y0 + (y1 - y0) * k + rr.uniform(-amp, amp)))
            pts.append((x1, y1)); return pts
        main = path(0, h * S / 2, w * S, h * S / 2, h * S * 0.32, 14)
        d.line(main, fill=255, width=7, joint='curve')
        for _ in range(3):
            i = rr.integers(2, 11); x, y = main[i]
            br = path(x, y, x + rr.uniform(40, 120) * S / 4 * 2, y + rr.choice([-1, 1]) * rr.uniform(10, 14) * S, 10, 5)
            d.line(br, fill=170, width=4)
        core = np.asarray(m.resize((w, h), Image.LANCZOS), dtype=float) / 255
        halo = np.asarray(m.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3)), dtype=float) / 255
        a = np.clip(core * 1.2 + halo * 1.3, 0, 1)
        col = ramp(0.6 - core * 0.6 - halo * 0.15, STORM)
        rgba = np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)
        rgba[a < 1 / 255] = 0
        full = os.path.join(ROOT, 'textures', 'item', 'vfx', f'bolt_{f}.png')
        Image.fromarray(rgba, 'RGBA').save(full)


# ---------- style animé ----------
def grid(cu, cv, seed):
    return np.random.default_rng(seed).random((cv, cu))

def sample(g, u, v):
    """bruit lisse périodique : g grille (cv, cu), u et v en cellules"""
    cv, cu = g.shape
    i = np.floor(u).astype(int); j = np.floor(v).astype(int); fu = u - i; fv = v - j
    fu = fu * fu * (3 - 2 * fu); fv = fv * fv * (3 - 2 * fv)
    i0, i1 = i % cu, (i + 1) % cu; j0, j1 = j % cv, (j + 1) % cv
    a = g[j0, i0] * (1 - fu) + g[j0, i1] * fu; b = g[j1, i0] * (1 - fu) + g[j1, i1] * fu
    return a * (1 - fv) + b * fv

def anime_core(name, bands, frames=8, n=96, seed=1):
    """boule de feu façon animé : boule ronde coiffée de langues de flamme courbes qui ondulent
    (mouvement périodique, donc la boucle de 8 images est fluide), aplats de couleur nets"""
    rr = np.random.default_rng(seed)
    # langues : angle de base (autour du haut), largeur, hauteur, phase, sens d'ondulation
    tongues = []
    for k in range(5):
        base = math.pi / 2 + (k - 2) * 0.36 + rr.uniform(-0.08, 0.08)
        tongues.append((base, rr.uniform(0.3, 0.42), rr.uniform(0.4, 0.65) * (1.2 - abs(k - 2) * 0.22),
                        rr.uniform(0, 2 * math.pi), rr.choice([1, 2])))
    y, x = np.mgrid[0:n, 0:n] + 0.5
    x = (x - n / 2) / (n / 2); y = -(y - n * 0.62) / (n / 2)
    r = np.sqrt(x * x + y * y); th = np.arctan2(y, x)
    BASE = 0.36
    for f in range(frames):
        t = f / frames * 2 * math.pi
        R = BASE + 0.025 * np.sin(th * 5 + t)
        for (a0, w, h, ph, sp) in tongues:
            hh = h * (0.75 + 0.25 * math.sin(t * sp + ph))
            bend = 0.35 * math.sin(t + ph)                          # la pointe ondule d'un côté à l'autre
            ang = th - a0 - bend * np.clip(r - BASE, 0, 1) * 2
            ang = (ang + math.pi) % (2 * math.pi) - math.pi
            prof = np.clip(1 - np.abs(ang) / w, 0, 1) ** 1.25        # profil pointu
            R = np.maximum(R, BASE + hh * prof)
        heat = r / R
        swirl = np.sin(th * 2 + r * 10 - t)
        heat = heat + swirl * 0.06 * np.clip(1 - heat, 0, 1)
        rgb = np.zeros((n, n, 3)); a = np.zeros((n, n))
        for lim, col in bands:
            m = heat < lim; rgb[m] = col; a[m] = 1
        edge = np.clip((bands[0][0] - heat) * 10, 0, 1)
        save(rgb, a * edge, f'{name}_{f}')

FIRE_BANDS = [(1.0, (140, 22, 14)), (0.93, (232, 66, 20)), (0.74, (255, 146, 32)), (0.52, (255, 218, 80)), (0.3, (255, 253, 232))]

# ---------- modèles ----------
def quad_model(tex):
    face = {'uv': [0, 0, 16, 16], 'texture': '#s'}
    return {
        'textures': {'s': f'evo:item/vfx/{tex}', 'particle': f'evo:item/vfx/{tex}'},
        'elements': [{'from': [0, 0, 8], 'to': [16, 16, 8], 'shade': False, 'light_emission': 15,
                      'faces': {'north': face, 'south': dict(face, uv=[16, 0, 0, 16])}}],
        'display': {}}


def write_models():
    texdir = os.path.join(ROOT, 'textures', 'item', 'vfx')
    ids = sorted(f[:-4] for f in os.listdir(texdir) if f.endswith('.png'))
    for i in ids:
        mp = os.path.join(ROOT, 'models', 'item', 'vfx', i + '.json')
        ip = os.path.join(ROOT, 'items', 'vfx', i + '.json')
        os.makedirs(os.path.dirname(mp), exist_ok=True); os.makedirs(os.path.dirname(ip), exist_ok=True)
        json.dump(quad_model(i), open(mp, 'w'), indent=1)
        json.dump({'model': {'type': 'minecraft:model', 'model': f'evo:item/vfx/{i}'}}, open(ip, 'w'), indent=1)
    return ids


if __name__ == '__main__':
    anime_core('fire_core', FIRE_BANDS, 8, 96, 3); ember(); explosion(cel=True); shockwave(); magic_circle()
    glow('glow_fire', 64, (255, 140, 40))
    glow('smoke', 64, (70, 62, 60), power=1.4, maxa=0.6)
    # arcane (Trait arcanique, Transfert)
    fire_core(6, 64, 'arcane_core', ARCANE, 700); star('spark_arcane', 32, ARCANE)
    explosion(6, 96, 'burst_arcane', ARCANE, False, 720); magic_circle(128, 'circle_arcane', ARCANE)
    shockwave(128, 'shockwave_arcane', ARCANE); glow('glow_arcane', 64, (190, 90, 255))
    # givre (Éclair de givre, Nova de glace)
    frost_core(); snowflake(); shards(); magic_circle(128, 'circle_frost', FROST)
    shockwave(128, 'shockwave_frost', FROST); glow('glow_frost', 64, (120, 200, 255)); glow('mist_frost', 64, (200, 230, 255), 1.4, 0.45)
    # foudre (Chaîne d'éclairs)
    bolt(); glow('glow_storm', 64, (140, 180, 255)); star('spark_storm', 32, STORM)
    print(' '.join(write_models()))
