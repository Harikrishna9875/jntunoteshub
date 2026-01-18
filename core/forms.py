from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Upload, Rating, Report


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ["subject", "title", "description", "upload_type", "file"]
        widgets = {
            "subject": forms.Select(attrs={"class": "form-select rounded-4"}),
            "title": forms.TextInput(attrs={"class": "form-control rounded-4"}),
            "description": forms.Textarea(attrs={"class": "form-control rounded-4", "rows": 4}),
            "upload_type": forms.Select(attrs={"class": "form-select rounded-4"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control rounded-4"}),
        }


class SignupForm(UserCreationForm):
    agree = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "agree")


class LoginAgreeForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    agree = forms.BooleanField(required=True)


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["stars"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason"]
