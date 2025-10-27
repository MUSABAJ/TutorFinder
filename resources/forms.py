from django import forms
from .models import Resource

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'subject', 'description', 'file', 'video_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            valid_extensions = ['.pdf', '.pptx', '.txt', '.docx', '.zip']
            ext = file.name.lower().rsplit('.', 1)[-1]
            if f'.{ext}' not in valid_extensions:
                raise forms.ValidationError('Unsupported file type!')
        return file
