from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


class TestViews(TestCase):
    def setUp(self):
        self.auth_user = get_user_model().objects.create_superuser(
            username="admin",
            first_name="Admin",
            last_name="Admin",
            license_number="ABC98765",
        )
        self.client.force_login(self.auth_user)

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(
            name="BWM",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Skoda",
            country="Czech Republic",
        )
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        manufacturer1 = Manufacturer.objects.create(
            name="BWM",
            country="Germany",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Skoda",
            country="Czech Republic",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "m"}
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), [manufacturer1]
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "a"}
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), [manufacturer2]
        )
