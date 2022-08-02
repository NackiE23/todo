from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.db import models


class TaskStatus(models.Model):
    name = models.CharField(max_length=8, verbose_name="Название")

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=8, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание задачи")

    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, verbose_name="Статус")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="Последнее редактирование")

    def __str__(self):
        return self.name


class TaskUser(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="users", verbose_name="Задача")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")


class TaskImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="images", verbose_name="Задача")
    image = models.ImageField(upload_to="images/%Y/%m/%d/", verbose_name="Изображение")
