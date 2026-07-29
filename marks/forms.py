from django import forms
from .models import InternalMark

class InternalMarkForm(forms.ModelForm):
    """Form for teachers to input internal marks for a student/component."""

    class Meta:
        model = InternalMark
        fields = ['student', 'component', 'score', 'max_score', 'date_recorded']
        widgets = {
            'date_recorded': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'student': 'Student',
            'component': 'Evaluation Component',
            'score': 'Score Obtained',
            'max_score': 'Maximum Score',
            'date_recorded': 'Date Recorded',
        }
