from django.contrib import admin
from .models import MemberSession, StrategyItem

@admin.register(MemberSession)
class MemberSessionAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'trainer_name', 'qs_score', 'jatc_score', 'route', 'qc_status', 'created_at')
    list_filter = ('route', 'qc_status')

@admin.register(StrategyItem)
class StrategyItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status')
    list_filter = ('category', 'priority', 'status')
