from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
p=Path(__file__).resolve().parent
im=ImageOps.fit(Image.open(p/'research.png').convert('RGB'),(1280,720))
overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
d.rounded_rectangle((32,119,770,636),radius=28,fill=(255,252,244,237))
d.rounded_rectangle((40,32,595,98),radius=32,fill=(20,55,59,245))
font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
d.text((66,48),'ENGLISH LISTENING & SHADOWING',font=ImageFont.truetype(font,25),fill='white')
d.text((72,150),'CAN AN EYE TEST',font=ImageFont.truetype(font,58),fill='#19363a')
d.text((72,238),'REVEAL',font=ImageFont.truetype(font,90),fill='#19363a')
d.text((72,351),'HIDDEN HEALTH',font=ImageFont.truetype(font,70),fill='#db704f')
d.text((72,446),'PROBLEMS?',font=ImageFont.truetype(font,79),fill='#19363a')
d.rounded_rectangle((75,564,355,574),radius=5,fill='#e4a359')
im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
im.save(p/'thumbnail.png')
