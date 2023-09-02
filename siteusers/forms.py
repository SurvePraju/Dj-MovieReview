from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="",
                                max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control mb-3", "placeholder": "Password"}))
    password2 = forms.CharField(label="",
                                max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control mb-3", "placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username",
                  "email", "password1", "password2"]
        help_texts = {
            "username": ""
        }
        labels = {item: "" for item in fields}
        error_messages = {item: "" for item in fields}
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "First Name", "colspan": "2"}),
            "last_name": forms.TextInput(attrs={"class": "form-control col-6", "placeholder": "Last Name"}),
            "username": forms.TextInput(attrs={"class": "form-control mb-3 exd", "placeholder": "Username", "style": "width:99%;"}),
            "email": forms.EmailInput(attrs={"class": "form-control mb-3 me-2", "placeholder": "Email", "style": "width:99%;"})
            # "password1": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
            # "password2": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={"class": "form-control ms-3 mb-3", "placeholder": "Username", "style": "width:90%"}))
    password = forms.CharField(label="", max_length=100, widget=forms.PasswordInput(
        attrs={"class": "form-control ms-3 mb-3", "placeholder": "Password", "style": "width:90%"}))

    class Meta:
        model = User
        fields = ["username", "password"]


class ChangePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["password1", "password2"]
