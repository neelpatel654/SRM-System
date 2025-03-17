from django import forms
from django.contrib.auth.models import User
from .models import Student,Result

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'
        