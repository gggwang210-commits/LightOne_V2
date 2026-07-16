from django.shortcuts import render

from lightone.services import dashboard_context
from lightone.models import Member


def dashboard(request):
    return render(request, 'dashboard/dashboard.html', dashboard_context(request.GET.get('member_id')))
