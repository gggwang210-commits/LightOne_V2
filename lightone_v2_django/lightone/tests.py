from django.test import TestCase
from django.urls import reverse

from accounts.models import MemberProfile, TrainerProfile, User
from .models import MemberSession


class DashboardPrivacyTests(TestCase):
    def test_dashboard_excludes_direct_member_identifiers(self):
        member_user = User.objects.create_user(
            username='privacy-member',
            password='pass12345',
            email='privacy-member@example.com',
            name='홍길동',
            role='member',
        )
        trainer_user = User.objects.create_user(
            username='privacy-trainer',
            password='pass12345',
            email='privacy-trainer@example.com',
            name='김트레이너',
            role='trainer',
        )
        login_user = User.objects.create_user(
            username='dashboard-viewer',
            password='pass12345',
            email='viewer@example.com',
            name='대시보드뷰어',
            role='trainer',
        )
        member = MemberProfile.objects.create(
            user=member_user,
            birth_date='1991-02-03',
            goals='운동 목표',
        )
        trainer = TrainerProfile.objects.create(user=trainer_user)
        session = MemberSession.objects.create(
            member=member,
            trainer=trainer,
            member_name='홍길동 010-1234-5678',
            trainer_name='김트레이너 서울시 강남구 테스트로 123',
            goal='근력 강화',
            discomfort_area='어깨',
            qs_score=88,
            jatc_score=77,
            form_accuracy=90,
            pain_response=1,
            rpe=6,
            route='AUTO',
            qc_status='PASS',
            memo='privacy-member@example.com 1991-02-03 서울시 강남구 테스트로 123',
        )

        self.client.force_login(login_user)
        response = self.client.get(reverse('lightone:dashboard'))

        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertContains(response, f'Member ID: {session.member_id}')
        self.assertNotContains(response, '홍길동')
        self.assertNotContains(response, '김트레이너')
        self.assertNotContains(response, '010-1234-5678')
        self.assertNotContains(response, 'privacy-member@example.com')
        self.assertNotContains(response, '서울시 강남구 테스트로 123')
        self.assertNotContains(response, '1991-02-03')
        self.assertNotIn(member_user.email, html)
        self.assertNotIn(member_user.name, html)
        self.assertNotIn(trainer_user.email, html)
        self.assertNotIn(trainer_user.name, html)
