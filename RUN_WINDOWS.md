# Windows 실행 가이드

이미 Anaconda Python이 정상 작동하고 있다면 가상환경 없이도 실행 확인이 가능합니다.

## 1단계: 프로젝트 폴더 확인

현재 터미널 위치에 `manage.py`와 `requirements.txt`가 보여야 합니다.

```powershell
dir
```

## 2단계: 설치 및 DB 준비

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
```

## 3단계: 샘플 데이터와 서버 실행

```powershell
python manage.py seed_lightone
python manage.py runserver
```

브라우저 주소:

```text
http://127.0.0.1:8000/lightone/
```
