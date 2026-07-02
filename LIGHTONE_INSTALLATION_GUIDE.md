# LIGHT ONE Django 프로젝트 — 설치 및 실행 가이드

## 📦 패키지 내용

`lightone_django_complete.zip`에 포함된 내용:
- **Django 4.2** 기반 완전한 웹 애플리케이션
- **SQLite 데이터베이스** (더미 데이터 사전 로드)
- **프리미엄 Bootstrap UI** (민트/청록 계열 디자인)
- **8명 회원 + 79개 세션** 더미 데이터
- **QS 점수화 엔진** (규칙 기반 MVP)
- **위험 라우팅** (AUTO/REVIEW/BLOCK)
- **상담 리포트 생성** 기능

---

## 🚀 5분 안에 시작하기

### Step 1: ZIP 파일 압축 해제
```bash
unzip lightone_django_complete.zip
cd lightone_django
```

### Step 2: 가상 환경 설정
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: 패키지 설치
```bash
pip install -r requirements.txt
```

### Step 4: 서버 실행
```bash
python manage.py runserver
```

### Step 5: 브라우저에서 접속
```
http://127.0.0.1:8000/
```

**로그인 정보:**
- 👨‍💼 **트레이너**: `trainer01` / `lightone2026`
- 🔐 **관리자**: `admin` / `admin1234`

---

## 📋 상세 설치 가이드

### 사전 요구사항
- **Python 3.8 이상** (3.10+ 권장)
- **pip** (Python 패키지 관리자)
- **터미널/CMD** 접근 권한

### 설치 단계

#### 1️⃣ 프로젝트 다운로드 및 진입
```bash
# ZIP 파일 압축 해제
unzip lightone_django_complete.zip

# 프로젝트 폴더로 이동
cd lightone_django
```

#### 2️⃣ 가상 환경 생성 및 활성화

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### 3️⃣ 필수 패키지 설치
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**설치되는 패키지:**
- `Django==4.2.30` — 웹 프레임워크
- `python-decouple==3.8` — 환경 변수 관리
- `django-extensions==3.2.3` — 개발 도구

#### 4️⃣ 데이터베이스 확인
```bash
# 이미 db.sqlite3가 포함되어 있으므로 마이그레이션 불필요
# 필요 시 초기화:
# python manage.py migrate
```

#### 5️⃣ 개발 서버 실행
```bash
python manage.py runserver
```

**출력 예시:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 02, 2026 - 16:00:00
Django version 4.2.30, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## 🎯 주요 기능 사용법

### 1. 로그인
```
URL: http://127.0.0.1:8000/accounts/login/
트레이너 계정: trainer01 / lightone2026
```

### 2. 대시보드 보기
```
로그인 후 자동으로 대시보드로 이동
- 활성 회원 수: 8명
- 총 세션: 79개
- 평균 QS: 약 72점
- 라우팅 분포: AUTO/REVIEW/BLOCK 차트
```

### 3. 회원 관리
```
좌측 사이드바 → "회원 관리"
- 기존 회원 8명 조회
- 새 회원 등록: "신규 회원 등록" 버튼
- 회원 상세: 회원명 클릭
```

### 4. 세션 기록 입력
```
좌측 사이드바 → "세션 입력"
- 회원 선택
- 운동 정보 입력 (운동명, 세트, 회수, 중량)
- 컨디션 지표 입력 (통증, RPE, 자세 정확도)
- 체형 관찰 6항목 입력
- 저장 → QS 점수 자동 계산 + 라우팅 자동 판정
```

### 5. 상담 리포트 생성
```
회원 상세 페이지 → "리포트 생성" 버튼
- 최근 4주 세션 데이터 자동 수집
- 평균 QS, 통증, RPE 계산
- 라우팅 분포 집계
- 재등록 신호 판정
```

### 6. 관리자 페이지
```
URL: http://127.0.0.1:8000/admin/
계정: admin / admin1234
- 모든 데이터 관리
- 사용자 추가/수정
- 세션 데이터 조회
```

---

## 🔧 트러블슈팅

### ❌ "ModuleNotFoundError: No module named 'django'"
**해결:**
```bash
# 가상 환경 활성화 확인
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate  # Windows

# 패키지 재설치
pip install -r requirements.txt
```

### ❌ "Port 8000 is already in use"
**해결:**
```bash
# 다른 포트에서 실행
python manage.py runserver 8001
# 또는 기존 프로세스 종료
# macOS/Linux: lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### ❌ "No such table: members_member"
**해결:**
```bash
# 데이터베이스 초기화 및 마이그레이션
python manage.py migrate
python manage.py seed_demo
```

### ❌ 로그인 후 "Page not found (404)"
**해결:**
```bash
# 정적 파일 수집
python manage.py collectstatic --noinput

# 캐시 삭제
rm -rf __pycache__ *//__pycache__
```

---

## 📊 데이터베이스 구조

### 포함된 더미 데이터
| 항목 | 수량 | 설명 |
|------|------|------|
| 회원 | 8명 | 다양한 나이, 성별, 운동 목표 |
| 세션 | 79개 | 회원당 8~12회 |
| 트레이너 | 1명 | trainer01 계정 |
| 관리자 | 1명 | admin 계정 |

### 주요 모델
- **User** — 사용자 (트레이너/관리자)
- **TrainerProfile** — 트레이너 프로필
- **Member** — PT 회원
- **MemberSession** — 세션 기록 (QS 점수 포함)
- **WeeklyReport** — 주간 상담 리포트

---

## 🎨 UI/UX 특징

### 디자인
- **민트/청록 계열** 브랜드 컬러
- **프리미엄 Bootstrap 5** 레이아웃
- **반응형 디자인** (데스크톱/태블릿/모바일)
- **COPD 팀 프로젝트 수준** 완성도

### 페이지 구성
1. **로그인** — 사용자 인증
2. **대시보드** — 통계 + 최근 세션
3. **회원 관리** — CRUD + 상세 조회
4. **세션 입력** — 데이터 기록 + QS 자동 계산
5. **세션 목록** — 전체 세션 조회
6. **상담 리포트** — 리포트 생성 + 상세 보기
7. **관리자 페이지** — Django Admin

---

## 📈 성능 및 확장성

### 현재 사양
- **데이터베이스**: SQLite (로컬 개발용)
- **동시 사용자**: 1~5명 (개발 서버)
- **저장 용량**: ~1MB (더미 데이터 포함)

### 프로덕션 배포 시
```bash
# 1. PostgreSQL/MySQL로 마이그레이션
# 2. Gunicorn + Nginx 구성
# 3. 정적 파일 CDN 연결
# 4. SSL/TLS 인증서 설정
# 5. 데이터베이스 백업 자동화
```

**권장 배포 플랫폼:**
- Heroku (간단함)
- AWS EC2 + RDS (확장성)
- Railway (모던)
- Render (사용 편의)

---

## 📚 추가 학습 자료

### 프로젝트 문서
- `README.md` — 프로젝트 개요 및 기능 설명
- `LIGHTONE_신규창업지원_전략서.md` — 사업 계획 및 지원 프로그램

### Django 공식 문서
- [Django 4.2 Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/4.2/topics/http/views/)

### 기술 스택
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 🤝 팀 정보

**프로젝트**: LIGHT ONE — AI 기반 체형분석 PT 솔루션 SaaS MVP
**개발자**: 송광일
**기술 스택**: Django 4.2 + Bootstrap 5 + Chart.js + SQLite
**완성도**: COPD 선별 서비스 팀 프로젝트 수준

---

## 📞 문제 해결

**문제가 발생하면:**
1. 터미널 오류 메시지 전체 복사
2. 위 "트러블슈팅" 섹션 확인
3. Django 공식 문서 검색
4. 프로젝트 README.md 재확인

---

**Last Updated**: 2026년 7월 2일
**Version**: 1.0 (MVP)
**License**: MIT (팀 프로젝트 학습용)

---

## ✅ 설치 완료 체크리스트

- [ ] Python 3.8+ 설치 확인
- [ ] ZIP 파일 압축 해제
- [ ] 가상 환경 생성 및 활성화
- [ ] `pip install -r requirements.txt` 실행
- [ ] `python manage.py runserver` 실행
- [ ] `http://127.0.0.1:8000/` 접속 확인
- [ ] 트레이너 계정 로그인 성공
- [ ] 대시보드 데이터 확인 (8명 회원, 79개 세션)
- [ ] 관리자 페이지 접속 확인

**모두 완료되었다면 설치가 성공적으로 완료된 것입니다! 🎉**
