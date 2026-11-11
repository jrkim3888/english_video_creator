from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parent;fonts=R.parents[1]/'eye-health-video/full/fonts'
f=lambda n:ImageFont.truetype(str(fonts/'NanumGothic-Bold.ttf'),n)
img=ImageOps.fit(Image.open(R/'images/rain-garden.png').convert('RGB'),(1280,720),Image.Resampling.LANCZOS).convert('RGBA')
shade=Image.new('RGBA',img.size);d=ImageDraw.Draw(shade)
for x in range(1000):
 alpha=round(230*max(0,1-x/1000)**.6);d.line((x,0,x,720),fill=(16,48,51,alpha))
img=Image.alpha_composite(img,shade);d=ImageDraw.Draw(img)
d.rounded_rectangle((50,40,625,89),radius=24,fill='#f6f2e8');d.text((72,56),'ENGLISH LISTENING & SHADOWING',font=f(22),fill='#193d42')
d.rounded_rectangle((1080,40,1230,89),radius=24,fill='#f6f2e8');d.text((1105,55),'L2 / A2',font=f(22),fill='#193d42')
d.text((52,201),'DRINK',font=f(104),fill='#fffaf0');d.text((52,321),'THE RAIN',font=f(104),fill='#f2a084')
d.text((58,497),'빗물을 받아들이는 도시',font=f(38),fill='#fffaf0')
d.text((60,564),'듣고 · 이해하고 · 따라 말하기',font=f(24),fill='#f1e8d8')
img.convert('RGB').save(R/'thumbnail.png')
(R/'thumbnail-layout.json').write_text(json.dumps({'background':'images/rain-garden.png','size':[1280,720],'title':['DRINK','THE RAIN'],'subtitle':'빗물을 받아들이는 도시','level':'L2 / A2','font':'NanumGothic-Bold.ttf','style':'현대적 편집 일러스트'},ensure_ascii=False,indent=2))
