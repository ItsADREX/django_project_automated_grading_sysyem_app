from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, Choice


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'cutoff_mark', 'timer']

class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter question here'}))

    class Meta:
        model = Question
        fields = ['text', 'score']


ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('text', 'is_correct'), extra=1)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
