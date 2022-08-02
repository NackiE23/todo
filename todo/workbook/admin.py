from django.contrib import admin
from .models import *


class TaskImageInline(admin.TabularInline):
    model = TaskImage
    extra = 1


class TaskUserInline(admin.TabularInline):
    model = TaskUser
    extra = 1


class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskImageInline, TaskUserInline]


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskStatus)
