from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from shorten.models import Short
from shorten.serializers import ShortSerializer


# Create your views here.
@csrf_exempt
def detail(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ShortSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = JsonResponse(serializer.data, status=201)
        else:
            response = JsonResponse(serializer.errors, status=400)
    else:
        response = JsonResponse({"message": "Solicitud invalida."}, status=400)
    return response
