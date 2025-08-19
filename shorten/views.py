from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from shorten.models import Short
from shorten.serializers import ShortSerializer


# Create your views here.
@csrf_exempt
def create(request):
    try:
        data = JSONParser().parse(request)
        serializer = ShortSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = JsonResponse(serializer.data, status=201)
        else:
            response = JsonResponse(serializer.errors, status=400)
    except Exception as e:
        print(e)
        response = JsonResponse({"message": "Ocurrio un problema al crear la URL."}, status=500)
    return response

def retrieve(request, short_code):
    try:
        short = Short.objects.filter(shortCode=short_code).first()
        if short is not None:
            if request.method == "GET":
                short.accessCount += 1
                short.save()
                resource = short.list_resource()
                response = JsonResponse(resource, status=200)
            elif request.method == "PUT":
                data = JSONParser().parse(request)
                serializer = ShortSerializer(short, data=data)
                if serializer.is_valid():
                    serializer.save()
                    response = JsonResponse(serializer.data)
                else:
                    response = JsonResponse(serializer.errors, status=400)
            elif request.method == "DELETE":
                short.delete()
                response = JsonResponse(short.list_resource(), status=204)
            else:
                response = JsonResponse({"message": "Metodo no valido"}, status=405)
        else:
            response = JsonResponse({"message": "URL no encontrada."}, status=404)
    except Exception as e:
        print(e)
        response = JsonResponse({"message": "Ocurrio un problema al obtener la URL."}, status=500)
    return response
