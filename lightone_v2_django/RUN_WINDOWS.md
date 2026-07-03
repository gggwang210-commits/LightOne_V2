# Windows 실행 가이드

현재 기준 Django 프로젝트 폴더는 `lightone_v2_django`입니다. 모든 명령은 `manage.py`와 `requirements.txt`가 있는 이 폴더에서 실행합니다.

> 구버전 안내: `lightone_django`, `lightone_django_complete.zip`, `LIGHTONE_V2_Complete.zip` 같은 이름이 보이는 예전 안내는 현재 `lightone_v2_django` 기준으로 바꿔 실행하세요.

## 1단계: 프로젝트 폴더로 이동

저장소 루트에서 실행하는 경우:

```powershell
cd lightone_v2_django
```

현재 위치 확인:

```powershell
dir manage.py, requirements.txt
```

## 2단계: 가상환경 준비

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

PowerShell 보안 오류가 나면 CMD에서 아래처럼 실행하세요.

```cmd
.venv\Scripts\activate.bat
```

## 3단계: 설치 및 DB 준비

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_lightone
```

## 4단계: 서버 실행

```powershell
python manage.py runserver
```

브라우저 주소:

```text
http://127.0.0.1:8000/lightone/
```

## 로그인 정보

| 역할 | 아이디 | 비밀번호 |
|---|---|---|
| 관리자/트레이너 | `admin` | `admin` |
| 회원 | `member1` | `1234` |
| 회원 | `member2` | `1234` |
