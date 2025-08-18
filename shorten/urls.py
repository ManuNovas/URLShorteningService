from django.urls import path

from shorten import views

app_name = "shorten"
urlpatterns = [
    path("", views.create, name="create"),
    path("<str:short_code>", views.retrieve, name="retrieve"),
]
