from django.db import models


class Shareholder(models.Model):
    name = models.CharField(max_length=20, unique=True)
    balance = models.FloatField(default=0)


class Project(models.Model):
    name = models.TextField(max_length=100)
    amount = models.IntegerField()
    owner = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProjectDetail(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projects_detail', to_field='id')
    name = models.CharField(max_length=20)
    share = models.FloatField()

    class Meta:
        verbose_name = "project_detail"
