from django.urls import path

from .views import AuthUserView, UserDetailView, userProfileApi,  PostApiView

urlpatterns = [

    path('api/users/',  userProfileApi ),
    path('api/posts/',  PostApiView.as_view() ),
    path('api/profile/<int:pk>',  UserDetailView.as_view() ),
    path('api/auth/me/<int:pk>',  AuthUserView.as_view() ),
]
