from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class StudentRegistrationForm(UserCreationForm):
    matric_number = forms.CharField(max_length=10, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'matric_number', 'password1', 'password2']

class InstructorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class InstructorLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

class StudentLoginForm(AuthenticationForm):
    matric_number = forms.CharField(max_length=10, required=True)
    
    