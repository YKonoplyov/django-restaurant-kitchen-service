from django import forms
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Cook, Dish, Ingredient, DishType


class CookForm(UserCreationForm):
    class Meta:
        model = Cook
        fields = ["username", "password1", "password2", "first_name", "last_name", "position", "years_of_experience"]


class CookUpdateForm(forms.ModelForm):

    class Meta:
        model = Cook
        fields = ["username", "first_name", "last_name", "position", "years_of_experience"]


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = "__all__"


# class DishForm(forms.ModelForm):
#
#     class Meta:
#         model = Dish
#         fields = "__all__"
