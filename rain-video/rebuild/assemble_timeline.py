from pathlib import Path
import json,math
R=Path(__file__).resolve().parent;L=json.loads((R/'content.json').read_text());M=json.loads((R/'audio-manifest.json').read_text());rows=L['rows'];E=[]
def add(stage,title,ko='',clip=None,scene='rain-garden',state='듣기',index=None,highlight='',rep='',duration=None,**kw):
 duration=M[clip]['duration']+.25 if clip else duration
 assert duration and duration>0
 E.append(dict(stage=stage,title=title,ko=ko,clip=clip,scene=scene,state=state,index=index,highlight=highlight,rep=rep,duration=duration,**kw))
def turn(stage,title,ko,clip,scene,highlight='',rep='',index=None):
 add(stage,title,ko,clip,scene,'먼저 들으세요',index,highlight,rep)
 speaking(stage,title,ko,clip,scene,highlight,rep,index)
def speaking(stage,title,ko,clip,scene,highlight='',rep='',index=None):
 n=max(4,math.ceil(M[clip]['duration']*1.25))
 for remaining in range(n,0,-1):add(stage,title,ko,scene=scene,state='따라 말하세요',index=index,highlight=highlight,rep=rep,duration=1,countdown=remaining,speak_total=n)
add(0,L['title'],'빗물을 받아들이는 도시','intro',state='학습 안내')
for row in rows:add(0,'Listen to the story.','영어 자막 없이 이야기의 흐름을 들어 보세요.',f'en-{row["id"]:02}',row['scene'],index=row['id'])
add(1,'Understand the story.','한 문장씩 뜻을 확인하고 문단의 핵심을 정리해 보세요.','understand',state='단계 안내')
for row in rows:
 for lang in ('en','ko'):add(1,row['en'],row['ko'],f'{lang}-{row["id"]:02}',row['scene'],'영어 듣기' if lang=='en' else '한국어 뜻',row['id'],row['highlight'])
 if row['id']%5==0:add(1,f'Paragraph {row["paragraph"]} · Key idea',L['paragraph_notes'][row['paragraph']-1].split('. ')[0]+'.',f'note-{row["paragraph"]}',row['scene'],'핵심 정리')
add(2,'Listen. Then speak.','전체 문장을 연습한 뒤 학습노트의 핵심 문장을 복습합니다.','shadow',state='연습 안내')
for row in rows:turn(2,row['en'],'문장을 듣고 남은 시간 동안 소리 내어 따라 하세요.',f'en-{row["id"]:02}',row['scene'],row['highlight'],'1 / 2' if row['id'] in L['shadow_focus'] else '1 / 1',row['id'])
for num in L['shadow_focus']:
 row=rows[num-1];turn(2,row['en'],row['ko'],f'en-{num:02}',row['scene'],row['highlight'],'2 / 2',num)
add(3,'Five useful expressions.','뜻과 예문을 확인하고, 뜻을 보고 영어로 말해 보세요.','expressions',state='단계 안내')
for i,p in enumerate(L['phrases'],1):
 add(3,p['en'],p['ko'],f'phrase-{i}',p['scene'],'표현 듣기',highlight=p['en'])
 add(3,p['en'],p['ko'],f'explain-{i}',p['scene'],'표현 이해',highlight=p['en'])
 add(3,p['example'],p['translation'],f'translation-{i}',p['scene'],'예문 뜻',highlight=p['en'])
 turn(3,p['example'],p['translation'],f'example-{i}',p['scene'],p['en'],'1 / 1')
 add(3,'Say it in English.',p['translation'],f'recall-{i}',p['scene'],'뜻을 보고 말하기')
 n=max(5,math.ceil(M[f'example-{i}']['duration']*1.5))
 for remaining in range(n,0,-1):add(3,'Say it in English.',p['translation'],scene=p['scene'],state='영어로 말하세요',duration=1,countdown=remaining,speak_total=n)
 add(3,p['example'],p['translation'],f'example-{i}',p['scene'],'답 확인',highlight=p['en'])
add(4,'Listen to the story again.','영어 자막을 보며 처음보다 더 잘 들리는 표현을 찾아보세요.','final',state='단계 안내')
for row in rows:add(4,row['en'],'',f'en-{row["id"]:02}',row['scene'],'다시 듣기',row['id'],row['highlight'])
add(4,'Make more room for rain.','오늘의 표현을 소리 내어 말하며 복습해 보세요.','outro',scene='benefits',state='마무리')
t=0
for e in E:e['start']=t;t+=e['duration'];e['end']=t
(R/'timeline.json').write_text(json.dumps(E,ensure_ascii=False,indent=2));print('total',round(t,2),'minutes',round(t/60,2),'events',len(E))
for i in range(5):print(i,round(sum(e['duration'] for e in E if e['stage']==i),2))
def stamp(v):
 ms=round(v*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
subs=[]
for e in E:
 if e['stage']>0 and not e.get('countdown'):
  subs.append(f"{len(subs)+1}\n{stamp(e['start'])} --> {stamp(e['end'])}\n{e['title']}\n{e['ko']}\n")
(R/'visible-captions.srt').write_text('\n'.join(subs))
chap=[]
for i,name in enumerate(['도입과 첫 듣기','문장별 이해','섀도잉','표현 연습','다시 듣기와 마무리']):
 e=next(x for x in E if x['stage']==i);chap.append(f"{int(e['start'])//60:02}:{int(e['start'])%60:02} {name}")
(R/'chapters.md').write_text('# 영상 챕터\n\n'+'\n\n'.join(chap))
