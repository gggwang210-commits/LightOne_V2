from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('lightone:dashboard')),
    path('admin/', admin.site.urls),
    path('lightone/', include('lightone.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
]
