SAFETY_NOTICE = (
    "LIGHT ONE은 비의료 운동상담 보조 도구입니다. QS/JATC와 AUTO/REVIEW/BLOCK은 "
    "진단·치료·처방이 아니며, 통증이나 이상 반응이 있으면 운동을 중단하고 전문가 상담을 권고합니다."
)


def _clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, float(value)))


def calculate_qs(form_accuracy, pain_response, rpe, qc_score):
    """Calculate Quality Score with 0.4/0.3/0.2/0.1 MVP weights."""
    form_component = _clamp(form_accuracy * 10)
    pain_component = _clamp(100 - (pain_response * 10))
    rpe_component = _clamp(100 - (abs(rpe - 7) * 12.5))
    qc_component = _clamp(qc_score)
    score = (
        form_component * 0.4
        + pain_component * 0.3
        + rpe_component * 0.2
        + qc_component * 0.1
    )
    return round(_clamp(score), 1)


def calculate_jatc(posture_score, lifestyle_score, function_training_score):
    """Calculate a trainer-facing JATC readiness score for MVP demos."""
    score = (
        _clamp(posture_score) * 0.4
        + _clamp(function_training_score) * 0.4
        + _clamp(lifestyle_score) * 0.2
    )
    return round(_clamp(score), 1)


def route_session(qs_score, pain_response, qc_status):
    """Route session output to AUTO, REVIEW, or BLOCK gates."""
    if pain_response >= 7 or qc_status == "FAIL" or qs_score < 40:
        return "BLOCK"
    if pain_response >= 4 or qc_status == "CHECK" or qs_score < 70:
        return "REVIEW"
    return "AUTO"
