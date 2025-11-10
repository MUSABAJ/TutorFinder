from django.db import models
from tutor_sessions.models import BookedSession
from users.models import User

DISPUTE_STATUS = [
    ('open', 'Open'),
    ('resolved', 'Resolved'),
 ]

class Dispute(models.Model):
    session = models.ForeignKey(BookedSession, on_delete=models.CASCADE)
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=DISPUTE_STATUS, default='open')
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
 