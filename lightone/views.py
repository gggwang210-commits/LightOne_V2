from django.shortcuts import get_object_or_404, render
from .models import MemberSession
from .services import dashboard_context


def dashboard(request):
    return render(request, 'lightone/dashboard.html', dashboard_context())


def report_detail(request, pk):
    session = get_object_or_404(MemberSession, pk=pk)
    return render(request, 'lightone/report_detail.html', {'session': session})


def method(request):
    return render(request, 'lightone/method.html')
