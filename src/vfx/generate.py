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


def magic_circle(n=128, name='circle_fire', stops=FIRE, tone=None):
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
    col = ramp(0.55 - lines * 0.5 - halo * 0.1, stops) if tone is None else ramp(tone + (1 - lines) * 0.35, stops)
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

# ---------- style animé : autres éléments ----------
def cel(heat, bands, aa=10):
    """aplats nets : bands = [(seuil, couleur), ...] du bord vers le coeur (seuils décroissants)"""
    n = heat.shape
    rgb = np.zeros(n + (3,)); a = np.zeros(n)
    for lim, col in bands:
        m = heat < lim; rgb[m] = col; a[m] = 1
    return rgb, a * np.clip((bands[0][0] - heat) * aa, 0, 1)


ARCANE_BANDS = [(1.0, (70, 20, 140)), (0.9, (150, 60, 235)), (0.68, (215, 130, 255)), (0.42, (250, 215, 255)), (0.22, (255, 255, 255))]
FROST_BANDS = [(1.0, (25, 70, 150)), (0.9, (60, 150, 235)), (0.68, (140, 215, 255)), (0.42, (220, 248, 255)), (0.2, (255, 255, 255))]
STORM_BANDS = [(1.0, (40, 50, 170)), (0.82, (90, 140, 255)), (0.5, (190, 225, 255)), (0.28, (255, 255, 255))]


def arcane_orb(frames=6, n=64):
    """orbe arcanique : boule ronde + 4 pointes d'étoile qui tournent"""
    r, th = polar(n)
    for f in range(frames):
        ph = f / frames * math.pi / 2
        R = 0.4 + 0.5 * np.abs(np.cos(2 * (th - ph))) ** 10 + 0.2 * np.abs(np.cos(2 * (th - ph) + math.pi / 2)) ** 10
        heat = r / R + 0.05 * np.sin(th * 3 + r * 12 - f)
        save(*cel(heat, ARCANE_BANDS), f'arcane_core_{f}')


def cel_star(name, bands, n=32, points=4):
    r, th = polar(n)
    R = 0.28 + 0.68 * np.abs(np.cos(th * points / 2)) ** 6
    save(*cel(r / R, bands), name)


def cel_burst(name, bands, frames=6, n=96, points=8, seed=0):
    """éclatement : anneau en étoile qui s'ouvre et s'amincit"""
    r, th = polar(n)
    rr = np.random.default_rng(seed); lens = rr.uniform(0.6, 1.0, points)
    for f in range(frames):
        t = (f + 1) / frames
        k = (th / (2 * math.pi) % 1) * points; i = k.astype(int) % points; fr = k - np.floor(k)
        spike = lens[i] * np.abs(np.sin(fr * math.pi)) ** 4
        outer = 0.35 + 0.6 * t ** 0.7 + 0.25 * spike * (1 - t * 0.4)
        inner = outer * (0.2 + 0.75 * t ** 1.2)
        band = (r - inner) / np.maximum(outer - inner, 1e-3)              # 0 au bord intérieur, 1 au bord extérieur
        heat = np.where(r < inner, 2.0, np.abs(band - 0.45) * 2.0)
        rgb, a = cel(heat, bands)
        save(rgb, a, f'{name}_{f}')


def cel_ring(name, bands, n=128, width=0.1):
    r, _ = polar(n)
    heat = np.abs(r - 0.82) / width
    save(*cel(heat, bands, 6), name)


def frost_crystal(frames=6, n=64):
    """cristal de givre : 6 pointes, facettes claires/sombres en aplats"""
    r, th = polar(n)
    for f in range(frames):
        ph = f / frames * math.pi / 3
        R = 0.32 + 0.62 * np.abs(np.cos(3 * (th - ph))) ** 6
        facet = (np.floor((th - ph) / (math.pi / 6)) % 2) * 0.16
        heat = r / R + facet
        save(*cel(heat, FROST_BANDS), f'frost_core_{f}')


def ice_spike(n=64):
    """pic de glace vertical (à afficher en VERTICAL), sort du sol"""
    y, x = np.mgrid[0:n, 0:n] + 0.5
    x = (x - n / 2) / (n / 2); y = (n - y) / n                               # y : 0 en bas, 1 en haut
    width = 0.42 * (1 - y) ** 0.9
    heat = np.abs(x) / np.maximum(width, 1e-3)
    heat = heat + (x > 0.02) * 0.25                                          # face droite plus sombre
    heat = np.where(y > 0.97, 2, heat)
    save(*cel(heat, FROST_BANDS), 'ice_spike')


def cel_bolt(frames=4, w=128, h=32):
    """éclair : coeur blanc net, bord bleu net, quelques branches"""
    from PIL import ImageDraw
    for f in range(frames):
        rr = np.random.default_rng(600 + f)
        S = 4; core = Image.new('L', (w * S, h * S), 0); d = ImageDraw.Draw(core)
        def path(x0, y0, x1, y1, amp, steps):
            pts = [(x0, y0)]
            for i in range(1, steps):
                k = i / steps
                pts.append((x0 + (x1 - x0) * k, y0 + (y1 - y0) * k + rr.uniform(-amp, amp)))
            pts.append((x1, y1)); return pts
        main = path(0, h * S / 2, w * S, h * S / 2, h * S * 0.3, 12)
        branches = []
        for _ in range(3):
            i = int(rr.integers(2, 10)); x, y = main[i]
            branches.append(path(x, y, x + rr.uniform(60, 160), y + rr.choice([-1, 1]) * rr.uniform(30, 52), 12, 4))
        outer = Image.new('L', (w * S, h * S), 0); o = ImageDraw.Draw(outer)
        o.line(main, fill=255, width=26, joint='curve'); [o.line(b, fill=255, width=14) for b in branches]
        d.line(main, fill=255, width=9, joint='curve'); [d.line(b, fill=255, width=5) for b in branches]
        cm = np.asarray(core.resize((w, h), Image.LANCZOS), dtype=float) / 255
        om = np.asarray(outer.resize((w, h), Image.LANCZOS), dtype=float) / 255
        rgb = np.zeros((h, w, 3)); rgb[:] = STORM_BANDS[1][1]
        rgb[cm > 0.5] = (255, 255, 255)
        rgb[(cm <= 0.5) & (cm > 0.12)] = STORM_BANDS[2][1]
        a = np.clip(om * 1.6, 0, 1)
        rgba = np.dstack([rgb, a * 255]).astype(np.uint8); rgba[a < 1 / 255] = 0
        Image.fromarray(rgba, 'RGBA').save(os.path.join(ROOT, 'textures', 'item', 'vfx', f'bolt_{f}.png'))



# ---------- Guerrier : acier, sang, rage, poussière ----------
STEEL_BANDS = [(1.0, (70, 90, 140)), (0.85, (150, 190, 240)), (0.55, (225, 240, 255)), (0.28, (255, 255, 255))]
BLOOD_BANDS = [(1.0, (70, 0, 10)), (0.85, (170, 10, 25)), (0.55, (235, 50, 45)), (0.28, (255, 205, 195))]
RAGE_BANDS = [(1.0, (90, 0, 10)), (0.9, (200, 20, 20)), (0.7, (255, 90, 30)), (0.45, (255, 190, 80)), (0.25, (255, 245, 210))]
DUST_BANDS = [(1.0, (95, 72, 52)), (0.8, (150, 120, 88)), (0.5, (196, 170, 132)), (0.25, (226, 208, 176))]
ROCK_BANDS = [(1.0, (45, 40, 36)), (0.85, (95, 86, 78)), (0.5, (138, 126, 114))]
WIND_BANDS = [(1.0, (150, 190, 230)), (0.7, (225, 240, 255)), (0.35, (255, 255, 255))]
WAR = [(0, (255, 250, 220)), (0.2, (255, 200, 90)), (0.45, (255, 110, 30)), (0.7, (210, 30, 20)), (0.88, (120, 10, 10)), (1, (50, 5, 5))]


def slash(name, bands, frames=6, n=128, span=1.0):
    """tranchant en croissant : la lame balaie (l'arc s'allonge), puis la traîne s'efface en s'amincissant"""
    r, th = polar(n)
    L = [0.7, 1.7, 2.6, 3.0, 3.0, 3.0]          # longueur de l'arc (rad)
    K = [0.75, 1.0, 1.0, 0.8, 0.55, 0.32]        # épaisseur
    C = [1.0, 1.0, 1.0, 0.72, 0.5, 0.32]         # part de l'arc encore visible (la queue disparaît)
    for f in range(frames):
        s = ((0.6 - th) % (2 * math.pi)) / (L[f] * span)  # 0 à la pointe, 1 au bout de la traîne
        rc = 0.74 + 0.04 * f / frames
        w = 0.28 * K[f] * np.sqrt(np.clip(s / 0.07, 0, 1)) * np.clip(1 - s / C[f], 0, 1) ** 0.9
        heat = np.where((s <= C[f]) & (w > 1e-3), np.abs(r - rc) / np.maximum(w, 1e-3), 2.0)
        save(*cel(heat, bands, 6), f'{name}_{f}')


def cross_slash(name, bands, frames=6, n=128):
    """deux entailles en X : la première trace, puis la seconde, puis les deux s'amincissent"""
    y, x = np.mgrid[0:n, 0:n] + 0.5
    x = (x - n / 2) / (n / 2); y = (y - n / 2) / (n / 2)
    def stroke(u, d, prog, k):
        w = 0.13 * k * np.clip(1 - u * u, 0, 1) ** 0.6
        vis = u <= -1 + 2 * prog
        return np.where(vis & (w > 1e-3), np.abs(d) / np.maximum(w, 1e-3), 2.0)
    for f in range(frames):
        pa = min(1, (f + 1) / 2.5); pb = min(1, max(0, (f - 1.5) / 2)); k = 1.0 if f < 4 else (0.6 if f == 4 else 0.3)
        h1 = stroke((x + y) / 1.35, (x - y) / 1.414, pa, k)
        h2 = stroke((x - y) / 1.35, (x + y) / 1.414, pb, k) if pb > 0 else 2.0
        save(*cel(np.minimum(h1, h2), bands, 6), f'{name}_{f}')


def dust(name='dust', n=64, seed=21):
    r, th = polar(n)
    R = 0.72 + 0.16 * angular(th, seed, kmin=3, kmax=7)
    shade = 0.18 * (np.mgrid[0:n, 0:n][0] / n - 0.4)                # bas du nuage plus sombre
    save(*cel(r / R + shade + 0.08 * (fbm(n, seed) - 0.5), DUST_BANDS), name)


def rock(name='rock', n=32, seed=33):
    r, th = polar(n)
    R = 0.62 + 0.22 * angular(th, seed, kmin=2, kmax=5)
    facet = (np.floor((th + 0.4) / (math.pi / 3)) % 2) * 0.22
    save(*cel(r / R + facet, ROCK_BANDS), name)


def cracks(name='cracks', n=128, seed=44):
    """fissures au sol (vue de dessus) : crevasses sombres bordées de terre claire"""
    from PIL import ImageDraw
    rr = np.random.default_rng(seed); S = 4; N = n * S
    inner = Image.new('L', (N, N), 0); outer = Image.new('L', (N, N), 0)
    di, do = ImageDraw.Draw(inner), ImageDraw.Draw(outer)
    def branch(x, y, ang, length, width, depth):
        pts = [(x, y)]
        for i in range(6):
            ang += rr.uniform(-0.45, 0.45); x += math.cos(ang) * length / 6; y += math.sin(ang) * length / 6; pts.append((x, y))
            if depth < 2 and rr.random() < 0.3:
                branch(x, y, ang + rr.choice([-1, 1]) * rr.uniform(0.5, 1.0), length * 0.45, width * 0.6, depth + 1)
        do.line(pts, fill=255, width=int(width * 2.4), joint='curve'); di.line(pts, fill=255, width=int(width), joint='curve')
    for k in range(9):
        a = k / 9 * 2 * math.pi + rr.uniform(-0.2, 0.2)
        branch(N / 2 + math.cos(a) * N * 0.05, N / 2 + math.sin(a) * N * 0.05, a, N * rr.uniform(0.34, 0.45), 18, 0)
    di.ellipse([N / 2 - N * 0.07, N / 2 - N * 0.07, N / 2 + N * 0.07, N / 2 + N * 0.07], fill=255)
    do.ellipse([N / 2 - N * 0.12, N / 2 - N * 0.12, N / 2 + N * 0.12, N / 2 + N * 0.12], fill=255)
    im = np.asarray(inner.resize((n, n), Image.LANCZOS), dtype=float) / 255
    om = np.asarray(outer.resize((n, n), Image.LANCZOS), dtype=float) / 255
    rgb = np.zeros((n, n, 3)); rgb[:] = (150, 118, 84)
    rgb[im > 0.45] = (38, 24, 16)
    rgb[(im > 0.15) & (im <= 0.45)] = (90, 62, 40)
    save(rgb, np.clip(om * 1.8, 0, 1), name)


def aura(name, bands, frames=8, n=96, seed=5):
    """aura de rage : contour de flammes autour du corps, centre vide (le joueur reste visible)"""
    rr = np.random.default_rng(seed)
    tongues = [(math.pi / 2 + (k - 3.5) * 0.42 + rr.uniform(-0.08, 0.08), rr.uniform(0.25, 0.34),
                rr.uniform(0.25, 0.42) * (1.15 - abs(k - 3.5) * 0.12), rr.uniform(0, 6.3), rr.choice([1, 2])) for k in range(8)]
    r, th = polar(n)
    for f in range(frames):
        t = f / frames * 2 * math.pi
        R = 0.52 + 0.03 * np.sin(th * 6 + t)
        for (a0, w, h, ph, sp) in tongues:
            hh = h * (0.7 + 0.3 * math.sin(t * sp + ph))
            ang = th - a0 - 0.3 * math.sin(t + ph) * np.clip(r - 0.5, 0, 1) * 2
            ang = (ang + math.pi) % (2 * math.pi) - math.pi
            R = np.maximum(R, 0.52 + hh * np.clip(1 - np.abs(ang) / w, 0, 1) ** 1.3)
        x = (r / R - 0.66) / 0.34                                   # 0 bord intérieur, 1 bord extérieur
        heat = np.where(x < 0, 2.0, x * 1.0 + 0.04 * np.sin(th * 9 - t * 2))
        rgb, a = cel(heat, bands, 8)
        a = a * np.clip(x * 6, 0, 1)                                 # bord intérieur adouci
        save(rgb, a, f'{name}_{f}')


def blood(name='blood', n=32):
    y, x = np.mgrid[0:n, 0:n] + 0.5
    x = (x - n / 2) / (n / 2); y = -(y - n / 2) / (n / 2)
    circ = np.sqrt(x * x + (y + 0.3) ** 2) / 0.5
    w = 0.5 * np.clip((0.85 - y) / 1.15, 0, 1) ** 1.3
    tri = np.where((y > -0.3) & (y < 0.85), np.abs(x) / np.maximum(w, 1e-3), 2.0)
    heat = np.minimum(circ, tri) + (x > 0.08) * 0.2
    save(*cel(heat, BLOOD_BANDS), name)


def speed_line(name='speed_line', w=128, h=16):
    y, x = np.mgrid[0:h, 0:w] + 0.5
    u = x / w; v = (y - h / 2) / (h / 2)
    width = 0.9 * np.sqrt(u) * (1 - u ** 10)
    heat = np.abs(v) / np.maximum(width, 1e-3)
    rgb, a = cel(heat, WIND_BANDS, 4)
    rgba = np.dstack([rgb, a * 255]).astype(np.uint8); rgba[a < 1 / 255] = 0
    Image.fromarray(rgba, 'RGBA').resize((w, w // 8)).save(os.path.join(ROOT, 'textures', 'item', 'vfx', name + '.png'))


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
    arcane_orb(); cel_star('spark_arcane', ARCANE_BANDS); cel_burst('burst_arcane', ARCANE_BANDS, seed=4)
    magic_circle(128, 'circle_arcane', ARCANE, 0.22); cel_ring('shockwave_arcane', ARCANE_BANDS); glow('glow_arcane', 64, (190, 90, 255))
    # givre (Éclair de givre, Nova de glace)
    frost_crystal(); snowflake(); shards(); ice_spike(); cel_burst('burst_frost', FROST_BANDS, points=6, seed=9)
    magic_circle(128, 'circle_frost', FROST, 0.18); cel_ring('shockwave_frost', FROST_BANDS)
    glow('glow_frost', 64, (120, 200, 255)); glow('mist_frost', 64, (200, 230, 255), 1.4, 0.45)
    # foudre (Chaîne d'éclairs)
    cel_bolt(); glow('glow_storm', 64, (140, 180, 255)); cel_star('spark_storm', STORM_BANDS)
    # feu : anneau d'onde en aplats aussi
    cel_ring('shockwave', FIRE_BANDS)
    # guerrier
    slash('slash', STEEL_BANDS); slash('whirl', STEEL_BANDS, span=1.7); slash('slash_red', BLOOD_BANDS); cross_slash('cross_red', BLOOD_BANDS)
    cel_star('spark_steel', STEEL_BANDS); cel_burst('burst_red', BLOOD_BANDS, points=7, seed=12)
    dust(); rock(); cracks(); cel_ring('shockwave_dust', DUST_BANDS); cel_ring('ring_wind', WIND_BANDS); speed_line()
    aura('aura_rage', RAGE_BANDS); blood(); cel_ring('roar_ring', RAGE_BANDS); cel_ring('roar_ring_thin', RAGE_BANDS, 256, 0.035); magic_circle(128, 'circle_war', WAR, 0.2)
    glow('glow_red', 64, (255, 60, 40))
    print(' '.join(write_models()))
