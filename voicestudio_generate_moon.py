#!/usr/bin/env python3
"""Render the spoken paragraphs of the moon lesson with local VoiceStudio."""
import hashlib
import json
import re
import urllib.error
import urllib.request
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'moon-voicestudio-audio'
source = (ROOT / 'moon-english-video-script.md').read_text()
source = source.split('## 제작 참고', 1)[0]
section = ''
segments = []
for block in re.split(r'\n\s*\n', source):
    lines = block.strip().splitlines()
    spoken = []
    for line in lines:
        if line.startswith('## '):
            section = line[3:]
        elif not line.startswith(('#', '>', '[')) and line.strip():
            spoken.append(line.strip())
    if spoken:
        value = ' '.join(spoken)
        lang = 'ko' if re.search(r'[가-힣]', value) else 'en'
        segments.append({'section': section, 'language': lang, 'text': value})

OUT.mkdir(exist_ok=True)
cache = {}
for index, segment in enumerate(segments, 1):
    key = (segment['language'], segment['text'])
    digest = hashlib.sha256((key[0] + '\0' + key[1]).encode()).hexdigest()[:16]
    filename = f'{digest}-{key[0]}.wav'
    target = OUT / filename
    if key not in cache:
        if not target.exists():
            payload = json.dumps({'model': 'omnivoice', 'input': key[1], 'language': key[0], 'voice': 'demo0001', 'response_format': 'wav'}).encode()
            req = urllib.request.Request('http://localhost:3900/v1/audio/speech', payload, {'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=300) as response:
                    audio = response.read()
            except urllib.error.HTTPError as e:
                raise RuntimeError(f'Clip {index}: HTTP {e.code}: {e.read().decode(errors="replace")}') from e
            temp = target.with_suffix('.tmp')
            temp.write_bytes(audio)
            with wave.open(str(temp), 'rb') as wav:
                if wav.getnframes() == 0:
                    raise ValueError(f'Empty audio for clip {index}')
            temp.rename(target)
        with wave.open(str(target), 'rb') as wav:
            duration = wav.getnframes() / wav.getframerate()
        cache[key] = (filename, duration)
    segment['file'], segment['duration_seconds'] = cache[key]
    segment['index'] = index
    (OUT / 'manifest.json').write_text(json.dumps(segments, ensure_ascii=False, indent=2))
    print(f'{index}/{len(segments)} {key[0]} {segment["duration_seconds"]:.1f}s', flush=True)
print(f'Completed {len(segments)} segments, {len(cache)} unique clips.', flush=True)
