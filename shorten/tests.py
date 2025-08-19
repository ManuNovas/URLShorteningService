from django.test import TestCase
from django.urls import reverse

from shorten.models import Short


# Create your tests here.
class TestShort(TestCase):
    @staticmethod
    def create_short(url, short_code):
        short = Short.objects.create(url=url, shortCode=short_code)
        short.save()
        return short

    def test_create_short(self):
        url = "https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ"
        response = self.client.post(reverse("shorten:create"), {
            "url": url
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["url"], url)

    def test_create_short_invalid_url(self):
        response = self.client.post(reverse("shorten:create"), {
            "url": "youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_retrieve_short(self):
        url = "https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ"
        short_code = "1234QWER"
        self.create_short(url, short_code)
        response = self.client.get(reverse("shorten:retrieve", args=[short_code]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["url"], url)

    def test_retrieve_short_invalid(self):
        short_code = "1234QWER"
        self.create_short("https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ", short_code)
        response = self.client.get(reverse("shorten:retrieve", args=["QWER1234"]))
        self.assertEqual(response.status_code, 404)

    def test_update_short(self):
        short_code = "1234QWER"
        self.create_short("https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ", short_code)
        url = "https://youtu.be/CNM6o9um1dc?si=YT88XZuKyjU2YGqx"
        response = self.client.put(reverse("shorten:retrieve", args=[short_code]), {
            "url": url
        }, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["url"], url)

    def test_update_short_not_found(self):
        short_code = "1234QWER"
        self.create_short("https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ", short_code)
        response = self.client.put(reverse("shorten:retrieve", args=["invalid"]), {
            "url": "https://youtu.be/CNM6o9um1dc?si=YT88XZuKyjU2YGqx"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_short_invalid_data(self):
        short_code = "1234QWER"
        self.create_short("https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ", short_code)
        response = self.client.put(reverse("shorten:retrieve", args=[short_code]), {
            "url": "youtu.be/CNM6o9um1dc?si=YT88XZuKyjU2YGqx"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_delete_short(self):
        short_code = "1234QWER"
        self.create_short("https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ", short_code)
        self.create_short("https://youtu.be/CNM6o9um1dc?si=YT88XZuKyjU2YGqx", "QWER1234")
        response = self.client.delete(reverse("shorten:retrieve", args=[short_code]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Short.objects.filter(shortCode=short_code).exists(), False)
        self.assertEqual(Short.objects.filter(shortCode="QWER1234").exists(), True)

    def test_delete_short_not_found(self):
        self.create_short("https://youtu.be/gV5rIW1Qums?si=eesQll2_GSwE5rZQ", "1234QWER")
        response = self.client.delete(reverse("shorten:retrieve", args=["QWER1234"]))
        self.assertEqual(response.status_code, 404)
