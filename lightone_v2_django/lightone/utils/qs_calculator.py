ROUTE_AUTO = 'AUTO'
ROUTE_REVIEW = 'REVIEW'
ROUTE_BLOCK = 'BLOCK'


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, float(value)))


def normalize_score(value):
    value = float(value)
    if value <= 10:
        return clamp(value * 10)
    return clamp(value)


def map_pain_response_score(pain_level):
    return clamp(100 - (float(pain_level) * 25))


def calculate_qs(
    form=None,
    rep=None,
    rest=None,
    pain_level=None,
    *,
    form_accuracy=None,
    discomfort_response=None,
    rpe=None,
    qc_score=None,
):
    if form_accuracy is not None:
        form = form_accuracy
    if discomfort_response is not None:
        pain_level = discomfort_response
    if rpe is not None:
        rep = 100 - (abs(clamp(rpe, 0, 10) - 7) * 10)
    if qc_score is not None:
        rest = qc_score

    form_component = normalize_score(form or 0)
    rep_component = normalize_score(100 if rep is None else rep)
    rest_component = normalize_score(100 if rest is None else rest)
    pain_component = map_pain_response_score(pain_level or 0)
    score = (
        (form_component * 0.4)
        + (rep_component * 0.3)
        + (rest_component * 0.2)
        + (pain_component * 0.1)
    )
    return round(clamp(score), 1)


def _has_safety_flags(safety_flags=None):
    if safety_flags is None:
        return False
    if isinstance(safety_flags, str):
        return bool(safety_flags.strip())
    if isinstance(safety_flags, dict):
        return any(bool(value) for value in safety_flags.values())
    if isinstance(safety_flags, (list, tuple, set)):
        return any(bool(value) for value in safety_flags)
    return bool(safety_flags)


def _is_low_or_none_pain(pain_level):
    if pain_level is None:
        return True

    try:
        numeric_pain = float(pain_level)
    except (TypeError, ValueError):
        normalized_pain = str(pain_level).strip().lower()
        return normalized_pain in {'none', 'no', 'low', '0', '없음', '낮음'}

    # Project pain scale convention for numeric inputs:
    # 0~3 = low/none (AUTO eligible), 4~6 = mild/review, 7~10 = high/block.
    return 0 <= numeric_pain <= 3


def _is_high_pain(pain_level):
    try:
        numeric_pain = float(pain_level)
    except (TypeError, ValueError):
        normalized_pain = str(pain_level).strip().lower()
        return normalized_pain in {'high', 'severe', 'block', '높음', '심함'}

    # Project pain scale convention for numeric inputs:
    # 0~3 = low/none (AUTO eligible), 4~6 = mild/review, 7~10 = high/block.
    return numeric_pain >= 7


def determine_routing(qs_score, pain_level, safety_flags=None):
    """Determine non-medical routing from QS, pain level, and safety flags."""
    if _has_safety_flags(safety_flags) or _is_high_pain(pain_level):
        return ROUTE_BLOCK
    if float(qs_score) >= 80 and _is_low_or_none_pain(pain_level):
        return ROUTE_AUTO
    return ROUTE_REVIEW
