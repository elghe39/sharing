from rest_framework import serializers
from .models import Shareholder, Project, ProjectDetail


class ShareholderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = Shareholder
        fields = ('name', 'balance')


class ProjectDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20, required=True)
    share = serializers.FloatField(required=True)

    class Meta:
        model = ProjectDetail
        fields = ('name', 'share')


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    amount = serializers.IntegerField(required=True)
    owner = serializers.CharField(max_length=20, required=True)
    projects_detail = ProjectDetailSerializer(many=True)

    class Meta:
        model = Project
        fields = ('name', 'amount', 'owner', 'created_at', 'updated_at', 'projects_detail')

    def create(self, validated_data):
        projects_detail = validated_data.pop('projects_detail')
        project = Project.objects.create(**validated_data)
        for detail in projects_detail:
            ProjectDetail.objects.create(project_id=project, **detail)

        return project

    def update(self, instance, validated_data):
        old_projects_detail = ProjectDetail.objects.filter(project_id=instance)
        for detail in old_projects_detail:
            detail.delete()
        instance.name = validated_data.get('name', instance.name)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.amount = validated_data.get('amount', instance.amount)
        projects_detail = validated_data.pop('projects_detail')
        for detail in projects_detail:
            ProjectDetail.objects.create(project_id=instance, **detail)

        instance.save()
        return instance
