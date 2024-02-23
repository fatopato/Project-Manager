from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Task, TaskAction, Project, TaskEffort

admin.site.register(Task)
admin.site.register(TaskAction)
admin.site.register(Project)
admin.site.register(TaskEffort)
