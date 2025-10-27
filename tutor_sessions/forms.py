from django import forms
from .models import BaseSession


class BookingForm(forms.ModelForm):
    subject_name = forms.CharField(label='Subject') 
    class Meta:
        model = BaseSession
        fields = ('subject_name',) 
 

