from django import forms
from django.contrib.auth.models import User
from .models import Student, Result, Subject
from django_select2.forms import Select2Widget


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "profile_image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }


class StudentAddForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=Select2Widget(
            attrs={"style": "width: 100%;", "data-placeholder": "Select a user"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(student__isnull=False)  # type: ignore


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]
