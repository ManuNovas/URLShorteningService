from django.test import TestCase
from django.urls import reverse

from shorten.models import Short


# Create your tests here.
class TestShort(TestCase):
    def test_create_short(self):
        response = self.client.post(reverse("shorten:create"), {
            "url": "https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_short_invalid_url(self):
        response = self.client.post(reverse("shorten:create"), {
            "url": "youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_retrieve_short(self):
        short_code = "1234QWER"
        short = Short.objects.create(url="https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ", shortCode=short_code)
        short.save()
        response = self.client.get(reverse("shorten:retrieve", args=[short_code]))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_short_invalid(self):
        response = self.client.get(reverse("shorten:retrieve", args=["invalid"]))
        self.assertEqual(response.status_code, 404)
