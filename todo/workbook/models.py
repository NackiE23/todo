from django.contrib.auth import get_user
from django.db import models

User = get_user()


class TaskStatus(models.Model):
    name = models.CharField(max_length=8, verbose_name="Название статуса")

    def __str__(self):
        return self.name


class Task(models.Model):
    pass
