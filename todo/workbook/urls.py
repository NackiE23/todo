from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import api
from .views import *

urlpatterns = [
    path('', main, name="main"),
    path('api/drf-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token-auth', obtain_auth_token),
    path('api/task_images', api.TaskImageListCreateAPIView.as_view(), name="api_task_images"),
    path('api/tasks', api.TaskListCreateAPIView.as_view(), name="api_tasks"),
    path('api/task/<int:task_pk>', api.TaskAPIView.as_view(), name="api_task"),
    path('api/close_task/<int:task_pk>', api.close_task, name="api_close_task"),
    path('api/start_task/<int:task_pk>', api.start_task, name="api_start_task"),
    path('api/task_user', api.TaskUserCreateAPIView.as_view(), name="api_task_user"),
    path('api/task_user_detail', api.DetailTaskUserCreateAPIView.as_view(), name="api_task_user_detail"),
    path('api/user_tasks/<int:user_pk>', api.TaskUserAPIView.as_view(), name="api_user_tasks"),
    path('api/users', api.UserAPIView.as_view(), name='api_users')
]
