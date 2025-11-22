from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from blogApp.serialiser import UserSerialiser,ProfileSerialiser
from rest_framework.response import Response
from blogApp.models import ProfileModel 
from rest_framework import authentication,permissions
from rest_framework.decorators import action

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
class ProfileView(ModelViewSet):
    queryset=ProfileModel
    serializer_class=ProfileSerialiser
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(methods=["POST"],detail=True)
    def add_followers(self,request,*args,**kwargs):
        profile_to_follow=ProfileModel.objects.get(id=kwargs.get("pk"))
        user=request.user
        profile_to_follow.followers.add(user)
        return Response({"msg":"followed"})




