"""Local synthesis with a shared content-addressed cache; never calls a paid API."""
from pathlib import Path
import hashlib,json,shutil
import sherpa_onnx,soundfile as sf
R=Path(__file__).resolve().parent;M=R.parent/'models';A=R/'audio';A.mkdir(exist_ok=True)
CACHE=R.parent/'audio-cache';CACHE.mkdir(exist_ok=True)
models={'en':('vits-piper-en_US-lessac-medium','en_US-lessac-medium.onnx',.72),'ko':('vits-mimic3-ko_KO-kss_low','ko_KO-kss_low.onnx',.82)}
texts=json.loads((R/'spoken-text.json').read_text())
old=json.loads((R.parent/'pilot/audio-manifest.json').read_text())
reuse={}
for key,row in old.items():reuse[(row['language'],row['text'],row['model'],row['speed'])]=R.parent/'pilot/audio'/(key+'.wav')
manifest={};stats={'previous_clip_reuse':0,'cache_hits':0,'generated_unique_clips':0,'paid_api_calls':0}
for lang,(folder,model,speed) in models.items():
 engine=None
 for key,row in texts.items():
  if row['language']!=lang:continue
  text=row['text'];spec={'schema':1,'text':text,'input_type':'text','language':lang,'model':folder,'voice':0,'speed':speed,'engine':'sherpa-onnx','version':sherpa_onnx.__version__}
  digest=hashlib.sha256(json.dumps(spec,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest();cache=CACHE/(digest+'.wav')
  if cache.exists():stats['cache_hits']+=1
  elif (lang,text,folder,speed) in reuse:
   shutil.copy2(reuse[(lang,text,folder,speed)],cache);stats['previous_clip_reuse']+=1
  else:
   if engine is None:
    p=M/folder;cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=str(p/model),tokens=str(p/'tokens.txt'),data_dir=str(p/'espeak-ng-data')),num_threads=2),max_num_sentences=1)
    assert cfg.validate();engine=sherpa_onnx.OfflineTts(cfg)
   out=engine.generate(text,sid=0,speed=speed);tmp=cache.with_suffix('.tmp.wav');sf.write(tmp,out.samples,out.sample_rate,subtype='PCM_16');assert sf.info(tmp).duration>.1;tmp.replace(cache);stats['generated_unique_clips']+=1
  info=sf.info(cache);assert info.samplerate==22050 and info.duration>.1
  shutil.copy2(cache,A/(key+'.wav'))
  manifest[key]={**spec,'cache_key':digest,'duration':info.duration,'sample_rate':info.samplerate,'sha256':hashlib.sha256(cache.read_bytes()).hexdigest()}
  print(key,round(info.duration,2),flush=True)
(R/'audio-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(R/'audio-usage.json').write_text(json.dumps(stats,indent=2));print(stats,flush=True)
