from django import forms
from .models import TutorPackage

PER_WEEK_CHOICE = [ 
    (1,'1 Session'),
    (2, '2 Session'),
    (3, '3 Session'),
    (4, '4 Session'),
]

TEACHING_pkg_CHOICES = [
    ('online', 'Online Only'),
    ('inperson','In-person Only') 
    ,('both','Both Online & In-person')]


class PackageForm(forms.ModelForm):
    session_perweek = forms.ChoiceField( choices=PER_WEEK_CHOICE)
    session_type = forms.ChoiceField( choices=TEACHING_pkg_CHOICES   )
    class Meta:
        model = TutorPackage
        fields = ('name','description','total_session','session_type',
                  'session_duration','session_perweek','price')
    