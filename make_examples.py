import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
rs={r['id']:r for r in json.loads(Path('scan_results/records.json').read_text(encoding='utf-8'))}
focus=list(zip([24,35,31,61,22,17,0,59,2,14,12],['Абсолютная длительность','Очень высокая длительность','Высокая длительность','Умеренная длительность','Небольшая длительность','Сбалансированный','Небольшая сила','Умеренная сила','Высокая сила','Очень высокая сила','Абсолютная сила']))
safety=list(zip([18,70,34,15,3,11,39],['Идеальный','Стабильный','Утончённый','Сбалансированный','Нестабильный','Летучий','Хаотичный']))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for kind,items in [('focus',focus),('safety',safety)]:
    canvas=Image.new('RGB',(1000,len(items)*108),'#f6f3f8'); draw=ImageDraw.Draw(canvas)
    for i,(idx,label) in enumerate(items):
        r=rs[idx]; y=i*108; icon=Image.open(f'scan_results/{idx}.png'); canvas.paste(icon,(5,y+12))
        draw.text((90,y+8),label,font=font,fill='black'); draw.text((90,y+36),Path(r['file']).name,font=font,fill='black')
        im=Image.open(r['file']); left,top,right,bottom=r['box']; title=im.crop((max(0,left-10),top-178,min(im.width,left+700),top-135))
        canvas.paste(title,(300,y+61))
        print(kind,label,Path(r['file']).name,idx)
    canvas.save(f'scan_results/{kind}_examples.png')
