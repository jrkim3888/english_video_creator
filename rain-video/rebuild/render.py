from pathlib import Path
import json,math,subprocess
import numpy as np
import soundfile as sf
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path(__file__).resolve().parent; C=R/'cards';B=R/'backgrounds';C.mkdir(exist_ok=True);B.mkdir(exist_ok=True)
FONTS=R.parents[1]/'eye-health-video/full/fonts'
def f(n,b=False):return ImageFont.truetype(str(FONTS/('NanumGothic-Bold.ttf' if b else 'NanumGothic-Regular.ttf')),n)
cream='#faf8f2';ink='#193d42';teal='#167b79';coral='#dc805f';gray='#617573'
E=json.loads((R/'timeline.json').read_text());total=E[-1]['end']; stages=['첫 듣기','내용 이해','섀도잉','표현 연습','다시 듣기']
assets=json.loads((R/'images/assets.json').read_text())
for name,p in assets.items():
 src=Image.open(R/'images'/p).convert('RGB')
 # Reserve about 60 percent of the video for scene imagery.
 ImageOps.fit(src,(1280,432),Image.Resampling.LANCZOS,centering=(.5,.55)).save(B/(name+'.jpg'),quality=95)
def wrap(d,text,font,w):
 lines=[];line=''
 for word in text.split():
  trial=(line+' '+word).strip()
  if line and d.textlength(trial,font=font)>w:lines.append(line);line=word
  else:line=trial
 if line:lines.append(line)
 return lines

def card(e):
 im=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(im)
 d.rounded_rectangle((33,24,276,66),radius=21,fill=ink);d.text((52,36),'ENGLISH  /  L2 · A2',font=f(17,True),fill='white')
 d.rounded_rectangle((984,24,1247,66),radius=21,fill=ink);d.text((1003,36),'RAIN & THE CITY',font=f(17,True),fill='white')
 d.rounded_rectangle((0,423,1280,760),radius=30,fill=cream)
 d.text((54,445),f"0{e['stage']+1}  {stages[e['stage']]}",font=f(19,True),fill=teal)
 label=e['state']
 if e.get('countdown') is not None:label+=f"  {e['countdown']:02}초"
 d.text((935,446),label,font=f(18,True),fill=teal)
 d.line((54,481,1226,481),fill='#d8dfd7')
 for size in (36,33,30,27):
  font=f(size,True);lines=wrap(d,e['title'],font,1140)
  if len(lines)<=2:break
 assert len(lines)<=2,(e['title'],lines)
 y=502
 hl={x.lower().strip('.,?!') for x in e.get('highlight','').split()}
 for line in lines:
  x=57
  for token in line.split():
   d.text((x,y),token+' ',font=font,fill=coral if token.lower().strip('.,?!') in hl else ink);x+=d.textlength(token+' ',font=font)
  y+=size+8
 ko_lines=wrap(d,e.get('ko',''),f(21),1120)
 assert len(ko_lines)<=2,(e.get('ko'),ko_lines)
 for line in ko_lines:d.text((58,y+7),line,font=f(21),fill=gray);y+=27
 assert y<635,(e['title'],e.get('ko'),y)
 if e.get('countdown') is not None:
  d.rounded_rectangle((58,638,970,646),radius=4,fill='#dbe5dd');d.rounded_rectangle((58,638,58+max(1,round(912*e['countdown']/e['speak_total'])),646),radius=4,fill=teal)
 if e.get('index'):d.text((57,646),f"文 {e['index']:02} / 35".replace('文','문장'),font=f(13),fill=gray)
 if e.get('rep'):d.text((1086,632),'반복 '+e['rep'],font=f(16),fill=teal)
 d.line((54,670,1226,670),fill='#d8dfd7')
 for i,name in enumerate(stages):
  x=60+i*195;d.ellipse((x,691,x+7,698),fill=teal if i==e['stage'] else '#c9d2cd');d.text((x+15,684),name,font=f(14,True),fill=teal if i==e['stage'] else '#7b8d86')
 d.text((1080,685),f"{int(e['start'])//60:02}:{int(e['start'])%60:02} / {math.ceil(total)//60:02}:{math.ceil(total)%60:02}",font=f(14),fill=ink)
 d.rectangle((0,716,round(1280*e['start']/total),720),fill=coral)
 return im
sr=22050; out=sf.SoundFile(R/'narration.wav','w',samplerate=sr,channels=1,subtype='PCM_16')
for i,e in enumerate(E):
 count=round(e['duration']*sr);arr=np.zeros(count,dtype=np.float32)
 if e.get('clip'):
  a,rate=sf.read(R/'audio'/(e['clip']+'.wav'),dtype='float32');assert rate==sr
  rms=float(np.sqrt(np.mean(a*a)));peak=float(np.max(abs(a)));assert rms>.001
  a*=min(.12/rms,.92/max(peak,.001));assert len(a)<=len(arr);arr[:len(a)]=a
 out.write(arr);card(e).save(C/f'{i:04}.png')
out.close()
for kind in ('cards','backgrounds'):
 with (R/(kind+'.txt')).open('w') as o:
  for i,e in enumerate(E):
   p=f'cards/{i:04}.png' if kind=='cards' else f"backgrounds/{e['scene']}.jpg"
   o.write(f"file '{p}'\noption framerate 1000\nduration {e['duration']:.9f}\n")
  o.write(f"file '{p}'\noption framerate 1000\n")
# Review images are composed from the same layers used by FFmpeg.
shots=[]
for stage in range(5):
 choices=[e for e in E if e['stage']==stage]
 e=next((x for x in choices if x.get('index') and (stage!=2 or x.get('countdown'))),choices[0])
 bg=Image.new('RGBA',(1280,720),cream);bg.paste(Image.open(B/(e['scene']+'.jpg')),(0,0));bg.alpha_composite(card(e));bg.convert('RGB').save(R/f'preview-{stage}.png');shots.append(bg.convert('RGB').resize((640,360)))
contact=Image.new('RGB',(1280,1080),cream)
for i,im in enumerate(shots):contact.paste(im,(i%2*640,i//2*360))
contact.save(R/'contact-sheet.jpg',quality=94)
filters="[0:v]fps=12,scale=1320:446,crop=1280:432:x='20+16*sin(t/8)':y='7+5*cos(t/11)',pad=1280:720:0:0:color=0xfaf8f2[bg];[1:v]fps=12,format=rgba[card];[bg][card]overlay=0:0:shortest=1,format=yuv420p[v]"
cmd=['ffmpeg','-y','-loglevel','warning','-f','concat','-safe','0','-i',str(R/'backgrounds.txt'),'-f','concat','-safe','0','-i',str(R/'cards.txt'),'-i',str(R/'narration.wav'),'-filter_complex_threads','2','-filter_complex',filters,'-map','[v]','-map','2:a','-c:v','libx264','-preset','veryfast','-crf','22','-c:a','aac','-b:a','112k','-movflags','+faststart','-t',str(total),'-shortest',str(R/'rain-english-learning.mp4')]
print('encoding',total,len(E),flush=True);subprocess.run(cmd,check=True);print('DONE',flush=True)
