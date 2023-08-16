import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from huscy.projects.models import Project
from huscy.subjects.models import Subject


class ProjectConsentCategory(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    template_text_fragments = models.JSONField(_('Template text fragments'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Project consent category')
        verbose_name_plural = _('Project consent categories')


class ProjectConsentToken(models.Model):
    id = models.UUIDField(_('ID'), primary_key=True, editable=False, default=uuid.uuid4)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    created_by = models.CharField(_('Created by'), max_length=255, editable=False)


class ProjectConsent(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name=_('Project'))
    text_fragments = models.JSONField(_('Text fragments'))
    version = models.PositiveIntegerField(_('Version'), default=1)

    def __str__(self):
        return f'{self.project.title} ({self.version})'

    class Meta:
        verbose_name = _('Project consent')
        verbose_name_plural = _('Project consents')


class ContactPerson(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)


def get_project_consent_file_upload_path(instance, filename):
    project = instance.project_consent.project
    return f'projects/{project.id}/consents/{filename}'


class ProjectConsentFile(models.Model):
    project_consent = models.ForeignKey(ProjectConsent, on_delete=models.CASCADE, editable=False,
                                        verbose_name=_('Project consent'))
    project_consent_version = models.PositiveIntegerField(_('Project consent version'),
                                                          editable=False)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, editable=False,
                                verbose_name=_('Subject'))

    filehandle = models.FileField(_('Filehandle'), upload_to=get_project_consent_file_upload_path,
                                  editable=False)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)

    class Meta:
        unique_together = 'project_consent', 'project_consent_version', 'subject'
        verbose_name = _('Project consent file')
        verbose_name_plural = _('Project consent files')
