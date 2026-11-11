from pathlib import Path
import json, hashlib
import sherpa_onnx, soundfile as sf
R=Path(__file__).resolve().parent
A=R/'audio'; A.mkdir(exist_ok=True)
M=R.parent/'models'
texts={
'intro':('ko','오늘은 도시가 빗물을 어떻게 받아들이는지 알아보겠습니다. 먼저 영어 자막 없이 이야기의 흐름을 들어 보세요.'),
'en1':('en','What if a city could drink the rain?'),
'en2':('en','During a storm, water runs across roads and sidewalks.'),
'en3':('en','It carries dirt and oil toward street drains.'),
'en4':('en','When too much water comes at once, streets may flood.'),
'en5':('en','But there is another way to handle rain.'),
'understand':('ko','이제 문장의 뜻을 확인해 보세요. 도시가 빗물을 마신다는 말은 빗물을 받아들이고 흡수하는 모습을 비유한 표현입니다.'),
'ko1':('ko','도시가 빗물을 마실 수 있다면 어떨까요?'),
'ko2':('ko','폭풍우가 치는 동안 물은 도로와 인도를 따라 흘러갑니다.'),
'shadow':('ko','이번에는 따라 말하기입니다. 문장을 듣고, 말할 차례에 소리 내어 두 번 따라 해 보세요.'),
'en6':('en','In a forest, soil and plants take in rain.'),
'ko6':('ko','숲에서는 흙과 식물이 빗물을 흡수합니다.'),
'expressions':('ko','핵심 표현을 연습해 보겠습니다. 이 표현은 흡수하다, 또는 받아들이다라는 뜻입니다.'),
'phrase':('en','take in'),
'example':('en','Healthy soil can take in rainwater.'),
'example_ko':('ko','건강한 흙은 빗물을 흡수할 수 있습니다. 예문을 듣고 따라 말해 보세요.'),
'limit':('ko','녹지 공간이 모든 홍수를 막는 것은 아닙니다. 도시에는 넘치는 물을 흘려보낼 배수구와 배관도 필요합니다.'),
'limit_en':('en','But green spaces cannot stop every flood.'),
'review':('ko','처음 들었던 문단을 다시 들어 보겠습니다. 이번에는 영어 자막을 보며 내용을 확인해 보세요.'),
'outro':('ko','오늘은 빗물의 흐름과 흡수에 관한 표현을 연습했습니다. 주변의 녹지 공간을 떠올리며 복습해 보세요.')}
(R/'spoken-text.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2))
configs={
'en':('vits-piper-en_US-lessac-medium','en_US-lessac-medium.onnx',0.72),
'ko':('vits-mimic3-ko_KO-kss_low','ko_KO-kss_low.onnx',0.82)}
manifest={}
for lang,(folder,model,speed) in configs.items():
 p=M/folder
 cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(p/model),tokens=str(p/'tokens.txt'),data_dir=str(p/'espeak-ng-data')),num_threads=2),max_num_sentences=1)
 assert cfg.validate()
 engine=sherpa_onnx.OfflineTts(cfg)
 for key,(language,text) in texts.items():
  if language!=lang:continue
  out=A/(key+'.wav')
  cache=A/(key+'.json')
  signature=hashlib.sha256(json.dumps([text,folder,speed,sherpa_onnx.__version__]).encode()).hexdigest()
  if not out.exists() or not cache.exists() or json.loads(cache.read_text())!=signature:
   result=engine.generate(text,sid=0,speed=speed)
   sf.write(out,result.samples,result.sample_rate,subtype='PCM_16')
   cache.write_text(json.dumps(signature))
  info=sf.info(out); assert info.duration>0.1
  manifest[key]={'text':text,'language':lang,'duration':info.duration,'sample_rate':info.samplerate,'model':folder,'speed':speed}
  print(key,round(info.duration,2),flush=True)
(R/'audio-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
