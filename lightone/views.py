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


def workflow(request):
    return render(request, 'lightone/workflow.html', dashboard_context())


def quality(request):
    return render(request, 'lightone/quality.html', dashboard_context())


def reports(request):
    return render(request, 'lightone/reports.html', dashboard_context())


def priority(request):
    return render(request, 'lightone/priority.html', dashboard_context())


def roadmap(request):
    return render(request, 'lightone/roadmap.html', dashboard_context())
