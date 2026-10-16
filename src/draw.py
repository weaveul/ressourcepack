import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from themes import make
TAL_LINKS=[(c+9*r,c+9*(r+1)) for c in (1,4,7) for r in range(4)]
MC_THEME={'skilloverview':'atelier','mining':'mine','excavation':'mine','woodcutting':'foret','herbalism':'foret','taming':'foret',
 'fishing':'eau','alchemy':'alchimie','repair':'forge','salvage':'forge','smelting':'forge'}
def menus():
    m={'menu':(5,[4,20,22,24,37,39,41,43],[20,22,24],'chateau',[]),
       'race':(4,[4,19,21,23,25],[19,21,23,25],'parchemin',[]),
       'classe':(6,[4,20,22,24,38,40,42],[20,22,24,38,40,42],'armurerie',[]),
       'talents':(6,[1,4,7]+[c+9*r for c in (1,4,7) for r in (1,2,3,4)]+[45,49,51,53],[],'arcane',TAL_LINKS),
       'attributs':(5,[13]+list(range(19,26))+[36,44],[13],'arcane',[]),
       'reset':(3,[11,15],[11,15],'autel',[]),
       'metiers':(6,[4,45],[],'atelier',[])}
    lj='/tmp/claude-0/sc/mgui/layouts.json'
    for k,(rows,used) in json.load(open(lj)).items():
        m['mc_'+k.lower()]=(rows,used,[],MC_THEME.get(k.lower(),'armurerie'),[])
    m['race_info']=(4,[13,27,29,31,33],[13],'parchemin',[])
    m['classe_info']=(6,[13]+list(range(28,35))+list(range(37,44))+[45,53],[13],'armurerie',[])
    m['fiche']=(5,[11,13,15]+list(range(28,35))+[36],[11,13,15],'parchemin',[])
    m['parametres']=(4,[4,10,11,12,13,14,15,16,21,23,27,31],[],'atelier',[])
    # PNJ de planque (EvoExtract) : boutique (U+E030) et quêtes (U+E031)
    m['marchand']=(6,[0,4,8]+[9*r+c for r in (1,2,3,4) for c in range(8)]+[45,49,53],[8],'alchimie',[])
    m['quetes']=(6,[4,18,20,22,24,36,38,40,42,45,49],[20,22,24,38,40,42],'parchemin',[])
    return m
if __name__=='__main__':
    out=sys.argv[1]
    for k,(rows,used,feat,theme,links) in menus().items():
        make(rows,used,feat,theme,links).save(f'{out}/{k}.png'); print(k,theme)
