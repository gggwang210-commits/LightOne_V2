from .utils.qs_calculator import (
    clamp,
    calculate_qs,
    map_pain_response_score,
    normalize_score,
    determine_routing as determine_qs_routing,
)

SAFETY_NOTICE = (
    "LIGHT ONE은 비의료 운동상담 보조 도구입니다. "
    "QS/JATC와 AUTO/REVIEW/BLOCK은 진단·치료·처방이 아니며, "
    "통증이나 이상 반응이 있으면 운동을 중단하고 전문가 상담을 권고합니다."
)

ROUTE_AUTO = "AUTO"
ROUTE_REVIEW = "REVIEW"
ROUTE_BLOCK = "BLOCK"


def calculate_jatc(qs_score, form_accuracy, discomfort_response, rpe):
    """JATC combines QS, movement quality, discomfort stability and session load fit."""
    form_component = normalize_score(form_accuracy)
    discomfort_component = map_pain_response_score(discomfort_response)
    rpe_component = 100 - (abs(clamp(rpe, 0, 10) - 7) * 10)
    score = (
        (clamp(qs_score) * 0.5)
        + (clamp(form_component) * 0.2)
        + (clamp(discomfort_component) * 0.2)
        + (clamp(rpe_component) * 0.1)
    )
    return round(clamp(score), 1)


def determine_routing(qs_score, jatc_score=None, discomfort_response=0, qc_status="PASS"):
    """Backward-compatible routing API for QS/JATC session checks."""
    if jatc_score is None:
        jatc_score = qs_score

    safety_flags = {
        "qc_status_fail": qc_status == "FAIL",
        "qs_critical_low": float(qs_score) < 40,
        "jatc_critical_low": float(jatc_score) < 40,
    }
    if determine_qs_routing(qs_score, discomfort_response, safety_flags=safety_flags) == ROUTE_BLOCK:
        return ROUTE_BLOCK

    if qc_status == "CHECK" or float(jatc_score) < 60 or float(qs_score) < 70:
        return ROUTE_REVIEW

    return ROUTE_AUTO


def route_session(qs_score, jatc_score, discomfort_response, qc_status="PASS"):
    return determine_routing(qs_score, jatc_score, discomfort_response, qc_status)
