from django import forms
from .models import FeedBack

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your feedback...'}),
        }
