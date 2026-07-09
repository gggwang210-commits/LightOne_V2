SAFETY_NOTICE = '비의료 운동상담 참고, 트레이너 검토 필요'

ROUTE_AUTO = 'AUTO'
ROUTE_REVIEW = 'REVIEW'
ROUTE_BLOCK = 'BLOCK'


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, float(value)))


def normalize_ten_scale(value):
    value = float(value)
    return value * 10 if value <= 10 else value


def calculate_qs(form_accuracy, discomfort_response, rpe, qc_score=100):
    """QS weighted average: form 0.4, discomfort stability 0.3, RPE fit 0.2, QC 0.1."""
    form_component = normalize_ten_scale(form_accuracy)
    discomfort_component = 100 - (clamp(discomfort_response, 0, 10) * 10)
    rpe_component = 100 - (abs(clamp(rpe, 0, 10) - 7) * 10)
    qc_component = normalize_ten_scale(qc_score)
    score = (
        clamp(form_component) * 0.4
        + clamp(discomfort_component) * 0.3
        + clamp(rpe_component) * 0.2
        + clamp(qc_component) * 0.1
    )
    return round(clamp(score), 1)


def calculate_jatc(qs_score, form_accuracy=None, discomfort_response=None, rpe=None):
    """Backward-compatible JATC score helper for numeric inputs or a session object."""
    if form_accuracy is None and hasattr(qs_score, '__dict__'):
        from lightone.utils.jatc_calculator import calculate_jatc as calculate_session_jatc

        return calculate_session_jatc(qs_score)['score']

    form_component = normalize_ten_scale(form_accuracy)
    discomfort_component = 100 - (clamp(discomfort_response, 0, 10) * 10)
    rpe_component = 100 - (abs(clamp(rpe, 0, 10) - 7) * 10)
    score = (clamp(qs_score) * 0.5) + (clamp(form_component) * 0.2) + (clamp(discomfort_component) * 0.2) + (clamp(rpe_component) * 0.1)
    return round(clamp(score), 1)


def route_session(qs_score, jatc_score, discomfort_response, qc_status='PASS'):
    if qc_status == 'FAIL' or discomfort_response >= 7 or qs_score < 40 or jatc_score < 40:
        return ROUTE_BLOCK
    if qc_status == 'CHECK' or discomfort_response >= 4 or qs_score < 70 or jatc_score < 60:
        return ROUTE_REVIEW
    return ROUTE_AUTO
