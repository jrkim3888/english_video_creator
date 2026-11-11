from pathlib import Path
import json,re
R=Path(__file__).resolve().parent;P=R.parent
raw=(P/'script.md').read_text().split('Level: L2 / A2')[1].strip();paras=raw.split('\n\n')
notes=(P/'study-notes.md').read_text(); ko_part=notes.split('## 전체 한국어 해석')[1].split('## 핵심 표현')[0]; ko_paras=re.findall(r'### 문단 \d+\s*\n(.*?)(?=\n### |\Z)',ko_part,re.S)
highlights=['What if','runs across','carries','at once','handle rain','Hard surfaces','take in','entering','faster','runoff','green infrastructure','using','rain garden','lower','some','special pavement','pass through','hold','may','Plants on roofs','more than','pollution','some','cooler','several jobs','cannot','very strong','regular care','still need','together','Next time','beside','more slowly','cannot','make more room for']
rows=[]
for p,(en,ko) in enumerate(zip(paras,ko_paras)):
 ens=re.split(r'(?<=[.!?])\s+',en.strip());kos=re.split(r'(?<=[.!?])\s+',ko.strip());assert len(ens)==len(kos)==5
 for j,(e,k) in enumerate(zip(ens,kos)):
  i=len(rows);scene=['city','city','rain-garden','pavement','benefits','care','rain-garden'][p]
  if p==1 and j==1:scene='forest'
  if p==3 and j==4:scene='roof'
  rows.append({'id':i+1,'paragraph':p+1,'en':e,'ko':k,'scene':scene,'highlight':highlights[i]})
assert len(rows)==35
phrases=[
{'en':'handle rain','ko':'빗물을 처리하다','example':'We need a better way to handle rain.','translation':'우리는 빗물을 처리할 더 나은 방법이 필요합니다.','scene':'city','explain':'첫 번째 표현은 빗물을 처리하다라는 뜻입니다. 처리하는 대상이 비나 빗물일 때 쓸 수 있습니다.','prompt':'빗물을 처리할 더 나은 방법이 필요하다고 말해 보세요.'},
{'en':'take in','ko':'흡수하다 · 받아들이다','example':'Healthy soil can take in rainwater.','translation':'건강한 흙은 빗물을 흡수할 수 있습니다.','scene':'forest','explain':'두 번째 표현은 흡수하다, 또는 받아들이다라는 뜻입니다. 여기서는 흙과 식물이 빗물을 흡수하는 모습을 나타냅니다.','prompt':'건강한 흙은 빗물을 흡수할 수 있다고 말해 보세요.'},
{'en':'pass through','ko':'통과하다','example':'Water can pass through this special pavement.','translation':'물은 이 특수 포장재를 통과할 수 있습니다.','scene':'pavement','explain':'세 번째 표현은 통과하다라는 뜻입니다. 물이 표면 위로만 흐르는 것이 아니라, 포장재의 틈을 지나가는 모습입니다.','prompt':'물이 이 특수 포장재를 통과할 수 있다고 말해 보세요.'},
{'en':'more than','ko':'~이상의 · ~뿐만 아니라','example':'This park does more than look beautiful.','translation':'이 공원은 아름답게 보이는 것 이상의 역할을 합니다.','scene':'benefits','explain':'네 번째 표현은 무엇 이상의, 또는 무엇뿐만 아니라라는 뜻입니다. 예문에서는 공원이 보기 좋은 것 외에도 다른 역할을 한다고 말합니다.','prompt':'이 공원은 아름답게 보이는 것 이상의 일을 한다고 말해 보세요.'},
{'en':'make more room for','ko':'~을 위한 공간을 더 마련하다','example':'We can make more room for trees.','translation':'우리는 나무를 위한 공간을 더 마련할 수 있습니다.','scene':'rain-garden','explain':'마지막 표현은 무엇을 위한 공간을 더 마련하다라는 뜻입니다. 이 문맥에서 공간은 실제 장소를 가리킵니다.','prompt':'우리는 나무를 위한 공간을 더 마련할 수 있다고 말해 보세요.'}]
commentary=[
'첫 문장의 도시는 실제로 물을 마시는 것이 아닙니다. 빗물을 받아들이는 모습을 비유하고 있습니다. 한꺼번에 많은 물이 몰릴 때 거리가 침수될 수 있다는 점에 주목하세요.',
'이 문단은 숲과 도시를 비교합니다. 흙과 식물은 비를 흡수하지만, 지붕과 도로는 물이 땅속으로 들어가는 것을 막습니다. 지표면을 따라 흐르는 물을 유출수라고 합니다.',
'빗물 정원은 주변 지면보다 낮게 만들어집니다. 물을 모아 일부가 흙으로 스며들도록 하는 것이 핵심입니다. 모든 물이 반드시 땅속으로 들어간다는 뜻은 아닙니다.',
'투수성 포장 아래의 자갈은 물을 잠시 머금습니다. 물의 일부는 땅으로 스며들고, 넘치는 물은 설계에 따라 배관으로 이동할 수 있습니다. 녹화 지붕도 비를 받아 머금을 수 있습니다.',
'녹지 공간은 빗물의 양과 흐름을 다루는 것 외에도 여러 역할을 할 수 있습니다. 흙은 오염물질 일부를 거르는 데 도움이 되고, 나무는 거리를 더 시원하게 만들 수 있습니다.',
'이 문단은 해결책의 한계를 설명합니다. 매우 강한 비에는 녹지 공간만으로 충분하지 않을 수 있습니다. 좋은 설계와 꾸준한 관리, 그리고 배수구와 배관이 함께 필요합니다.',
'마지막 문장은 앞에서 나온 도시를 가리킵니다. 비 자체를 통제할 수는 없지만, 빗물이 머물 공간을 더 만들 수 있다는 뜻입니다. 정원과 포장재를 주변에서 찾아보라는 제안으로 글을 마칩니다.']
prompts={
'intro':'안녕하세요. 오늘은 도시가 빗물을 어떻게 받아들일 수 있는지 영어로 알아보겠습니다. 전체 이야기를 듣고, 문장의 뜻을 확인하고, 직접 따라 말해 보겠습니다. 먼저 영어 자막 없이 흐름에 집중해 보세요.',
'understand':'이제 한 문장씩 뜻을 살펴보겠습니다. 영어 문장을 듣고 한국어 뜻을 확인하세요. 문단이 끝나면 핵심 내용을 정리해 드리겠습니다.',
'shadow':'이번에는 따라 말하기입니다. 문장을 들은 뒤 말할 차례에 소리 내어 따라 하세요. 화면에 남은 시간이 표시됩니다. 핵심 문장은 한 번 더 연습하겠습니다.',
'expressions':'이제 학습노트의 핵심 표현 다섯 개를 연습하겠습니다. 뜻과 예문을 확인하고, 한국어 뜻을 보고 영어로 말해 보세요.',
'final':'전체 이야기를 다시 들어 보겠습니다. 이번에는 영어 자막을 보면서 내용을 확인해 보세요. 처음보다 어떤 표현이 더 잘 들리는지 살펴보세요.',
'outro':'오늘은 도시의 빗물 관리에 관한 영어를 연습했습니다. 흙과 식물의 흡수, 물이 통과하는 포장재, 그리고 녹지 공간과 배수시설의 협력을 기억해 보세요. 핵심 표현을 일상에서도 소리 내어 말하며 복습해 보세요. 함께해 주셔서 감사합니다.'}
texts={}
def put(key,lang,text):texts[key]={'language':lang,'text':text}
for row in rows:put(f'en-{row["id"]:02}','en',row['en']);put(f'ko-{row["id"]:02}','ko',row['ko'])
for i,c in enumerate(commentary,1):put(f'note-{i}','ko',c)
for k,v in prompts.items():put(k,'ko',v)
for i,p in enumerate(phrases,1):
 for key,lang,text in [('phrase','en',p['en']),('example','en',p['example']),('explain','ko',p['explain']),('translation','ko',p['translation']),('recall','ko',p['prompt'])]:put(f'{key}-{i}',lang,text)
lesson={'title':'How Cities Learn to Drink the Rain','level':'L2 / A2','style':'현대적 편집 일러스트','rows':rows,'phrases':phrases,'paragraph_notes':commentary,'prompts':prompts,'shadow_focus':[1,7,17,26,35]}
(R/'content.json').write_text(json.dumps(lesson,ensure_ascii=False,indent=2));(R/'spoken-text.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2))
s=['# 빗물을 받아들이는 도시 — 학습 대본과 스토리보드','','이미지 7개를 먼저 제작하고 문장·학습 단계를 연결했다. 현대적 편집 일러스트, 청록·세이지·벽돌색·코랄 포인트. 원문 35문장과 학습노트의 해석·표현을 반영한다.','','## 학습 순서','','도입과 자막 없는 첫 듣기 → 문장별 이해와 문단 해설 → 전체 문장 섀도잉 및 핵심 문장 복습 → 표현 5개·예문·회상 발화 → 영어 자막과 다시 듣기 → 마무리','','## 문장별 대본','','| 번호 | 이미지 ID | 영어 | 한국어 |','| --- | --- | --- | --- |']
for row in rows:s.append(f'| {row["id"]} | {row["scene"]} | {row["en"]} | {row["ko"]} |')
s+=['','## 문단 해설','']
for i,c in enumerate(commentary,1):s+=['### 문단 '+str(i),'',c,'']
s+=['## 핵심 표현','']
for p in phrases:s+=[f'### {p["en"]} — {p["ko"]}','',p['explain'],'',p['example'],'',p['translation'],'',p['prompt'],'']
s+=['## 단계 안내','']
for k,v in prompts.items():s+=[f'### {k}','',v,'']
s+=['## 이미지 사용과 움직임','','도시 유출수(city) → 숲(forest) → 빗물 정원(rain-garden) → 투수성 포장(pavement) → 녹화 지붕(roof) → 녹지 편익(benefits) → 관리와 배수(care). 문장 내용에 맞춰 교체하고 상단 이미지에 완만한 이동을 적용한다. 하단 카드는 고정한다. 투수성 포장의 단면은 작동 원리를 설명하는 연출이며 특정 시설의 시공도면이 아니다.','','## 출처와 검수','','원문 및 사실 확인 출처는 ../study-notes.md를 따른다. 해당 문서의 기관 페이지 날짜와 독립 사실 검증을 이번 제작에서 다시 완료했다고 주장하지 않는다. 특정 도시의 실제 사례나 정량 효과를 추가하지 않는다. 녹지가 모든 홍수를 막는다는 표현을 사용하지 않는다. 정확한 시간표는 음성 길이를 측정한 뒤 timeline.json과 chapters.md에 기록한다.']
(R/'학습-원고와-스토리보드.md').write_text('\n'.join(s))
print('prepared',len(rows),'sentences',len(texts),'voice entries')
