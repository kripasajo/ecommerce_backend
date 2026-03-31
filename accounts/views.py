from django.shortcuts import render
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def health_check(request):
    return Response({"status": "Authenticated user"})


@api_view(['POST'])
@permission_classes([AllowAny]) #update register view
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny]) # Allow anyone to access the login endpoint
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        return Response(
            {"message": "Login successful"},
            status=status.HTTP_200_OK
        )

    return Response(
        {"error": "Invalid credentials"},
        status=status.HTTP_401_UNAUTHORIZED
    )