import json,re,sys
from pathlib import Path
from melo.api import TTS

base=Path(__file__).resolve().parent
text=(base.parent/'학습-원고.md').read_text()
part=text.split('## 본문과 문장별 해설')[1].split('## 섀도잉')[0]
rows=re.findall(r'\d+\. \*\*(.*?)\*\*\s*\n\s*(.*?)(?=\n\d+\. |\Z)',part,re.S)
assert len(rows)==20,len(rows)
items=[]
for en,ko in rows:
 ko=re.sub(r'\*(.*?)\*',r'\1',ko).strip()
 items.append({'en':en,'ko':ko})
phrases=[('What if ...?', '만약 ~라면 어떨까요?', 'What if we could detect a problem earlier?', '문제를 더 일찍 발견할 수 있다면 어떨까요?'),('identify patterns', '패턴을 찾아내다.', 'Researchers use data to identify patterns.', '연구자들은 데이터를 사용해 패턴을 찾아냅니다.'),('early warning signs', '초기 경고 신호.', 'Doctors look for early warning signs of disease.', '의사들은 질병의 초기 경고 신호를 살핍니다.'),('combine A with B', 'A와 B를 결합하다.', 'The team combined images with health data.', '연구팀은 영상과 건강 데이터를 결합했습니다.'),('instead of -ing', '~하는 대신에.', 'Instead of guessing, ask a professional.', '추측하는 대신 전문가에게 물어보세요.'),('easy to miss', '놓치기 쉬운.', 'Small changes can be easy to miss.', '작은 변화는 놓치기 쉬울 수 있습니다.')]
# Avoid having the Korean voice pronounce English expressions.
phrase_ko=['첫 번째 표현은 만약 무엇이라면 어떨까요, 라는 뜻입니다.','두 번째 표현은 패턴을 찾아내다, 라는 뜻입니다.','세 번째 표현은 초기 경고 신호라는 뜻입니다.','네 번째 표현은 에이와 비를 결합하다, 라는 뜻입니다.','다섯 번째 표현은 무엇을 하는 대신에, 라는 뜻입니다.','마지막 표현은 놓치기 쉬운, 이라는 뜻입니다.']
for row in items:
 row['ko']=re.sub(r'[A-Za-z][A-Za-z .?,-]*?(?=는|은|의|가|를|을|과|와|부터|\s|$)', '', row['ko'])
 row['ko']=re.sub(r'\s+', ' ',row['ko']).strip()
# Korean explanations are separately authored to keep spoken Korean clean.
ko_lines=[
'안과에 가면 보통 안경이 필요한지, 눈이 건강한지 확인하게 될 거라고 생각합니다. 이 문장에는 무엇인지 아닌지를 나타내는 표현이 나옵니다.',
'그런데 눈 검사가 몸 전체의 건강에 관해 무언가를 알려 줄 수 있다면 어떨까요? 이 표현은 새로운 가능성을 제안합니다.',
'영국의 연구자들이 이를 가능하게 할 수도 있는 기술을 개발하고 있습니다. 조동사는 확정이 아닌 가능성을 나타냅니다.',
'선덜랜드 대학교의 연구 프로젝트는 정기 눈 검사에서 촬영한 영상을 인공지능으로 분석할 계획입니다.',
'아이디어는 놀라울 만큼 단순합니다.',
'눈 뒤쪽에는 아주 작은 혈관과 신경 조직이 있습니다.',
'이런 구조의 변화는 때때로 전반적인 건강에 관한 중요한 정보를 제공할 수 있습니다.',
'연구자들은 인공지능이 사람이 알아채기 어려울 수 있는 패턴을 찾아내기를 기대합니다.',
'예를 들어 이런 패턴은 의사가 당뇨병이나 심장 질환의 초기 경고 신호를 알아보는 데 도움이 될 수 있습니다.',
'이 프로젝트는 눈 영상과 다른 건강 정보도 결합해 연구자들이 잠재적인 건강 위험을 이해하도록 도울 예정입니다.',
'그렇지만 이것이 인공지능이 사진 한 장으로 모든 질병을 이미 진단할 수 있다는 뜻은 아닙니다.',
'이 기술은 아직 개발과 시험이 진행 중입니다.',
'의사들이 일상적인 진료에 이 기술을 널리 사용하려면 먼저 믿을 만한 근거가 필요합니다.',
'연구가 성공한다면 조기 발견이 더 편리해질 수 있습니다.',
'심각한 증상이 나타날 때까지 기다리는 대신, 의사들이 일부 건강 문제를 더 일찍 발견하고 추가 검사를 권할 수도 있습니다.',
'이는 환자가 더 이른 단계에서 진료를 받는 데 도움이 될 수 있습니다.',
'또한 인공지능이 미래의 의료를 어떻게 바꿀 수 있는지 보여 줍니다.',
'인공지능은 로봇이나 챗봇에 관한 것만은 아닙니다.',
'때로는 의료 전문가들이 놓치기 쉬운 중요한 정보를 알아보도록 돕는 것이 가장 가치 있는 역할일 수 있습니다.',
'미래에는 간단한 눈 검사가 우리가 예상하는 것보다 훨씬 많은 것을 알려 줄지도 모릅니다.']
for row,ko in zip(items,ko_lines):row['ko']=ko
prompts={
'intro':'안녕하세요. 오늘은 눈 검사가 우리 몸의 건강에 어떤 단서를 줄 수 있는지 영어로 알아보겠습니다. 먼저 자막 없이 편하게 들어 보세요.',
'understand':'이제 한 문장씩 뜻을 살펴보겠습니다. 영어 문장을 듣고 한국어 설명을 확인해 보세요.',
'shadow':'이번에는 섀도잉입니다. 문장을 듣고 말할 차례에 소리 내어 두 번 따라 해 보세요.',
'expressions':'다음은 핵심 표현 연습입니다. 표현과 예문을 듣고 직접 따라 말해 보세요.',
'final':'이제 전체 이야기를 다시 들어 보겠습니다. 이번에는 영어 자막을 보며 내용을 확인해 보세요.',
'outro':'오늘은 눈 검사와 건강 연구에 관한 영어를 연습했습니다. 중요한 표현을 다시 말해 보며 복습해 보세요. 함께해 주셔서 감사합니다.'}
(base/'content.json').write_text(json.dumps({'sentences':items,'phrases':phrases,'prompts':prompts},ensure_ascii=False,indent=2))
texts={'EN':{},'KR':{}}
for i,row in enumerate(items,1):
 texts['EN'][f'en-{i:02}']=row['en']; texts['KR'][f'ko-{i:02}']=row['ko']
for k,v in prompts.items(): texts['KR'][k]=v
for i,(phrase,meaning,example,translation) in enumerate(phrases,1):
 texts['EN'][f'phrase-{i:02}']=phrase.replace(' ...?','?').replace(' -ing','')
 texts['EN'][f'example-{i:02}']=example
 texts['KR'][f'explain-{i:02}']=phrase_ko[i-1]+' '+translation
for language in ('EN','KR'):
 model=TTS(language=language,device='cpu')
 speaker=model.hps.data.spk2id['EN-US' if language=='EN' else 'KR']
 for name,text in texts[language].items():
  out=base/'audio'/f'{name}.wav'
  if out.exists() and out.stat().st_size>44:continue
  print('GENERATING',name,flush=True)
  model.tts_to_file(text,speaker,str(out),speed=0.95 if language=='EN' else 1.0,quiet=True)
