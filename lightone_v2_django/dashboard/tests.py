from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from lightone.models import Indicator, Member, Session


class DashboardPrivacyAndContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.selected_member = Member.objects.create(
            synthetic_id='synthetic-selected',
            display_label='테스트 선택 회원',
            gender=Member.GENDER_OTHER,
            age_group='30s',
            goals='비의료 운동상담 참고용 목표',
            consent=True,
        )
        cls.other_member = Member.objects.create(
            synthetic_id='synthetic-other',
            display_label='테스트 비교 회원',
            gender=Member.GENDER_OTHER,
            age_group='40s',
            goals='비교 회원 목표',
            consent=True,
        )

        cls.selected_qs_scores = [93, 74, 41]
        cls.selected_routes = ['AUTO', 'REVIEW', 'BLOCK']
        for index, route in enumerate(cls.selected_routes):
            session = Session.objects.create(
                session_id=f'selected-session-{index}',
                member=cls.selected_member,
                exercise_name=f'selected exercise {index}',
                session_date=(timezone.now() - timezone.timedelta(days=2 - index)).date(),
                planned_reps=10,
                completed_reps=8 + index,
                planned_rest_seconds=60,
                actual_rest_seconds=55 + index,
                rpe=6 + index,
                pain_response=index,
                trainer_memo='비의료 테스트 메모',
                route=route,
            )
            Indicator.objects.create(
                session=session,
                qs_score=cls.selected_qs_scores[index],
                posture_score=80 - index,
                lifestyle_score=70 - index,
                rep_achievement_rate=0.80 + (index * 0.05),
                rest_compliance=0.85 - (index * 0.05),
                pain_score=0.10 + index,
                function_training_score=75 - index,
                jatc_score=65 - index,
                route=route,
                review_signal=route,
                qc_status='PASS',
            )

        other_session = Session.objects.create(
            session_id='other-session-0',
            member=cls.other_member,
            exercise_name='other exercise',
            session_date=timezone.now().date(),
            planned_reps=10,
            completed_reps=10,
            planned_rest_seconds=60,
            actual_rest_seconds=60,
            rpe=5,
            pain_response=0,
        )
        Indicator.objects.create(
            session=other_session,
            qs_score=11,
            review_signal='AUTO',
            route='AUTO',
        )

        User = get_user_model()
        cls.user = User.objects.create_user(
            username='synthetic_trainer',
            email='synthetic-trainer@example.test',
            password='test-pass-1234',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_url_returns_200(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_selected_member_context_is_populated_from_member_id(self):
        response = self.client.get(
            reverse('dashboard'),
            {'member_id': self.selected_member.member_id},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_member_id'], str(self.selected_member.member_id))
        self.assertEqual(response.context['qs_scores'], self.selected_qs_scores)
        self.assertEqual(len(response.context['qs_labels']), 3)
        self.assertEqual(len(response.context['breakdown_values']), 8)
        self.assertEqual(len(response.context['recent_sessions']), 3)
        self.assertNotIn(11, response.context['qs_scores'])
        self.assertTrue(
            all(session.member_id == self.selected_member.id for session in response.context['recent_sessions'])
        )

    def test_dashboard_renders_required_safety_copy_without_pii(self):
        response = self.client.get('/dashboard/', {'member_id': self.selected_member.member_id})
        html = response.content.decode('utf-8')

        self.assertIn('비의료 운동상담 참고 자료입니다. 최종 판단은 트레이너 검토가 필요합니다.', html)
        for forbidden in [
            '홍길동',
            '010-1234-5678',
            'privacy-member@example.test',
            '서울시 개인정보로 123',
            '1990-01-01',
        ]:
            self.assertNotIn(forbidden, html)

    def test_dashboard_renders_auto_review_block_badges(self):
        response = self.client.get('/dashboard/', {'member_id': self.selected_member.member_id})
        self.assertContains(response, 'badge-auto badge-green')
        self.assertContains(response, 'badge-review badge-yellow')
        self.assertContains(response, 'badge-block badge-red')
        self.assertContains(response, '>AUTO<')
        self.assertContains(response, '>REVIEW<')
        self.assertContains(response, '>BLOCK<')

    def test_font_family_fallback_stack_contains_korean_fonts(self):
        response = self.client.get('/dashboard/')
        html = response.content.decode('utf-8')
        self.assertContains(response, 'Pretendard')
        self.assertContains(response, 'SUIT')
        self.assertContains(response, 'Noto Sans KR')
        self.assertContains(response, 'Malgun Gothic')
        self.assertIn('font-family', html)
