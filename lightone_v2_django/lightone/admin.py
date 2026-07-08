from django.contrib import admin

from .models import MemberSession, StrategyItem


@admin.register(MemberSession)
class MemberSessionAdmin(admin.ModelAdmin):
    list_display = (
        'member_name',
        'trainer_name',
        'qs_score',
        'jatc_score',
        'route',
        'qc_status',
        'created_at',
    )
    list_filter = ('route', 'qc_status', 'created_at')
    search_fields = ('member_name', 'trainer_name', 'goal', 'discomfort_area')
    readonly_fields = (
        'qs_score',
        'jatc_score',
        'qs_form_component',
        'qs_discomfort_component',
        'qs_rpe_component',
        'qs_qc_component',
        'safety_notice',
        'route',
        'created_at',
    )


@admin.register(StrategyItem)
class StrategyItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status')
    list_filter = ('category', 'priority', 'status')
    search_fields = ('title', 'category', 'output', 'risk')
