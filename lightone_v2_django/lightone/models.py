from django.db import models

from .algorithms import SAFETY_NOTICE, calculate_jatc, calculate_qs, route_session
from accounts.models import MemberProfile, TrainerProfile

class MemberSession(models.Model):
    ROUTE_CHOICES = [
        ('AUTO', 'AUTO'),
        ('REVIEW', 'REVIEW'),
        ('BLOCK', 'BLOCK'),
    ]
    QC_CHOICES = [
        ('PASS', 'PASS'),
        ('CHECK', 'CHECK'),
        ('FAIL', 'FAIL'),
    ]

    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='sessions')
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='conducted_sessions')
    
    member_name = models.CharField(max_length=80)
    trainer_name = models.CharField(max_length=80, default='김라이트')
    goal = models.CharField(max_length=120)
    discomfort_area = models.CharField(max_length=120, blank=True)
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0)
    form_accuracy = models.FloatField(default=0)
    pain_response = models.FloatField(default=0)
    rpe = models.FloatField(default=0)
    qc_score = models.FloatField(default=100)
    qs_form_component = models.FloatField(default=0)
    qs_discomfort_component = models.FloatField(default=0)
    qs_rpe_component = models.FloatField(default=0)
    qs_qc_component = models.FloatField(default=100)
    safety_notice = models.CharField(max_length=80, default=SAFETY_NOTICE)
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        return f'{self.member_name} - {self.route}'

    def calculate_qs_and_route(self):
        """Calculate MVP QS/JATC scores and non-medical trainer review routing."""
        self.qs_form_component = self.form_accuracy * 10 if self.form_accuracy <= 10 else self.form_accuracy
        self.qs_discomfort_component = 100 - (self.pain_response * 10)
        self.qs_rpe_component = 100 - (abs(self.rpe - 7) * 10)
        self.qs_qc_component = self.qc_score
        self.qs_score = calculate_qs(self.form_accuracy, self.pain_response, self.rpe, self.qc_score)
        self.jatc_score = calculate_jatc(self.qs_score, self.form_accuracy, self.pain_response, self.rpe)
        self.route = route_session(self.qs_score, self.jatc_score, self.pain_response, self.qc_status)
        self.safety_notice = SAFETY_NOTICE
        self.save()


class StrategyItem(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    priority = models.CharField(max_length=30, default='높음')
    status = models.CharField(max_length=40, default='진행 필요')
    output = models.TextField(blank=True)
    risk = models.TextField(blank=True)

    def __str__(self):
        return self.title
