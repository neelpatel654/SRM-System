from django import forms
from django.contrib.auth.models import User
from .models import Student,Result, Subject



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

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
    
    widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

