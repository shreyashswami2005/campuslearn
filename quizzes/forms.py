from django import forms
from .models import Quiz, Question, Choice

class QuizForm(forms.Form):
    """Dynamically generated form for a quiz.
    The form fields are added in the view based on the questions.
    """
    pass
