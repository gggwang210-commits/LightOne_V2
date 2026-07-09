from django.test import TestCase
from django.utils import timezone

from lightone.algorithms import calculate_jatc, calculate_qs, route_session
from lightone.models import Member, MemberSession, Session
from lightone.utils.jatc_calculator import calculate_jatc as calculate_session_jatc


class QsJatcAlgorithmTests(TestCase):
    def test_qs_uses_weighted_average(self):
        score = calculate_qs(form_accuracy=80, discomfort_response=2, rpe=7, qc_score=90)
        self.assertEqual(score, 85.0)

    def test_jatc_and_routing_auto_review_block(self):
        qs = calculate_qs(90, 1, 7, 100)
        jatc = calculate_jatc(qs, 90, 1, 7)
        self.assertEqual(route_session(qs, jatc, 1, 'PASS'), 'AUTO')
        self.assertEqual(route_session(65, 65, 4, 'PASS'), 'REVIEW')
        self.assertEqual(route_session(80, 80, 8, 'PASS'), 'BLOCK')

    def test_model_calculates_scores_and_notice_on_save(self):
        session = MemberSession.objects.create(
            member_name='Synthetic Member A',
            goal='Synthetic conditioning check',
            form_accuracy=8,
            pain_response=2,
            rpe=7,
            qc_score=90,
        )
        self.assertEqual(session.qs_score, 85.0)
        self.assertGreater(session.jatc_score, 0)
        self.assertEqual(session.route, 'AUTO')
        self.assertIn('비의료 운동상담 참고', session.safety_notice)

    def test_model_recalculates_scores_on_save_update(self):
        session = MemberSession.objects.create(
            member_name='Synthetic Member B',
            goal='Synthetic routing check',
            form_accuracy=8,
            pain_response=2,
            rpe=7,
            qc_score=90,
        )

        session.pain_response = 8
        session.save(update_fields=['pain_response'])
        session.refresh_from_db()

        self.assertEqual(session.route, 'BLOCK')
        self.assertEqual(session.qs_discomfort_component, 20)
