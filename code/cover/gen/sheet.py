import json,sys
from PIL import Image
D=json.load(open('data.json'));l=sys.argv[1]
fs=[o for o in D if o['l']==l];n=len(fs);cols=8;rows=(n+cols-1)//cols
W=Image.new('RGB',(cols*270,rows*480),'white')
for i,o in enumerate(fs): W.paste(Image.open(f"out/{o['v']}_{l}.png").resize((270,480)),(270*(i%cols),480*(i//cols)))
W.save(f'sheet_{l}.jpg',quality=80)
