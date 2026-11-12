# How Cities Learn to Drink the Rain — 제작 예시

수정된 작업 플랜을 적용한 **19분 20초 영어 학습 영상**과 이전 **2분 20초 시범 영상**을 함께 보존합니다. 난이도는 원고에 명시된 **L2 / A2**입니다.

## 신규 제작 참고 샘플

다음 영상 제작 시 [최신 영어 안내 샘플 영상](transparent-title/rain-english-learning.mp4)과 [썸네일](transparent-title/thumbnail.png)을 먼저 살펴봅니다. [학습 원고](transparent-title/학습-원고.md)와 [제작 기록](transparent-title/제작-기록.md)도 함께 보관합니다. 이 샘플의 청록색 강조는 다른 글자색과 비슷하다는 피드백이 있으므로, 새 영상은 작업 지침에 따라 분위기에 어울리면서 다른 화면 요소와 구별되는 색을 선택합니다. 전체 음성의 직접 청취 검수는 아직 완료하지 않았습니다.

## 먼저 볼 자료

| 자료 | 본편 | 이전 시범 |
| --- | --- | --- |
| 영상 | [19분 20초 MP4](rebuild/rain-english-learning.mp4) | [2분 20초 MP4](pilot/rain-learning-pilot.mp4) |
| 썸네일 | [PNG](rebuild/thumbnail.png) | [PNG](pilot/thumbnail.png) |
| 단계별 화면 | [연락 인화지](rebuild/contact-sheet.jpg) | [연락 인화지](pilot/contact-sheet.jpg) |
| 학습 대본·스토리보드 | [본편 대본](rebuild/학습-원고와-스토리보드.md) | [시범 스토리보드](pilot/storyboard.md) |
| 제작·출처 기록 | [본편 기록](rebuild/제작-기록.md) | [시범 기록](pilot/제작-기록.md) |
| 자막 | [SRT](rebuild/visible-captions.srt) | [SRT](pilot/visible-captions.srt) |

GitHub에서 영상이 바로 재생되지 않으면 해당 파일의 **Download raw file**로 내려받아 재생하세요. 이 예시는 Git LFS 포인터가 아닌 실제 파일로 커밋되어 있어 별도의 LFS 다운로드가 필요하지 않습니다.

## 포함한 자료

- 입력 원고와 학습노트: [script.md](script.md), [study-notes.md](study-notes.md)
- 본편: 장면 일러스트 7개·프롬프트·화풍 선택 기록, 썸네일과 편집 설정, 문장별 오디오 108개와 전체 내레이션, 자막, 타임라인, 챕터, 학습 대본, 제작 소스, 카드·배경 등 조립 중간 산출물, 검사 결과와 실행 로그
- 시범: 영상·썸네일·음성·화면·소스·타임라인·기록과 라이선스 사본
- `artifact-manifest.json`: 예시 파일들의 크기와 SHA-256. 파일 자체와 무결성 검사 스크립트는 자기 참조를 피하기 위해 목록에서 제외합니다.

`models/`의 외부 TTS 모델·압축 파일, `audio-cache/`의 중복 캐시, Python 가상환경은 포함하지 않습니다. 완성 영상 보기와 저장된 음성으로 재조립하는 데에는 모델 다운로드나 TTS 인증이 필요하지 않습니다.

## 다른 PC에서 가져오기

이 예시는 `work` 브랜치에 있습니다. 기존 체크아웃에 미커밋 작업이 있다면 먼저 보관하세요.

```sh
git clone --branch work https://github.com/jrkim3888/english_video_creator.git
cd english_video_creator
python3 rain-video/verify_artifacts.py
```

기존 저장소라면 `git fetch origin` 후 `work` 브랜치의 최신 커밋을 가져옵니다. 위의 `rebuild/`·`pilot/` 링크와 경로는 이 README 기준의 상대 경로입니다.

## 기존 음성으로 본편 다시 조립하기

저장소 루트에서 실행합니다. Python 3.12와 시스템 `ffmpeg`, `ffprobe`가 필요합니다. Windows에서는 환경에 따라 `python3` 대신 `python`을 사용하세요.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r rain-video/rebuild/requirements-render.txt
.venv/bin/python rain-video/rebuild/render.py
.venv/bin/python rain-video/rebuild/thumbnail.py
.venv/bin/python rain-video/rebuild/verify.py
```

Windows의 가상환경 Python 경로는 `.venv\Scripts\python.exe`입니다. FFmpeg는 해당 OS의 설치 방법으로 설치하고 PATH에서 실행 가능하게 준비합니다. 재조립은 기존 MP4·카드·배경·내레이션·화면 예시를 덮어쓰므로 비교할 원본은 먼저 복사해 두세요. 재조립 후에는 파일 체크섬이 달라질 수 있습니다. 다른 PC에서의 전체 실행은 아직 검증하지 않았습니다.

대본을 바꾸어 **새 음성을 생성**하려면 `generate_audio.py`가 참조하는 모델 두 개를 별도로 준비해야 합니다. 다운로드 출처와 실행 순서는 [본편 제작 기록](rebuild/제작-기록.md)에 있습니다. `prepare_lesson.py`는 대본을, `assemble_timeline.py`는 실측 음성 기준 시간표를 다시 만듭니다.

## 검수와 이용조건

본편은 전체 디코딩, 원고 35문장·표현 5개·이미지 7개, 오디오 신호와 주요 화면 배치 검사를 통과했습니다. 전체 사람 청취를 통한 발음·자연스러움 검수와 독립 사실 확인은 완료하지 않았습니다.

한국어 Mimic3 KSS low와 영어 Piper lessac medium을 무료 로컬 실행했으며, 이 결과에 Google TTS나 MeloTTS는 사용하지 않았습니다. 모델·폰트·자료 이용조건 및 공개 전 남은 확인 항목은 제작 기록과 [라이선스 사본](pilot/licenses/)을 함께 참고하세요.
