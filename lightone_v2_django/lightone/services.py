import json

from django.core.exceptions import ValidationError

from .models import MemberSession, Session, StrategyItem

RECENT_SESSION_LIMIT = 10
BREAKDOWN_LABELS = ["Form", "Rep", "Rest", "Pain"]


def _serialize_chart_list(values):
    return json.dumps(values, ensure_ascii=False)


def _session_label(session):
    if hasattr(session, 'date'):
        return session.date.strftime('%m/%d')
    return session.created_at.strftime('%m/%d')


def _indicator_sessions(member_id):
    sessions = Session.objects.select_related('indicator').order_by('-date')
    if member_id:
        try:
            sessions = sessions.filter(member_id=member_id)
        except (ValidationError, ValueError):
            return []
    return list(sessions[:RECENT_SESSION_LIMIT])


def _fallback_member_sessions(member_id):
    sessions = MemberSession.objects.all().order_by('-created_at')
    if member_id:
        try:
            sessions = sessions.filter(member_id=member_id)
        except (ValidationError, ValueError):
            return []
    return list(sessions[:RECENT_SESSION_LIMIT])


def _dashboard_chart_context(member_id=None):
    completion_log = []
    recent_sessions = _indicator_sessions(member_id)
    latest_indicator = None

    indicator_sessions = []
    for session in recent_sessions:
        indicator = getattr(session, 'indicator', None)
        if indicator is not None:
            indicator_sessions.append((session, indicator))

    if indicator_sessions:
        chart_pairs = list(reversed(indicator_sessions))
        latest_indicator = indicator_sessions[0][1]
        qs_labels = [_session_label(session) for session, _indicator in chart_pairs]
        qs_scores = [indicator.qs_score for _session, indicator in chart_pairs]
        breakdown_values = [
            latest_indicator.form_accuracy,
            latest_indicator.rep_rate,
            latest_indicator.rest_compliance,
            latest_indicator.pain_score,
        ]
    else:
        recent_sessions = _fallback_member_sessions(member_id)
        chart_sessions = list(reversed(recent_sessions))
        qs_labels = [_session_label(session) for session in chart_sessions]
        qs_scores = [session.qs_score for session in chart_sessions]
        latest_session = recent_sessions[0] if recent_sessions else None
        breakdown_values = [
            latest_session.form_accuracy if latest_session else 0,
            0,
            0,
            latest_session.pain_response if latest_session else 0,
        ]
        completion_log.append(
            '[확인필요] MemberSession fallback에는 rep_rate, rest_compliance 저장값이 없어 '
            'breakdown_values의 Rep/Rest는 0으로 전달됩니다.'
        )

    return {
        'selected_member_id': member_id or '',
        'qs_labels': _serialize_chart_list(qs_labels),
        'qs_scores': _serialize_chart_list(qs_scores),
        'breakdown_labels': _serialize_chart_list(BREAKDOWN_LABELS),
        'breakdown_values': _serialize_chart_list(breakdown_values),
        'completion_log': completion_log,
    }


def dashboard_context(member_id=None):
    sessions = list(MemberSession.objects.all())
    total = len(sessions)
    if total:
        avg_qs = round(sum(s.qs_score for s in sessions) / total, 1)
        avg_jatc = round(sum(s.jatc_score for s in sessions) / total, 1)
    else:
        avg_qs = 0
        avg_jatc = 0

    counts = {key: sum(1 for s in sessions if s.route == key) for key in ['AUTO', 'REVIEW', 'BLOCK']}
    qc_counts = {key: sum(1 for s in sessions if s.qc_status == key) for key in ['PASS', 'CHECK', 'FAIL']}

    feature_importance = [
        {'name': '통증 반응', 'value': 0.28},
        {'name': '폼 정확도', 'value': 0.25},
        {'name': 'RPE', 'value': 0.18},
        {'name': '촬영 QC', 'value': 0.13},
        {'name': 'JATC', 'value': 0.10},
        {'name': '생활습관', 'value': 0.06},
    ]

    context = {
        'sessions': sessions,
        'strategy_items': StrategyItem.objects.all()[:6],
        'total': total,
        'avg_qs': avg_qs,
        'avg_jatc': avg_jatc,
        'counts': counts,
        'qc_counts': qc_counts,
        'feature_importance': feature_importance,
    }
    context.update(_dashboard_chart_context(member_id))
    return context
