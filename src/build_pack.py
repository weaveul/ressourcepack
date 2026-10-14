import json, os, shutil, zipfile, hashlib
from PIL import Image
S=12; M=26
SRC='/tmp/claude-0/sc/rp/out3'; PK='/tmp/claude-0/sc/rp/pack'
os.makedirs(PK+'/assets/evo/textures/gui',exist_ok=True); os.makedirs(PK+'/assets/minecraft/font',exist_ok=True)
names=['menu','race','classe','talents','reset','metiers']
prov=[]; glyph={}
for i,n in enumerate(names):
    shutil.copy(f'{SRC}/{n}.png',f'{PK}/assets/evo/textures/gui/{n}.png')
    h=Image.open(f'{SRC}/{n}.png').height
    ch=chr(0xE000+i); glyph[n]=(ch,Image.open(f'{SRC}/{n}.png').width)
    prov.append({'type':'bitmap','file':f'evo:gui/{n}.png','ascent':13+M,'height':h,'chars':[ch]})
adv={chr(0xF100+n):-n for n in range(1,256)}; adv.update({chr(0xF300+n):n for n in range(1,256)})
prov.append({'type':'space','advances':adv})
json.dump({'providers':prov},open(PK+'/assets/minecraft/font/default.json','w'),ensure_ascii=False,indent=1)
json.dump({'pack':{'description':'§6Evo Extract §7- menus','pack_format':88,'min_format':88,'max_format':88}},open(PK+'/pack.mcmeta','w'),ensure_ascii=False)
os.makedirs('/mnt/project-files/resourcepack',exist_ok=True)
z='/mnt/project-files/resourcepack/EvoExtract-pack.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
    for root,_,files in os.walk(PK):
        for fn in files:
            full=os.path.join(root,fn); f.write(full,os.path.relpath(full,PK))
print(hashlib.sha1(open(z,'rb').read()).hexdigest(), os.path.getsize(z))
json.dump({n:[ord(c),w] for n,(c,w) in glyph.items()},open('/tmp/claude-0/sc/rp/glyphs.json','w'))
