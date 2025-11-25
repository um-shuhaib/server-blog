from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from blogApp.serialiser import UserSerialiser,ProfileSerialiser,PostSerialiser,CommentSerialiser
from rest_framework.response import Response
from blogApp.models import ProfileModel,PostModel,CommentModel
from rest_framework import authentication,permissions
from rest_framework.decorators import action

# jwt authentication
from rest_framework_simplejwt import authentication as simplejwt_auth

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
        profile_to_follow.followers.add(user)   # add is used to add in M2M fields
        return Response({"msg":"followed"})
    
    @action(methods=["GET"],detail=True)
    def list_followers(self,request,*args,**kwargs):
        profile=ProfileModel.objects.get(id=kwargs.get("pk"))
        followers=profile.followers.all()
        serialiser=UserSerialiser(followers,many=True)
        return Response(data=serialiser.data)

class PostView(ModelViewSet):
    queryset=PostModel.objects.all()
    serializer_class=PostSerialiser
    # authentication_classes=[authentication.TokenAuthentication]
    authentication_classes=[simplejwt_auth.JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(methods=["POST"],detail=True)
    def add_likes(self,request,*args,**kwargs):
        post_to_like=PostModel.objects.get(id=kwargs.get("pk"))
        user=request.user
        post_to_like.likes.add(user)
        return Response({"msg":"liked to the post"})
    @action(methods=["POST"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        post=PostModel.objects.get(id=kwargs.get("pk"))
        user=request.user
        serialiser=CommentSerialiser(data=request.data)
        if serialiser.is_valid():
            CommentModel.objects.create(**serialiser.validated_data,user=user,post=post)
            return Response(data=serialiser.data)
        else:
            return Response(data=serialiser.errors)
    @action(methods=["GET"],detail=True)        
    def list_comments(self,request,*args,**kwargs):
        post=PostModel.objects.get(id=kwargs.get("pk"))
        comments=CommentModel.objects.filter(post=post)
        serialiser=CommentSerialiser(comments,many=True)
        return Response(data=serialiser.data)


class CommentView(ModelViewSet):
    queryset=CommentModel.objects.all()
    serializer_class=CommentSerialiser
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
