
from django.contrib.auth.models import User

from django.shortcuts import render

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from rest_api.models import UserProfile, Post
from rest_api.serializers import AuthUserSerializer, UserProfileSerializer,  PostApiSerializer
from django.core.paginator import Paginator



# class TestApiView(generics.ListAPIView):
#     serializer_class = TestApiSerializer
#     queryset = TestApi.objects.all()
#
class PostApiView(generics.ListCreateAPIView):
    serializer_class = PostApiSerializer
    queryset = Post.objects.all()




@api_view(['GET'])
def userProfileApi(request):
    if request.method == 'GET':
        authors = UserProfile.objects.all()
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1

        if 'on_page' in request.GET:
            on_page = request.GET['on_page']
        else:
            on_page = 2
        paginator = Paginator(authors, on_page)
        page = paginator.get_page(page_num)
        serializer = UserProfileSerializer(page,  many=True)
        return Response({'users':serializer.data, 'count': paginator.count})

class UserDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer



class AuthUserView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = AuthUserSerializer

    def get(self, request, *args, **kwargs):
        print(request.__dict__)
        # for a in request.__dict__:
        #     print(f'{a} --- {a.value}')
        return super().get(request, *args, **kwargs)










#
# @api_view(['GET', 'POST'])
# def postApi(request):
#
#
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostApiSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     if request.method == 'POST':
#         print(request.data)
#         serializer = PostApiSerializer(data=request.data)
#         if serializer.is_valid():
#             user = UserProfile.objects.get(username = request.data['author']) //берёт пользователя из запроса выбирает из модели
#             serializer.save(author= user)
#             return Response(serializer.data, status=HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#     else:
#         posts = Post.objects.all()
#         serializer = PostApiSerializer(posts, many=True)
#         return Response(serializer.data)



