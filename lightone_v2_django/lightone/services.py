import json

from django.core.exceptions import ValidationError

ROUTING_BADGE_CLASSES = {
    'AUTO': 'badge-green',
    'GREEN': 'badge-green',
    'REVIEW': 'badge-yellow',
    'YELLOW': 'badge-yellow',
    'BLOCK': 'badge-red',
    'RED': 'badge-red',
}


def routing_label(route):
    return str(route or '').strip()


def routing_badge_class(route):
    normalized_route = routing_label(route).upper()
    return ROUTING_BADGE_CLASSES.get(normalized_route, 'badge-gray')


def enrich_routing_badges(sessions):
    for session in sessions:
        session.routing_label = routing_label(session.route)
        session.routing_badge_class = routing_badge_class(session.route)
    return sessions


def dashboard_context():
    sessions = enrich_routing_badges(list(MemberSession.objects.all()))
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

    recent_sessions = sorted(sessions, key=lambda session: session.created_at)[-8:]
    qs_labels = [session.created_at.strftime('%m/%d') for session in recent_sessions]
    qs_scores = [session.qs_score for session in recent_sessions]
    breakdown_labels = ['Form Accuracy', 'Pain Response', 'RPE', 'JATC']
    breakdown_values = [
        round(sum(s.form_accuracy for s in sessions) / total, 1) if total else 0,
        round(sum(s.pain_response for s in sessions) / total, 1) if total else 0,
        round(sum(s.rpe for s in sessions) / total, 1) if total else 0,
        avg_jatc,
    ]

    return {
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
    context.update(_dashboard_chart_context(member_id))
    return context
