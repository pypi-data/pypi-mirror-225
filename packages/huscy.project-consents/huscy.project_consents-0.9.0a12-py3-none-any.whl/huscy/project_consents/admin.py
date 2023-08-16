from django.contrib import admin

from . import models


class ContactPersonAdmin(admin.ModelAdmin):
    list_display = 'project', 'user', 'email', 'phone'


class ProjectConsentAdmin(admin.ModelAdmin):
    list_display = 'id', '_project', 'version'

    def _project(self, project_consent):
        return project_consent.project.title


class ProjectConsentTokenAdmin(admin.ModelAdmin):
    list_display = 'id', 'project', 'subject', 'created_at'


admin.site.register(models.ContactPerson, ContactPersonAdmin)
admin.site.register(models.ProjectConsent, ProjectConsentAdmin)
admin.site.register(models.ProjectConsentCategory)
admin.site.register(models.ProjectConsentFile)
admin.site.register(models.ProjectConsentToken, ProjectConsentTokenAdmin)
