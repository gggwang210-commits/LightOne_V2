import json

from django.test import TestCase, override_settings

from lightone.ai.gemini import AI_DRAFT_FAILURE_MESSAGE, build_trainer_report_draft
from lightone.models import MemberSession


class FakeInteraction:
    def __init__(self, output_text):
        self.output_text = output_text


class FakeInteractions:
    def __init__(self, output_text=None, error=None):
        self.output_text = output_text
        self.error = error
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        if self.error:
            raise self.error
        return FakeInteraction(self.output_text)


class FakeClient:
    def __init__(self, interactions):
        self.interactions = interactions


class GeminiDraftTests(TestCase):
    def make_session(self):
        session = MemberSession.objects.create(
            member_name='Synthetic Member A',
            trainer_name='Synthetic Trainer',
            goal='Synthetic conditioning check',
            discomfort_area='Synthetic shoulder note',
            form_accuracy=8,
            pain_response=2,
            rpe=7,
            qc_score=90,
            memo='Synthetic non-medical demo memo',
        )
        session.calculate_qs_and_route()
        return session

    @override_settings(AI_ENABLED=False, GEMINI_API_KEY='')
    def test_ai_disabled_keeps_rule_based_flow_only(self):
        session = self.make_session()
        original_qs = session.qs_score
        original_route = session.route

        result = build_trainer_report_draft(session)

        self.assertFalse(result.enabled)
        self.assertIsNone(result.draft)
        self.assertEqual(session.qs_score, original_qs)
        self.assertEqual(session.route, original_route)

    @override_settings(
        AI_ENABLED=True,
        GEMINI_API_KEY='test-placeholder-key',
        GEMINI_REPORT_MODEL='gemini-test-model',
        GEMINI_TIMEOUT_SECONDS=5,
    )
    def test_gemini_structured_output_is_validated(self):
        payload = {
            'summary': '세션 반응은 안정적이며 트레이너 검토용 초안입니다.',
            'risk_flags': ['통증 반응 낮음', 'QC PASS'],
            'trainer_review_required': True,
            'next_session_focus': '동작 안정성과 RPE 변화를 함께 확인합니다.',
            'safety_notice': '비의료 운동 상담 참고 자료이며 트레이너가 최종 검토합니다.',
        }
        interactions = FakeInteractions(output_text=json.dumps(payload, ensure_ascii=False))
        session = self.make_session()

        result = build_trainer_report_draft(
            session,
            client_factory=lambda: FakeClient(interactions),
        )

        self.assertTrue(result.enabled)
        self.assertEqual(result.model, 'gemini-test-model')
        self.assertEqual(result.draft.summary, payload['summary'])
        self.assertEqual(
            interactions.kwargs['response_format']['mime_type'],
            'application/json',
        )
        self.assertIn('summary', interactions.kwargs['response_format']['schema']['properties'])

    @override_settings(AI_ENABLED=True, GEMINI_API_KEY='test-placeholder-key')
    def test_gemini_errors_fall_back_to_trainer_review_message(self):
        interactions = FakeInteractions(error=RuntimeError('provider unavailable'))
        session = self.make_session()

        with self.assertLogs('lightone.ai.gemini', level='WARNING'):
            result = build_trainer_report_draft(
                session,
                client_factory=lambda: FakeClient(interactions),
            )

        self.assertTrue(result.enabled)
        self.assertIsNone(result.draft)
        self.assertEqual(result.error_message, AI_DRAFT_FAILURE_MESSAGE)
