from rest_framework import serializers
from .models import Task, Category,Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meat:
        model = User
        filed = ['id','userName','passwrod']
        extra_kwargs = {'password':{'write_only': True, 'required': True}}

    # passwordをハッシュ化
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','user_profile','img']
        extra_kwargs = {'user_profile': {'read_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = ['id','item']

class TaskSerializer(serializers.ModelSerializer):
    # 他のオブジェクトから取得
    category_item = serializers.ReadOnlyField(source='category.item', read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username', read_only=True)
    responsible_username = serializers.ReadOnlyField(source='responsible.username')
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DataTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'task', 'description', 'criteria', 'status', 'status_name', 'category', 'category_item',
                  'estimate', 'responsible', 'responsible_username', 'owner', 'owner_username', 'created_at',
                  'updated_at']

        extra_kwargs = {'owner', {'read_only': True}}


