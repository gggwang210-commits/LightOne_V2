from django.shortcuts import render

from lightone.services import qs_dashboard_context


def dashboard(request):
    return render(
        request,
        'dashboard/dashboard.html',
        qs_dashboard_context(request.GET.get('member_id')),
    )
