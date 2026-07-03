from django.core.management.base import BaseCommand
from lightone.models import MemberSession, StrategyItem


class Command(BaseCommand):
    help = 'Create LIGHT ONE premium dashboard demo data.'

    def handle(self, *args, **options):
        MemberSession.objects.all().delete()
        StrategyItem.objects.all().delete()

        sessions = [
            {'member_name': '김도윤', 'goal': '체형 변화 기록 및 재등록 상담', 'discomfort_area': '목·어깨', 'qs_score': 72.4, 'jatc_score': 68.0, 'form_accuracy': 79, 'pain_response': 2, 'rpe': 6, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '상담 리포트 자동 생성 가능. 촬영 조건 양호.'},
            {'member_name': '이서연', 'goal': '하체 근력 컨디셔닝 및 운동 지속', 'discomfort_area': '무릎', 'qs_score': 63.2, 'jatc_score': 61.5, 'form_accuracy': 70, 'pain_response': 4, 'rpe': 7, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': '통증 반응 기록이 있어 트레이너 검토 권장.'},
            {'member_name': '박민준', 'goal': '러닝 자세 개선', 'discomfort_area': '허리', 'qs_score': 81.5, 'jatc_score': 74.3, 'form_accuracy': 86, 'pain_response': 1, 'rpe': 5, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '전후 비교 리포트에 적합.'},
            {'member_name': '최하린', 'goal': '상체 안정화 루틴', 'discomfort_area': '손목', 'qs_score': 49.0, 'jatc_score': 44.6, 'form_accuracy': 50, 'pain_response': 7, 'rpe': 8, 'route': 'BLOCK', 'qc_status': 'FAIL', 'memo': '통증 반응이 높아 운동 중단 및 전문가 상담 권고 문구 필요.'},
            {'member_name': '정유찬', 'goal': '바디프로필 준비 관리', 'discomfort_area': '없음', 'qs_score': 67.5, 'jatc_score': 66.1, 'form_accuracy': 74, 'pain_response': 2, 'rpe': 7, 'route': 'AUTO', 'qc_status': 'PASS', 'memo': '상담 자료로 사용 가능.'},
            {'member_name': '오지민', 'goal': '운동 습관 형성', 'discomfort_area': '어깨', 'qs_score': 58.2, 'jatc_score': 55.9, 'form_accuracy': 63, 'pain_response': 5, 'rpe': 8, 'route': 'REVIEW', 'qc_status': 'CHECK', 'memo': 'RPE와 통증 반응 확인 필요.'},
        ]
        for item in sessions:
            MemberSession.objects.create(**item)

        strategies = [
            {'title': '고객 인터뷰 질문지 작성', 'category': '고객검증', 'priority': '높음', 'status': '대기', 'output': 'PT샵 대표, 헬스장 대표, 트레이너 대상 인터뷰 질문지', 'risk': '지인 중심 인터뷰는 편향 가능'},
            {'title': 'PT샵 파일럿 제안서 작성', 'category': '고객검증', 'priority': '높음', 'status': '대기', 'output': '1~2개 센터 대상 파일럿 제안서', 'risk': '실제 회원 이미지·민감정보 수집 금지'},
            {'title': '수익모델 가설표 작성', 'category': '사업계획서', 'priority': '보통', 'status': '대기', 'output': '센터 월 구독, 트레이너 계정 추가, 리포트 저장 옵션별 가격 가설표', 'risk': '미검증 가격을 확정처럼 쓰면 감점'},
            {'title': '촬영 QC 기술 재배치', 'category': 'GitHub / 사업계획서', 'priority': '높음', 'status': '완료', 'output': '촬영 QC·카메라 보정·조명 정규화를 리포트 신뢰도 보조 기술로 재정의', 'risk': '기술이 서비스 주인공처럼 보이지 않게 유지'},
            {'title': 'GitHub 첫 화면 정체성 강화', 'category': 'GitHub', 'priority': '높음', 'status': '진행 필요', 'output': 'PT 트레이너를 위한 회원 변화 기록·상담 리포트 SaaS MVP 설명', 'risk': '저장소 메타데이터 수정 권한 확인 필요'},
        ]
        for item in strategies:
            StrategyItem.objects.create(**item)

        self.stdout.write(self.style.SUCCESS('LIGHT ONE premium demo data created.'))
