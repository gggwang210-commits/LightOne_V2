from django.shortcuts import render

from lightone.services import apply_routing_badges, dashboard_context


def dashboard(request):
    context = dashboard_context()
    context['recent_sessions'] = apply_routing_badges(context.get('recent_sessions', []))
    return render(request, 'dashboard/dashboard.html', context)
