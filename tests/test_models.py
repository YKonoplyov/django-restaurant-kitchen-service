from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.setup import SetUpKitchenDB


class ModelsTest(SetUpKitchenDB):

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


