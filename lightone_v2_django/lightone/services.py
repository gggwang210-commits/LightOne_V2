from .models import MemberSession, StrategyItem


def safe_member_id_for_session(session):
    """Return the safest available member identifier for dashboard display."""
    member = getattr(session, 'member', None)
    if member is not None and hasattr(member, 'member_id'):
        return str(member.member_id)

    member_id = getattr(session, 'member_id', None)
    if member_id is not None:
        return str(member_id)

    return str(session.pk)


def dashboard_context():
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

    dashboard_sessions = [
        {
            'pk': s.pk,
            'member_id': safe_member_id_for_session(s),
            'goal': s.goal,
            'qs_score': s.qs_score,
            'jatc_score': s.jatc_score,
            'route': s.route,
            'qc_status': s.qc_status,
        }
        for s in sessions
    ]

    return {
        'sessions': dashboard_sessions,
        'strategy_items': StrategyItem.objects.all()[:6],
        'total': total,
        'avg_qs': avg_qs,
        'avg_jatc': avg_jatc,
        'counts': counts,
        'qc_counts': qc_counts,
        'feature_importance': feature_importance,
    }
