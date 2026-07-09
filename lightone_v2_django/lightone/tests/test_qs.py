from django.test import TestCase

from lightone.algorithms import calculate_jatc, calculate_qs, route_session
from lightone.models import Indicator, MemberSession


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

    def test_model_calculates_scores_and_notice(self):
        session = MemberSession.objects.create(
            member_name='Synthetic Member A',
            goal='Synthetic conditioning check',
            form_accuracy=8,
            pain_response=2,
            rpe=7,
            qc_score=90,
        )
        session.calculate_qs_and_route()
        self.assertEqual(session.qs_score, 85.0)
        self.assertEqual(session.route, 'AUTO')
        self.assertIn('비의료 운동상담 참고', session.safety_notice)
        indicator = Indicator.objects.get(member_session=session)
        self.assertEqual(indicator.qs_score, session.qs_score)
        self.assertEqual(indicator.jatc_score, session.jatc_score)
        self.assertEqual(indicator.route, session.route)
        self.assertEqual(indicator.qc_status, session.qc_status)
        self.assertFalse(indicator.trainer_review_required)
