from pathlib import Path
import sys, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, r'C:\Users\User\OneDrive\Документы\Alchemy')
from alchemy_importer.screenshot_ocr import _tooltip_title_box

src=Path(r'C:\Users\User\OneDrive\Документы\Alchemy\screenshots')
out=Path('scan_results'); out.mkdir(exist_ok=True)
groups={}; records=[]
for n,p in enumerate(sorted(src.glob('*.png'))):
    im=Image.open(p).convert('RGB'); box=_tooltip_title_box(im)
    if not box: continue
    a=np.asarray(im); y0=box[1]-3
    candidates=[]
    for y in range(y0+140,min(y0+260,im.height)):
        row=np.all(a[y]==(67,57,74),axis=1)
        xs=np.flatnonzero(row)
        if len(xs)>280:
            candidates.append((y,xs))
    if not candidates: continue
    y,xs=candidates[0]; left=int(xs[0]); right=int(xs[-1])
    if left<box[0]-10: continue
    for kind,frac in [('focus',1/6),('safety',5/6)]:
        x=round(left+(right-left)*frac)
        crop=im.crop((x-36,y+28,x+36,y+104))
        ar=np.asarray(crop); mask=(ar.max(axis=2)>100)
        key=(kind,mask.tobytes())
        if key not in groups:
            idx=len(groups); groups[key]=idx
            crop.save(out/f'{idx}.png')
            records.append(dict(id=idx,kind=kind,file=str(p),box=[left,y,right,y+108]))
    if n%100==0: print(n, len(groups),flush=True)
(out/'records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for offset in range(0,len(records),100):
    subset=records[offset:offset+100]; sheet=Image.new('RGB',(1000,((len(subset)+9)//10)*110),'#eeeeee'); d=ImageDraw.Draw(sheet)
    for i,r in enumerate(subset):
        x=(i%10)*100; y=(i//10)*110
        sheet.paste(Image.open(out/f'{r["id"]}.png'),(x,y+20)); d.text((x,y),f'{r["id"]} {r["kind"]}',fill='black')
    sheet.save(out/f'montage{offset}.png')
print('TOTAL',len(records))
