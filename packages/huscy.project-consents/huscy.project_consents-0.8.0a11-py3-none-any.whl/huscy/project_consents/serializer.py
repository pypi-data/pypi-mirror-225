from rest_framework import serializers

from . import models, services
from .models import ProjectConsent, ProjectConsentCategory
from .services import (create_project_consent, create_project_consent_category,
                       update_project_consent, update_project_consent_category)


class ProjectConsentCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    template_text_fragments = serializers.JSONField()

    class Meta:
        model = ProjectConsentCategory
        fields = 'id', 'name', 'template_text_fragments'

    def create(self, validated_data):
        return create_project_consent_category(**validated_data)

    def update(self, project_consent_category, validated_data):
        return update_project_consent_category(project_consent_category, **validated_data)


class ProjectConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectConsent
        fields = 'id', 'project', 'text_fragments'
        read_only_fields = 'project',

    def create(self, validated_data):
        return create_project_consent(**validated_data)

    def update(self, project_consent, validated_data):
        return update_project_consent(project_consent, **validated_data)


class ProjectConsentTokenSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.ProjectConsentToken
        fields = 'id', 'created_at', 'created_by', 'project', 'subject'
        extra_kwargs = {
            'project': {'required': False},
        }

    def create(self, validated_data):
        creator = validated_data.pop('created_by')
        return services.create_project_consent_token(creator=creator, **validated_data)
