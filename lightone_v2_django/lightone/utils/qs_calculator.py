"""Quality Score (QS) calculation and routing helpers.

All values are non-medical wellness/PT consultation support metrics.
QS/JATC and AUTO/REVIEW/BLOCK are not diagnostic outputs.
"""

ROUTE_AUTO = "AUTO"
ROUTE_REVIEW = "REVIEW"
ROUTE_BLOCK = "BLOCK"

PAIN_NONE_ALIASES = {"none", "no", "low", "0", "없음", "낮음", "무통증"}
PAIN_MILD_ALIASES = {"mild", "minor", "light", "경미", "약간"}
PAIN_HIGH_ALIASES = {"moderate", "high", "severe", "block", "중간", "중간 이상", "높음", "심함"}


def clamp(value, minimum=0, maximum=100):
    """Clamp a numeric value into the inclusive 0-100 scoring range."""
    return max(minimum, min(maximum, float(value)))


def normalize_score(value):
    """Normalize project score values: 0-10 inputs become 0-100, 0-100 inputs pass through."""
    value = float(value)
    return value * 10 if value <= 10 else value


def map_pain_response_score(pain_level):
    """Map pain/discomfort response into a QS contribution score.

    Project convention:
    - none/low/0: 100 points
    - numeric 1-3 or mild labels: 50 points
    - numeric >=4 or high/moderate labels: 0 points
    """
    if pain_level is None or pain_level == "":
        return 100.0

    if isinstance(pain_level, str):
        normalized = pain_level.strip().lower()
        if normalized in PAIN_NONE_ALIASES:
            return 100.0
        if normalized in PAIN_MILD_ALIASES:
            return 50.0
        if normalized in PAIN_HIGH_ALIASES:
            return 0.0
        try:
            pain_level = float(normalized)
        except ValueError:
            return 0.0

    pain_value = float(pain_level)
    if pain_value <= 0:
        return 100.0
    if pain_value <= 3:
        return 50.0
    return 0.0


def calculate_qs(form, rep, rest, pain_level):
    """Calculate QS = Form*0.4 + Rep*0.3 + Rest*0.2 + Pain*0.1."""
    form_score = clamp(normalize_score(form))
    rep_score = clamp(normalize_score(rep))
    rest_score = clamp(normalize_score(rest))
    pain_score = clamp(map_pain_response_score(pain_level))
    score = (form_score * 0.4) + (rep_score * 0.3) + (rest_score * 0.2) + (pain_score * 0.1)
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
        return str(pain_level).strip().lower() in PAIN_NONE_ALIASES

    return 0 <= numeric_pain <= 3


def _is_high_pain(pain_level):
    try:
        numeric_pain = float(pain_level)
    except (TypeError, ValueError):
        return str(pain_level).strip().lower() in PAIN_HIGH_ALIASES

    return numeric_pain >= 7


def determine_routing(qs_score, pain_level, safety_flags=None):
    """Determine non-medical routing from QS, pain level, and safety flags."""
    if _has_safety_flags(safety_flags) or _is_high_pain(pain_level):
        return ROUTE_BLOCK
    if float(qs_score) >= 80 and _is_low_or_none_pain(pain_level):
        return ROUTE_AUTO
    return ROUTE_REVIEW
