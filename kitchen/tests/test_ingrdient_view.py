from django.urls import reverse

from kitchen.models import Ingredient
from kitchen.tests.setup import SetUpKitchenDB

INGREDIENT_LIST_URL = reverse("kitchen:ingredient-list")


class PublicIngredientViewsTest(SetUpKitchenDB):

    def test_login_required_ingredient_list(self) -> None:
        response = self.client.get(INGREDIENT_LIST_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_ingredient_create(self) -> None:
        ingredient_create_url = reverse("kitchen:ingredient-create")
        response = self.client.get(ingredient_create_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_ingredient_update(self) -> None:
        ingredient_update_url = reverse(
            "kitchen:ingredient-update",
            kwargs={"pk": self.ingredient_apple.pk}

        )
        response = self.client.get(ingredient_update_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_ingredient_delete(self) -> None:
        ingredient_delete_url = reverse(
            "kitchen:ingredient-delete",
            kwargs={"pk": self.ingredient_flour.pk}
        )
        response = self.client.get(ingredient_delete_url)
        self.assertNotEquals(response.status_code, 200)


class IngredientListViewTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_retrieve_ingredient_list(self) -> None:
        response = self.client.get(INGREDIENT_LIST_URL)
        ingredients = Ingredient.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(ingredients)
        )

    def test_search_ingredient_by_name(self) -> None:
        url = reverse("kitchen:ingredient-list")
        ingredients = Ingredient.objects.all()
        response = self.client.get(f"{url}?name=apple")
        self.assertIn(
            self.ingredient_apple,
            list(response.context["ingredient_list"])
        )
        self.assertNotIn(
            self.ingredient_flour,
            list(response.context["ingredient_list"])
        )

        response = self.client.get(f"{url}?name=")
        self.assertEqual(
            list(ingredients),
            list(response.context["ingredient_list"])
        )


class IngredientViewsTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_ingredient_create_view(self) -> None:
        ingredient_data = {
            "name": "potato",
        }
        url = reverse("kitchen:ingredient-create")
        response = self.client.post(url, ingredient_data)

        self.assertEqual(response.status_code, 302)

        created_ingredient = Ingredient.objects.last()

        self.assertEqual(created_ingredient.name, ingredient_data["name"])

    def test_ingredient_update_page(self):
        ingredient_data = {
            "name": "potato",
        }

        url = reverse(
            "kitchen:ingredient-update",
            kwargs={"pk": self.ingredient_apple.id}
        )
        response = self.client.post(url, ingredient_data)

        self.ingredient_apple.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.ingredient_apple.name, ingredient_data["name"])

    def test_ingredient_delete_view(self):

        url = reverse(
            "kitchen:ingredient-delete",
            kwargs={"pk": self.ingredient_apple.id}
        )
        response = self.client.post(url)
        ingredients = Ingredient.objects.all()

        self.assertEqual(response.status_code, 302)

        self.assertNotIn(self.ingredient_apple, ingredients)

    def test_ingredient_delete_view_non_exist_ingredient(self):
        url = reverse("kitchen:ingredient-delete", kwargs={"pk": 999})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
