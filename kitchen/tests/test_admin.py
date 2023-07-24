from django.urls import reverse
from kitchen.tests.setup import AdminSiteSetUpMixin


class AdminSiteCookTest(AdminSiteSetUpMixin):


    def test_cook_years_of_experience_listed(self):
        url = "http://127.0.0.1:8000/admin/kitchen/cook/"
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_detailed_years_of_experience_listed(self):
        cook_id = self.cook.id
        url = f"http://127.0.0.1:8000/admin/kitchen/cook/{cook_id}/change/"
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_position_listed(self):
        cook_id = self.cook.id
        url = f"http://127.0.0.1:8000/admin/kitchen/cook/{cook_id}/change/"
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_cook_detailed_position_listed(self):
        cook_id = self.cook.id
        url = f"http://127.0.0.1:8000/admin/kitchen/cook/{cook_id}/change/"
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)
