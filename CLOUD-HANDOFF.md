# Codex 클라우드 작업 인계

이 저장소는 영어 학습 영상 제작 프로젝트의 로컬 작업 자료를 담고 있습니다. Codex Cloud에서 저장소를 선택해 작업을 이어갈 수 있습니다. 이 문서는 이전 상태를 기록하며, 클라우드에서 영상 생성이 검증됐다는 뜻은 아닙니다.

## 포함된 자료

- `english-study-video-plan.md`: 영상 제작 계획과 학습·화면 구성 기준.
- `eye-health-video/학습-원고.md`: 눈 건강 영상의 원고와 구성.
- `eye-health-video/full/`: 영상 조립 코드, 실제 사용한 텍스트·타임라인, 이미지 및 기존 MeloTTS 음성 클립.
- `moon-english-video-script.md`: 달 탐사 영어 학습 영상 원고.
- `voicestudio_generate_moon.py`: 로컬 VoiceStudio API를 사용하는 실험 스크립트. VoiceStudio가 실행되는 컴퓨터에 종속됩니다.

## 포함되지 않은 자료

완성 MP4, 조립 중간 프레임과 전체 내레이션 WAV, 참고 영상·이미지, VoiceStudio 샘플 및 로컬 모델·프로그램은 포함하지 않았습니다. 대용량 파일 또는 별도로 재현하거나 이용 권한을 확인해야 하는 자료입니다. 로컬 원본은 유지되어 있습니다.

## 클라우드에서 이어갈 때

1. 기존 결과물과 원고, `eye-health-video/full/제작-기록.md`를 먼저 확인합니다.
2. `build.py`와 `thumbnail.py`는 포함된 Nanum Gothic 글꼴을 사용합니다. 글꼴의 SIL Open Font License 1.1은 `eye-health-video/full/fonts/OFL.txt`, 원본은 https://github.com/google/fonts/tree/main/ofl/nanumgothic 에 있습니다. 한국어·영어 글꼴 표시와 배치는 실제 렌더링으로 확인해야 합니다.
3. `generate_audio.py`의 MeloTTS는 로컬 임시 환경에서 수정해 사용했으며, 설치 재현성이 아직 검증되지 않았습니다. 기존 `audio/`는 영상 조립에 재사용할 수 있습니다.
4. Google Cloud TTS를 우선 시험합니다. 프로젝트·결제 계정 연결, Text-to-Speech API 활성화, 클라우드 실행 환경의 인증과 네트워크 설정이 필요합니다. 모델별 무료 할당량·요금과 상업적 사용 조건을 확인하고, 키나 인증 파일은 저장소에 넣지 않습니다. API 연동은 아직 구현되지 않았습니다.
5. Codex Cloud는 별도 환경이므로 로컬 파일, VoiceStudio, 설치된 플러그인, 인증 정보와 대화 내용이 자동으로 옮겨진다고 가정하지 않습니다.

이전된 자료는 GitHub 저장소의 공개 설정을 따릅니다. 의료 관련 사실관계 및 음성·이미지의 사용 권리는 게시 전에 별도로 확인합니다.

## 기존 음성으로 영상 조립 준비

Python 3.11이 준비된 환경에서 저장소 루트에서 실행합니다.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-render.txt
python eye-health-video/full/build.py
```

기존 음성을 사용해 영상을 조립합니다. FFmpeg는 `imageio-ffmpeg`가 제공하는 바이너리를 사용합니다. 환경에 따라 `soundfile`의 libsndfile 시스템 라이브러리가 필요할 수 있습니다. 이 명령은 `frames/`, `frames.txt`, `narration.wav`, `eye-health-english-learning.mp4`와 `timeline.json`을 생성하거나 덮어쓰므로 기존 결과물은 먼저 보관하세요. `timeline.json`은 버전 관리 대상이므로 실행 후 diff를 확인하세요. macOS 임시 환경에서는 의존성 설치와 썸네일 렌더링을 확인했지만, Linux에서의 전체 빌드와 패키지 버전 조합은 아직 검증되지 않았습니다.

## Google Cloud TTS 연결 계획

1. Google Cloud 프로젝트에 결제 계정을 연결하고 Cloud Text-to-Speech API를 활성화합니다. 예산 알림과 모델별 무료 사용량·요금을 확인합니다.
2. 로컬 개발에는 Google Cloud CLI의 Application Default Credentials(ADC)를 사용할 수 있습니다. 클라우드 작업 환경에서는 해당 환경에 맞는 단기 인증 또는 비밀 관리 방식을 설정합니다. 사용자 로컬 ADC 파일을 저장소에 복사하지 않습니다.
3. 원고를 영어·한국어 문장으로 분리하고 적합한 음성을 사용합니다. 동일한 텍스트와 설정은 생성 파일을 재사용해 호출을 줄입니다. 샘플 청취 후 본편을 생성합니다.
4. 이 저장소에는 현재 Google TTS 호출 코드·인증·환경변수 설정이 없습니다. 향후 연결 작업에서 클라우드 네트워크 접근, 인증, 모델 선택, 출력 파일 검증 및 실패 처리를 구현하고 소량의 샘플로 검증해야 합니다.

공식 안내: https://cloud.google.com/text-to-speech/docs/get-started , https://cloud.google.com/text-to-speech/docs/authentication , https://cloud.google.com/text-to-speech/pricing
