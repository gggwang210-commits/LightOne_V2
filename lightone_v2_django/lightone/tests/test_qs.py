from django.test import TestCase

from lightone.algorithms import calculate_jatc, calculate_qs, route_session
from lightone.utils.qs_calculator import map_pain_response_score
from lightone.models import MemberSession


class QsJatcAlgorithmTests(TestCase):
    def test_qs_uses_weighted_average(self):
        score = calculate_qs(form=80, rep=90, rest=70, pain_level=0)
        self.assertEqual(score, 83.0)

    def test_jatc_and_routing_auto_review_block(self):
        qs = calculate_qs(90, 90, 90, 1)
        jatc = calculate_jatc(qs, 90, 1, 7)
        self.assertEqual(route_session(qs, jatc, 1, 'PASS'), 'AUTO')
        self.assertEqual(route_session(65, 65, 4, 'PASS'), 'REVIEW')
        self.assertEqual(route_session(80, 80, 8, 'PASS'), 'BLOCK')

    def test_pain_mapping_is_explicit(self):
        self.assertEqual(map_pain_response_score(0), 100.0)
        self.assertEqual(map_pain_response_score("low"), 100.0)
        self.assertEqual(map_pain_response_score("경미"), 50.0)
        self.assertEqual(map_pain_response_score(3), 50.0)
        self.assertEqual(map_pain_response_score(4), 0.0)

    def test_model_calculates_scores_and_notice(self):
        session = MemberSession.objects.create(
            member_name='Synthetic Member A',
            goal='Synthetic conditioning check',
            form_accuracy=8,
            pain_response=2,
            rpe=7,
            rep_score=90,
            rest_score=70,
            qc_score=90,
        )
        session.calculate_qs_and_route()
        self.assertEqual(session.qs_score, 78.0)
        self.assertEqual(session.route, 'AUTO')
        self.assertIn('비의료 운동상담 참고', session.safety_notice)
