from pathlib import Path
import json, math, re, subprocess, wave
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

root=Path(__file__).resolve().parent
content=json.loads((root/'content.json').read_text()); rows=content['sentences']; phrases=content['phrases']
FF=imageio_ffmpeg.get_ffmpeg_exe(); audio=root/'audio'; frames=root/'frames'; frames.mkdir(exist_ok=True)
rate=44100
regular=root/'fonts'/'NanumGothic-Regular.ttf'; bold=root/'fonts'/'NanumGothic-Bold.ttf'; korean=regular
font=lambda path,size:ImageFont.truetype(path,size)
# Brief meanings for the learning cards; narration contains the full explanations.
meanings=[x['ko'].split('。')[0].split('. ')[0] for x in rows]
highlights=['whether','what if','may','artificial intelligence','surprisingly simple','blood vessels','overall health','identify patterns','early warning signs','combine','does not mean','being developed','reliable evidence','early detection','Instead of','medical attention','healthcare','not just','easy to miss','might']
stages=['LISTEN','UNDERSTAND','SHADOWING','EXPRESSIONS','LISTEN AGAIN']
assets=[root.parent/'illustration.png',root/'research.png',root/'consultation.png']
assets=[p if p.exists() else assets[0] for p in assets]
backgrounds=[ImageOps.fit(Image.open(p).convert('RGB'),(1280,448),method=Image.Resampling.LANCZOS,centering=(.5,.5)) for p in assets]

def duration(name):
 with sf.SoundFile(str(audio/(name+'.wav'))) as f:return len(f)/f.samplerate

events=[]
def add(stage, title, subtitle='', clip=None, seconds=None, index=None, highlight='', state='', bg=0, repeat='', countdown=None):
 d=duration(clip) if clip else seconds
 events.append(dict(stage=stage,title=title,subtitle=subtitle,clip=clip,duration=d,index=index,highlight=highlight,state=state,bg=bg,repeat=repeat,countdown=countdown))
def spoken(stage,title,subtitle,clip,**kw):
 add(stage,title,subtitle,clip=clip,**kw)

def speaking(stage,title,subtitle,clip,repeat,index=None,highlight='',bg=0):
 spoken(stage,title,subtitle,clip,index=index,highlight=highlight,state='LISTEN',bg=bg,repeat=repeat)
 n=max(3,math.ceil(duration(clip)*0.85))
 for remaining in range(n,0,-1):add(stage,title,subtitle,seconds=1,index=index,highlight=highlight,state='SPEAK',bg=bg,repeat=repeat,countdown=remaining)

spoken(0,'Can an Eye Test Reveal Hidden Health Problems?','눈 검사로 건강 문제의 단서를 찾을 수 있을까요?', 'intro',state='WELCOME')
for i,row in enumerate(rows,1):
 spoken(0,'Listen to the story.','영어 자막 없이 이야기의 흐름을 들어 보세요.',f'en-{i:02}',index=i,state='FIRST LISTEN',bg=0 if i<5 else 1 if i<16 else 2)
 add(0,'Listen to the story.','영어 자막 없이 이야기의 흐름을 들어 보세요.',seconds=.35,index=i,state='FIRST LISTEN',bg=0 if i<5 else 1 if i<16 else 2)
spoken(1,'Understand the story.','한 문장씩 듣고 뜻을 확인해 보세요.', 'understand',state='GET READY',bg=1)
for i,row in enumerate(rows,1):
 kw=dict(index=i,highlight=highlights[i-1],bg=0 if i<5 else 1 if i<16 else 2)
 spoken(1,row['en'],meanings[i-1],f'en-{i:02}',state='LISTEN',**kw)
 spoken(1,row['en'],meanings[i-1],f'ko-{i:02}',state='MEANING',**kw)
spoken(2,'Listen, then speak.','문장을 듣고 두 번 따라 말해 보세요.', 'shadow',state='GET READY',bg=1)
for i,row in enumerate(rows,1):
 for rep in (1,2):speaking(2,row['en'], '문장을 듣고 소리 내어 따라 하세요.', f'en-{i:02}',f'{rep:02} / 02',i,highlights[i-1],0 if i<5 else 1 if i<16 else 2)
spoken(3,'Practice useful expressions.','핵심 표현과 예문을 따라 해 보세요.', 'expressions',state='GET READY',bg=1)
for i,(phrase,meaning,example,translation) in enumerate(phrases,1):
 spoken(3,phrase,meaning,f'phrase-{i:02}',index=i,highlight=phrase,state='LISTEN',bg=1)
 spoken(3,phrase,meaning,f'explain-{i:02}',index=i,highlight=phrase,state='MEANING',bg=1)
 speaking(3,example,translation,f'example-{i:02}','01 / 01',i,'',1)
spoken(4,'Listen to the story again.','이번에는 영어 자막을 보며 들어 보세요.', 'final',state='GET READY',bg=2)
for i,row in enumerate(rows,1):
 spoken(4,row['en'],'',f'en-{i:02}',index=i,highlight=highlights[i-1],state='LISTEN',bg=0 if i<5 else 1 if i<16 else 2)
 add(4,row['en'],'',seconds=.35,index=i,highlight=highlights[i-1],state='LISTEN',bg=0 if i<5 else 1 if i<16 else 2)
spoken(4,'Keep practicing!','오늘의 표현을 다시 말하며 복습해 보세요.', 'outro',state='FINISH',bg=2)

# Frame durations come from actual audio, not estimated reading times.
total=sum(e['duration'] for e in events); elapsed=0
print('duration',round(total,1),'events',len(events),flush=True)

def wrap_words(draw,text,f,maxwidth):
 words=text.split(); lines=[]; line=''
 for w in words:
  trial=(line+' '+w).strip()
  if line and draw.textlength(trial,font=f)>maxwidth:lines.append(line);line=w
  else:line=trial
 if line:lines.append(line)
 return lines

def draw_title(draw,text,hl):
 for size in (39,36,32,29,26):
  f=font(bold,size); lines=wrap_words(draw,text,f,1065)
  if len(lines)<=2:break
 y=515 if len(lines)<=2 else 507
 for line in lines:
  # Exact case-insensitive phrase highlighting, including across individual words.
  x=76
  for match in re.finditer(r'\S+\s*',line):
   token=match.group(); raw=token.strip(' ,.:;!?')
   color='#df7954' if raw and raw.lower() in {w.strip(' ,.:;!?').lower() for w in hl.split()} else '#202b2e'
   draw.text((x,y),token,font=f,fill=color,stroke_width=0);x+=draw.textlength(token,font=f)
  y+=size+7
 return y

with sf.SoundFile(str(root/'narration.wav'),'w',samplerate=rate,channels=1,subtype='PCM_16') as out:
 for i,e in enumerate(events):
  if e['clip']:
   data,sr=sf.read(str(audio/(e['clip']+'.wav')),dtype='float32')
   if data.ndim>1:data=data.mean(axis=1)
   if sr!=rate:raise ValueError((e['clip'],sr))
   rms=float(np.sqrt(np.mean(data*data)))
   if rms<1e-5:raise ValueError('silent clip '+e['clip'])
   gain=min(.12/rms, 5.0, .93/max(float(np.max(np.abs(data))),.001))
   out.write(data*gain)
  else:out.write(np.zeros(round(e['duration']*rate),dtype='float32'))
  canvas=Image.new('RGB',(1280,720),'#f7f5f1');canvas.paste(backgrounds[e['bg']],(0,0)); d=ImageDraw.Draw(canvas)
  d.rounded_rectangle((44,28,304,76),radius=24,fill='#263738');d.text((64,43),'THE DAILY LISTEN',font=font(bold,16),fill='white')
  d.rounded_rectangle((1050,28,1235,76),radius=24,fill='#263738');d.text((1070,43),'HEALTH & AI',font=font(bold,16),fill='white')
  d.rounded_rectangle((-4,439,1284,750),radius=35,fill='#f8f6f3')
  d.rounded_rectangle((54,467,60,493),radius=3,fill='#df7954')
  d.text((75,468),f'{e["stage"]+1:02}  {stages[e["stage"]]}',font=font(bold,16),fill='#197c7a')
  d.text((1015,469), (f"SPEAK  {e['countdown']:02}s" if e['countdown'] is not None else e['state']), font=font(bold,16),fill='#197c7a')
  d.line((70,499,1210,499),fill='#dfdfd9',width=1)
  if e['index']:
   n=6 if e['stage']==3 else 20
   d.text((1165,482),f'{e["index"]:02} / {n:02}',font=font(bold,14),fill='#85908d')
  end=draw_title(d,e['title'],e['highlight'])
  if e['subtitle']:
   f=font(korean,19); y=max(638,end+4)
   for line in wrap_words(d,e['subtitle'],f,1090)[:2]:d.text((78,y),line,font=f,fill='#6b7976');y+=23
  if e['repeat']:d.text((1055,652),'REPEAT '+e['repeat'],font=font(bold,15),fill='#197c7a')
  d.line((54,690,1226,690),fill='#dddfd9',width=2)
  d.text((55,693),'LISTEN    ·    UNDERSTAND    ·    SPEAK    ·    EXPRESSIONS    ·    REVIEW',font=font(bold,12),fill='#87908b')
  d.text((1065,693),'ENGLISH LEARNING',font=font(bold,12),fill='#87908b')
  d.rectangle((54,708,1226,713),fill='#d7ddd8');d.rectangle((54,708,54+int(1172*elapsed/total),713),fill='#df7954')
  canvas.save(frames/f'{i:04}.jpg',quality=86,optimize=True)
  elapsed+=e['duration']
(root/'timeline.json').write_text(json.dumps(events,ensure_ascii=False,indent=2))
concat=root/'frames.txt'
with concat.open('w') as f:
 for i,e in enumerate(events):f.write(f"file 'frames/{i:04}.jpg'\noption framerate 1000\nduration {e['duration']:.8f}\n")
 f.write(f"file 'frames/{len(events)-1:04}.jpg'\noption framerate 1000\n")
print('encoding',flush=True)
subprocess.run([FF,'-y','-loglevel','warning','-f','concat','-safe','0','-i',str(concat),'-i',str(root/'narration.wav'),'-vf','fps=10,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','23','-c:a','aac','-b:a','96k','-movflags','+faststart','-shortest',str(root/'eye-health-english-learning.mp4')],check=True)
print('DONE',flush=True)
