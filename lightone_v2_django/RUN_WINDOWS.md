# Windows 실행 가이드

> 저장소 루트 기준의 자세한 Windows 안내는 [`../docs/execution-guide/windows-run-guide.md`](../docs/execution-guide/windows-run-guide.md)를 참고하세요. 전체 사업 방향은 [`../README.md`](../README.md), MVP 기능과 계정 정보는 [`README.md`](README.md)에 정리되어 있습니다.

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
