from django.urls import path

from shorten import views

app_name = "shorten"
urlpatterns = [
    path("", views.detail, name="create"),
]
