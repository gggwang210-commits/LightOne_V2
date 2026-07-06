import os
import sys
from pathlib import Path

import django
from django.test import TestCase

PROJECT_DIR = Path(__file__).resolve().parents[2]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from lightone.algorithms import SAFETY_NOTICE, calculate_jatc, calculate_qs, route_session  # noqa: E402
from lightone.models import MemberSession  # noqa: E402


class QsAlgorithmTests(TestCase):
    def test_calculate_qs_uses_documented_weights(self):
        score = calculate_qs(form_accuracy=8, pain_response=2, rpe=7, qc_score=90)
        self.assertEqual(score, 85.0)

    def test_route_session_respects_review_and_block_gates(self):
        self.assertEqual(route_session(85, 1, "PASS"), "AUTO")
        self.assertEqual(route_session(85, 4, "PASS"), "REVIEW")
        self.assertEqual(route_session(85, 1, "FAIL"), "BLOCK")

    def test_member_session_recalculates_scores_and_safety_notice(self):
        session = MemberSession.objects.create(
            member_name="데모회원 A",
            goal="합성 테스트",
            form_accuracy=8,
            qc_score=90,
            posture_score=82,
            lifestyle_score=70,
            function_training_score=78,
            pain_response=2,
            rpe=7,
            qc_status="PASS",
        )
        session.calculate_qs_and_route()
        self.assertEqual(session.qs_score, 85.0)
        self.assertEqual(session.jatc_score, calculate_jatc(82, 70, 78))
        self.assertEqual(session.route, "AUTO")
        self.assertEqual(session.safety_notice, SAFETY_NOTICE)
