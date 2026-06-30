from django.db import models


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
    route = models.CharField(max_length=10, choices=ROUTE_CHOICES, default='AUTO')
    qc_status = models.CharField(max_length=10, choices=QC_CHOICES, default='PASS')
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-qs_score']

    def __str__(self):
        return f'{self.member_name} - {self.route}'

    def calculate_qs_and_route(self):
        """
        규칙 기반 엔진 (MVP용)
        """
        base_score = 100
        penalty = (self.pain_response * 5) + (abs(self.rpe - 7) * 2)
        bonus = (self.form_accuracy * 2)
        
        final_score = base_score - penalty + bonus
        self.qs_score = max(0, min(100, round(final_score, 1)))
        
        if self.pain_response >= 7 or self.qs_score < 40:
            self.route = 'BLOCK'
        elif self.pain_response >= 4 or self.qs_score < 70:
            self.route = 'REVIEW'
        else:
            self.route = 'AUTO'
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
