from rest_framework import serializers
from django.contrib.auth.models import User
from blogApp.models import ProfileModel,PostModel

class UserSerialiser(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password"]

class ProfileSerialiser(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    user=UserSerialiser(read_only=True)
    followers=serializers.CharField(read_only=True)
    class Meta:
        model=ProfileModel
        fields="__all__"

class PostSerialiser(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    user=UserSerialiser(read_only=True)
    likes=serializers.CharField(read_only=True)
    class Meta:
        model=PostModel
        fields="__all__"