# LIGHTONE V2 저장소 맵

이 문서는 저장소 루트에서 어떤 문서를 먼저 읽고, 어떤 폴더가 어떤 역할을 하는지 빠르게 파악하기 위한 안내서입니다. 전체 사업 방향은 [루트 README](../README.md), Django MVP 실행과 기능은 [Django README](../lightone_v2_django/README.md), Windows 실행 절차는 [기존 RUN_WINDOWS](../lightone_v2_django/RUN_WINDOWS.md)와 [Windows 실행 가이드](execution-guide/windows-run-guide.md)를 함께 확인합니다.

## 1. 최상위 문서

| 경로 | 역할 | 먼저 볼 사람 |
|------|------|--------------|
| [`README.md`](../README.md) | LIGHTONE V2의 사업 전략, 제품 포지셔닝, 비의료 경계, 시장 진출 계획 | 심사자, 사업 검토자, 신규 기여자 |
| [`docs/repository-map.md`](repository-map.md) | 문서와 코드 위치를 연결하는 저장소 지도 | 모든 신규 참여자 |
| [`docs/governance/non-medical-boundary.md`](governance/non-medical-boundary.md) | 의료 오인 방지를 위한 표현·기능 경계 | 기획, 디자인, 개발, 영업 |
| [`docs/governance/privacy-checklist.md`](governance/privacy-checklist.md) | 개인정보·민감정보 취급 점검표 | 운영, 개발, 파일럿 담당 |
| [`docs/validation/pilot-validation-plan.md`](validation/pilot-validation-plan.md) | 파일럿 검증 목표, 지표, 절차 | 대표, PM, 파일럿 센터 담당 |
| [`docs/submission/modu-startup-summary.md`](submission/modu-startup-summary.md) | 모두의창업 2기 제출용 요약 | 심사 대응, 제안서 작성자 |
| [`docs/execution-guide/windows-run-guide.md`](execution-guide/windows-run-guide.md) | 루트 기준 Windows 실행 안내 | 비개발자, Windows 사용자 |

## 2. Django MVP 영역

| 경로 | 역할 |
|------|------|
| [`lightone_v2_django/README.md`](../lightone_v2_django/README.md) | MVP 소개, 빠른 시작, 계정, 기능 URL, 위험 라우팅 기준 |
| [`lightone_v2_django/RUN_WINDOWS.md`](../lightone_v2_django/RUN_WINDOWS.md) | Django 폴더 내부에서 실행하는 간단한 Windows 명령 |
| `lightone_v2_django/manage.py` | Django 관리 명령 진입점 |
| `lightone_v2_django/requirements.txt` | Python 패키지 의존성 |
| `lightone_v2_django/lightone/` | LIGHTONE 앱의 모델, 뷰, 템플릿, 관리 명령 영역 |

## 3. 문서 사용 순서

1. 사업 방향과 규제 경계를 이해하려면 [루트 README](../README.md)를 먼저 읽습니다.
2. 의료 표현을 만들기 전에 [비의료 경계 문서](governance/non-medical-boundary.md)를 확인합니다.
3. 회원 데이터, 이미지, 상담 기록을 다루기 전에 [개인정보 체크리스트](governance/privacy-checklist.md)를 적용합니다.
4. 센터 파일럿을 시작하기 전에 [파일럿 검증 계획](validation/pilot-validation-plan.md)의 동의, 지표, 중단 기준을 확정합니다.
5. Windows에서 MVP를 실행할 때는 [Windows 실행 가이드](execution-guide/windows-run-guide.md)를 사용하고, 세부 앱 설명은 [Django README](../lightone_v2_django/README.md)를 참조합니다.

## 4. 문서 관리 원칙

- 루트 `README.md`는 사업 전략의 기준 문서입니다.
- `docs/governance/`는 서비스 표현, 개인정보, 운영 리스크의 기준 문서입니다.
- `docs/validation/`은 가설 검증과 파일럿 결과를 기록하는 영역입니다.
- `docs/submission/`은 외부 제출용 요약 문서를 보관하는 영역입니다.
- 실행 방법이 바뀌면 `lightone_v2_django/README.md`, `lightone_v2_django/RUN_WINDOWS.md`, `docs/execution-guide/windows-run-guide.md`를 함께 갱신합니다.
