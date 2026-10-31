"""Aperçu : chaque cadre rendu en nine-slice (bords répétés) sur une infobulle de 200x90, zoom x3."""
import os
from PIL import Image
D = os.path.join(os.path.dirname(__file__), '..', '..', 'pack', 'assets', 'evo', 'textures', 'gui', 'sprites', 'tooltip')
N, B = 100, 9


def nine(src, w, h):
    out = Image.new('RGBA', (w, h))
    c = N - 2 * B
    def tile(box, dst):
        part = src.crop(box)
        pw, ph = part.size
        x0, y0, x1, y1 = dst
        for y in range(y0, y1, ph):
            for x in range(x0, x1, pw):
                out.paste(part.crop((0, 0, min(pw, x1 - x), min(ph, y1 - y))), (x, y))
    for (sx0, sx1, dx0, dx1) in ((0, B, 0, B), (B, N - B, B, w - B), (N - B, N, w - B, w)):
        for (sy0, sy1, dy0, dy1) in ((0, B, 0, B), (B, N - B, B, h - B), (N - B, N, h - B, h)):
            tile((sx0, sy0, sx1, sy1), (dx0, dy0, dx1, dy1))
    return out


rs = ['commun', 'peu_commun', 'rare', 'epique', 'legendaire']
W, H = 200, 90
sheet = Image.new('RGBA', ((W + 10) * len(rs) + 10, H + 20), (70, 110, 60, 255))
for i, r in enumerate(rs):
    bg = nine(Image.open(f'{D}/{r}_background.png'), W, H)
    fr = nine(Image.open(f'{D}/{r}_frame.png'), W, H)
    t = Image.alpha_composite(bg, fr)
    sheet.alpha_composite(t, (10 + i * (W + 10), 10))
sheet = sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST)
sheet.save(os.path.join(os.path.dirname(__file__), 'apercu.png'))
