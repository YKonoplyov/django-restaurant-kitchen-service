from django.urls import reverse

from kitchen.models import Dish
from tests.setup import SetUpKitchenDB

DISH_LIST_URL = reverse("kitchen:dish-list")


class PublicDishViewsTest(SetUpKitchenDB):

    def test_login_required_dish_list(self) -> None:
        response = self.client.get(DISH_LIST_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_detail(self) -> None:
        dish_detail_url = reverse(
            "kitchen:dish-details",
            kwargs={"pk": self.borch.pk}
        )
        response = self.client.get(dish_detail_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_create(self) -> None:
        dish_create_url = reverse("kitchen:dish-create")
        response = self.client.get(dish_create_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_update(self) -> None:
        dish_update_url = reverse(
            "kitchen:dish-update",
            kwargs={"pk": self.borch.pk}

        )
        response = self.client.get(dish_update_url)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_delete(self) -> None:
        dish_delete_url = reverse(
            "kitchen:dish-delete",
            kwargs={"pk": self.borch.pk}
        )
        response = self.client.get(dish_delete_url)
        self.assertNotEquals(response.status_code, 200)


class DishListViewTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_retrieve_dish_list(self) -> None:
        response = self.client.get(DISH_LIST_URL)
        dishes = Dish.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["dish_list"]), list(dishes))

    def test_search_dish_by_name(self) -> None:
        url = reverse("kitchen:dish-list")
        dishes = Dish.objects.all()
        response = self.client.get(f"{url}?name=borch")
        self.assertIn(self.borch, list(response.context["dish_list"]))
        self.assertNotIn(self.apple_pie, list(response.context["dish_list"]))

        response = self.client.get(f"{url}?name=")
        self.assertEqual(list(dishes), list(response.context["dish_list"]))


class DishViewsTest(SetUpKitchenDB):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_dish_detail_view(self) -> None:
        url = reverse("kitchen:dish-details", kwargs={"pk": self.borch.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["dish"], self.borch)

    def test_dish_create_view(self) -> None:
        dish_data = {
            "name": "pork steak",
            "description": "fried meat",
            "price": 5.2,
            "dish_type": self.dish_type_soup.id,
            "ingredients": [
                self.ingredient_apple.id,
                self.ingredient_water.id
            ],
            "cooks": [self.main_cook.id, self.cook.id],
        }
        url = reverse("kitchen:dish-create")
        response = self.client.post(url, dish_data)

        self.assertEqual(response.status_code, 302)

        created_dish = Dish.objects.last()

        self.assertEqual(created_dish.name, dish_data["name"])

    def test_dish_update_page(self):
        dish_data = {
            "name": "pork steak",
            "description": "fried meat",
            "price": 5.20,
            "dish_type": self.dish_type_soup.id,
            "ingredients": [
                self.ingredient_apple.id,
                self.ingredient_water.id
            ],
            "cooks": [self.main_cook.id, self.cook.id],
        }

        url = reverse("kitchen:dish-update", kwargs={"pk": self.borch.id})
        response = self.client.post(url, dish_data)

        self.borch.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.borch.name, dish_data["name"])
        self.assertEqual(self.borch.description, dish_data["description"])
        self.assertEqual(float(self.borch.price), dish_data["price"])

    def test_dish_delete_view(self):
        url = reverse("kitchen:dish-delete", kwargs={"pk": self.borch.id})
        response = self.client.post(url)
        dishes = Dish.objects.all()

        self.assertEqual(response.status_code, 302)

        self.assertNotIn(self.borch, dishes)

    def test_dish_delete_view_non_exist_dish(self):
        url = reverse("kitchen:dish-delete", kwargs={"pk": 999})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
