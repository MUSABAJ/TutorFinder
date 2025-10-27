from django import forms
from .models import FeedBack

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['rating', 'feedback']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, '⭐' * i) for i in range(1, 6)]),
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your feedback...'}),
        }

    # def clean_feedback(self):
    #     data = self.cleaned_data.get('feedback', '').strip()
    #     if not data:
    #         raise forms.ValidationError("Feedback cannot be empty.")
    #     return data
