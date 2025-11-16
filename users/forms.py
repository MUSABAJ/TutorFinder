from dataclasses import fields
import email
from random import choices
from django import forms
from django.contrib.admin.utils import help_text_for_field
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import widgets
from django.forms.widgets import Widget
from .models import *


GENDER_CHOICES = [
    ('male','Male'),
    ('female', 'Female'),
]
PAYMMENT_METHOD = [
    ('bank', 'Bank'),
     ('mobile','Mobile Bank')
    ]
LANGUAGE_CHOICES = [
    ('am', 'Amharic'),
    ('eng', 'English'),
    ('arab', 'Arabic'),
    ('oro', 'Affan-Oromo'),
    ('tig', 'Tigrigna'),
]
TEACHING_PREFRENCE_CHOICES = [
    ('online', 'Online Only'),
    ('inperson','In-person Only') 
    ,('both','Both Online & In-person')]
EXPIRIENCE_CHOICES = [
    ('lt1', 'Less than 1 Year'),
    ('1-3','1-3 Years') ,
    ('3-5','3-5 Years'),
    ('5-8','5-8 Years') ,
    ('gt8','8+ yeaers') 

    ]
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


class StudentRegisterForm(UserCreationForm):
    learning_goal = forms.ChoiceField( choices=GRADE_CHOICES)  
    grade_level = forms.ChoiceField(choices=GOAL_CHOICES)
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email','password1','password2']
        

class TutorRegisterForm(UserCreationForm):
    qualification = forms.CharField(widget=forms.Textarea(attrs={'class':'classnmae'}))
    experience = forms.ChoiceField( choices=EXPIRIENCE_CHOICES   )
    subjects = forms.CharField(widget=forms.Textarea)
    teaching_prefrence = forms.ChoiceField(  choices=TEACHING_PREFRENCE_CHOICES)
    horuly_rate = forms.IntegerField()
 

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password1','password2', 
                 ]

        help_texts = {
                    'password2': None,
                    }
        Widget = {'first_name': forms.TextInput(attrs={'class': 'classname', }),
                'last_name': forms.TextInput(attrs={'class': 'classname', }),
                'email': forms.TextInput(attrs={'class': 'classname', }), 
        }


class UserProfileEditForm(forms.ModelForm):
   
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 
                'phone','bio','date_of_birth', 'gender','country','city','sub_city',
                'username','avatar'
                
                 ]


class StudentProfileEditForm(forms.ModelForm):
    grade_level = forms.ChoiceField(choices=GRADE_CHOICES, required=False)
    field_of_study = forms.CharField(required=False)
    learning_goal = forms.ChoiceField(choices=GOAL_CHOICES, required=False)
    

    class Meta:
        model = StudentProfile
        fields = ['grade_level','field_of_study',  'learning_goal']  #add 'field_of_study',


class TutorProfileEditForm(forms.ModelForm):
    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LANGUAGE_CHOICES, required=False)
    qualification = forms.CharField(widget=forms.Textarea() , required=False)
    experience = forms.ChoiceField( choices=EXPIRIENCE_CHOICES ,required=False )
    subjects = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'English, Math, CS, Hemtigna'}))
    teaching_prefrence = forms.ChoiceField(  choices=TEACHING_PREFRENCE_CHOICES,required=False)
    horuly_rate = forms.IntegerField( required=False)
    # account_type = forms.ChoiceField( choices=PAYMMENT_METHOD, required=False)
    # account_number = forms.CharField( required=False,)
    # bank_code = forms.CharField( required=False)
    id_card = forms.FileField( required=False)
    certificate_file = forms.FileField( required=False)
    class Meta:
        model = TutorProfile
        fields = ['language','qualification','experience','subjects','teaching_prefrence'
                ,'horuly_rate','id_card','certificate_file','horuly_rate']


# class ChangePasswordForm(forms.ModelForm):
    
#         model = User
#         fields = ['password1', 'password2']

class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

# class CertificateForm(forms.ModelForm):
#     model = TutorProfile
#     fields = ['certificates']

class loginForm(AuthenticationForm): 
    fields = '__all__'


