from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

class SubmissionForm(forms.Form):
    file = forms.FileField(label='Upload your submission', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
