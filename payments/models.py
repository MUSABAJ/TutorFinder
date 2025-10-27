from msilib.schema import Class
from django.db import models
from django.contrib.auth import get_user_model
from tutor_sessions.models import BaseSession
User = get_user_model()


STATUS_CHOICE = [
    ('pending', 'Pending'),
    ('relese', 'Held in System'),
    ('success', 'Succsess'),
    ('failed', 'Failed'),
]
class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students' ,limit_choices_to={'role': 'student'})
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutors', limit_choices_to={'role': 'tutor'})
    session = models.ForeignKey(BaseSession, on_delete=models.CASCADE, related_name='session')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    refrence_id = models.CharField(max_length=100, null=True, blank=True ) #set nulll and blanck to true
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
