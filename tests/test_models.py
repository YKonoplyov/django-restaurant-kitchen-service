from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import (
    Cook, Dish,
    DishType, Ingredient,
    Position
)


class ModelsTest(TestCase):
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
        self.borch.ingredients.add(self.ingredient_beetroot, self.ingredient_water)

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
    def test_str_ingredient(self):
        self.assertEqual(str(self.ingredient_flour), "Flour")

    def test_str_dish_type(self):
        self.assertEqual(str(self.dish_type_soup), "soup")

    def test_dish_type_get_absolut_url(self):
        self.assertEqual(
            self.dish_type_soup.get_absolute_url(),
            reverse("kitchen:dish-type-list")
        )
    def test_str_position(self):
        self.assertEqual(str(self.main_cook_position), "main cook")

    def test_cook_get_absolute_url(self):
        self.assertEqual(
            self.main_cook.get_absolute_url(),
            reverse("kitchen:cook-detail", kwargs={"pk": self.main_cook.pk})
        )

    def test_dish_progres_percent(self):
        self.assertEqual(
            self.borch.progres_percent(), 0
        )
        self.borch.finished_cooks.add(self.main_cook)
        self.assertEqual(
            self.borch.progres_percent(), 50
        )

    def test_dish_get_absolute_url(self):
        self.assertEqual(
            self.borch.get_absolute_url(),
            reverse("kitchen:dish-list")
        )

    def test_dish_str(self):
        self.assertEqual(
            str(self.borch),
            "Borch"
        )


