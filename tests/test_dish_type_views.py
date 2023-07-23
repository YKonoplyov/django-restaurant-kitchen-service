from django.urls import reverse

from kitchen.models import DishType
from tests.setup import SetUpKitchenDB
DISH_TYPE_LIST_URL = reverse("kitchen:dish-type-list")


class PublicDishTypeViewsTest(SetUpKitchenDB):

    def test_login_required_dish_type_list(self) -> None:
        response = self.client.get(DISH_TYPE_LIST_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_type_create(self) -> None:
        dish_type_create_url = reverse("kitchen:dish-type-create")
        response = self.client.get(dish_type_create_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_type_update(self) -> None:
        dish_type_update_url = reverse(
            "kitchen:dish-type-update",
            kwargs={"pk": self.dish_type_soup.pk}

        )
        response = self.client.get(dish_type_update_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_type_delete(self) -> None:
        dish_type_delete_url = reverse(
            "kitchen:dish-type-delete",
            kwargs={"pk": self.dish_type_soup.pk}
        )
        response = self.client.get(dish_type_delete_url)
        self.assertNotEquals(response.status_code, 200)


class DishTypeListViewTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_retrieve_dish_type_list(self) -> None:
        response = self.client.get(DISH_TYPE_LIST_URL)
        dish_types = DishType.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dishtype_list"]),
            list(dish_types)
        )

    def test_search_dish_type_by_name(self) -> None:
        url = reverse("kitchen:dish-type-list")
        dish_types = DishType.objects.all()
        response = self.client.get(f"{url}?name=soup")
        self.assertIn(
            self.dish_type_soup,
            list(response.context["dishtype_list"])
        )
        self.assertNotIn(
            self.dish_type_desert,
            list(response.context["dishtype_list"])
        )

        response = self.client.get(f"{url}?name=")
        self.assertEqual(
            list(dish_types),
            list(response.context["dishtype_list"])
        )


class DishTypeViewsTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_dish_type_create_view(self) -> None:
        dish_type_data = {
            "name": "steak",
        }
        url = reverse("kitchen:dish-type-create")
        response = self.client.post(url, dish_type_data)

        self.assertEqual(response.status_code, 302)

        created_dish_type = DishType.objects.last()

        self.assertEqual(created_dish_type.name, dish_type_data["name"])

    def test_dish_type_update_page(self):
        dish_type_data = {
            "name": "steak",
        }

        url = reverse(
            "kitchen:dish-type-update",
            kwargs={"pk": self.dish_type_soup.id}
        )
        response = self.client.post(url, dish_type_data)

        self.dish_type_soup.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.dish_type_soup.name, dish_type_data["name"])

    def test_dish_type_delete_view(self):

        url = reverse(
            "kitchen:dish-type-delete",
            kwargs={"pk": self.dish_type_soup.id}
        )
        response = self.client.post(url)
        dish_types = DishType.objects.all()

        self.assertEqual(response.status_code, 302)

        self.assertNotIn(self.dish_type_soup, dish_types)

    def test_dish_type_delete_view_non_exist_dish_type(self):
        url = reverse("kitchen:dish-type-delete", kwargs={"pk": 999})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
