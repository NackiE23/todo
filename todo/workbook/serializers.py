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


class TaskImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskImage
        fields = ('id', 'task', 'image')
        required = ('task', 'image', )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskImage
        fields = ('image',)


class TaskSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'status_name', 'author', 'author_name',
                  'images', 'created', 'last_modified', 'users', 'users_names')
        read_only_fields = ['author', 'images', 'users']

    def get_images(self, obj):
        return [ImageSerializer(s).data for s in obj.images.all()]

    def create(self, validated_data):
        if validated_data['status'] is int:
            status_obj = TaskStatus.objects.get(pk=validated_data['status'])
        else:
            status_obj = validated_data['status']

        task = Task.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            status=status_obj,
            author=self.context['request'].user
        )
        task.save()

        if validated_data.get('users'):
            for user_data in validated_data['users']:
                if user_data is int:
                    TaskUser.objects.create(task=task, user=User.objecs.get(pk=user_data)).save()
                elif isinstance(user_data, TaskUser):
                    TaskUser.objects.create(task=task, user=user_data.user).save()
                elif isinstance(user_data, User):
                    TaskUser.objects.create(task=task, user=user_data).save()

        return task


class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskUser
        fields = ('task', 'user')


class DetailTaskUserSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    user = UserSerializer()

    class Meta:
        model = TaskUser
        fields = ('task', 'user')
