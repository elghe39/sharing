from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from .serializer import ProjectSerializer, ShareholderSerializer
from .models import Project, ProjectDetail, Shareholder
from django.http import Http404


# Shareholder
class ShareholderListView(generics.ListCreateAPIView):
    queryset = Shareholder.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ShareholderSerializer


class ShareholderDetailView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)

    def get_object(self, pk):
        try:
            return Shareholder.objects.get(pk=pk)
        except Shareholder.DoesNotExist:
            return Http404

    def delete(self, request, pk):
        shareholder = self.get_object(pk)
        if shareholder.balance != 0:
            return Response({"msg": "Please pay off all your debts before leaving the company"}, status=status.HTTP_400_BAD_REQUEST)
        shareholder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Project
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProjectSerializer

    def post(self, request, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Plus money for the owner
            owner = Shareholder.objects.get(name=serializer.data.get('owner'))
            owner.balance += serializer.data.get('amount')
            owner.save()

            # Deduct money for shareholders
            total = 0
            projects_detail = serializer.data.get('projects_detail')
            for detail in projects_detail:
                total += detail.get('share')
            for detail in projects_detail:
                shareholder = Shareholder.objects.get(name=detail.get('name'))
                shareholder.balance -= (serializer.data.get('amount') / total * detail.get('share'))
                shareholder.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        project = self.get_object(pk)

        # Deduct money for the owner
        owner = Shareholder.objects.get(name=project.owner)
        owner.balance -= project.amount
        owner.save()

        # Plus money for shareholders
        total = 0
        projects_detail = ProjectDetail.objects.filter(project_id=project)
        for detail in projects_detail:
            total += detail.share
        for detail in projects_detail:
            shareholder = Shareholder.objects.get(name=detail.name)
            shareholder.balance += (project.amount / total * detail.share)
            shareholder.save()

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        project = self.get_object(pk)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            # Deduct money for the owner
            owner = Shareholder.objects.get(name=project.owner)
            owner.balance -= project.amount
            owner.save()

            # Plus money for shareholders
            total = 0
            projects_detail = ProjectDetail.objects.filter(project_id=project)
            for detail in projects_detail:
                total += detail.share
            for detail in projects_detail:
                shareholder = Shareholder.objects.get(name=detail.name)
                shareholder.balance += (project.amount / total * detail.share)
                shareholder.save()

            serializer.save()

            # Plus money for the owner
            owner = Shareholder.objects.get(name=serializer.data.get('owner'))
            owner.balance += serializer.data.get('amount')
            owner.save()

            # Deduct money for shareholders
            total = 0
            projects_detail = serializer.data.get('projects_detail')
            for detail in projects_detail:
                total += detail.get('share')
            for detail in projects_detail:
                shareholder = Shareholder.objects.get(name=detail.get('name'))
                shareholder.balance -= (serializer.data.get('amount') / total * detail.get('share'))
                shareholder.save()

            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)