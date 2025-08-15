from django.utils.crypto import get_random_string
from rest_framework.fields import IntegerField, CharField, DateTimeField
from rest_framework.serializers import Serializer, URLField

from shorten.models import Short


class ShortSerializer(Serializer):
    id = IntegerField(read_only=True)
    url = URLField(max_length=200, required=True)
    shortCode = CharField(max_length=16, required=False, read_only=True)
    accessCount = IntegerField(read_only=True)
    createdAt = DateTimeField(read_only=True)
    updatedAt = DateTimeField(read_only=True)

    def create(self, validated_data):
        short_code = None
        short_code_exists = True
        while short_code_exists:
            short_code = get_random_string(8)
            short_code_exists = Short.objects.filter(shortCode=short_code).exists()
        validated_data["shortCode"] = short_code
        return Short.objects.create(**validated_data)
