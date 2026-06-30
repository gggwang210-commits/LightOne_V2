from django.urls import path
from . import views

app_name = 'lightone'

urlpatterns = [
    path('roadmap/', views.roadmap, name='roadmap'),
    path('priority/', views.priority, name='priority'),
    path('reports/', views.reports, name='reports'),
    path('', views.dashboard, name='dashboard'),
    path('method/', views.method, name='method'),
    path('workflow/', views.workflow, name='workflow'),
    path('quality/', views.quality, name='quality'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
]
