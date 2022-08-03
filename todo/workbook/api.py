from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from . import models
from .permissions import IsAuthorOrReadOnly
from .serializers import TaskSerializer, UserSerializer, TaskUserSerializer, TaskImageSerializer, \
    DetailTaskUserSerializer


@swagger_auto_schema(method='get', operation_description="Переводит статус задачи в 'Закрыто'",
                     responses={200: "{'detail': 'response'}"})
@api_view(['GET'])
def close_task(request, task_pk):
    task_obj = models.Task.objects.get(pk=task_pk)

    if request.user == task_obj.author:
        task_obj.status = models.TaskStatus.objects.get(name="Закрыто")
        task_obj.save()
        return Response({'detail': f'Задача успешно переведена в статус "Закрыто"!'})
    else:
        return Response({'detail': f'Вы не являетесь автором этой задачи. Операция была отклонена!'})


@swagger_auto_schema(method='get', operation_description="Переводит статус задачи 'Новая' в 'В работе'",
                     responses={200: "{'detail': 'response'}"})
@api_view(['GET'])
def start_task(request, task_pk):
    task_obj = models.Task.objects.get(pk=task_pk)

    if request.user.pk in [task_user.user.pk for task_user in task_obj.users.all()]:
        if task_obj.status.name == "Новая":
            task_obj.status = models.TaskStatus.objects.get(name="В работе")
            task_obj.save()
            return Response({'detail': f'Задача успешно переведена в статус "В работе"!'})
        else:
            return Response({'detail': f'Задача не находится в статусе "Новая". Операция была отклонена!'})
    else:
        return Response({'detail': f'Вы не входите в список людей, которые работают над этой задачей. '
                                   f'Операция была отклонена!'})


class TaskUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Get all user tasks. Add a ?status_pk or ?status_name for filtering",
                         responses={200: TaskUserSerializer()})
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


class TaskUserCreateAPIView(CreateAPIView):
    serializer_class = TaskUserSerializer


class DetailTaskUserCreateAPIView(CreateAPIView):
    serializer_class = DetailTaskUserSerializer


class TaskImageListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskImageSerializer

    def get_queryset(self):
        return models.TaskImage.objects.all()


class TaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Task.objects.get(pk=pk)
        except models.Task.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: TaskSerializer()})
    def get(self, request, task_pk):
        task_obj = self.get_object(task_pk)
        serializer = TaskSerializer(task_obj)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=TaskSerializer(), responses={200: TaskSerializer()})
    def put(self, request, task_pk):
        task_obj = self.get_object(task_pk)
        serializer = TaskSerializer(task_obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TaskSerializer(), responses={200: TaskSerializer()})
    def patch(self, request, task_pk):
        task_obj = self.get_object(task_pk)
        serializer = TaskSerializer(task_obj, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_pk):
        task_obj = self.get_object(task_pk)
        task_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.request.query_params.get('status_name'):
            task_user_objs = models.Task.objects.filter(status__name=self.request.query_params.get('status_name'))
        elif self.request.query_params.get('status_pk'):
            task_user_objs = models.Task.objects.filter(status__pk=self.request.query_params.get('status_pk'))
        else:
            task_user_objs = models.Task.objects.all()

        return task_user_objs


class UserAPIView(APIView):
    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request):
        serializer = UserSerializer(models.User.objects.all(), many=True)

        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer(), responses={201: UserSerializer()})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})
