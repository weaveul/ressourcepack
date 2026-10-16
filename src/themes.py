# Décors thématiques des menus Evo Extract (pixel art généré). Coordonnées : repère de l'inventaire vanilla.
import random, math
from PIL import Image, ImageDraw
S=12; M=26; W=176+2*S
def C(h,a=255): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(a,)
def mix(c1,c2,t): return tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3))+(255,)
def jit(c,r,rnd): return tuple(max(0,min(255,c[i]+rnd.randint(-r,r))) for i in range(3))+(255,)
def rect(d,x0,y0,x1,y1,c): d.rectangle([x0,y0,x1,y1],fill=c)
def bevel(d,x0,y0,x1,y1,fill,hl,sh,o=None):
    if o: rect(d,x0-1,y0-1,x1+1,y1+1,o)
    rect(d,x0,y0,x1,y1,fill); d.line([x0,y0,x1,y0],fill=hl); d.line([x0,y0,x0,y1],fill=hl)
    d.line([x0,y1,x1,y1],fill=sh); d.line([x1,y0,x1,y1],fill=sh)
GOLD=C('f2b43a'); GOLDD=C('b97a1c'); GOLDL=C('ffe08a')
PURP=C('8e5bd6'); PURPD=C('6a3cb0'); PURPL=C('b58cf0')
LEAF=C('4f9a3a'); LEAFD=C('2f6b25'); LEAFL=C('7cc24f')
WOOD=C('6b4226'); WOOD2=C('7d4f2c'); WOODD=C('4a2c18'); WOODL=C('94643a')
IRON=C('8a8f98'); IROND=C('5a5f68')
DARK=C('2e2e38')

# ---------- murs ----------
def wall_bricks(d,x0,y0,x1,y1,rnd,stones,mortar,hl,sh,bw=16,bh=8):
    rect(d,x0,y0,x1,y1,mortar); row=0
    for y in range(y0,y1+1,bh):
        off=(bw//2 if row%2 else 0); row+=1
        for x in range(x0-off,x1+1,bw):
            a,b=max(x,x0),min(x+bw-2,x1); c,e=y,min(y+bh-2,y1)
            if a>b or c>e: continue
            col=rnd.choice(stones); rect(d,a,c,b,e,col)
            if rnd.random()<.7: d.line([a,c,b,c],fill=hl)
            d.line([a,e,b,e],fill=sh)
def wall_planks(d,x0,y0,x1,y1,rnd,cols,dark,pw=10,vertical=True):
    if vertical:
        for x in range(x0,x1+1,pw):
            col=rnd.choice(cols); rect(d,x,y0,min(x+pw-2,x1),y1,col); d.line([min(x+pw-1,x1),y0,min(x+pw-1,x1),y1],fill=dark)
            for _ in range((y1-y0)//10):
                yy=rnd.randint(y0,y1); d.line([x+1,yy,min(x+pw-3,x1),yy],fill=jit(col,12,rnd))
            for yy in (y0+3,y1-3): d.point((x+pw//2-1,yy),fill=IROND)
    else:
        for y in range(y0,y1+1,pw):
            col=rnd.choice(cols); rect(d,x0,y,x1,min(y+pw-2,y1),col); d.line([x0,min(y+pw-1,y1),x1,min(y+pw-1,y1)],fill=dark)
def wall_noise(d,x0,y0,x1,y1,rnd,base,var,speck=None,n=0):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): d.point((x,y),fill=jit(base,var,rnd))
    for _ in range(n):
        x,y=rnd.randint(x0,x1),rnd.randint(y0,y1); d.point((x,y),fill=rnd.choice(speck))
def wall_parchment(img,d,x0,y0,x1,y1,rnd):
    base=C('e3cf9f')
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            e=min(x-x0,x1-x,y-y0,y1-y); t=max(0,1-e/10)
            d.point((x,y),fill=jit(mix(base,C('a07a43'),t*0.75),6,rnd))
    # dessins à l'encre : chemin pointillé, montagnes, arbres
    ink=C('6b4a2a')
    pts=[(x0+10,y1-12),(x0+40,y1-30),(x0+80,y1-20),(x0+120,y1-40),(x1-12,y0+20)]
    for (ax,ay),(bx,by) in zip(pts,pts[1:]):
        n=int(math.hypot(bx-ax,by-ay)/3)
        for i in range(0,n,2): d.point((int(ax+(bx-ax)*i/n),int(ay+(by-ay)*i/n)),fill=ink)
    for _ in range(4):
        mx,my=rnd.randint(x0+15,x1-15),rnd.randint(y0+20,y1-10)
        d.line([mx-4,my,mx,my-5,mx+4,my],fill=ink)
    d.line([x1-14,y1-14,x1-14,y1-24],fill=ink); d.line([x1-19,y1-19,x1-9,y1-19],fill=ink)  # rose des vents
    d.point((x1-14,y1-26),fill=C('8e2a1e'))
def wall_stars(d,x0,y0,x1,y1,rnd):
    for y in range(y0,y1+1):
        t=(y-y0)/max(1,y1-y0)
        for x in range(x0,x1+1): d.point((x,y),fill=jit(mix(C('1b1638'),C('3a1f5c'),t),4,rnd))
    for _ in range((x1-x0)*(y1-y0)//40):
        x,y=rnd.randint(x0,x1),rnd.randint(y0,y1); d.point((x,y),fill=rnd.choice([C('ffffff'),C('cdb8ff'),C('8fb4ff'),C('fff3b0')]))
    for _ in range(5):
        x,y=rnd.randint(x0+3,x1-3),rnd.randint(y0+3,y1-3)
        for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): d.point((x+dx,y+dy),fill=C('fff3b0') if (dx,dy)==(0,0) else C('cdb8ff'))
def wall_water(d,x0,y0,x1,y1,rnd):
    for y in range(y0,y1+1):
        t=(y-y0)/max(1,y1-y0)
        for x in range(x0,x1+1): d.point((x,y),fill=jit(mix(C('3f88c5'),C('1f4f7d'),t),5,rnd))
    for y in range(y0+6,y1,9):
        for x in range(x0,x1,12):
            xo=x+((y//9)%2)*6
            d.line([xo,y,xo+3,y-1,xo+6,y],fill=C('8cc6ef'))
def wall_cave(d,x0,y0,x1,y1,rnd):
    wall_noise(d,x0,y0,x1,y1,rnd,C('4a4650'),10)
    for _ in range(18):
        x,y=rnd.randint(x0+2,x1-6),rnd.randint(y0+2,y1-6); r=rnd.randint(2,5)
        d.ellipse([x,y,x+r,y+r-1],fill=jit(C('5b5763'),8,rnd))
    for col,n in ((C('5ce1e6'),6),(C('f5c542'),7),(C('d63b2f'),6),(C('2fa84f'),3)):
        for _ in range(n):
            x,y=rnd.randint(x0+2,x1-3),rnd.randint(y0+2,y1-3)
            for dx,dy in ((0,0),(1,0),(0,1),(1,1)):
                if rnd.random()<.8: d.point((x+dx,y+dy),fill=col)
def wall_forest(d,x0,y0,x1,y1,rnd):
    # écorce verticale
    for x in range(x0,x1+1):
        base=mix(C('5a3d24'),C('6e4a2b'),(math.sin(x*0.7)+1)/2)
        for y in range(y0,y1+1): d.point((x,y),fill=jit(base,6,rnd))
    for _ in range(40):
        x=rnd.randint(x0,x1); y=rnd.randint(y0,y1-6); d.line([x,y,x,y+rnd.randint(3,7)],fill=C('3e2916'))
    for _ in range(14):   # mousse
        x,y=rnd.randint(x0,x1-4),rnd.randint(y0,y1-2)
        for i in range(5): d.point((x+i,y+rnd.randint(-1,1)),fill=rnd.choice([LEAF,LEAFD,LEAFL]))
def wall_redbrick(d,x0,y0,x1,y1,rnd):
    wall_bricks(d,x0,y0,x1,y1,rnd,[C('8a3a2a'),C('9b4330'),C('7d3426'),C('a34a35')],C('3a1e17'),C('b9614a'),C('5e2a1f'),bw=14,bh=7)
    # lueur du feu en bas
    for y in range(y1-14,y1+1):
        t=(y-(y1-14))/14
        for x in range(x0,x1+1):
            if rnd.random()<t*0.5: d.point((x,y),fill=rnd.choice([C('ff8a1f'),C('ffb347'),C('e0521b')]))
def wall_dark_altar(d,x0,y0,x1,y1,rnd):
    wall_bricks(d,x0,y0,x1,y1,rnd,[C('2c2630'),C('342d39'),C('282229')],C('141016'),C('4a3f52'),C('1a151d'))
    runes=['|-|','/\\','<>','+']
    for i in range(7):
        x=x0+12+i*((x1-x0-24)//6); y=y0+6
        d.line([x,y,x+3,y+5],fill=C('d63b2f')); d.line([x+3,y,x,y+5],fill=C('ff5a3c'))

# ---------- décorations ----------
def banner(d,x,y0,y1,c=PURP,cd=PURPD,cl=PURPL):
    rect(d,x-1,y0-2,x+10,y0-1,C('9a9aa8'))
    d.polygon([(x,y0),(x+9,y0),(x+9,y1),(x+4,y1-5),(x,y1)],fill=c)
    d.line([x,y0,x,y1],fill=cd); d.line([x+9,y0,x+9,y1],fill=cd); d.line([x+2,y0,x+2,y1-4],fill=cl); d.line([x,y0+1,x+9,y0+1],fill=GOLD)
    # blason
    d.polygon([(x+3,y0+8),(x+7,y0+8),(x+7,y0+12),(x+5,y0+14),(x+3,y0+12)],fill=GOLD)
def crystal(d,x,y):
    d.polygon([(x,y+12),(x+4,y),(x+8,y+4),(x+9,y+12)],fill=PURP); d.polygon([(x+4,y),(x+6,y+12),(x,y+12)],fill=PURPL)
    d.polygon([(x+9,y+12),(x+12,y+5),(x+15,y+12)],fill=PURPD)
def torch(d,x,y):
    rect(d,x,y+5,x+2,y+14,WOODD); rect(d,x-1,y+4,x+3,y+5,IROND)
    d.polygon([(x-1,y+4),(x+1,y-2),(x+3,y+4)],fill=C('ff8a1f')); d.point((x+1,y+1),fill=C('ffe08a')); d.point((x+1,y+2),fill=C('ffe08a'))
def candle(d,x,y):
    rect(d,x,y+3,x+2,y+10,C('efe6cf')); d.point((x+1,y+2),fill=C('3a2a1a')); d.polygon([(x,y+2),(x+1,y-2),(x+2,y+2)],fill=C('ffb347'))
    rect(d,x-1,y+10,x+3,y+11,C('8a8f98'))
def sword(d,x,y,h=34):
    d.line([x,y,x,y+h],fill=C('cfd6df')); d.line([x+1,y+1,x+1,y+h],fill=C('8a93a0'))
    rect(d,x-3,y+h,x+4,y+h+1,GOLDD); rect(d,x,y+h+2,x+1,y+h+6,WOODD); rect(d,x-1,y+h+7,x+2,y+h+8,GOLD)
def shield(d,x,y,c=C('8e2a1e')):
    d.polygon([(x,y),(x+12,y),(x+12,y+9),(x+6,y+15),(x,y+9)],fill=GOLDD)
    d.polygon([(x+1,y+1),(x+11,y+1),(x+11,y+9),(x+6,y+14),(x+1,y+9)],fill=c)
    d.line([x+6,y+2,x+6,y+12],fill=GOLD); d.line([x+2,y+6,x+10,y+6],fill=GOLD)
def vine(d,x,y0,y1,rnd):
    for y in range(y0,y1):
        xx=x+int(math.sin(y*0.35)*2); d.point((xx,y),fill=LEAFD)
        if y%5==0: d.point((xx+1,y),fill=LEAF); d.point((xx-1,y+1),fill=LEAFL)
        if y%13==0: d.point((xx+2,y),fill=C('e86fa8'))
def chain(d,x,y0,y1):
    for y in range(y0,y1,4): d.rectangle([x,y,x+2,y+3],outline=IRON)
def bottle(d,x,y,c):
    rect(d,x+2,y,x+3,y+2,C('d9d2c0')); d.ellipse([x,y+2,x+5,y+9],fill=c); d.point((x+1,y+4),fill=C('ffffff'))
def lantern(d,x,y):
    rect(d,x,y,x+6,y+1,IROND); rect(d,x+1,y+2,x+5,y+8,C('ffcf5a')); d.rectangle([x,y+2,x+6,y+9],outline=IROND)
def leaf(d,x,y,flip=1):
    for i,(dx,dy) in enumerate([(0,0),(1,-1),(2,-2),(3,-2),(1,0),(2,-1),(4,-3),(3,-1)]): d.point((x+dx*flip,y+dy),fill=LEAF if i%3 else LEAFD)
def tools(d,x,y):
    d.line([x,y+12,x+10,y+2],fill=WOODD); d.polygon([(x+8,y),(x+13,y+1),(x+12,y+5)],fill=IRON)      # pioche
    d.line([x+14,y+12,x+20,y+2],fill=WOODD); rect(d,x+18,y,x+22,y+3,IRON)                        # marteau

# ---------- emplacements ----------
SLOTSTY={'bois':(C('2a170d'),C('5b3220'),C('7a4429'),C('432414')),'parchemin':(C('5a3b1e'),C('c9ad78'),C('e6d3a8'),C('a88a58')),
 'pierre':(C('1c1c24'),C('3a3a48'),C('55556a'),C('2a2a34')),'arcane':(C('120e26'),C('2b2050'),C('6a52b0'),C('1d163a'))}
def slot(d,x,y,sty='bois'):
    o,i,hl,sh=SLOTSTY[sty]
    # L'objet occupe x..x+15 : contour sombre autour, liseré clair symétrique pour que l'icône tombe pile au centre.
    rect(d,x-1,y-1,x+16,y+16,o); rect(d,x,y,x+15,y+15,hl); rect(d,x+1,y+1,x+14,y+14,sh); rect(d,x+2,y+2,x+13,y+13,i)
def alcove(d,x,y,c=C('8e2a1e'),cd=C('5e1a12'),cl=C('b23a28')):
    x0,y0,x1,y1=x-6,y-8,x+21,y+21
    d.rounded_rectangle([x0-1,y0-1,x1+1,y1+1],radius=7,fill=GOLDD); d.rounded_rectangle([x0,y0,x1,y1],radius=6,fill=c)
    d.rounded_rectangle([x0+2,y0+2,x1-2,y1-2],radius=5,fill=cd); d.line([x0+3,y0+2,x1-3,y0+2],fill=cl); d.line([x0+2,y1,x1-2,y1],fill=GOLD)
def shade(img,x0,y0,x1,y1,n=4,col=(10,10,20)):
    ov=Image.new('RGBA',img.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    for i in range(n): od.rectangle([x0+i,y0+i,x1-i,y1-i],outline=col+(70-i*16,))
    img.alpha_composite(ov)

# ---------- thèmes ----------
THEMES={
 'chateau':  dict(frame=C('77778a'),top='creneaux',plaque=C('3a3a46'),slot='bois',alc=None,deco='bannieres'),
 'parchemin':dict(frame=WOODD,top='rouleau',plaque=C('5a3b1e'),slot='parchemin',alc=(C('7a5a2e'),C('a8844c'),C('c9a86a')),deco='sceaux'),
 'armurerie':dict(frame=WOODD,top='poutre',plaque=C('3b2414'),slot='bois',alc=None,deco='armes'),
 'atelier':  dict(frame=WOODD,top='poutre',plaque=C('3b2414'),slot='bois',alc=None,deco='outils'),
 'arcane':   dict(frame=C('2a2140'),top='runes',plaque=C('1a1430'),slot='arcane',alc=(C('3b2a70'),C('1d163a'),C('6a52b0')),deco='cristaux'),
 'mine':     dict(frame=WOODD,top='poutre',plaque=C('2a2620'),slot='pierre',alc=None,deco='lanternes'),
 'foret':    dict(frame=C('3e2916'),top='feuillage',plaque=C('2f2416'),slot='bois',alc=None,deco='lianes'),
 'forge':    dict(frame=C('3a3a42'),top='creneaux',plaque=C('2a1a14'),slot='pierre',alc=None,deco='chaines'),
 'eau':      dict(frame=WOOD,top='ponton',plaque=C('1f3a55'),slot='bois',alc=None,deco='cordes'),
 'alchimie': dict(frame=WOODD,top='poutre',plaque=C('2a1838'),slot='bois',alc=None,deco='fioles'),
 'autel':    dict(frame=C('2a2430'),top='creneaux',plaque=C('1a1218'),slot='pierre',alc=(C('5e1a12'),C('2a0c08'),C('b23a28')),deco='bougies'),
}
def make(rows, used, feature=(), theme='chateau', links=(), seed=0):
    th=THEMES[theme]; rnd=random.Random(seed or rows*31+len(used))
    top=17+rows*18; H=M+top+96
    img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    gx=lambda x:x+S; gy=lambda y:y+M
    X0,Y0,X1,Y1=gx(2),gy(4),gx(173),gy(top-2)
    # haut
    if th['top'] in ('creneaux',):
        stones=[C('5d5d6e'),C('666678'),C('6f6f82')] if theme!='autel' else [C('2c2630'),C('342d39')]
        for i,bx in enumerate(range(gx(-2),gx(178),30)):
            h=14 if i%2==0 else 9; bevel(d,bx,gy(-h),bx+26,gy(4),stones[i%len(stones)],C('8d8da3') if theme!='autel' else C('4a3f52'),C('44444f'),DARK)
    elif th['top']=='poutre':
        rect(d,gx(-4),gy(-10),gx(179),gy(4),WOODD); rect(d,gx(-4),gy(-9),gx(179),gy(2),WOOD); d.line([gx(-4),gy(-9),gx(179),gy(-9)],fill=WOODL)
        for bx in (gx(10),gx(160)): rect(d,bx,gy(-11),bx+5,gy(5),IROND); d.point((bx+2,gy(-3)),fill=IRON)
        rect(d,gx(60),gy(-20),gx(115),gy(-10),WOODD); rect(d,gx(61),gy(-19),gx(114),gy(-11),WOOD2)  # enseigne
        d.line([gx(66),gy(-20),gx(66),gy(-26)],fill=IROND); d.line([gx(109),gy(-20),gx(109),gy(-26)],fill=IROND)
    elif th['top']=='rouleau':
        for yy in (gy(-6),):
            d.rounded_rectangle([gx(-6),yy-6,gx(181),yy+6],radius=6,fill=WOODD); d.rounded_rectangle([gx(-5),yy-5,gx(180),yy+4],radius=5,fill=WOOD2)
            d.line([gx(-3),yy-4,gx(178),yy-4],fill=WOODL)
            for cx in (gx(-9),gx(182)): d.ellipse([cx-4,yy-7,cx+4,yy+7],fill=GOLDD); d.ellipse([cx-3,yy-6,cx+3,yy+5],fill=GOLD)
    elif th['top']=='runes':
        for i,bx in enumerate(range(gx(-2),gx(178),30)):
            h=12 if i%2==0 else 7; bevel(d,bx,gy(-h),bx+26,gy(4),C('2a2140'),C('4a3a78'),C('15102a'),C('0d0a1a'))
            d.line([bx+10,gy(-h+3),bx+16,gy(-h+3)],fill=PURPL); d.point((bx+13,gy(-h+5)),fill=C('cdb8ff'))
    elif th['top']=='feuillage':
        for _ in range(260):
            x=rnd.randint(gx(-8),gx(183)); y=rnd.randint(gy(-24),gy(6)); r=rnd.randint(2,4)
            d.ellipse([x-r,y-r,x+r,y+r],fill=rnd.choice([LEAF,LEAFD,LEAFL,C('3d7a2e')]))
        for _ in range(8):
            x=rnd.randint(gx(0),gx(175)); y=rnd.randint(gy(-22),gy(2)); d.point((x,y),fill=C('e86fa8')); d.point((x+1,y),fill=C('ffd1e6'))
    elif th['top']=='ponton':
        wall_planks(d,gx(-4),gy(-14),gx(179),gy(4),rnd,[WOOD,WOOD2,C('73492a')],WOODD,pw=6,vertical=False)
        for px in (gx(-4),gx(40),gx(84),gx(128),gx(172)): rect(d,px,gy(-18),px+6,gy(4),WOODD); d.line([px+1,gy(-18),px+1,gy(4)],fill=WOOD)
    # mur
    rect(d,gx(-2),gy(0),gx(177),gy(top+2),DARK)
    if theme in ('chateau',): wall_bricks(d,X0,Y0,X1,Y1,rnd,[C('5d5d6e'),C('666678'),C('6f6f82'),C('62627a')],C('3c3c4a'),C('8d8da3'),C('44444f'))
    elif theme=='forge': wall_redbrick(d,X0,Y0,X1,Y1,rnd)
    elif theme=='autel': wall_dark_altar(d,X0,Y0,X1,Y1,rnd)
    elif theme=='parchemin': wall_parchment(img,d,X0,Y0,X1,Y1,rnd)
    elif theme in ('armurerie','atelier','alchimie'):
        cols=[C('6b4226'),C('73482a'),C('62391f'),C('7a4e2d')] if theme!='alchimie' else [C('4a2c3a'),C('543244'),C('432636')]
        wall_planks(d,X0,Y0,X1,Y1,rnd,cols,WOODD)
    elif theme=='arcane': wall_stars(d,X0,Y0,X1,Y1,rnd)
    elif theme=='mine': wall_cave(d,X0,Y0,X1,Y1,rnd)
    elif theme=='foret': wall_forest(d,X0,Y0,X1,Y1,rnd)
    elif theme=='eau': wall_water(d,X0,Y0,X1,Y1,rnd)
    if theme!='parchemin': shade(img,X0,Y0,X1,Y1)
    # cadre
    fr=th['frame']
    for (a,b,c,e) in [(gx(-2),gy(0),gx(3),gy(top+2)),(gx(172),gy(0),gx(177),gy(top+2))]:
        bevel(d,a,b,c,e,fr,jit(fr,0,rnd) if False else mix(fr,C('ffffff'),.25),mix(fr,C('000000'),.35))
    # plaque titre
    pl=th['plaque']; px0,px1=gx(33),gx(143)
    bevel(d,px0,gy(3),px1,gy(15),pl,mix(pl,C('ffffff'),.2),mix(pl,C('000000'),.4),DARK)
    d.line([px0+2,gy(14),px1-2,gy(14)],fill=GOLDD)
    # décor latéral
    deco=th['deco']; hb=min(top-6,70)
    if deco=='bannieres': banner(d,1,gy(0),gy(hb)); banner(d,W-11,gy(0),gy(hb))
    elif deco=='sceaux':
        for x in (2,W-12):
            d.ellipse([x,gy(20),x+9,gy(29)],fill=C('8e2a1e')); d.ellipse([x+2,gy(22),x+7,gy(27)],fill=C('b23a28'))
            d.line([x+3,gy(29),x+1,gy(40)],fill=C('8e2a1e')); d.line([x+6,gy(29),x+8,gy(40)],fill=C('8e2a1e'))
    elif deco=='armes': sword(d,4,gy(2),40); sword(d,W-6,gy(2),40); shield(d,0,gy(56)); shield(d,W-13,gy(56),C('1f4f8e'))
    elif deco=='outils': torch(d,4,gy(10)); torch(d,W-7,gy(10)); tools(d,gx(4),gy(top-16))
    elif deco=='cristaux': crystal(d,-2,gy(30)); crystal(d,W-14,gy(30)); crystal(d,-1,gy(60)); crystal(d,W-15,gy(60))
    elif deco=='lanternes':
        for x in (3,W-9): rect(d,x+2,gy(0),x+4,gy(top),WOODD); lantern(d,x,gy(30))
    elif deco=='lianes': vine(d,4,gy(0),gy(top-4),rnd); vine(d,W-6,gy(0),gy(top-4),rnd)
    elif deco=='chaines': chain(d,4,gy(0),gy(hb)); chain(d,W-7,gy(0),gy(hb)); torch(d,gx(6),gy(top-20)); torch(d,gx(166),gy(top-20))
    elif deco=='cordes':
        for x in (5,W-7):
            for y in range(gy(0),gy(hb)): d.point((x+(y//2)%2,y),fill=C('c9a86a'))
    elif deco=='fioles':
        for i,(x,c) in enumerate([(1,C('d63b2f')),(W-8,C('3fb0d6')),(1,C('5fd13b')),(W-8,C('b05fe0'))]): bottle(d,x,gy(20+i//2*30),c)
    elif deco=='bougies': candle(d,4,gy(20)); candle(d,W-7,gy(20)); candle(d,4,gy(50)); candle(d,W-7,gy(50))
    # liens (arbre de talents)
    for a,b in links:
        (ra,ca),(rb,cb)=divmod(a,9),divmod(b,9)
        xa,ya=gx(8+ca*18)+7,gy(18+ra*18)+7; xb,yb=gx(8+cb*18)+7,gy(18+rb*18)+7
        d.line([xa,ya,xb,yb],fill=GOLDD,width=3); d.line([xa,ya,xb,yb],fill=GOLD,width=1)
    # emplacements
    for s_ in feature:
        r,c=divmod(s_,9); alcove(d,gx(8+c*18),gy(18+r*18),*(th['alc'] or ()))
    for s_ in used:
        r,c=divmod(s_,9); slot(d,gx(8+c*18),gy(18+r*18),th['slot'])
    # accents bas du mur
    last=(rows-1)*9
    acc={'chateau':crystal,'arcane':crystal}.get(theme)
    if acc:
        if last not in used: acc(d,gx(4),gy(top-14))
        if last+8 not in used: acc(d,gx(156),gy(top-14))
    if theme=='mine':
        for xx in (gx(6),gx(160)):
            if True: d.polygon([(xx,gy(top-2)),(xx+5,gy(top-9)),(xx+10,gy(top-2))],fill=C('5b5763')); d.point((xx+5,gy(top-6)),fill=C('5ce1e6'))
    # étagère et partie basse (commune)
    rect(d,gx(-2),gy(top),gx(177),gy(top+6),WOODD); rect(d,gx(-2),gy(top+1),gx(177),gy(top+4),WOOD)
    d.line([gx(-2),gy(top+1),gx(177),gy(top+1)],fill=WOOD2); d.line([gx(-2),gy(top+6),gx(177),gy(top+6)],fill=GOLD)
    rect(d,gx(0),gy(top+7),gx(175),gy(top+95),C('3b2214'))
    for r in range(3):
        for c in range(9): slot(d,gx(8+c*18),gy(top+14+r*18))
    hy=top+71
    rect(d,gx(4),gy(hy-1),gx(171),gy(hy+18),GOLDD); rect(d,gx(5),gy(hy),gx(170),gy(hy+17),GOLD); d.line([gx(5),gy(hy),gx(170),gy(hy)],fill=GOLDL)
    for c in range(9): slot(d,gx(8+c*18),gy(hy+1))
    leaf(d,gx(4),gy(hy-1),1); leaf(d,gx(171),gy(hy-1),-1)
    return img
