
from django.contrib.auth.models import User
from django.http import JsonResponse

from django.shortcuts import render,get_object_or_404

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from rest_api.models import  UserProfile, Post
from rest_api.serializers import AuthUserSerializer, UserProfileSerializer,  PostApiSerializer, UsersSerializer
from django.core.paginator import Paginator






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
        serializer = UsersSerializer(page,  many=True, context={'session_user_id': request.session['_auth_user_id']})
        return Response({'users':serializer.data, 'count': paginator.count})



class UserDetailView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer



class AuthUserView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = AuthUserSerializer

    def get(self, request, *args, **kwargs):
        print(request.COOKIES)
        print(request.__dict__['_user'])
        print(request.META.get('HTTP_X_USERNAME'))
        # for a in request.__dict__:
        #     print(f'{a} --- {a.value}')
        return super().get(request, *args, **kwargs)




from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


@api_view(['GET'])
def authenticateApi(request):

    # колхозный способ определения пользователя из куков и сессии
    username = request.__dict__['_user']
    session_user_id = request.session['_auth_user_id']
    print(username)
    print(request.session['_auth_user_id'])



    if not username:
        return JsonResponse({'data': 'Not Logined'})
    
    if username == 'AnonymousUser':
        return JsonResponse({'data': 'Not Logined'})
 

    try:
        user = UserProfile.objects.get(user__id=session_user_id)
        serializer = AuthUserSerializer(user)

    except User.DoesNotExist:
        return JsonResponse({'messages': 'You are not athorized'})
            # raise exceptions.AuthenticationFailed('No such user')    
    
    return JsonResponse({'data':serializer.data, 'resultCode': 0})




# добавление пользователей в подписанные и удаление оттуда
@api_view(['GET', 'POST', 'DELETE'])
def followToggle(request, pk):

    session_user_id = request.session['_auth_user_id']
    authorObj = UserProfile.objects.get(user__id=session_user_id)
    other_user = get_object_or_404(UserProfile, pk=pk)
    # other_user = UserProfile.objects.get(pk=pk)
    following = authorObj.following.all()
    if pk != authorObj.pk:
        if request.method == 'GET':
            if other_user in following:
                return JsonResponse({'status':'followed','resultCode': 0})
            else: 
                return JsonResponse({'status':'unfollowed','resultCode': 0})

            

        elif request.method == 'POST':
            if other_user not in following:
                authorObj.following.add(other_user)
                return JsonResponse({'action':'followed','resultCode': 0})
            else: 
                return JsonResponse({'action':'already followed','resultCode': 1})


        elif request.method == 'DELETE':
            if other_user in following:
                authorObj.following.remove(other_user)
                return JsonResponse({'action':'unfollowed','resultCode': 0})
            else: 
                return JsonResponse({'action':'not in followed','resultCode': 1})


    return JsonResponse({'action':'can not follow youself','resultCode': 1})

    























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



