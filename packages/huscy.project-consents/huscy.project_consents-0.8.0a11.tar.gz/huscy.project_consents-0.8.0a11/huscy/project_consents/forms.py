from django import forms
from django.core.exceptions import ValidationError

from huscy.projects.models import Project
from huscy.projects.services import get_participating_projects
from huscy.subjects.models import Subject


class ProjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, project):
        return project.title


class TokenForm(forms.Form):
    project = ProjectChoiceField(queryset=Project.objects.none())
    subject = forms.UUIDField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        queryset = get_participating_projects(user)
        self.fields['project'].queryset = queryset.filter(projectconsent__isnull=False)

    def clean_subject(self):
        subject_id = self.cleaned_data['subject']
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            raise ValidationError('subject does not exist')
        return subject
