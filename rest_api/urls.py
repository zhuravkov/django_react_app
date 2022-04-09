from urllib import request
from django.urls import path

from .views import AuthUserView, authenticateApi, UserDetailView, userProfileApi,  PostApiView

urlpatterns = [

    path('api/users/',  userProfileApi ),
    path('api/posts/',  PostApiView.as_view() ),
    path('api/profile/<int:pk>',  UserDetailView.as_view() ),
    path('api/auth/me/',  authenticateApi ),
]
