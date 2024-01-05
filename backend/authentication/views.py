from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SignUpSerializer, LoginSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


# Create your views here.
class Login(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
