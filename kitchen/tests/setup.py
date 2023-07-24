from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import (
    Dish, DishType,
    Ingredient, Position
)


class SetUpKitchenDB(TestCase):
    def setUp(self):
        self.main_cook_position = Position.objects.create(
            name="main cook"
        )
        self.cook_position = Position.objects.create(
            name="cook"
        )
        self.dish_type_soup = DishType.objects.create(
            name="soup"
        )
        self.dish_type_desert = DishType.objects.create(
            name="desert"
        )
        self.ingredient_beetroot = Ingredient.objects.create(
            name="Beetroot"
        )
        self.ingredient_apple = Ingredient.objects.create(
            name="Apple"
        )
        self.ingredient_water = Ingredient.objects.create(
            name="Water"
        )
        self.ingredient_flour = Ingredient.objects.create(
            name="Flour"
        )
        self.main_cook = get_user_model().objects.create_user(
            username="main.cook",
            password="Admin654",
            position=self.main_cook_position,
            years_of_experience=5
        )
        self.cook = get_user_model().objects.create_user(
            username="helper.cook",
            password="Admin654",
            position=self.cook_position,
            years_of_experience=2
        )
        self.borch = Dish.objects.create(
            name="Borch",
            description="Ukraine national dish",
            dish_type=self.dish_type_soup,
            price=5,
        )
        self.borch.cooks.add(self.main_cook, self.cook)
        self.borch.ingredients.add(
            self.ingredient_beetroot,
            self.ingredient_water
        )

        self.apple_pie = Dish.objects.create(
            name="Apple pie",
            description="Ukraine national dish",
            dish_type=self.dish_type_desert,
            price=4,
        )
        self.apple_pie.cooks.add(self.cook)
        self.apple_pie.ingredients.add(
            self.ingredient_apple, self.ingredient_flour
        )


class AdminSiteSetUpMixin(TestCase):
    def setUp(self) -> None:
        self.main_cook_position = Position.objects.create(
            name="main cook"
        )
        self.cook_position = Position.objects.create(
            name="cook"
        )

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test12345",
            years_of_experience=15,
            position=self.main_cook_position,


        )
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="driver12345",
            years_of_experience=3,
            position=self.cook_position
        )
        self.client.force_login(self.admin_user)
