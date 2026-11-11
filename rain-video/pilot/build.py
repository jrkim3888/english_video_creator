from pathlib import Path
import json, math, subprocess
import numpy as np
import soundfile as sf
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
fonts=R.parents[1]/'eye-health-video/full/fonts'
F=lambda n,b=False:ImageFont.truetype(str(fonts/('NanumGothic-Bold.ttf' if b else 'NanumGothic-Regular.ttf')),n)
ink='#183d42'; teal='#187b79'; peach='#e78d6e'; cream='#faf8f2'
manifest=json.loads((R/'audio-manifest.json').read_text()); E=[]
def add(stage,title,ko,clip=None,scene=0,highlight='',state='듣기',duration=None,rep=''):
 E.append(dict(stage=stage,title=title,ko=ko,clip=clip,scene=scene,highlight=highlight,state=state,duration=manifest[clip]['duration']+.22 if clip else duration,rep=rep))
def speak(clip,title,ko,scene=1,stage=2,rep=''):
 add(stage,title,ko,clip,scene,state='먼저 들으세요',rep=rep)
 add(stage,title,ko,scene=scene,state='따라 말하세요',duration=max(4,manifest[clip]['duration']*1.2),rep=rep)
add(0,'How Cities Learn to Drink the Rain','빗물을 받아들이는 도시','intro',state='학습 안내')
for k in range(1,6):add(0,'Follow the rain.','영어 자막 없이 빗물의 흐름을 따라가 보세요.',f'en{k}',scene=0)
add(1,'A city that drinks the rain?','도시가 빗물을 마신다면?','understand',scene=1,state='뜻 살펴보기')
for n,ko in [(1,'도시가 빗물을 마실 수 있다면 어떨까요?'),(2,'폭풍우가 치는 동안 물은 도로와 인도를 따라 흘러갑니다.')]:
 for clip in (f'en{n}',f'ko{n}'):add(1,manifest[f'en{n}']['text'],ko,clip,scene=0,highlight='drink the rain' if n==1 else 'runs across',state='영어 듣기' if clip.startswith('en') else '한국어 뜻')
add(1,manifest['en6']['text'],'숲에서는 흙과 식물이 빗물을 흡수합니다.','en6',scene=1,highlight='take in')
add(1,manifest['en6']['text'],'숲에서는 흙과 식물이 빗물을 흡수합니다.','ko6',scene=1,highlight='take in',state='한국어 뜻')
add(2,'Listen. Repeat. Make it yours.','문장을 듣고 두 번 따라 말해 보세요.','shadow',scene=1,state='연습 안내')
for i in range(1,3):speak('en6',manifest['en6']['text'],'soil and plants / take in rain',rep=f'{i} / 2')
add(3,'take in','흡수하다 · 받아들이다','expressions',scene=1,highlight='take in',state='핵심 표현')
add(3,'take in','흡수하다 · 받아들이다','phrase',scene=1,highlight='take in')
add(3,manifest['example']['text'],'건강한 흙은 빗물을 흡수할 수 있습니다.','example_ko',scene=2,highlight='take in',state='예문 뜻')
speak('example',manifest['example']['text'],'건강한 흙은 빗물을 흡수할 수 있습니다.',scene=2,stage=3,rep='1 / 1')
add(3,manifest['limit_en']['text'],'녹지 공간도 모든 홍수를 막을 수는 없습니다.','limit_en',scene=2,highlight='cannot',state='내용 확인')
add(3,manifest['limit_en']['text'],'배수구와 배관도 함께 필요합니다.','limit',scene=2,highlight='cannot',state='내용 확인')
add(4,'Listen once more.','이번에는 영어 자막과 함께 들어 보세요.','review',scene=1,state='다시 듣기 안내')
for k in range(1,6):add(4,manifest[f'en{k}']['text'],'',f'en{k}',scene=0 if k<5 else 1)
add(4,'Make more room for rain.','도시는 빗물이 머물 공간을 만들 수 있습니다.','outro',scene=1,state='복습 안내')
total=sum(e['duration'] for e in E); elapsed=0
for e in E:e['start']=elapsed; elapsed+=e['duration'];e['end']=elapsed
(R/'timeline.json').write_text(json.dumps(E,ensure_ascii=False,indent=2))

def wrap(d,text,font,width):
 lines=[];line=''
 for word in text.split():
  new=(line+' '+word).strip()
  if d.textlength(new,font=font)>width and line:lines.append(line);line=word
  else:line=new
 if line:lines.append(line)
 return lines

def arrow(d,x,y,x2,y2,color=teal,w=4):
 d.line((x,y,x2,y2),fill=color,width=w)
 a=math.atan2(y2-y,x2-x)
 d.polygon([(x2,y2),(x2-12*math.cos(a-.5),y2-12*math.sin(a-.5)),(x2-12*math.cos(a+.5),y2-12*math.sin(a+.5))],fill=color)

def tree(d,x,y,s=1):
 d.rounded_rectangle((x-5*s,y-68*s,x+5*s,y),radius=4,fill='#91745d')
 for dx,dy,rr in [(-23,-77,32),(24,-75,34),(0,-106,39)]:d.ellipse((x+(dx-rr)*s,y+(dy-rr)*s,x+(dx+rr)*s,y+(dy+rr)*s),fill='#46927c')

def scene(n,t):
 im=Image.new('RGB',(1280,432),'#dcebec');d=ImageDraw.Draw(im)
 # Stylized city; diagrams illustrate mechanisms, not a real location.
 for x,y,w,h in [(30,168,130,150),(173,118,135,200),(335,187,120,131),(1010,137,125,181),(1155,190,110,128)]:
  d.rounded_rectangle((x,y,x+w,y+h),radius=8,fill='#b4cacc')
  for wx in range(x+18,x+w-10,32):
   for wy in range(y+20,310,34):d.rectangle((wx,wy,wx+12,wy+17),fill='#e8f0ea')
 d.rectangle((0,315,1280,432),fill='#9baaaa')
 if n==0:
  d.polygon([(0,339),(1280,355),(1280,432),(0,432)],fill='#6c868c')
  for x in range(20,1280,150):d.line((x,398,x+75,398),fill='#e4d5ad',width=4)
  d.ellipse((435,338,1065,380),fill='#95c7d4')
  d.rounded_rectangle((1030,344,1144,369),radius=6,fill=ink)
  for x in range(1040,1140,15):d.line((x,348,x,365),fill='#a3b6b9',width=3)
  for x in range(130,1000,170):
   xx=x+(t*30)%80;arrow(d,xx,355,xx+70,355,'#edf8f4',3)
  label='01   RUNOFF';sub='딱딱한 표면 위로 흐르는 빗물'
 elif n==1:
  d.polygon([(0,325),(400,325),(470,371),(846,371),(915,325),(1280,325),(1280,432),(0,432)],fill='#b69b7a')
  d.polygon([(407,325),(476,362),(840,362),(909,325)],fill='#8cc6bc')
  for x in range(478,845,48):
   d.line((x,350,x+4,316),fill='#4d8060',width=4)
   d.ellipse((x-11,310,x+15,327),fill='#6f9a61')
   arrow(d,x,379,x,411,'#5c8e88',3)
  tree(d,310,325,1.1);tree(d,966,325,.95)
  arrow(d,170,339,405,346,'#468e9f',5)
  arrow(d,1080,339,910,346,'#468e9f',5)
  label='02   RAIN GARDEN';sub='낮은 정원에 모이고 흙으로 스미는 빗물'
 else:
  d.rounded_rectangle((320,236,962,292),radius=12,fill='#d9dbd0')
  for x in range(332,950,64):d.line((x,238,x,289),fill='#8faca7',width=5)
  d.rectangle((320,293,962,350),fill='#bdaf9b');d.rectangle((320,351,962,427),fill='#ab8c71')
  for x in range(340,950,37):
   for y in (309,333):d.ellipse((x,y,x+23,y+13),fill='#dfd6c6')
  d.line((660,396,1040,396),fill='#d7ddd7',width=18)
  for x in (410,550,690,830):arrow(d,x,211,x,306,'#458fa0',4)
  arrow(d,530,355,530,418,'#468e9f');arrow(d,795,395,1030,395,'#468e9f')
  label='03   PERMEABLE PAVEMENT';sub='자갈층에 저장되고 흙 또는 배관으로 이동'
 # Falling rain moves continuously, confined to illustration.
 for i in range(38):
  x=(i*97+29)%1280;y=105+(i*37+t*67)%190
  d.line((x,y,x-5,y+13),fill='#88b2be',width=2)
 d.rounded_rectangle((42,94,615,153),radius=16,fill=cream)
 d.text((61,103),label,font=F(16,True),fill=teal)
 d.text((61,126),sub,font=F(14),fill=ink)
 d.text((1035,398),'개념을 설명하는 그림',font=F(13),fill=ink)
 return im

stages=['첫 듣기','내용 이해','섀도잉','표현 연습','다시 듣기']
def frame(e,local,clock):
 im=Image.new('RGB',(1280,720),cream);im.paste(scene(e['scene'],clock),(0,0));d=ImageDraw.Draw(im)
 d.rounded_rectangle((35,24,268,67),radius=21,fill=ink);d.text((55,36),'ENGLISH  /  L2 · A2',font=F(17,True),fill='white')
 d.rounded_rectangle((928,24,1245,67),radius=21,fill=ink);d.text((950,36),'RAIN & THE CITY  ·  PILOT',font=F(16,True),fill='white')
 d.rounded_rectangle((22,422,1258,749),radius=30,fill=cream)
 d.text((56,446),f"0{e['stage']+1}  {stages[e['stage']]}",font=F(19,True),fill=teal)
 status=e['state']
 if e['state']=='따라 말하세요':status+=f"  {max(1,math.ceil(e['duration']-local)):02d}초"
 d.text((946,446),status,font=F(18,True),fill=teal)
 d.line((56,481,1224,481),fill='#d9dfd7',width=1)
 for size in (36,33,30,27):
  font=F(size,True);lines=wrap(d,e['title'],font,1140)
  if len(lines)<3:break
 y=505
 for line in lines:
  x=58; tokens=line.split(' '); hl=e['highlight'].lower().split()
  for token in tokens:
   color=peach if token.lower().strip('.,?') in hl else ink
   d.text((x,y),token+' ',font=font,fill=color);x+=d.textlength(token+' ',font=font)
  y+=size+9
 for line in wrap(d,e['ko'],F(22),1120):d.text((59,y+6),line,font=F(22),fill='#536b6b');y+=29
 if e['rep']:d.text((1083,624),'반복 '+e['rep'],font=F(17),fill=teal)
 if e['state']=='따라 말하세요':
  d.rounded_rectangle((60,632,970,640),radius=4,fill='#dbe5dd')
  d.rounded_rectangle((60,632,60+max(1,int(910*(1-local/e['duration']))),640),radius=4,fill=teal)
 d.line((56,666,1224,666),fill='#d9dfd7')
 for i,name in enumerate(stages):
  x=60+i*196;d.ellipse((x,688,x+8,696),fill=teal if i==e['stage'] else '#c9d2cd');d.text((x+16,683),name,font=F(14,True),fill=teal if i==e['stage'] else '#7a8d88')
 d.text((1070,684),f'{int(clock)//60:02}:{int(clock)%60:02} / {int(total)//60:02}:{int(total)%60:02}',font=F(14),fill=ink)
 d.rectangle((0,716,round(1280*clock/total),720),fill=peach)
 return im
# Assemble audio with fixed sample rate, normalization, and short natural gaps.
sr=22050; audio=[]
for e in E:
 count=round(e['duration']*sr);arr=np.zeros(count,dtype=np.float32)
 if e['clip']:
  a,rate=sf.read(R/'audio'/(e['clip']+'.wav'),dtype='float32');assert rate==sr
  rms=np.sqrt(np.mean(a*a));assert rms>0.001
  a=a*min(.13/rms,.92/max(abs(a)));arr[:len(a)]=a
 audio.append(arr)
sf.write(R/'narration.wav',np.concatenate(audio),sr,subtype='PCM_16')
# The SRT follows visible English captions; no transcript leaks into first listen.
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
subs=[]
for e in E:
 if e['stage']>0:subs.append(f"{len(subs)+1}\n{stamp(e['start'])} --> {stamp(e['end'])}\n{e['title']}\n{e['ko']}\n")
(R/'visible-captions.srt').write_text('\n'.join(subs))
# Reference frames and thumbnail are generated from the same layout.
shots=[]
for stage in range(5):
 e=next(x for x in E if x['stage']==stage and (stage==0 or x['clip'] not in ('understand','shadow','expressions','review')))
 im=frame(e,0,e['start']);im.save(R/f'preview-{stage}.png');shots.append(im.resize((640,360)))
contact=Image.new('RGB',(1280,1080),cream)
for i,im in enumerate(shots):contact.paste(im,((i%2)*640,(i//2)*360))
contact.save(R/'contact-sheet.jpg',quality=93)
thumb=scene(1,0).resize((1280,720));d=ImageDraw.Draw(thumb);d.rounded_rectangle((45,55,915,265),radius=24,fill=cream)
d.text((74,82),'DRINK THE RAIN',font=F(62,True),fill=ink);d.text((78,166),'빗물을 받아들이는 도시',font=F(36,True),fill=teal)
d.text((78,223),'English Listening & Shadowing   ·   A2',font=F(20),fill=ink);thumb.save(R/'thumbnail.png')
fps=12
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','-','-i',str(R/'narration.wav'),'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(R/'rain-learning-pilot.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
idx=0
for n in range(math.ceil(total*fps)):
 t=n/fps
 while idx<len(E)-1 and t>=E[idx]['end']:idx+=1
 p.stdin.write(frame(E[idx],t-E[idx]['start'],t).tobytes())
 if n%(fps*20)==0:print('rendered',round(t), '/',round(total),flush=True)
p.stdin.close();assert p.wait()==0
print('DONE',total,flush=True)
