from django import forms
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Cook


class CookForm(UserCreationForm):
    class Meta:
        model = Cook
        fields = ["username", "password1", "password2", "first_name", "last_name", "position", "years_of_experience"]


class CookUpdateForm(forms.ModelForm):

    class Meta:
        model = Cook
        fields = ["username", "first_name", "last_name", "position", "years_of_experience"]
