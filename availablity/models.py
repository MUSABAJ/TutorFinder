from django.db import models
from users.models import User



class Availablity(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'tutor'})
    availablity = models.JSONField(default=dict)
    updated_at= models.DateTimeField( auto_now=True)
    def __str__(self):
        return f"{self.tutor.username} - {self.updated_at} "


class TutorPackage(models.Model):
    tutor = models.ForeignKey(User, on_delete = models.CASCADE, limit_choices_to={'role': 'tutor'} )
    name = models.CharField(max_length = 100)
    description  = models.TextField()
    session_type = models.CharField(max_length = 10, choices=[
                                                            ('online','Online'),
                                                            ('in-person','In_person'),
                                                            ('both','Both')])
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_session = models.PositiveIntegerField()
    session_duration = models.PositiveIntegerField()    # eg..........5 session ///1 session=60 min
    session_perweek = models.PositiveIntegerField()

 