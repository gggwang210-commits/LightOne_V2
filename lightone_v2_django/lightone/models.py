import uuid
from django.db import models

from django.db import models

from accounts.models import MemberProfile, TrainerProfile
from .algorithms import SAFETY_NOTICE, calculate_jatc, calculate_qs, route_session


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

    member_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        help_text='비의료 참고 목적의 성별 분류이며 직접 식별정보를 포함하지 않습니다.',
    )
    age_group = models.CharField(max_length=20, help_text='비의료 참고 목적의 연령대입니다.')
    goals = models.TextField(blank=True, help_text='비의료 참고 목적의 운동 목표입니다.')
    consent = models.BooleanField(default=False, help_text='비의료 참고 데이터 활용 동의 여부입니다.')

    class Meta:
        ordering = ['age_group', 'member_id']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        return f'Member {str(self.member_id)[:8]} ({self.age_group})'


class Session(models.Model):
    """회원별 운동 세션 기록(비의료 참고)으로 트레이너 상담 보조에만 사용한다."""

    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateTimeField(help_text='비의료 참고 목적의 운동 세션 일시입니다.')
    exercise_name = models.CharField(max_length=120, help_text='비의료 참고 목적의 운동명입니다.')
    sets = models.PositiveIntegerField(help_text='비의료 참고 목적의 세트 수입니다.')
    reps_target = models.PositiveIntegerField(help_text='비의료 참고 목적의 목표 반복 수입니다.')
    reps_completed = models.PositiveIntegerField(help_text='비의료 참고 목적의 완료 반복 수입니다.')
    rpe = models.FloatField(help_text='비의료 참고 목적의 운동자각도입니다.')
    pain_response = models.PositiveSmallIntegerField(help_text='비의료 참고 목적의 통증 반응 점수입니다.')
    trainer_notes = models.TextField(blank=True, help_text='비의료 참고 목적의 트레이너 메모입니다.')

    class Meta:
        ordering = ['-date', 'exercise_name', 'session_id']
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'

    def __str__(self):
        return f'Session {str(self.session_id)[:8]} - {self.date:%Y-%m-%d} - {self.exercise_name}'


class Indicator(models.Model):
    """운동 세션별 지표(비의료 참고)로 자동 라우팅 보조에만 사용한다."""

    ROUTING_AUTO = 'AUTO'
    ROUTING_REVIEW = 'REVIEW'
    ROUTING_BLOCK = 'BLOCK'
    ROUTING_STATUS_CHOICES = [
        (ROUTING_AUTO, 'AUTO'),
        (ROUTING_REVIEW, 'REVIEW'),
        (ROUTING_BLOCK, 'BLOCK'),
    ]

    indicator_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='indicator')
    qs_score = models.FloatField(help_text='비의료 참고 목적의 품질 점수입니다.')
    form_accuracy = models.FloatField(help_text='비의료 참고 목적의 자세 정확도입니다.')
    rep_rate = models.FloatField(help_text='비의료 참고 목적의 반복 속도입니다.')
    rest_compliance = models.FloatField(help_text='비의료 참고 목적의 휴식 준수율입니다.')
    pain_score = models.FloatField(help_text='비의료 참고 목적의 통증 점수입니다.')
    jatc_pain = models.FloatField(help_text='비의료 참고 목적의 JATC 통증 지표입니다.')
    jatc_posture = models.FloatField(help_text='비의료 참고 목적의 JATC 자세 지표입니다.')
    jatc_function = models.FloatField(help_text='비의료 참고 목적의 JATC 기능 지표입니다.')
    jatc_lifestyle = models.FloatField(help_text='비의료 참고 목적의 JATC 생활습관 지표입니다.')
    routing_status = models.CharField(
        max_length=10,
        choices=ROUTING_STATUS_CHOICES,
        default=ROUTING_AUTO,
        help_text='비의료 참고 목적의 자동 라우팅 상태입니다.',
    )

    class Meta:
        ordering = ['routing_status', 'indicator_id']
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'

    def __str__(self):
        return f'Indicator {str(self.indicator_id)[:8]} - {self.routing_status}'

from .algorithms import SAFETY_NOTICE, calculate_qs, route_session
from .utils.jatc_calculator import calculate_jatc


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
    jatc_score = models.FloatField(default=0, help_text='비의료 운동상담 참고용 JATC 점수입니다.')
    form_accuracy = models.FloatField(default=0)
    pain_response = models.FloatField(default=0)
    rpe = models.FloatField(default=0)
    qs_form_component = models.FloatField(default=0)
    qs_discomfort_component = models.FloatField(default=0)
    qs_rpe_component = models.FloatField(default=0)
    qs_qc_component = models.FloatField(default=100)
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        return f'{self.member_name} - {self.route}'

    def calculate_qs_and_route(self, commit=True):
        """Calculate MVP QS/JATC scores and non-medical trainer review routing."""
        self.qs_form_component = self.form_accuracy * 10 if self.form_accuracy <= 10 else self.form_accuracy
        self.qs_discomfort_component = 100 - (self.pain_response * 10)
        self.qs_rpe_component = 100 - (abs(self.rpe - 7) * 10)
        self.qs_qc_component = self.qc_score
        self.qs_score = calculate_qs(self.form_accuracy, self.pain_response, self.rpe, self.qc_score)
        jatc_result = calculate_jatc(self)
        self.jatc_score = jatc_result['score']
        self.route = route_session(self.qs_score, self.jatc_score, self.pain_response, self.qc_status)
        self.safety_notice = jatc_result['notice']
        if commit:
            self.save()
        return jatc_result

    def save(self, *args, **kwargs):
        if not getattr(self, '_calculating_scores', False):
            self._calculating_scores = True
            self.calculate_qs_and_route(commit=False)
            self._calculating_scores = False
        super().save(*args, **kwargs)


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
    ROUTE_CHOICES = MemberSession.ROUTE_CHOICES
    QC_CHOICES = MemberSession.QC_CHOICES

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

    def update_indicator_scores(self):
        indicator, _created = Indicator.objects.get_or_create(session=self)
        jatc_result = calculate_jatc(self)
        indicator.qs_score = jatc_result['qs_score']
        indicator.jatc_score = jatc_result['score']
        indicator.pain_score = jatc_result['pain_component']
        indicator.review_signal = route_session(indicator.qs_score, indicator.jatc_score, self.pain_response, self.qc_status)
        indicator.review_note = jatc_result['notice']
        indicator.save()
        self.route = indicator.review_signal
        self.save(update_fields=['route', 'updated_at'])
        return indicator


class Indicator(models.Model):
    ROUTE_CHOICES = Session.ROUTE_CHOICES
    REPORT_CHOICES = [
        ('PENDING', 'Pending'),
        ('READY', 'Ready'),
        ('HELD', 'Held'),
    ]

    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='indicator', null=True, blank=True)
    member_session = models.OneToOneField(
        MemberSession,
        on_delete=models.CASCADE,
        related_name='indicator',
        null=True,
        blank=True,
    )
    posture_score = models.FloatField(default=0)
    lifestyle_score = models.FloatField(default=0)
    rep_achievement_rate = models.FloatField(default=0)
    rest_compliance = models.FloatField(default=0)
    pain_score = models.FloatField(default=0)
    function_training_score = models.FloatField(default=0)
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0, help_text='비의료 운동상담 참고용 JATC 점수입니다.')
    review_signal = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    counseling_priority = models.PositiveSmallIntegerField(default=3)
    report_status = models.CharField(max_length=10, choices=REPORT_CHOICES, default='PENDING')
    review_note = models.TextField(blank=True, help_text='비의료 운동상담 참고용 안내 문구입니다.')
    trainer_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-qs_score', 'session__session_id']

    def __str__(self):
        if self.member_session_id:
            return f'{self.member_session.member_name} indicator'
        if not self.session_id:
            return 'Unlinked indicator'
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


@receiver(post_save, sender=MemberSession)
def sync_member_session_indicator(sender, instance, **kwargs):
    """Create or update the non-medical indicator snapshot when a member session is saved."""
    Indicator.objects.update_or_create(
        member_session=instance,
        defaults={
            'posture_score': instance.posture_score,
            'lifestyle_score': instance.lifestyle_score,
            'pain_score': instance.pain_response,
            'function_training_score': instance.function_training_score,
            'qs_score': instance.qs_score,
            'jatc_score': instance.jatc_score,
            'review_signal': instance.route,
            'review_note': instance.review_note,
            'trainer_confirmed': instance.trainer_confirmed,
            'report_status': 'HELD' if instance.route == 'BLOCK' else 'READY',
            'counseling_priority': 1 if instance.route == 'BLOCK' else 2 if instance.route == 'REVIEW' else 3,
        },
    )
