from django.test import TestCase
from django.urls import reverse


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
