"""Quality Score (QS) calculation helpers.

QS uses normalized 0-100 inputs for form, rep, rest, and pain response.
Pain response is mapped separately so the scale is explicit and reusable.
"""

PAIN_NONE_ALIASES = {'none', 'no', 'low', '없음', '낮음', '무통증'}
PAIN_MILD_ALIASES = {'mild', 'minor', 'light', '경미', '약간'}
PAIN_MODERATE_ALIASES = {'moderate', 'high', 'severe', '중간', '중간 이상', '높음', '심함'}


def clamp(value, minimum=0, maximum=100):
    """Clamp a numeric value into the inclusive 0-100 scoring range."""
    return max(minimum, min(maximum, float(value)))


def normalize_score(value):
    """Normalize project score values: 0-10 inputs become 0-100, 0-100 pass through."""
    value = float(value)
    return value * 10 if value <= 10 else value


def map_pain_response_score(pain_level):
    """Map pain response into a QS contribution score.

    Project data uses 0-10 pain response values in forms and fixtures. The QS
    pain contribution is intentionally coarse:
    - none/low/0: 100 points
    - mild numeric response 1-3 or '경미': 50 points
    - moderate or higher numeric response >=4 or '중간 이상': 0 points
    """
    if pain_level is None or pain_level == '':
        return 100.0

    if isinstance(pain_level, str):
        normalized = pain_level.strip().lower()
        if normalized in PAIN_NONE_ALIASES:
            return 100.0
        if normalized in PAIN_MILD_ALIASES:
            return 50.0
        if normalized in PAIN_MODERATE_ALIASES:
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
