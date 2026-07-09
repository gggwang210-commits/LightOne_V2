# LIGHTONE V2 Windows 실행 가이드

이 문서는 저장소 루트에서 Windows 사용자가 Django MVP를 실행하는 방법을 안내합니다. 앱 설명과 계정 정보는 [Django README](../../lightone_v2_django/README.md), Django 폴더 내부 기준의 짧은 실행 명령은 [기존 RUN_WINDOWS](../../lightone_v2_django/RUN_WINDOWS.md), 사업 배경은 [루트 README](../../README.md)를 함께 확인합니다.

## 기준 앱

현재 기준 앱은 `lightone_v2_django`입니다.

구버전 안내에서 `lightone_django`, `lightone_django_complete.zip`, `LIGHTONE_V2_Complete.zip` 같은 이름이 보이면 현재 기준인 `lightone_v2_django`로 바꿔 실행하세요.

## 1. 준비물

- Windows 10 이상
- Python 3.11 권장 또는 Anaconda Python
- PowerShell 또는 Windows Terminal
- Git으로 받은 `LightOne_V2` 저장소

## 2. 프로젝트 폴더로 이동

저장소 루트에서 실행하는 경우:

```powershell
cd lightone_v2_django
```

현재 위치 확인:

```powershell
dir manage.py, requirements.txt
```

## 3. 가상환경 준비

일반 Python을 사용하는 경우 가상환경을 권장합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

PowerShell 실행 정책 오류가 나면 현재 터미널에서만 다음 명령을 실행한 뒤 다시 활성화합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

PowerShell 보안 오류가 계속 나면 CMD에서 아래처럼 실행하세요.

```cmd
.venv\Scripts\activate.bat
```

이미 Anaconda Python이 정상 작동하고 있다면 가상환경 없이도 실행 확인이 가능합니다.

## 4. 설치 및 DB 준비

```powershell
python manage.py migrate
python manage.py seed_lightone
```

## 5. 서버 실행

```powershell
python manage.py runserver
```

브라우저 주소:

```text
http://127.0.0.1:8000/lightone/
```

## 6. Gemini AI 초안 실행 옵션

기본 QS/JATC 계산과 AUTO/REVIEW/BLOCK 라우팅은 API 키 없이도 동작합니다. Gemini는 트레이너 검토용 리포트 초안에만 사용합니다.

API 키를 코드, 문서, 채팅에 붙여넣지 마세요. 아래 스크립트는 키를 숨김 입력으로 받아 현재 PowerShell 프로세스와 Django 자식 프로세스에만 설정합니다.

```powershell
.\scripts\run_gemini_server.ps1
```

라이브 API 연결만 먼저 확인하려면 합성 데이터로 1회 호출하는 스모크 테스트를 실행하세요. 무료 등급에서는 호출 제한이 있을 수 있습니다.

```powershell
.\scripts\gemini_live_smoke.ps1
```

모델이나 timeout을 바꿔 실행할 수 있습니다.

```powershell
.\scripts\run_gemini_server.ps1 -Model gemini-3.5-flash -TimeoutSeconds 20
.\scripts\gemini_live_smoke.ps1 -Model gemini-3.5-flash -TimeoutSeconds 20
```

## 로그인 정보

| 역할 | 아이디 | 비밀번호 |
|---|---|---|
| 관리자/트레이너 | `admin` | `admin` |
| 회원 | `member1` | `1234` |
| 회원 | `member2` | `1234` |

## 7. 실행 확인 체크리스트

- [ ] `/accounts/login/` 로그인 화면이 열리는가?
- [ ] `/lightone/` 대시보드에서 회원 목록이 보이는가?
- [ ] 세션 입력 화면에서 RPE와 통증 반응을 입력할 수 있는가?
- [ ] 리포트 화면에서 AUTO / REVIEW / BLOCK 상태가 표시되는가?
- [ ] Gemini 설정이 없어도 기존 규칙 기반 리포트가 표시되는가?
- [ ] 실제 회원 데이터가 아니라 더미 데이터로만 테스트했는가?

## 8. 주의사항

이 MVP는 비의료 운동 상담 보조 도구입니다. 의료 진단, 치료, 처방을 대체하지 않으며, 통증 관련 입력과 Gemini 초안은 트레이너 검토를 위한 참고 정보입니다. 표현 기준은 [비의료 경계 정책](../governance/non-medical-boundary.md), 데이터 취급 기준은 [개인정보 보호 체크리스트](../governance/privacy-checklist.md)를 따릅니다.
