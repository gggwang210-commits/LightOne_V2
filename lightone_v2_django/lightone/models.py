import uuid

from django.db import models

from accounts.models import MemberProfile, TrainerProfile
from .algorithms import (
    SAFETY_NOTICE,
    calculate_jatc,
    determine_routing,
    calculate_qs,
    map_pain_response_score,
    normalize_score,
    route_session,
)


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

    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sessions',
    )
    trainer = models.ForeignKey(
        TrainerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conducted_sessions',
    )
    member_name = models.CharField(max_length=80)
    trainer_name = models.CharField(max_length=80, default='김라이트')
    goal = models.CharField(max_length=120)
    discomfort_area = models.CharField(max_length=120, blank=True)
    posture_score = models.FloatField(default=0)
    lifestyle_score = models.FloatField(default=0)
    function_training_score = models.FloatField(default=0)
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0)
    form_accuracy = models.FloatField(default=0)
    pain_response = models.FloatField(default=0)
    rpe = models.FloatField(default=0)
    rep_score = models.FloatField(default=100)
    rest_score = models.FloatField(default=100)
    qc_score = models.FloatField(default=100)
    qs_form_component = models.FloatField(default=0)
    qs_discomfort_component = models.FloatField(default=0)
    qs_rpe_component = models.FloatField(default=0)
    qs_qc_component = models.FloatField(default=100)
    route = models.CharField(
        max_length=10, choices=ROUTE_CHOICES, default='AUTO'
    )
    qc_status = models.CharField(
        max_length=10, choices=QC_CHOICES, default='PASS'
    )
    safety_notice = models.TextField(default=SAFETY_NOTICE)
    review_note = models.TextField(blank=True)
    trainer_confirmed = models.BooleanField(default=False)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        return f'{self.member_name} - {self.route}'

    def calculate_qs_and_route(self):
        """Calculate QS/JATC scores and non-medical review routing."""
        self.qs_form_component = normalize_score(self.form_accuracy)
        self.qs_discomfort_component = map_pain_response_score(
            self.pain_response,
        )
        self.qs_rpe_component = normalize_score(self.rep_score)
        self.qs_qc_component = normalize_score(self.rest_score)
        calculated_qs = calculate_qs(
            self.form_accuracy,
            self.rep_score,
            self.rest_score,
            self.pain_response,
        )
        calculated_jatc = calculate_jatc(
            calculated_qs,
            self.form_accuracy,
            self.pain_response,
            self.rpe,
        )
        if not self.qs_score:
            self.qs_score = calculated_qs
        if not self.jatc_score:
            self.jatc_score = calculated_jatc
        self.route = determine_routing(
            self.qs_score,
            self.jatc_score,
            self.pain_response,
            self.qc_status,
        )
        self.safety_notice = SAFETY_NOTICE

    def save(self, *args, **kwargs):
        self.calculate_qs_and_route()
        super().save(*args, **kwargs)
        Indicator.objects.update_or_create(
            member_session=self,
            defaults={
                'posture_score': self.posture_score,
                'lifestyle_score': self.lifestyle_score,
                'pain_score': self.pain_response,
                'function_training_score': self.function_training_score,
                'qs_score': self.qs_score,
                'jatc_score': self.jatc_score,
                'route': self.route,
                'review_signal': self.route,
                'qc_status': self.qc_status,
                'non_medical_notice': SAFETY_NOTICE,
                'review_note': self.review_note,
                'trainer_confirmed': self.trainer_confirmed,
                'report_status': (
                    'HELD' if self.route == 'BLOCK' else 'READY'
                ),
                'counseling_priority': (
                    1 if self.route == 'BLOCK' else 2
                    if self.route == 'REVIEW' else 3
                ),
                'trainer_review_required': (
                    self.route in {'REVIEW', 'BLOCK'}
                    or self.qc_status != 'PASS'
                ),
            },
        )


class Member(models.Model):
    """회원 운동 참고 프로필(비의료 참고)로 직접 식별정보를 저장하지 않는다."""

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'Other'
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('ARCHIVED', 'Archived'),
    ]

    member_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    synthetic_id = models.CharField(max_length=40, unique=True, blank=True)
    display_label = models.CharField(max_length=80, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        help_text='비의료 참고 목적의 성별 분류입니다.',
    )
    age_group = models.CharField(
        max_length=20,
        blank=True,
        help_text='비의료 참고 목적의 연령대입니다.',
    )
    goals = models.TextField(
        blank=True,
        help_text='비의료 참고 목적의 운동 목표입니다.',
    )
    consent = models.BooleanField(
        default=False,
        help_text='비의료 참고 데이터 활용 동의 여부입니다.',
    )
    goal = models.CharField(max_length=120, blank=True)
    experience_level = models.CharField(max_length=40, blank=True)
    discomfort_area = models.CharField(max_length=80, blank=True)
    consent_status = models.CharField(max_length=30, default='synthetic_demo')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='ACTIVE'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['synthetic_id']

    def __str__(self):
        return self.display_label or str(self.member_id)


class Session(models.Model):
    ROUTE_CHOICES = MemberSession.ROUTE_CHOICES
    QC_CHOICES = MemberSession.QC_CHOICES

    session_id = models.CharField(max_length=40, unique=True)
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='session_records',
    )
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
    qc_status = models.CharField(
        max_length=10, choices=QC_CHOICES, default='PASS'
    )
    route = models.CharField(
        max_length=10, choices=ROUTE_CHOICES, default='AUTO'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-session_date', 'session_id']

    def __str__(self):
        return f'{self.session_id} - {self.member.display_label}'

    def update_indicator_scores(self):
        indicator, _created = Indicator.objects.get_or_create(session=self)
        qs_score = calculate_qs(
            self.completed_reps,
            self.planned_reps,
            self.actual_rest_seconds,
            self.pain_response,
        )
        jatc_score = calculate_jatc(
            qs_score,
            self.completed_reps,
            self.pain_response,
            self.rpe,
        )
        indicator.qs_score = qs_score
        indicator.jatc_score = jatc_score
        indicator.pain_score = self.pain_response
        indicator.review_signal = route_session(
            indicator.qs_score,
            indicator.jatc_score,
            self.pain_response,
            self.qc_status,
        )
        indicator.review_note = SAFETY_NOTICE
        indicator.save()
        self.route = indicator.review_signal
        self.save(update_fields=['route', 'updated_at'])
        return indicator


class Indicator(models.Model):
    ROUTE_CHOICES = MemberSession.ROUTE_CHOICES
    QC_CHOICES = MemberSession.QC_CHOICES
    REPORT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('READY', 'Ready'),
        ('HELD', 'Held'),
    ]

    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='indicator',
    )
    member_session = models.OneToOneField(
        MemberSession,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='indicator',
    )
    posture_score = models.FloatField(default=0)
    lifestyle_score = models.FloatField(default=0)
    rep_achievement_rate = models.FloatField(default=0)
    rest_compliance = models.FloatField(default=0)
    pain_score = models.FloatField(default=0)
    function_training_score = models.FloatField(default=0)
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0)
    route = models.CharField(
        max_length=10, choices=ROUTE_CHOICES, default='AUTO'
    )
    review_signal = models.CharField(
        max_length=10,
        choices=ROUTE_CHOICES,
        default='AUTO',
    )
    qc_status = models.CharField(
        max_length=10, choices=QC_CHOICES, default='PASS'
    )
    counseling_priority = models.PositiveSmallIntegerField(default=3)
    report_status = models.CharField(
        max_length=10,
        choices=REPORT_STATUS_CHOICES,
        default='PENDING',
    )
    non_medical_notice = models.TextField(default=SAFETY_NOTICE)
    review_note = models.TextField(blank=True)
    trainer_confirmed = models.BooleanField(default=False)
    trainer_review_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        if self.member_session_id:
            return (
                f'{self.member_session.member_name} indicator - {self.route}'
            )
        return f'{self.session_id} indicator - {self.review_signal}'


class StrategyItem(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    priority = models.CharField(max_length=30, default='높음')
    status = models.CharField(max_length=40, default='진행 필요')
    output = models.TextField(blank=True)
    risk = models.TextField(blank=True)

    def __str__(self):
        return self.title
