import jsonschema

from .models import ProjectConsent, ProjectConsentCategory, ProjectConsentToken
from huscy.consents.services import TEXT_FRAGMENTS_SCHEMA


def create_project_consent_category(name, template_text_fragments):
    jsonschema.validate(template_text_fragments, TEXT_FRAGMENTS_SCHEMA)
    return ProjectConsentCategory.objects.create(
        name=name,
        template_text_fragments=template_text_fragments,
    )


def create_project_consent(project, text_fragments):
    jsonschema.validate(text_fragments, TEXT_FRAGMENTS_SCHEMA)
    return ProjectConsent.objects.create(project=project, text_fragments=text_fragments)


def create_project_consent_token(project, subject, creator):
    token, _created = ProjectConsentToken.objects.get_or_create(
        created_by=creator.get_full_name(),
        project=project,
        subject=subject,
    )
    return token


def update_project_consent_category(project_consent_category, name=None,
                                    template_text_fragments=None):
    update_fields = []

    if name is not None and name != project_consent_category.name:
        project_consent_category.name = name
        update_fields.append('name')

    if (template_text_fragments is not None
            and template_text_fragments != project_consent_category.template_text_fragments):
        jsonschema.validate(template_text_fragments, TEXT_FRAGMENTS_SCHEMA)
        project_consent_category.template_text_fragments = template_text_fragments
        update_fields.append('template_text_fragments')

    project_consent_category.save(update_fields=update_fields)

    return project_consent_category


def update_project_consent(project_consent, text_fragments=None):
    update_fields = []

    if text_fragments is not None and text_fragments != project_consent.text_fragments:
        jsonschema.validate(text_fragments, TEXT_FRAGMENTS_SCHEMA)
        project_consent.text_fragments = text_fragments
        update_fields.append('text_fragments')

    if update_fields:
        project_consent.version += 1
        update_fields.append('version')
        project_consent.save(update_fields=update_fields)

    return project_consent
