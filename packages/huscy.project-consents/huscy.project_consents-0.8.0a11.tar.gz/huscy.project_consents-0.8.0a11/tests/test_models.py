import pytest
from model_bakery import baker

from huscy.project_consents.models import get_project_consent_file_upload_path

pytestmark = pytest.mark.django_db


def test_get_consent_file_upload_path():
    project_consent = baker.make('project_consents.ProjectConsent')
    project_consent_file = baker.prepare('project_consents.ProjectConsentFile',
                                         consent=project_consent)

    result = get_project_consent_file_upload_path(project_consent_file, 'filename.pdf')

    assert f'projects/{project_consent.project.id}/consents/filename.pdf' == result
