import random
from PIL import Image, ImageDraw
S=12; M=26; W=176+2*S
def C(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,)
STONE=[C('5d5d6e'),C('666678'),C('6f6f82'),C('62627a')]; MORTAR=C('3c3c4a'); HL=C('8d8da3'); SH=C('44444f')
DARK=C('2e2e38')
WOOD=C('6b4226'); WOOD2=C('7d4f2c'); WOODD=C('4a2c18')
SLOT_O=C('2a170d'); SLOT_I=C('5b3220'); SLOT_HL=C('7a4429'); SLOT_SH=C('432414')
GOLD=C('f2b43a'); GOLDD=C('b97a1c'); GOLDL=C('ffe08a')
PURP=C('8e5bd6'); PURPD=C('6a3cb0'); PURPL=C('b58cf0')
LEAF=C('4f9a3a'); LEAFD=C('2f6b25')
def rect(d,x0,y0,x1,y1,c): d.rectangle([x0,y0,x1,y1],fill=c)
def bricks(d,x0,y0,x1,y1,seed=1,bw=16,bh=8):
    rnd=random.Random(seed); rect(d,x0,y0,x1,y1,MORTAR)
    row=0
    for y in range(y0,y1+1,bh):
        off=(bw//2 if row%2 else 0); row+=1
        for x in range(x0-off,x1+1,bw):
            a,b=max(x,x0),min(x+bw-2,x1); c,e=y,min(y+bh-2,y1)
            if a>b or c>e: continue
            col=rnd.choice(STONE); rect(d,a,c,b,e,col)
            d.line([a,c,b,c],fill=HL if rnd.random()<.7 else col); d.line([a,e,b,e],fill=SH)
def bevel(d,x0,y0,x1,y1,fill,hl,sh,o=None):
    if o: rect(d,x0-1,y0-1,x1+1,y1+1,o)
    rect(d,x0,y0,x1,y1,fill); d.line([x0,y0,x1,y0],fill=hl); d.line([x0,y0,x0,y1],fill=hl)
    d.line([x0,y1,x1,y1],fill=sh); d.line([x1,y0,x1,y1],fill=sh)
def slot(d,x,y):  # x,y = item pos (16x16), frame 18x18
    rect(d,x-1,y-1,x+16,y+16,SLOT_O); rect(d,x,y,x+15,y+15,SLOT_I)
    d.line([x,y+15,x+15,y+15],fill=SLOT_HL); d.line([x+15,y,x+15,y+15],fill=SLOT_HL)
    d.line([x,y,x+15,y],fill=SLOT_SH); d.line([x,y,x,y+15],fill=SLOT_SH)
def banner(d,x,y0,y1):
    rect(d,x-1,y0-2,x+10,y0-1,C('9a9aa8'))
    pts=[(x,y0),(x+9,y0),(x+9,y1),(x+4,y1-5),(x,y1)]
    d.polygon(pts,fill=PURP); d.line([x,y0,x,y1],fill=PURPD); d.line([x+9,y0,x+9,y1],fill=PURPD)
    d.line([x+2,y0,x+2,y1-4],fill=PURPL); d.line([x,y0+1,x+9,y0+1],fill=GOLD)
def crystal(d,x,y):
    d.polygon([(x,y+12),(x+4,y),(x+8,y+4),(x+9,y+12)],fill=PURP)
    d.polygon([(x+4,y),(x+6,y+12),(x,y+12)],fill=PURPL); d.line([x+8,y+4,x+9,y+12],fill=PURPD)
    d.polygon([(x+9,y+12),(x+12,y+5),(x+15,y+12)],fill=PURPD); d.line([x+12,y+5,x+12,y+12],fill=PURPL)
def leaf(d,x,y,flip=1):
    for i,(dx,dy) in enumerate([(0,0),(1,-1),(2,-2),(3,-2),(1,0),(2,-1),(4,-3),(3,-1)]):
        d.point((x+dx*flip,y+dy),fill=LEAF if i%3 else LEAFD)
RED=C('8e2a1e'); REDD=C('5e1a12'); REDL=C('b23a28')
def alcove(d,x,y):  # cadre d'honneur autour d'un emplacement
    x0,y0,x1,y1=x-6,y-8,x+21,y+21
    d.rounded_rectangle([x0-1,y0-1,x1+1,y1+1],radius=7,fill=GOLDD)
    d.rounded_rectangle([x0,y0,x1,y1],radius=6,fill=RED)
    d.rounded_rectangle([x0+2,y0+2,x1-2,y1-2],radius=5,fill=REDD)
    d.line([x0+3,y0+2,x1-3,y0+2],fill=REDL)
    d.line([x0+2,y1,x1-2,y1],fill=GOLD)
def shade(img,x0,y0,x1,y1,n=4):
    ov=Image.new('RGBA',img.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    for i in range(n):
        a=70-i*16
        od.rectangle([x0+i,y0+i,x1-i,y1-i],outline=(10,10,20,a))
    img.alpha_composite(ov)
def make(rows, used, feature=(), plaque_w=110):
    top=17+rows*18; H=M+top+96
    img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    gx=lambda x:x+S; gy=lambda y:y+M
    # créneaux / blocs au-dessus
    for i,bx in enumerate(range(gx(-2),gx(178),30)):
        h=14 if i%2==0 else 9
        bevel(d,bx,gy(-h),bx+26,gy(4),STONE[i%4],HL,SH,DARK)
    # mur principal (partie haute)
    rect(d,gx(-2),gy(0),gx(177),gy(top+2),DARK)
    bricks(d,gx(2),gy(4),gx(173),gy(top-2),seed=rows)
    shade(img,gx(2),gy(4),gx(173),gy(top-2))
    # cadre pierre
    for (a,b,c,e) in [(gx(-2),gy(0),gx(3),gy(top+2)),(gx(172),gy(0),gx(177),gy(top+2))]:
        bevel(d,a,b,c,e,C('77778a'),HL,SH)
    # plaque titre
    px0=gx(88-plaque_w//2); px1=gx(88+plaque_w//2)
    bevel(d,px0,gy(3),px1,gy(15),C('3a3a46'),C('55556a'),C('24242c'),DARK)
    d.line([px0+2,gy(14),px1-2,gy(14)],fill=GOLDD)
    # bannières
    banner(d,1,gy(0),gy(min(top-6,70))); banner(d,W-11,gy(0),gy(min(top-6,70)))
    # emplacements utilisés
    for s in feature:
        r,c=divmod(s,9); alcove(d,gx(8+c*18),gy(18+r*18))
    for s in used:
        r,c=divmod(s,9); slot(d,gx(8+c*18),gy(18+r*18))
    # cristaux
    last=(rows-1)*9
    if last not in used: crystal(d,gx(4),gy(top-14))
    if last+8 not in used: crystal(d,gx(156),gy(top-14))
    # étagère bois
    rect(d,gx(-2),gy(top),gx(177),gy(top+6),WOODD); rect(d,gx(-2),gy(top+1),gx(177),gy(top+4),WOOD)
    d.line([gx(-2),gy(top+1),gx(177),gy(top+1)],fill=WOOD2); d.line([gx(-2),gy(top+6),gx(177),gy(top+6)],fill=GOLD)
    # partie basse : tuiles marron
    b0=top+7
    rect(d,gx(0),gy(b0),gx(175),gy(top+95),C('3b2214'))
    for r in range(3):
        for c in range(9): slot(d,gx(8+c*18),gy(top+14+r*18))
    # barre d'action dorée
    hy=top+71
    rect(d,gx(4),gy(hy-1),gx(171),gy(hy+18),GOLDD); rect(d,gx(5),gy(hy),gx(170),gy(hy+17),GOLD)
    d.line([gx(5),gy(hy),gx(170),gy(hy)],fill=GOLDL)
    for c in range(9): slot(d,gx(8+c*18),gy(hy+1))
    leaf(d,gx(4),gy(hy-1),1); leaf(d,gx(171),gy(hy-1),-1); leaf(d,gx(5),gy(hy-2),1); leaf(d,gx(170),gy(hy-2),-1)
    return img
if __name__=='__main__':
    import json,sys
    out=sys.argv[1]
    menus={'menu':(5,[4,20,22,24,38,40,42],[20,22,24]),
           'race':(4,[4,19,21,23,25],[19,21,23,25]),
           'classe':(6,[4,20,22,24,38,40,42],[20,22,24,38,40,42]),
           'talents':(6,[1,4,7]+[c+9*r for c in (1,4,7) for r in (1,2,3,4)]+[45,49,53],[]),
           'reset':(3,[11,15],[11,15]),
           'metiers':(6,[4,11,12,13,14,15,20,21,23,24,28,29,30,31,32,33,34,39,40,41,45],[])}
    for k,(rows,used,feat) in menus.items():
        im=make(rows,used,feat); im.save(f'{out}/{k}.png')
        im.resize((im.width*4,im.height*4),Image.NEAREST).save(f'{out}/preview_{k}.png')
        print(k,im.size)
