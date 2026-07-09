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

    def test_jatc_mvp_reflects_qs_qc_pain_and_trainer_memo_flag(self):
        """MVP JATC: QS 45%, QC 20%, pain response inverse score 20%, function 15%, memo flag -15."""
        clean = MemberSession.objects.create(
            member_name='Clean', goal='운동상담', form_accuracy=90, pain_response=1, rpe=7, qc_score=100, qc_status='PASS'
        )
        flagged = MemberSession.objects.create(
            member_name='Flagged', goal='운동상담', form_accuracy=90, pain_response=1, rpe=7, qc_score=100, qc_status='FAIL', memo='통증 검토 필요'
        )
        clean_result = calculate_session_jatc(clean)
        flagged_result = calculate_session_jatc(flagged)
        self.assertFalse(clean_result['trainer_memo_flag'])
        self.assertTrue(flagged_result['trainer_memo_flag'])
        self.assertLess(flagged_result['qc_component'], clean_result['qc_component'])
        self.assertLess(flagged_result['score'], clean_result['score'])
        self.assertIn('비의료 운동상담 참고', flagged_result['notice'])

    def test_session_updates_indicator_with_jatc_reference_notice(self):
        member = Member.objects.create(synthetic_id='M-001', display_label='Synthetic member')
        session = Session.objects.create(
            session_id='S-001',
            member=member,
            exercise_name='Squat',
            session_date=timezone.now().date(),
            planned_reps=10,
            completed_reps=9,
            planned_rest_seconds=60,
            actual_rest_seconds=65,
            rpe=7,
            pain_response=2,
            trainer_memo='비의료 운동상담 참고용 기록',
            qc_status='PASS',
        )
        indicator = session.update_indicator_scores()
        self.assertGreater(indicator.jatc_score, 0)
        self.assertEqual(indicator.review_signal, session.route)
        self.assertIn('비의료 운동상담 참고', indicator.review_note)
