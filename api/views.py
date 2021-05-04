from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets
from .serializers import UserSerializer, CategorySerializer, TaskSerializer, ProfileSerializer
from rest_framework.response import Response
from .models import Task, Category, Profile
from django.contrib.auth.models import User
from . import custompermissions

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # 新規登録時なので、誰でもアクセスできるようにしておく
    permission_classes = (permissions.AllowAny,)

# 取得したオブジェクトをリストにして返す
class ListUserView(generics.ListAPIView):
    # オブジェクトを全て取得する
    queryset = User.objects.all()
    serializer_class = UserSerializer

# オブジェクトを検索して返す
class LoginUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    # 現在ログインしているユーザーのオブジェクトを返す
    def get_object(self):
        return self.request.user

# ModelViewSetにはデフォルトでCRUD処理が実装されている
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # user_profileの属性にログインユーザーを割り当てる
    def perform_create(self, serializer):
        serializer.save(user_profile=self.user)

    # deleteメソッドを無効化
    def destory(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'DELETE method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'PUT method is not allowed'}

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # ログインユーザーとユーザーIDが一致しない場合は登録、更新出来ないようにする
    permission_classes = (permissions.IsAuthenticated, custompermissions.OwnerPermission)

    # owner属性にログインユーザーを割り当てる
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'PATCH method is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)