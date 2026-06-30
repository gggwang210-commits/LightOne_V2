# LIGHT ONE Healthcare Premium Django

LIGHT ONE 프리미엄 헬스케어 SaaS 스타일의 Django 대시보드입니다.

이 프로젝트는 PT 트레이너가 회원의 운동 기록, 통증 반응, 촬영 QC, 상담 메모를 구조화하여 상담 리포트로 활용할 수 있도록 만든 비의료 웰니스 프로토타입입니다.

## 실행 순서

PowerShell에서 프로젝트 폴더로 이동한 뒤 아래 순서로 실행합니다.

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_lightone
python manage.py runserver
```

접속 주소:

```text
http://127.0.0.1:8000/lightone/
```

## 주요 페이지

- `/lightone/`: 프리미엄 대시보드
- `/lightone/method/`: QS/JATC 라우팅 코드 방법론
- `/lightone/report/<id>/`: 회원별 상담 리포트

## 반영된 스타일

- 좌측 고정 사이드바
- 네이비 헬스케어 히어로 섹션
- 의료 데이터 네트워크 느낌의 배경 효과
- KPI 카드, Feature Importance, 위험 라우팅, 상담 리포트 카드
- Inter + Noto Sans KR 폰트
- 카드 hover, 순차 등장 애니메이션

## 안전 경계

이 프로젝트는 의료 진단, 치료, 재활 효과 판단, 질병 예측을 제공하지 않습니다.
QS/JATC는 PT 상담 참고 지표이며, 최종 판단은 트레이너 검토를 전제로 합니다.
