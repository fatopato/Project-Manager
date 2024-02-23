from django.db import models
from django.contrib.auth.models import User


class AbstractBaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class Task(AbstractBaseModel):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('BLOCKED', 'Blocked'),
        ('DELETED', 'Deleted'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    subtasks = models.ManyToManyField('Task', related_name='parent_task', blank=True)

    def __str__(self):
        return self.title


class TaskAction(AbstractBaseModel):
    ACTION_CHOICES = [
        ('CREATED', 'Created'),
        ('DELETED', 'Deleted'),
        ('BLOCKED', 'Blocked'),
        ('UNASSIGNED', 'Unassigned'),
        ('ASSIGNED', 'Assigned'),
        ('COMPLETED', 'Completed'),
        ('EFFORT_CHANGED', 'Effort Changed'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_created')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_to')
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=ACTION_CHOICES)

    def __str__(self):
        return f"{self.get_type_display()} - {self.task}"


class Project(AbstractBaseModel):
    project_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    tasks = models.ManyToManyField(Task, related_name='project_tasks', blank=True)
    subProjects = models.ManyToManyField('self', related_name='parent_project', blank=True)

    def __str__(self):
        return f"Project - {self.id}"


class TaskEffort(AbstractBaseModel):
    EFFORT_TYPE_CHOICES = [
        ('ANALYSIS', 'Analysis'),
        ('DEVELOPMENT', 'Development'),
        ('TEST', 'Test'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    effort = models.IntegerField()
    effort_type = models.CharField(max_length=20, choices=EFFORT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.effort_type} Effort for Task - {self.task}"
