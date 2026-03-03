from django.shortcuts import render

# Create your views here.
#test view to check if the api is working or not
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health_check(request):
    return Response({"status": "API is working"})
