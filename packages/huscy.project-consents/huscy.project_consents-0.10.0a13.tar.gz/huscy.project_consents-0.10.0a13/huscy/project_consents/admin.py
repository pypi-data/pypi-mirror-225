from django.contrib import admin

from . import models


class ProjectConsentAdmin(admin.ModelAdmin):
    list_display = 'id', '_project', 'version'

    def _project(self, project_consent):
        return project_consent.project.title


class ProjectConsentTokenAdmin(admin.ModelAdmin):
    list_display = 'id', 'project', 'subject', 'created_at'


class ProjectIntermediaryAdmin(admin.ModelAdmin):
    list_display = '_project', '_username', 'email', 'phone'

    def _project(self, project_intermediary):
        return project_intermediary.project_membership.project

    def _username(self, project_intermediary):
        return project_intermediary.project_membership.user.username


admin.site.register(models.ProjectConsent, ProjectConsentAdmin)
admin.site.register(models.ProjectConsentCategory)
admin.site.register(models.ProjectConsentFile)
admin.site.register(models.ProjectConsentToken, ProjectConsentTokenAdmin)
admin.site.register(models.ProjectIntermediary, ProjectIntermediaryAdmin)
