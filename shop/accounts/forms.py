from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Необязательно")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserEmailForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["email"]
