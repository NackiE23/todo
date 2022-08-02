from django.http import Http404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from . import models
from .serializers import TaskSerializer, UserSerializer, TaskUserSerializer, TaskImageSerializer


class TaskUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_pk):
        if request.query_params.get('status_name'):
            task_user_objs = models.TaskUser.objects.filter(user__pk=user_pk,
                                                            task__status__name=request.query_params.get('status_name'))
        elif request.query_params.get('status_pk'):
            task_user_objs = models.TaskUser.objects.filter(user__pk=user_pk,
                                                            task__status__pk=request.query_params.get('status_pk'))
        else:
            task_user_objs = models.TaskUser.objects.filter(user__pk=user_pk)

        serializer = TaskUserSerializer(task_user_objs, many=True)
        return Response(serializer.data)


class TaskImageAPIView(APIView):
    def get(self, request, pk):
        serializer = TaskImageSerializer(models.TaskImage.objects.get(pk=pk),
                                         context={'request': request})
        return Response(serializer.data)


class TaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.Task.objects.get(pk=pk)
        except models.Task.DoesNotExist:
            raise Http404

    def get(self, request, task_pk):
        serializer = TaskSerializer(self.get_object(task_pk), many=False)

        return Response(serializer.data)


class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return models.Task.objects.all()


class UserAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(models.User.objects.all(), many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})
