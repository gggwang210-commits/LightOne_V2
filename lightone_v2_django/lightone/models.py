from django.db import models

from accounts.models import MemberProfile, TrainerProfile
from .algorithms import SAFETY_NOTICE, calculate_jatc, calculate_qs
from .utils.qs_calculator import determine_routing, map_pain_response_score, normalize_score


class MemberSession(models.Model):
    """Trainer-reviewed non-medical PT consultation session."""

    ROUTE_AUTO = "AUTO"
    ROUTE_REVIEW = "REVIEW"
    ROUTE_BLOCK = "BLOCK"
    ROUTE_CHOICES = [
        (ROUTE_AUTO, "AUTO"),
        (ROUTE_REVIEW, "REVIEW"),
        (ROUTE_BLOCK, "BLOCK"),
    ]

    QC_PASS = "PASS"
    QC_CHECK = "CHECK"
    QC_FAIL = "FAIL"
    QC_CHOICES = [
        (QC_PASS, "PASS"),
        (QC_CHECK, "CHECK"),
        (QC_FAIL, "FAIL"),
    ]

    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sessions",
    )
    trainer = models.ForeignKey(
        TrainerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conducted_sessions",
    )

    member_name = models.CharField(max_length=80)
    trainer_name = models.CharField(max_length=80, default="김라이트")
    goal = models.CharField(max_length=120)
    discomfort_area = models.CharField(max_length=120, blank=True)

    form_accuracy = models.FloatField(default=0)
    pain_response = models.FloatField(default=0)
    rpe = models.FloatField(default=0)
    rep_score = models.FloatField(default=100)
    rest_score = models.FloatField(default=100)
    qc_score = models.FloatField(default=100)

    posture_score = models.FloatField(default=0)
    lifestyle_score = models.FloatField(default=0)
    function_training_score = models.FloatField(default=0)

    qs_form_component = models.FloatField(default=0)
    qs_discomfort_component = models.FloatField(default=0)
    qs_rpe_component = models.FloatField(default=0)
    qs_qc_component = models.FloatField(default=100)
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0, help_text="비의료 운동상담 참고용 JATC 점수입니다.")

    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default=ROUTE_AUTO)
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default=QC_PASS)
    safety_notice = models.TextField(default=SAFETY_NOTICE)
    review_note = models.TextField(blank=True)
    trainer_confirmed = models.BooleanField(default=False)
    memo = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-qs_score"]

    def __str__(self):
        return f"{self.member_name} - {self.route}"

    @property
    def routing_badge_class(self):
        return {
            self.ROUTE_AUTO: "badge-auto",
            self.ROUTE_REVIEW: "badge-review",
            self.ROUTE_BLOCK: "badge-block",
        }.get(self.route, "badge-review")

    @property
    def routing_label(self):
        return self.route

    def calculate_qs_and_route(self):
        """Calculate MVP QS/JATC scores and non-medical trainer review routing."""
        self.qs_form_component = normalize_score(self.form_accuracy)
        self.qs_discomfort_component = map_pain_response_score(self.pain_response)
        self.qs_rpe_component = normalize_score(self.rep_score)
        self.qs_qc_component = normalize_score(self.rest_score)
        self.qs_score = calculate_qs(
            self.form_accuracy,
            self.rep_score,
            self.rest_score,
            self.pain_response,
        )
        self.jatc_score = calculate_jatc(
            self.qs_score,
            self.form_accuracy,
            self.pain_response,
            self.rpe,
        )
        safety_flags = {
            "qc_status_fail": self.qc_status == self.QC_FAIL,
            "qc_score_low": self.qc_score < 60,
        }
        self.route = determine_routing(self.qs_score, self.pain_response, safety_flags=safety_flags)
        self.safety_notice = SAFETY_NOTICE

        if self.route == self.ROUTE_BLOCK:
            self.review_note = "BLOCK: 통증 반응 또는 QC 안전 신호 확인이 필요합니다."
        elif self.route == self.ROUTE_REVIEW:
            self.review_note = "REVIEW: 트레이너 검토 후 상담 리포트 생성이 권장됩니다."
        elif not self.review_note:
            self.review_note = "AUTO: 비의료 상담 리포트 초안 생성 가능 상태입니다."

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")
        self.calculate_qs_and_route()
        if update_fields is not None:
            kwargs["update_fields"] = set(update_fields) | {
                "qs_form_component",
                "qs_discomfort_component",
                "qs_rpe_component",
                "qs_qc_component",
                "qs_score",
                "jatc_score",
                "route",
                "safety_notice",
                "review_note",
                "updated_at",
            }
        super().save(*args, **kwargs)
        Indicator.objects.update_or_create(
            member_session=self,
            defaults={
                "qs_score": self.qs_score,
                "jatc_score": self.jatc_score,
                "route": self.route,
                "qc_status": self.qc_status,
                "non_medical_notice": SAFETY_NOTICE,
                "trainer_review_required": self.route in {self.ROUTE_REVIEW, self.ROUTE_BLOCK} or self.qc_status != self.QC_PASS,
            },
        )


class Member(models.Model):
    """Synthetic/demo member for dashboard experiments. Do not store direct identifiers here."""

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("PAUSED", "Paused"),
        ("ARCHIVED", "Archived"),
    ]

    synthetic_id = models.CharField(max_length=40, unique=True)
    display_label = models.CharField(max_length=80)
    goal = models.CharField(max_length=120, blank=True)
    experience_level = models.CharField(max_length=40, blank=True)
    discomfort_area = models.CharField(max_length=80, blank=True)
    consent_status = models.CharField(max_length=30, default="synthetic_demo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["synthetic_id"]

    def __str__(self):
        return self.display_label


class Session(models.Model):
    """Legacy synthetic session model retained for migration compatibility."""

    ROUTE_CHOICES = MemberSession.ROUTE_CHOICES
    QC_CHOICES = MemberSession.QC_CHOICES

    session_id = models.CharField(max_length=40, unique=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="session_records")
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
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default=MemberSession.QC_PASS)
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default=MemberSession.ROUTE_AUTO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-session_date", "session_id"]

    def __str__(self):
        return f"{self.session_id} - {self.member.display_label}"

    def calculate_reference_scores(self):
        rep_rate = 100.0 if not self.planned_reps else min(100.0, (self.completed_reps / self.planned_reps) * 100)
        if not self.planned_rest_seconds:
            rest_compliance = 100.0
        else:
            rest_gap = abs(self.actual_rest_seconds - self.planned_rest_seconds) / self.planned_rest_seconds
            rest_compliance = max(0.0, 100.0 - (rest_gap * 100))

        qs_score = calculate_qs(100, rep_rate, rest_compliance, self.pain_response)
        jatc_score = calculate_jatc(qs_score, 100, self.pain_response, self.rpe)
        route = determine_routing(
            qs_score,
            self.pain_response,
            safety_flags={"qc_status_fail": self.qc_status == MemberSession.QC_FAIL},
        )
        return {"qs_score": qs_score, "jatc_score": jatc_score, "route": route}

    def update_route(self):
        result = self.calculate_reference_scores()
        self.route = result["route"]
        self.save(update_fields=["route", "updated_at"])
        return result


class Indicator(models.Model):
    """Non-medical score snapshot generated from MemberSession."""

    ROUTE_CHOICES = MemberSession.ROUTE_CHOICES
    QC_CHOICES = MemberSession.QC_CHOICES

    member_session = models.OneToOneField(MemberSession, on_delete=models.CASCADE, related_name="indicator")
    qs_score = models.FloatField(default=0)
    jatc_score = models.FloatField(default=0)
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default=MemberSession.ROUTE_AUTO)
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default=MemberSession.QC_PASS)
    non_medical_notice = models.TextField(default=SAFETY_NOTICE)
    trainer_review_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-qs_score"]

    def __str__(self):
        return f"{self.member_session.member_name} indicator - {self.route}"


class StrategyItem(models.Model):
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    priority = models.CharField(max_length=30, default="높음")
    status = models.CharField(max_length=40, default="진행 필요")
    output = models.TextField(blank=True)
    risk = models.TextField(blank=True)

    def __str__(self):
        return self.title
