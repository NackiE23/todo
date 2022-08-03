from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from . import models
from .permissions import IsAuthorOrReadOnly
from .serializers import TaskSerializer, UserSerializer, TaskUserSerializer, TaskImageSerializer


@api_view(['GET', 'POST'])
def close_task(request, task_pk):
    task_obj = models.Task.objects.get(pk=task_pk)

    if request.user == task_obj.author:
        task_obj.status = models.TaskStatus.objects.get(name="Закрыто")
        task_obj.save()

        return Response({'detail': f'Задача успешно переведена в статус "Закрыто"!'})
    else:
        return Response({'detail': f'Вы не являетесь автором этой задачи. Операция была отклонена!'})


@api_view(['GET', 'POST'])
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


# class TaskImageAPIView(APIView):
#     def get(self, request, pk):
#         serializer = TaskImageSerializer(models.TaskImage.objects.get(pk=pk),
#                                          context={'request': request})
#         return Response(serializer.data)


class TaskAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Task.objects.get(pk=pk)
        except models.Task.DoesNotExist:
            raise Http404

    def get(self, request, task_pk):
        serializer = TaskSerializer(self.get_object(task_pk), many=False)

        return Response(serializer.data)

    def post(self, request, task_pk):
        task_obj = self.get_object(task_pk)
        serializer = TaskSerializer(task_obj, many=False)

        return Response(serializer.data)

    def put(self, request, task_pk):
        task_obj = self.get_object(task_pk)
        serializer = TaskSerializer(task_obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
