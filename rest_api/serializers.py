import email
from rest_framework import serializers
from rest_framework.relations import RelatedField

from .models import UserProfile, Post
from django.contrib.auth.models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= User
#         fields = '__all__'
#
#

class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='__str__')

    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'followed', 'status')


class AuthUserSerializer(serializers.ModelSerializer):
    # email = serializers.SerializerMethodField()
    login = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','login', 'email')


    # def get_email(self, obj):
    #     return obj.email

    def get_login(self, obj):
        return obj.username




class PostApiSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('pk', 'user', 'content', 'created_at', 'author')

    def get_author (self, obj):
        return obj.user.user.username
