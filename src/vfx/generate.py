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
def fire_core(frames=8, n=64):
    r, th = polar(n)
    for f in range(frames):
        ph = f / frames * 2 * math.pi
        noise = fbm(n, 100 + f * 3, 4, 3)
        # langues de flamme qui tournent
        tongues = 0.5 + 0.5 * angular(th + noise * 0.6, 11, ph)
        edge = 0.58 + 0.3 * tongues + 0.14 * (noise - 0.5)
        heat = r / edge
        a = np.clip(1.25 - heat, 0, 1) ** 0.8
        col = ramp(heat * 0.95 + (noise - 0.5) * 0.25, FIRE)
        save(col, a, f'fire_core_{f}')


def glow(name, n, color, power=2.2, maxa=0.55):
    r, _ = polar(n)
    a = np.clip(1 - r, 0, 1) ** power * maxa
    col = np.ones((n, n, 3)) * np.array(color)
    save(col, a, name)


def ember(n=32):
    r, _ = polar(n)
    core = np.clip(1 - r * 2.4, 0, 1)
    a = np.clip(np.clip(1 - r, 0, 1) ** 2.4 + core, 0, 1)
    col = ramp(0.75 - core * 0.75, FIRE)
    save(col, a, 'ember')


def explosion(frames=8, n=128):
    r, th = polar(n)
    for f in range(frames):
        t = (f + 1) / frames
        noise = fbm(n, 300 + f, 5, 3)
        radius = 0.35 + 0.6 * t ** 0.6
        lumps = 0.14 * angular(th + noise * 0.8, 21, t * 2) + 0.28 * (noise - 0.5)
        d = r / (radius * (1 + lumps))
        # coeur brûlant qui refroidit, fumée sur le bord vers la fin
        heat = d * (0.55 + 0.9 * t) + (noise - 0.5) * 0.3
        fire = ramp(heat, FIRE)
        smoke_amt = np.clip((d - 0.55) * 2 + t * 0.9 - 0.5, 0, 1) * np.clip(t * 1.6, 0, 1)
        smoke = ramp(noise, SMOKE)
        col = fire * (1 - smoke_amt[..., None]) + smoke * smoke_amt[..., None]
        a = np.clip((1.15 - d) * 3, 0, 1) * (1 - np.clip((t - 0.55) * 2.2, 0, 1) * (0.3 + 0.7 * noise))
        # anneau intérieur qui se creuse en fin d'explosion
        a *= np.clip(1 - np.clip(t - 0.6, 0, 1) * 2.5 * np.clip(1 - d * 1.4, 0, 1), 0, 1)
        save(col, a, f'explosion_{f}')


def shockwave(n=128):
    r, th = polar(n)
    noise = fbm(n, 900, 4, 4)
    band = np.exp(-((r - 0.82) / 0.07) ** 2) + 0.35 * np.exp(-((r - 0.7) / 0.12) ** 2) * noise
    a = np.clip(band, 0, 1) * np.clip((1 - r) * 12, 0, 1)
    col = ramp(1 - np.clip(band, 0, 1) * 0.8 + 0.25, FIRE)
    save(col, a, 'shockwave')


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
    fire_core(); ember(); explosion(); shockwave(); magic_circle()
    glow('glow_fire', 64, (255, 140, 40))
    glow('smoke', 64, (70, 62, 60), power=1.4, maxa=0.6)
    print(' '.join(write_models()))
