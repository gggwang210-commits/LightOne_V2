# LIGHT ONE V2 — PT 의사결정지원 서비스 Django MVP

> **프로의 기준, 이제는 데이터입니다.**  
> Data-Driven, Evidence-Based Personal Training

---

## 이 프로젝트는 무엇인가요?

LIGHT ONE은 PT(퍼스널 트레이닝) 현장에서 회원의 운동 기록, 통증 수치(NRS), 운동자각도(RPE), 자세 관찰 데이터를 구조화하여 트레이너의 판단을 보조하는 **데이터 기반 PT 의사결정지원 서비스**입니다.

- AI가 트레이너를 대체하는 것이 아니라, **트레이너의 판단을 보조**합니다.
- 의료적 진단·치료·처방을 대체하지 않습니다.
- 현재 버전은 **가상 데이터(더미 데이터)** 기반의 MVP입니다.

---

## 처음 실행하는 분은 여기부터!

**👉 `docs/초보자_실행가이드.md` 파일을 먼저 읽어주세요!**

Python 설치부터 서버 실행까지 따라할 수 있도록 Windows 기준으로 단계별 설명이 정리되어 있습니다.

---

## 현재 기준 실행 경로

| 항목 | 최신 기준 |
|---|---|
| Django 프로젝트 폴더 | `lightone_v2_django` |
| 패키지 목록 | `requirements.txt` |
| 실행 파일 | `manage.py` |
| 더미 데이터 명령 | `python manage.py seed_lightone` |
| 접속 URL | `http://127.0.0.1:8000/lightone/` |

> 구버전 안내: 예전 문서의 `lightone_django`, `lightone_django_complete.zip`, `LIGHTONE_V2_Complete.zip`, `python setup_dummy.py`, `http://127.0.0.1:8000` 안내는 현재 기준으로는 위 표를 따르세요.

---

## 빠른 시작 (이미 Python이 설치된 분)

```bash
# 저장소 루트에서 시작했다면 Django 폴더로 이동
cd lightone_v2_django

# 1. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
                            # Windows CMD: .venv\Scripts\activate.bat

# 2. 패키지 설치
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. DB 세팅 및 더미 데이터 입력
python manage.py migrate
python manage.py seed_lightone

# 4. 서버 실행
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/lightone/` 접속

---

## 기본 계정 (`seed_lightone` 기준)

| 역할 | 아이디 | 비밀번호 |
|------|--------|----------|
| 관리자/트레이너 | `admin` | `admin` |
| 회원 | `member1` | `1234` |
| 회원 | `member2` | `1234` |

---

## 주요 기능

| 기능 | URL | 설명 |
|------|-----|------|
| 로그인 | `/accounts/login/` | 회원/트레이너 계정 분리 |
| 대시보드 | `/lightone/` | 회원 목록 및 QS 현황 |
| 세션 입력 | `/lightone/session/new/` | 운동 기록, 통증, RPE 입력 |
| 리포트 | `/lightone/report/<id>/` | 회원별 상세 리포트 |
| 관리자 | `/admin/` | Django 관리자 페이지 |

---

## 위험 라우팅 기준 (AUTO / REVIEW / BLOCK)

| 라우팅 | 조건 | 의미 |
|--------|------|------|
| **AUTO** (초록) | NRS < 4 & QS ≥ 70 | 일반 진행 가능 |
| **REVIEW** (노랑) | NRS 4–6 또는 QS 40–70 | 트레이너 검토 필요 |
| **BLOCK** (빨강) | NRS ≥ 7 또는 QS < 40 | 안전상 중단 권고 신호 (의료 진단 아님) |

> BLOCK은 의료적 진단이 아니라 안전 신호입니다. 최종 판단은 트레이너가 합니다.

---

## 포함된 문서 목록 (`docs/` 폴더)

| 문서 | 내용 |
|------|------|
| `초보자_실행가이드.md` | Python 설치부터 서버 실행까지 단계별 안내 |
| `프로젝트_구조_설명.md` | 폴더/파일 구조 및 핵심 개념 설명 |
| `기능_개발_가이드.md` | 다음 기능 추가 방법 (대시보드, PDF 리포트 등) |
| `전략서_및_인포그래픽/` | 사업 기획 문서 및 인포그래픽 Rev.5 |

---

## 기술 스택

- **Backend:** Python 3.11 + Django 4.2
- **Database:** SQLite (개발용) / PostgreSQL (배포용)
- **Frontend:** HTML/CSS/JavaScript + Chart.js
- **인증:** Django 커스텀 유저 모델 + 로그인 미들웨어
- **배포:** GCP + Nginx + Gunicorn (`deploy.sh` 참고)

---

## 주의사항

- 본 서비스는 비의료 운동상담 보조 도구입니다.
- 현재 버전의 QS 점수 산식은 내부 규칙 기반이며, 실제 센터 데이터로 검증이 필요합니다.
- 개인정보보호법, 의료법 관련 사항은 서비스 출시 전 전문가 확인이 필요합니다. [확인필요]

---

**LIGHT ONE V2 · Rev.05 · 2026.07.01**
