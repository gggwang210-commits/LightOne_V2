import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass

from django.conf import settings
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

AI_DRAFT_FAILURE_MESSAGE = 'AI 초안 생성 실패, 트레이너 직접 검토 필요'
DEFAULT_SAFETY_NOTICE = '비의료 PT 상담 참고용이며 최종 판단은 트레이너 검토가 필요합니다.'


class TrainerReportDraft(BaseModel):
    summary: str = Field(description='트레이너가 검토할 세션 요약')
    risk_flags: list[str] = Field(description='통증, QC, 라우팅 관련 확인 필요 항목')
    trainer_review_required: bool = Field(description='트레이너 검토 필요 여부')
    next_session_focus: str = Field(description='다음 세션에서 확인할 비의료 운동 상담 포커스')
    safety_notice: str = Field(description='비의료, 트레이너 최종 검토 안내 문구')


@dataclass
class GeminiDraftResult:
    enabled: bool
    draft: TrainerReportDraft | None = None
    error_message: str = ''
    model: str = ''


def create_gemini_client():
    from google import genai

    return genai.Client()


def build_trainer_report_prompt(session):
    return f'''
당신은 LIGHTONE의 트레이너 보조 리포트 작성 도우미입니다.
아래 데이터는 비의료 PT 상담 참고 자료입니다.
진단, 치료, 처방, 질병 위험 예측을 하지 마세요.
최종 판단과 회원 안내는 반드시 트레이너가 검토합니다.
회원에게 직접 확정적으로 말하지 말고 트레이너가 검토할 초안으로 작성하세요.

세션 데이터:
- 회원명: {session.member_name}
- 목표: {session.goal}
- 불편 부위: {session.discomfort_area or '기록 없음'}
- 트레이너 메모: {session.memo or '기록 없음'}
- QS 점수: {session.qs_score}
- JATC 점수: {session.jatc_score}
- 라우팅: {session.route}
- QC 상태: {session.qc_status}
- 자세 정확도: {session.form_accuracy}
- 통증 반응: {session.pain_response}
- RPE: {session.rpe}

출력은 스키마에 맞는 JSON만 반환하세요.
'''.strip()


def _call_gemini(client, model, prompt):
    return client.interactions.create(
        model=model,
        input=prompt,
        response_format={
            'type': 'text',
            'mime_type': 'application/json',
            'schema': TrainerReportDraft.model_json_schema(),
        },
    )


def build_trainer_report_draft(session, client_factory=None, timeout_seconds=None):
    model = getattr(settings, 'GEMINI_REPORT_MODEL', 'gemini-3.5-flash')

    if not getattr(settings, 'AI_ENABLED', False) or not getattr(settings, 'GEMINI_API_KEY', ''):
        return GeminiDraftResult(enabled=False, model=model)

    timeout = timeout_seconds or getattr(settings, 'GEMINI_TIMEOUT_SECONDS', 20)
    factory = client_factory or create_gemini_client
    prompt = build_trainer_report_prompt(session)
    executor = ThreadPoolExecutor(max_workers=1)

    try:
        future = executor.submit(lambda: _call_gemini(factory(), model, prompt))
        interaction = future.result(timeout=timeout)
        draft = TrainerReportDraft.model_validate_json(getattr(interaction, 'output_text', ''))
        return GeminiDraftResult(enabled=True, draft=draft, model=model)
    except TimeoutError as exc:
        logger.warning('Gemini report draft timed out: %s', exc.__class__.__name__)
    except ValidationError as exc:
        logger.warning('Gemini report draft validation failed: %s', exc.__class__.__name__)
    except Exception as exc:
        logger.warning('Gemini report draft failed: %s', exc.__class__.__name__)
    finally:
        executor.shutdown(wait=False, cancel_futures=True)

    return GeminiDraftResult(
        enabled=True,
        error_message=AI_DRAFT_FAILURE_MESSAGE,
        model=model,
    )
