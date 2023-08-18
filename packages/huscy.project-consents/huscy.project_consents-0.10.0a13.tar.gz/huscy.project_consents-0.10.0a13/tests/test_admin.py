import pytest

from django.contrib.admin.sites import AdminSite

from huscy.project_consents.admin import ProjectConsentAdmin
from huscy.project_consents.models import ProjectConsent

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin():
    return ProjectConsentAdmin(ProjectConsent, AdminSite)


def test_project_consent_admin(admin, project_consent):
    assert 'Any title for the project' == admin._project(project_consent)
