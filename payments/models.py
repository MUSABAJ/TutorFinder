from msilib.schema import Class
from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from tutor_sessions.models import BaseSession
User = get_user_model()


STATUS_CHOICE = [
    ('pending', 'Pending'),
    ('held', 'Held in Escrow'),
    ('success', 'Succsess'),
    ('released', 'Withdrawn'),
    ('failed', 'Failed'),
]
class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students' ,limit_choices_to={'role': 'student'})
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutors', limit_choices_to={'role': 'tutor'})
    session = models.ForeignKey(BaseSession, on_delete=models.CASCADE, related_name='session')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    refrence_id = models.CharField(max_length=100, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_earnings(self):
        result = Payment.objects.filter(session__tutor=self,
                                        status='success').aggregate(total=models.Sum('amount'))
        return result['total']or 0

    def pending_balance(self):
        pending_payouts = Payment.objects.filter(session__tutor=self,
                                                 status='pending').aggregate(total=models.Sum('amount'))