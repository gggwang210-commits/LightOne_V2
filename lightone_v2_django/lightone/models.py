from django.db import models


from accounts.models import MemberProfile, TrainerProfile
from .algorithms import SAFETY_NOTICE, calculate_jatc, calculate_qs, route_session

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
    qc_score = models.FloatField(default=100)
    posture_score = models.FloatField(default=0)
    lifestyle_score = models.FloatField(default=0)
    function_training_score = models.FloatField(default=0)
    pain_response = models.FloatField(default=0)
    rpe = models.FloatField(default=0)
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    memo = models.TextField(blank=True)
    review_note = models.TextField(blank=True)
    safety_notice = models.TextField(default=SAFETY_NOTICE)
    trainer_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        return f'{self.member_name} - {self.route}'

    def calculate_qs_and_route(self):
        """
        규칙 기반 엔진 (MVP용)
        """
        self.qs_score = calculate_qs(
            self.form_accuracy,
            self.pain_response,
            self.rpe,
            self.qc_score,
        )
        self.jatc_score = calculate_jatc(
            self.posture_score or (self.form_accuracy * 10),
            self.lifestyle_score,
            self.function_training_score or self.qs_score,
        )
        self.route = route_session(self.qs_score, self.pain_response, self.qc_status)
        self.safety_notice = SAFETY_NOTICE
        self.save()


class Member(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('ARCHIVED', 'Archived'),
    ]

    synthetic_id = models.CharField(max_length=40, unique=True)
    display_label = models.CharField(max_length=80)
    goal = models.CharField(max_length=120, blank=True)
    experience_level = models.CharField(max_length=40, blank=True)
    discomfort_area = models.CharField(max_length=80, blank=True)
    consent_status = models.CharField(max_length=30, default='synthetic_demo')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['synthetic_id']

    def __str__(self):
        return self.display_label


class Session(models.Model):
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

    session_id = models.CharField(max_length=40, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='session_records')
    exercise_name = models.CharField(max_length=120)
    session_date = models.DateField()
    planned_reps = models.PositiveIntegerField(default=0)
    completed_reps = models.PositiveIntegerField(default=0)
    planned_rest_seconds = models.PositiveIntegerField(default=0)
    actual_rest_seconds = models.PositiveIntegerField(default=0)
    rpe = models.PositiveSmallIntegerField(default=0)
    pain_response = models.PositiveSmallIntegerField(default=0)
    trainer_memo = models.TextField(blank=True)
    capture_condition = models.CharField(max_length=120, blank=True)
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-session_date', 'session_id']

    def __str__(self):
        return f'{self.session_id} - {self.member.display_label}'


class Indicator(models.Model):
    ROUTE_CHOICES = Session.ROUTE_CHOICES
    REPORT_CHOICES = [
        ('PENDING', 'Pending'),
        ('READY', 'Ready'),
        ('HELD', 'Held'),
    ]

    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='indicator')
    posture_score = models.FloatField(default=0)
    lifestyle_score = models.FloatField(default=0)
    rep_achievement_rate = models.FloatField(default=0)
    rest_compliance = models.FloatField(default=0)
    pain_score = models.FloatField(default=0)
    function_training_score = models.FloatField(default=0)
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0)
    review_signal = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    counseling_priority = models.PositiveSmallIntegerField(default=3)
    report_status = models.CharField(max_length=10, choices=REPORT_CHOICES, default='PENDING')
    review_note = models.TextField(blank=True)
    trainer_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-qs_score', 'session__session_id']

    def __str__(self):
        return f'{self.session.session_id} indicator'


class StrategyItem(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    priority = models.CharField(max_length=30, default='높음')
    status = models.CharField(max_length=40, default='진행 필요')
    output = models.TextField(blank=True)
    risk = models.TextField(blank=True)

    def __str__(self):
        return self.title
