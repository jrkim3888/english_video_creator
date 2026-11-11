from pathlib import Path
import json,subprocess,collections
import numpy as np,soundfile as sf
R=Path(__file__).resolve().parent;L=json.loads((R/'content.json').read_text());E=json.loads((R/'timeline.json').read_text());M=json.loads((R/'audio-manifest.json').read_text())
assert len(L['rows'])==35 and len(L['phrases'])==5
for i in range(len(E)-1):assert abs(E[i]['end']-E[i+1]['start'])<1e-7
for stage in (0,4):assert len([e for e in E if e['stage']==stage and (e.get('clip') or '').startswith('en-')])==35
assert all(e['title']=='Listen to the story.' for e in E if e['stage']==0 and (e.get('clip') or '').startswith('en-'))
assert len(set(e['scene'] for e in E))==7
for num in L['shadow_focus']:assert len([e for e in E if e['stage']==2 and e.get('clip')==f'en-{num:02}'])==2
rms=[]
for key in M:
 a,sr=sf.read(R/'audio'/(key+'.wav'));r=float(np.sqrt(np.mean(a*a)));assert r>.001 and sr==22050;rms.append(r)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-show_entries','stream=codec_name,codec_type,width,height,sample_rate','-of','json',str(R/'rain-english-learning.mp4')]))
assert abs(float(info['format']['duration'])-E[-1]['end'])<.25
subprocess.run(['ffmpeg','-v','error','-i',str(R/'rain-english-learning.mp4'),'-f','null','-'],check=True)
result={'duration_seconds':float(info['format']['duration']),'sentence_count':35,'phrase_count':5,'illustration_count':7,'first_and_last_listen_complete':True,'first_listen_body_hidden':True,'focus_shadow_repetitions':2,'audio_clip_count':len(M),'minimum_clip_rms':min(rms),'full_decode':'passed','streams':info['streams'],'paid_tts_api_calls':0,'human_full_listening_review':False,'independent_source_fact_check':False}
(R/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
