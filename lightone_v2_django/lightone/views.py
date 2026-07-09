from django.shortcuts import get_object_or_404, render, redirect
from .models import MemberSession
from .services import dashboard_context


def dashboard(request):
    return render(request, 'dashboard/dashboard.html', dashboard_context())


def report_detail(request, pk):
    session = get_object_or_404(MemberSession, pk=pk)
    return render(request, 'lightone/report_detail.html', {'session': session})


def method(request):
    return render(request, 'lightone/method.html')

def session_create(request):
    from .forms import SessionRecordForm
    if request.method == 'POST':
        form = SessionRecordForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            if request.user.is_authenticated and hasattr(request.user, 'trainer_profile'):
                session.trainer = request.user.trainer_profile
                session.trainer_name = request.user.name
            session.save()
            session.calculate_qs_and_route()
            return redirect('lightone:dashboard')
    else:
        form = SessionRecordForm()
    return render(request, 'lightone/session_form.html', {'form': form})
