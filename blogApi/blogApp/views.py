from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from blogApp.serialiser import UserSerialiser
from rest_framework.response import Response

# Create your views here.
class UserView(ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerialiser

    def create(self, request, *args, **kwargs):
        serialiser=UserSerialiser(data=request.data)
        if serialiser.is_valid():
            User.objects.create_user(**serialiser.validated_data)
            return Response(data=serialiser.data)
        else:
            return Response(data=serialiser.errors)
