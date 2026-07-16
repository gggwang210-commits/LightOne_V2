from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from lightone.models import Indicator, Member, Session


class DashboardPrivacyAndContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.member = Member.objects.create(
            gender=Member.GENDER_OTHER,
            age_group='30s',
            goals='synthetic mobility goal',
            consent=True,
        )
        statuses = ['AUTO', 'REVIEW', 'BLOCK']
        for index, status in enumerate(statuses):
            session = Session.objects.create(
                session_id=f'synthetic-session-{index}',
                member=cls.member,
                session_date=timezone.localdate() - timezone.timedelta(days=2 - index),
                exercise_name=f'synthetic squat pattern {index}',
                planned_reps=10,
                completed_reps=8 + index,
                planned_rest_seconds=60,
                actual_rest_seconds=55 + index,
                rpe=6 + index,
                pain_response=index,
                trainer_memo='synthetic non-medical note',
                route=status,
            )
            Indicator.objects.create(
                session=session,
                qs_score=92 - (index * 18),
                posture_score=90 - (index * 10),
                rep_achievement_rate=80 - (index * 5),
                rest_compliance=85 - (index * 5),
                pain_score=10 + (index * 30),
                review_signal=status,
            )
        User = get_user_model()
        cls.user = User.objects.create_user(
            username='synthetic_trainer',
            email='synthetic-trainer@example.test',
            password='test-pass-1234',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_url_returns_200_for_selected_member(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.member_id})
        self.assertEqual(response.status_code, 200)

    def test_selected_member_context_contains_dashboard_data(self):
        response = self.client.get(reverse('dashboard'), {'member_id': self.member.member_id})
        self.assertEqual(response.context['selected_member_id'], str(self.member.member_id))
        self.assertIn('qs_labels', response.context)
        self.assertIn('qs_scores', response.context)
        self.assertIn('breakdown_values', response.context)
        self.assertIn('recent_sessions', response.context)
        self.assertEqual(len(response.context['qs_labels']), 3)
        self.assertEqual(len(response.context['qs_scores']), 3)
        self.assertEqual(len(response.context['breakdown_values']), 4)
        self.assertEqual(len(response.context['recent_sessions']), 3)
        self.assertEqual(response.context['qs_scores'], [92, 74, 56])
        self.assertEqual(response.context['breakdown_values'], [70, 70, 75, 70])

    def test_dashboard_renders_safety_copy_without_pii(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.member_id})
        html = response.content.decode('utf-8')
        self.assertContains(response, '비의료 운동상담 참고 자료입니다. 최종 판단은 트레이너 검토가 필요합니다.')
        forbidden_context_keys = {'name', 'phone', 'email', 'address', 'birth_date', 'date_of_birth'}
        context_keys = set()
        for rendered_context in response.context:
            if hasattr(rendered_context, 'flatten'):
                context_keys.update(rendered_context.flatten().keys())
        self.assertTrue(forbidden_context_keys.isdisjoint(context_keys))
        for forbidden in ['이름', '전화번호', '이메일', '주소', '생년월일', '홍길동', '010-1234-5678', 'member@example.test', '서울시 개인정보로', '1990-01-01']:
            self.assertNotIn(forbidden, html)

    def test_dashboard_renders_status_badge_classes(self):
        response = self.client.get('/dashboard/', {'member_id': self.member.member_id})
        self.assertContains(response, 'badge-auto badge-green')
        self.assertContains(response, 'badge-review badge-yellow')
        self.assertContains(response, 'badge-block badge-red')

    def test_font_family_fallback_stack_exists_in_css(self):
        from pathlib import Path
        css_text = Path(__file__).resolve().parents[1].joinpath('static/lightone/css/lightone.css').read_text(encoding='utf-8')
        self.assertIn('--font-dashboard:', css_text)
