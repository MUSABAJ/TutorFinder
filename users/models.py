from email.policy import default
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('admin', 'Admin')
    ]
       
    first_name = models.CharField(max_length= 29)
    last_name = models.CharField(max_length =29)
    username = models.CharField(unique=True, max_length=25)
    role = models.CharField(max_length= 10, default='student', choices = ROLE_CHOICES )
    bio = models.TextField(blank=True, null=True)
    email =models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=100,blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    sub_city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField (default='user.png')
    phone = models.CharField(max_length=15 ,blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10 ,blank=True, null=True)
    
    # @receiver(post_save, sender=User)
    # def create_student_profile(sender, instance, created, **kwargs):
    #     if created and instance.role == 'student':
    #         StudentProfile.objects.create(user=instance)


    def __str__(self): return self.username  
    def is_admin(self): return self.role == 'admin'
    def is_tutor(self): return self.role == 'tutor' 
    def is_student(self): return self.role == 'student'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor')
    language = models.TextField()
    qualification = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=50,blank=True, null=True)
    teaching_prefrence = models.CharField(max_length=60,default='both')
    subjects = models.TextField()
    account_type = models.CharField(max_length=10,blank=True, null=True)     # bank or mobile banking
    account_number = models.CharField(max_length=15,blank=True, null=True)    # bank or mobile banking acc no
    bank_code = models.CharField(max_length=15, blank=True, null=True)
    id_card = models.FileField(upload_to='id_cards/', blank=True ,null=True)
    certificate_file = models.FileField(upload_to='verification_docs/', blank=True, null= True)
    horuly_rate = models.IntegerField()
    rating = models.DecimalField(default=0.0 ,max_digits=5, decimal_places=2)
    is_verified = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):
    GRADE_CHOICES = [
        ('elementary', 'Elementary (kG-5)'),
        ('primary', 'Primary (6-8)'),
        ('secondary', 'High School (9-12)'),
        ('college', 'College/University'),
        ('adult', 'Adult Learner'),
        ('professional', 'professional Development'),
     ]
    GOAL_CHOICES = [
        ('homework', 'Study and Homework help'),
        ('language', 'Language learning'),
        ('career', 'Career Advancment'),
        ('skill','Skill Development'),
        ('exam', 'Exam Preparation'),
        ('other', 'Other')
      ]
    user = models.OneToOneField(User, related_name='profile', on_delete = models.CASCADE)
    learning_goal = models.CharField(max_length=60, choices=GOAL_CHOICES ,default='other')
    grade_level = models.CharField(max_length=60,choices=GRADE_CHOICES, default='primary')
    favorite = models.CharField(blank=True, null=True)
    field_of_study = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):return self.user.username
    