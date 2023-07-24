from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Dish, Ingredient


class CookForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username", "password1", "password2",
            "first_name", "last_name", "position",
            "years_of_experience"]


class CookUpdateForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = [
            "username", "first_name", "last_name",
            "position", "years_of_experience"
        ]


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = "__all__"


class DishForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = "__all__"
        exclude = ("finished_cooks",)
        widgets = {
            "cooks": forms.CheckboxSelectMultiple(),
            "ingredients": forms.CheckboxSelectMultiple(),
        }


class CookUsernameSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
