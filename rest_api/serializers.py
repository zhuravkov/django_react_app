import email
from rest_framework import serializers
from rest_framework.relations import RelatedField

from .models import UserProfile, Post
from django.contrib.auth.models import User




# UserDetailView
class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='__str__')
    following = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'following', 'status', 'pk')



# userProfileApi выдача пользователей постранично
class UsersSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='__str__')

    followed = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'followed', 'status')

    def get_followed(self, obj):
        # проверяем есть ли объект в подписках зарегистрированного пользователя
        session_user_id = self.context.get('session_user_id')
        current_user = UserProfile.objects.get(user__id=session_user_id)
        following = current_user.following.all()
        if obj in following:
            return True

        return False





class AuthUserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    login = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id','login', 'email')


    def get_email(self, obj):
        return obj.user.email

    def get_login(self, obj):
        return obj.user.username




class PostApiSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('pk', 'user', 'content', 'created_at', 'author')

    def get_author (self, obj):
        return obj.user.user.username
