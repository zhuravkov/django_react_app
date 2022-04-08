from django.contrib import admin

# Register your models here.
from rest_api.models import UserProfile, Message, Post


admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Post)