from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.views import Index
from kitchen.tests.setup import SetUpKitchenDB


class IndexViewTest(SetUpKitchenDB):
    def test_public(self):
        response = self.client.get(
            reverse("kitchen:index")
        )
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        super().setUp()
        self.client.force_login(self.main_cook)

    def test_get_context_data(self):
        response = self.client.get(reverse(
            "kitchen:index")
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context["cooks"], 2)
        self.assertEqual(response.context["dishes"], 2)
        self.assertEqual(response.context["ingredients"], 4)
        self.assertEqual(response.context["dish_types"], 2)