"""Aperçu des modèles d'objets (vue inventaire), pour vérifier le rendu avant de publier le pack."""
import math
from PIL import Image, ImageDraw
from kit import face_frame, FACES


def rot(axis, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return {'x': [[1, 0, 0], [0, c, -s], [0, s, c]],
            'y': [[c, 0, s], [0, 1, 0], [-s, 0, c]],
            'z': [[c, -s, 0], [s, c, 0], [0, 0, 1]]}[axis]


def mul(m, v):
    return [sum(m[i][k] * v[k] for k in range(3)) for i in range(3)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def render(img, elements, display, size=256, view='gui'):
    tr = display.get(view, {})
    r = tr.get('rotation', [0, 0, 0])
    R = mm(mm(rot('x', r[0]), rot('y', r[1])), rot('z', r[2]))
    sc = tr.get('scale', [1, 1, 1])
    t = tr.get('translation', [0, 0, 0])
    W = img.width
    px = img.load()
    quads = []
    light = [-0.4, 0.7, 0.6]
    ln = math.sqrt(sum(v * v for v in light))
    light = [v / ln for v in light]
    for e in elements:
        rz = e.get('rotation')
        Rz = rot(rz.get('axis', 'z'), rz['angle']) if rz else None

        def tf(p):
            p = list(p)
            if Rz:
                o = rz['origin']
                p = [a - b for a, b in zip(p, o)]
                p = mul(Rz, p)
                p = [a + b for a, b in zip(p, o)]
            p = [(p[i] - 8) * sc[i] for i in range(3)]
            p = mul(R, p)
            return [p[i] + t[i] for i in range(3)]

        for f in FACES:
            o, u, v, du, dv = face_frame(f, e['from'], e['to'])
            uv = e['faces'][f]['uv']
            x0, y0, x1, y1 = [round(c * W / 16) for c in uv]
            w, hh = max(1, x1 - x0), max(1, y1 - y0)
            n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
            n = [-c for c in n]
            if Rz:
                n = mul(Rz, n)
            n = mul(R, n)
            if n[2] <= 1e-6:
                continue
            shade = 0.55 + 0.45 * max(0, sum(n[i] * light[i] for i in range(3)))
            glow = e.get('light_emission', 0) / 15
            for ty in range(hh):
                for tx in range(w):
                    c = px[x0 + tx, y0 + ty]
                    if c[3] == 0:
                        continue
                    pts = []
                    for a, b in ((tx, ty), (tx + 1, ty), (tx + 1, ty + 1), (tx, ty + 1)):
                        fu, fv = a / w * du, b / hh * dv
                        pts.append(tf([o[k] + u[k] * fu + v[k] * fv for k in range(3)]))
                    z = sum(p[2] for p in pts) / 4
                    k = shade + (1 - shade) * glow
                    col = tuple(min(255, int(c[i] * k)) for i in range(3))
                    quads.append((z, [(p[0], p[1]) for p in pts], col))
    quads.sort(key=lambda q: q[0])
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    s = size / 16
    for _, pts, col in quads:
        d.polygon([(size / 2 + x * s, size / 2 - y * s) for x, y in pts], fill=col + (255,))
    return out
