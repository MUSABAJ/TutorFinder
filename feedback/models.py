from django.db import models
from tutor_sessions.models import BaseSession
from users.models import User


class FeedBack(models.Model):
    session = models.OneToOneField(BaseSession, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_feedback')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedback')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('session', 'student')  # prevents duplicate feedback for same session

    def __str__(self):
        return f"{self.student.username} rated {self.tutor.username} ({self.rating}/5)"

    @staticmethod
    def get_tutor_average(tutor):
        """Returns average rating for a given tutor"""
        avg = FeedBack.objects.filter(tutor=tutor).aggregate(models.Avg('rating'))['rating__avg']
        return round(avg or 0, 1)

    def short_feedback(self):
        return self.feedback[:50] + "..." if self.feedback else "No comments"
