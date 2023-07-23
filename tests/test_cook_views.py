from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import (
    Dish, DishType,
    Ingredient, Position, Cook
)
from tests.setup import SetUpKitchenDB

COOK_LIST_URL = reverse("kitchen:cook-list")


class PublicCookViewsTest(SetUpKitchenDB):
    def setUp(self) -> None:
        self.main_cook_position = Position.objects.create(
            name="main cook"
        )
        self.cook_position = Position.objects.create(
            name="cook"
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

    def test_login_required_cook_list(self) -> None:
        response = self.client.get(COOK_LIST_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cook_detail(self) -> None:
        cook_detail_url = reverse(
            "kitchen:cook-detail",
            kwargs={"pk": self.main_cook.pk}
        )
        response = self.client.get(cook_detail_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cook_create(self) -> None:
        cook_create_url = reverse("kitchen:cook-create")
        response = self.client.get(cook_create_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cook_update(self) -> None:
        cook_update_url = reverse(
            "kitchen:cook-update",
            kwargs={"pk": self.main_cook.pk}

        )
        response = self.client.get(cook_update_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cook_delete(self) -> None:
        cook_delete_url = reverse("kitchen:cook-delete", kwargs={"pk": self.main_cook.pk})
        response = self.client.get(cook_delete_url)
        self.assertNotEquals(response.status_code, 200)


class CookListViewTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_retrieve_cook_list(self) -> None:
        response = self.client.get(COOK_LIST_URL)
        cooks = Cook.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["cook_list"]), list(cooks))

    def test_search_cok_by_username(self) -> None:
        url = reverse("kitchen:cook-list")
        cooks = Cook.objects.all()
        response = self.client.get(f"{url}?username=main.cook")
        self.assertIn(self.main_cook, list(response.context["cook_list"]))
        self.assertNotIn(self.cook, list(response.context["cook_list"]))

        response = self.client.get(f"{url}?username=")
        self.assertEqual(list(cooks), list(response.context["cook_list"]))


class CookViewsTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_cook_detail_view(self) -> None:
        url = reverse("kitchen:cook-detail", kwargs={"pk": self.main_cook.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["cook"], self.main_cook)

    def test_cook_create_view(self) -> None:
        cook_data = {
            "username": "cook1",
            "password1": "Admin654",
            "password2": "Admin654",
            "position": self.cook.id,
            "first_name": "Vasyl",
            "last_name": "Vasylyovych",
            "years_of_experience": 0,
        }
        url = reverse("kitchen:cook-create")
        response = self.client.post(url, cook_data)

        self.assertEqual(response.status_code, 302)

        created_cook = Cook.objects.last()

        self.assertEqual(created_cook.username, cook_data["username"])

    def test_cook_update_page(self):
        cook_data = {
            "username": "cook1",
            "first_name": "Vasyl",
            "last_name": "Vasylyovych",
            "position": self.main_cook.id,
            "years_of_experience": 1,
        }

        url = reverse("kitchen:cook-update", kwargs={"pk": self.main_cook.id})
        response = self.client.post(url, cook_data)

        self.main_cook.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.main_cook.username, cook_data["username"])
        self.assertEqual(self.main_cook.first_name, cook_data["first_name"])
        self.assertEqual(self.main_cook.last_name, cook_data["last_name"])

    def test_cook_delete_view(self):
        url = reverse("kitchen:cook-delete", kwargs={"pk": self.main_cook.id})
        response = self.client.post(url)
        cooks = Cook.objects.all()

        self.assertEqual(response.status_code, 302)

        self.assertNotIn(self.main_cook, cooks)

    def test_cook_delete_view_non_exist_cook(self):
        url = reverse("kitchen:cook-delete", kwargs={"pk": 999})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)


