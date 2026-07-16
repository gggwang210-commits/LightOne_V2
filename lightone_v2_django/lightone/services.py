from django.db import models

from .models import Indicator, Member, MemberSession, StrategyItem


ROUTING_CLASS_MAP = {
    'AUTO': 'badge-green',
    'GREEN': 'badge-green',
    'REVIEW': 'badge-yellow',
    'YELLOW': 'badge-yellow',
    'BLOCK': 'badge-red',
    'RED': 'badge-red',
}


def routing_status_value(session):
    indicator = getattr(session, 'indicator', None)
    return getattr(indicator, 'routing_status', None) or getattr(session, 'route', '') or ''


def routing_label(status):
    return str(status or 'UNKNOWN')


def routing_badge_class(status):
    normalized_status = str(status or '').upper()
    return ROUTING_CLASS_MAP.get(normalized_status, 'badge-gray')


def apply_routing_badges(sessions):
    for session in sessions:
        status = routing_status_value(session)
        session.routing_status = status
        session.routing_badge_class = routing_badge_class(status)
        session.routing_label = routing_label(status)
    return sessions


def _empty_member_dashboard():
    return {
        'selected_member_id': None,
        'qs_labels': [],
        'qs_scores': [],
        'breakdown_values': [],
        'recent_sessions': [],
        'status_badges': {
            'AUTO': 'badge-auto badge-green',
            'REVIEW': 'badge-review badge-yellow',
            'BLOCK': 'badge-block badge-red',
        },
    }


def _member_dashboard_context(member_id=None):
    member_qs = Member.objects.all().order_by('member_id')
    if member_id:
        member_qs = member_qs.filter(member_id=member_id)

    member = member_qs.first()
    if not member:
        return _empty_member_dashboard()

    recent_sessions = apply_routing_badges(list(
        member.sessions.select_related('indicator').order_by('-date', 'exercise_name')[:5]
    ))
    chronological_sessions = list(reversed(recent_sessions))
    indicators = [getattr(session, 'indicator', None) for session in chronological_sessions]
    indicators = [indicator for indicator in indicators if indicator is not None]

    latest_indicator = getattr(recent_sessions[0], 'indicator', None) if recent_sessions else None
    breakdown_values = []
    if latest_indicator:
        breakdown_values = [
            getattr(latest_indicator, 'form_accuracy', latest_indicator.posture_score),
            getattr(latest_indicator, 'rep_rate', latest_indicator.rep_achievement_rate),
            latest_indicator.rest_compliance,
            latest_indicator.pain_score,
        ]

    return {
        'selected_member_id': str(member.member_id),
        'qs_labels': [session.session_date.strftime('%m/%d') for session in chronological_sessions],
        'qs_scores': [indicator.qs_score for indicator in indicators],
        'breakdown_values': breakdown_values,
        'recent_sessions': recent_sessions,
        'status_badges': {
            'AUTO': 'badge-auto badge-green',
            'REVIEW': 'badge-review badge-yellow',
            'BLOCK': 'badge-block badge-red',
        },
    }


def dashboard_context(member_id=None):
    sessions = apply_routing_badges(list(MemberSession.objects.all()))
    total = len(sessions)
    if total:
        avg_qs = round(sum(s.qs_score for s in sessions) / total, 1)
        avg_jatc = round(sum(s.jatc_score for s in sessions) / total, 1)
    else:
        avg_qs = 0
        avg_jatc = 0

    counts = {key: sum(1 for s in sessions if s.route == key) for key in ['AUTO', 'REVIEW', 'BLOCK']}
    qc_counts = {key: sum(1 for s in sessions if s.qc_status == key) for key in ['PASS', 'CHECK', 'FAIL']}

    indicator_counts = {
        key: Indicator.objects.filter(review_signal=key).count()
        for key in ['AUTO', 'REVIEW', 'BLOCK']
    }
    for key, value in indicator_counts.items():
        if value:
            counts[key] += value
    total += sum(indicator_counts.values())

    feature_importance = [
        {'name': '통증 반응', 'value': 0.28},
        {'name': '폼 정확도', 'value': 0.25},
        {'name': 'RPE', 'value': 0.18},
        {'name': '촬영 QC', 'value': 0.13},
        {'name': 'JATC', 'value': 0.10},
        {'name': '생활습관', 'value': 0.06},
    ]

    qs_labels = [session.created_at.strftime('%m/%d') for session in sessions]
    qs_scores = [session.qs_score for session in sessions]
    breakdown_labels = ['통증 반응', '폼 정확도', 'RPE', '촬영 QC', 'JATC', '생활습관']
    breakdown_values = [0.28, 0.25, 0.18, 0.13, 0.10, 0.06]

    context = {
        'sessions': sessions,
        'recent_sessions': sessions,
        'strategy_items': StrategyItem.objects.all()[:6],
        'total': total,
        'avg_qs': avg_qs,
        'avg_jatc': avg_jatc,
        'counts': counts,
        'qc_counts': qc_counts,
        'feature_importance': feature_importance,
        'qs_labels': qs_labels,
        'qs_scores': qs_scores,
        'breakdown_labels': breakdown_labels,
        'breakdown_values': breakdown_values,
    }
    context.update(_member_dashboard_context(member_id))
    return context


def _routing_badges():
    return {
        'AUTO': 'badge-auto badge-green',
        'REVIEW': 'badge-review badge-yellow',
        'BLOCK': 'badge-block badge-red',
    }


def _indicator_session_date(indicator):
    if indicator.session_id and indicator.session:
        return indicator.session.session_date
    if indicator.member_session_id and indicator.member_session:
        return indicator.member_session.created_at.date()
    return indicator.created_at.date()


def _indicator_member_id(indicator):
    if indicator.session_id and indicator.session and indicator.session.member_id:
        return str(indicator.session.member.member_id)
    if (
        indicator.member_session_id
        and indicator.member_session
        and indicator.member_session.member_id
    ):
        return str(indicator.member_session.member.member_id)
    return ''


def _indicator_form_score(indicator):
    if indicator.member_session_id and indicator.member_session:
        return indicator.member_session.form_accuracy
    return indicator.posture_score


def _indicator_rep_score(indicator):
    if indicator.member_session_id and indicator.member_session:
        return indicator.member_session.rep_score
    return indicator.rep_achievement_rate


def _indicator_rest_score(indicator):
    if indicator.member_session_id and indicator.member_session:
        return indicator.member_session.rest_score
    return indicator.rest_compliance


def _indicator_route(indicator):
    return indicator.review_signal or indicator.route


def qs_dashboard_context(member_id=None):
    """Return only non-identifying QS dashboard data for dashboard app."""
    indicators = Indicator.objects.select_related(
        'session__member',
        'member_session__member',
    ).order_by('-created_at', '-qs_score')

    if member_id:
        indicators = indicators.filter(
            models.Q(session__member__member_id=member_id)
            | models.Q(member_session__member__member_id=member_id)
        )

    rows = []
    for indicator in indicators[:20]:
        row_member_id = _indicator_member_id(indicator)
        rows.append({
            'session_date': _indicator_session_date(indicator),
            'member_id': row_member_id,
            'qs_score': indicator.qs_score,
            'form': _indicator_form_score(indicator),
            'rep': _indicator_rep_score(indicator),
            'rest': _indicator_rest_score(indicator),
            'pain': indicator.pain_score,
            'routing_status': _indicator_route(indicator),
        })

    chronological_rows = list(reversed(rows[:8]))
    selected_member_id = member_id or (rows[0]['member_id'] if rows else '')

    return {
        'member_id': str(selected_member_id),
        'qs_labels': [row['session_date'].strftime('%m/%d') for row in chronological_rows],
        'qs_scores': [row['qs_score'] for row in chronological_rows],
        'breakdown_labels': ['Form', 'Rep', 'Rest', 'Pain'],
        'breakdown_values': [
            rows[0]['form'] if rows else 0,
            rows[0]['rep'] if rows else 0,
            rows[0]['rest'] if rows else 0,
            rows[0]['pain'] if rows else 0,
        ],
        'dashboard_rows': rows,
        'status_badges': _routing_badges(),
        'safety_notice': '비의료 운동상담 참고 자료입니다. 최종 판단은 트레이너 검토가 필요합니다.',
    }
