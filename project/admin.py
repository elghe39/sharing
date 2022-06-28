from django.contrib import admin
from .models import Shareholder, Project, ProjectDetail


class ShareholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'amount', 'created_at', 'updated_at')


class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'name', 'share')


admin.site.register(Shareholder, ShareholderAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectDetail, ProjectDetailAdmin)
