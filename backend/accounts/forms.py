from django import forms
from django.core import validators
from django.contrib.auth.forms import (
    AuthenticationForm, 
    UserCreationForm, 
    UsernameField
)
from django.utils.translation import gettext, gettext_lazy as _

from . import models 


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label=_("Username"),
        required=True,
        strip=True,
        validators=[],
        widget=forms.TextInput(
            attrs={
                "autofocus" : True,
                "class" : "form-control ",
                "placeholder": "email",
                "title" : "Enter your email here",
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class" : "form-control w-100",
                "placeholder" : "password",
                "title" : "Enter your password here"
            }
        )
    )