from .algorithms import SAFETY_NOTICE
from .models import MemberSession, StrategyItem


ROUTE_KEYS = ["AUTO", "REVIEW", "BLOCK"]
QC_KEYS = ["PASS", "CHECK", "FAIL"]


def dashboard_context(member_id=None):
    """Build dashboard context from the canonical MemberSession data model."""
    queryset = MemberSession.objects.select_related("member", "trainer").order_by("-created_at")
    if member_id:
        queryset = queryset.filter(member_id=member_id)

    sessions = list(queryset[:80])
    total = len(sessions)

    avg_qs = round(sum(session.qs_score for session in sessions) / total, 1) if total else 0
    avg_jatc = round(sum(session.jatc_score for session in sessions) / total, 1) if total else 0

    counts = {key: sum(1 for session in sessions if session.route == key) for key in ROUTE_KEYS}
    qc_counts = {key: sum(1 for session in sessions if session.qc_status == key) for key in QC_KEYS}

    chronological_sessions = list(reversed(sessions[:12]))
    chart_labels = [session.created_at.strftime("%m/%d") for session in chronological_sessions]
    chart_qs = [session.qs_score for session in chronological_sessions]

    latest_session = sessions[0] if sessions else None
    breakdown_labels = ["폼", "통증", "반복", "휴식/QC", "JATC"]
    if latest_session:
        breakdown_values = [
            latest_session.qs_form_component,
            latest_session.qs_discomfort_component,
            latest_session.qs_rpe_component,
            latest_session.qs_qc_component,
            latest_session.jatc_score,
        ]
    else:
        breakdown_values = [0, 0, 0, 0, 0]

    feature_importance = [
        {"name": "통증 반응", "value": 0.28},
        {"name": "폼 정확도", "value": 0.25},
        {"name": "RPE", "value": 0.18},
        {"name": "촬영 QC", "value": 0.13},
        {"name": "JATC", "value": 0.10},
        {"name": "생활습관", "value": 0.06},
    ]

    return {
        "sessions": sessions,
        "recent_sessions": sessions[:10],
        "strategy_items": StrategyItem.objects.all()[:6],
        "total": total,
        "avg_qs": avg_qs,
        "avg_jatc": avg_jatc,
        "counts": counts,
        "qc_counts": qc_counts,
        "feature_importance": feature_importance,
        "chart_labels": chart_labels,
        "chart_qs": chart_qs,
        "qs_labels": chart_labels,
        "qs_scores": chart_qs,
        "breakdown_labels": breakdown_labels,
        "breakdown_values": breakdown_values,
        "status_badges": {
            "AUTO": "lo-pill route-auto",
            "REVIEW": "lo-pill route-review",
            "BLOCK": "lo-pill route-block",
        },
        "selected_member_id": member_id or "",
        "safety_notice": SAFETY_NOTICE,
    }
