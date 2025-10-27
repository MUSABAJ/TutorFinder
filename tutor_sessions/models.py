from django.db import models
from users.models import User
from django.utils import timezone

class BaseSession(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Accepted'),
        ('ongoing', 'Ongoing'),
        ('decline', 'Request Not Accepted'),
        ('canceld', 'Canceld'),
        ('completed', 'Completed')]    
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_sessions',
                                 limit_choices_to={'role': 'student'})
    tutor = models.ForeignKey(User, on_delete= models.CASCADE, related_name='tutor_sessions',
                                limit_choices_to={'role': 'tutor'} )
    subject_name = models.CharField()
    total_session = models.PositiveIntegerField(default=3) # in minutes
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_payed = models.BooleanField(default=False)
    session_duration = models.PositiveIntegerField(default=45)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)    
    remaining_hours = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    scheduled_at = models.DateTimeField(auto_now_add=True)
    remaining_sessions = models.IntegerField() 
    # Real-tiem tracking
    current_start_time = models.DateTimeField(blank=True, null=True)
    current_end_time = models.DateTimeField(blank=True, null=True)
    
    def __str__(self): return f'{self.tutor}-{self.student}'
    
    def start_session(self):
        self.current_start_time = timezone.now()
        self.status='active'
        self.save()
    
    def end_session(self):
        self.current_end_time = timezone.now()

        duration_second = (self.current_end_time-self.current_start_time).total_seconds() 
        duration_hours = round(duration_second / 3600 ,2)
        self.remaining_hours = float(self.remaining_hours )- duration_hours
        if self.remaining_hours <= 0:
            self.status='completed'
            self.remaining_hours = 0
            self.save()
            
        else:
            self.status='ongoing'
            self.save()
 
  
class BookedSession(models.Model):

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('missed', 'Missed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Reschedule'),
        ]   
    TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'In_person'),
        ]
    NOTIFICATION_CHOICES = [
    ('0', 'not_notified'),
    ('1', 'notified_morning'),
    ('2', 'notified_hour'),
    ('3', 'notified'),
    ]   
     
    base_session = models.ForeignKey(BaseSession, related_name='sessions', on_delete=models.CASCADE)
    topic = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50) 
    location = models.CharField(max_length=255, blank=True, null=True)
    room_name = models.CharField(max_length=255, blank=True, null=True)
    session_type = models.CharField(choices=TYPE_CHOICES)
    schedule_date = models.DateTimeField(auto_now_add=True)
    notification_status = models.CharField(max_length=15, choices=NOTIFICATION_CHOICES, default= '0')
    
 

class VirtualClass(models.Model):
    session = models.OneToOneField(BookedSession, on_delete=models.CASCADE, related_name='virtual_calss')
    room_name = models.CharField(max_length=100, unique=True)
    created_at = models.TimeField(auto_now_add=True)