from django.shortcuts import render

from lightone.services import qs_dashboard_context


NOTICE_TEXT = '비의료 운동상담 참고 자료입니다. 최종 판단은 트레이너 검토가 필요합니다.'


def _indicator_value(indicator, *field_names):
    if not indicator:
        return 0
    for field_name in field_names:
        if hasattr(indicator, field_name):
            return getattr(indicator, field_name) or 0
    return 0


def _stored_member_context(selected_member_id):
    members = [
        {'member_id': str(member_id)}
        for member_id in Member.objects.values_list('member_id', flat=True)
    ]

    if not selected_member_id and members:
        selected_member_id = members[0]['member_id']

    recent_sessions = []
    if selected_member_id:
        recent_sessions = list(
            Session.objects.filter(member__member_id=selected_member_id)
            .select_related('indicator')
            .order_by('-session_date', 'session_id')[:10]
        )

    chronological_sessions = list(reversed(recent_sessions))
    qs_labels = [
        session.session_date.strftime('%m/%d')
        for session in chronological_sessions
    ]
    qs_scores = [
        _indicator_value(getattr(session, 'indicator', None), 'qs_score')
        for session in chronological_sessions
    ]

    latest_indicator = (
        getattr(recent_sessions[0], 'indicator', None) if recent_sessions else None
    )
    breakdown_values = [
        _indicator_value(latest_indicator, 'form_accuracy', 'posture_score'),
        _indicator_value(latest_indicator, 'rep_rate', 'rep_achievement_rate'),
        _indicator_value(latest_indicator, 'rest_compliance'),
        _indicator_value(latest_indicator, 'pain_score'),
    ] if latest_indicator else []

    return {
        'members': members,
        'selected_member_id': selected_member_id,
        'recent_sessions': recent_sessions,
        'qs_labels': qs_labels,
        'qs_scores': qs_scores,
        'breakdown_labels': ['폼 정확도', '반복 수행률', '휴식 준수', '통증 반응'],
        'breakdown_values': breakdown_values,
        'notice_text': NOTICE_TEXT,
    }


def dashboard(request):
    return render(request, 'dashboard/dashboard.html', dashboard_context(request.GET.get('member_id')))
