from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        user.save()

        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'status_name', 'author', 'author_name',
                  'images', 'created', 'last_modified', 'users', 'users_names')


class TaskUserSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=False)

    class Meta:
        model = TaskUser
        fields = ('task', )
