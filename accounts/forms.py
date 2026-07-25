from django import forms

from .models import StudentProfile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False, label='First name')
    last_name = forms.CharField(max_length=150, required=False, label='Last name')
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = StudentProfile
        fields = (
            'phone',
            'college',
            'department',
            'year_of_study',
            'student_id',
            'bio',
        )
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email
        for name, field in self.fields.items():
            css = 'form-control'
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault('class', css)
            else:
                field.widget.attrs.setdefault('class', css)

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data.get('first_name', '')
        self.user.last_name = self.cleaned_data.get('last_name', '')
        self.user.email = self.cleaned_data.get('email', '')
        if commit:
            self.user.save()
            profile.save()
        return profile
