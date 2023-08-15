import pytest
from pytest_bdd import scenarios, when

from rest_framework.reverse import reverse


scenarios('viewsets')

pytestmark = pytest.mark.django_db


@when('I try to create a project consent', target_fixture='request_result')
def create_project_consent(client, project, paragraph):
    return client.post(
        reverse('projectconsent-list', kwargs=dict(project_pk=project.pk)),
        data=dict(text_fragments=[paragraph]),
        format='json'
    )


@when('I try to create a project consent category', target_fixture='request_result')
def create_project_consent_category(client, text_fragments):
    return client.post(
        reverse('projectconsentcategory-list'),
        data=dict(name='foobar', template_text_fragments=text_fragments),
        format='json'
    )


@when('I try to delete a project consent', target_fixture='request_result')
def delete_project_consent(client, project, project_consent):
    return client.delete(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk))
    )


@when('I try to delete a project consent category', target_fixture='request_result')
def delete_project_consent_category(client, project_consent_category):
    return client.delete(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk))
    )


@when('I try to list project consents', target_fixture='request_result')
def list_project_consents(client, project):
    return client.get(reverse('projectconsent-list', kwargs=dict(project_pk=project.pk)))


@when('I try to list project consent categories', target_fixture='request_result')
def list_project_consent_categories(client):
    return client.get(reverse('projectconsentcategory-list'))


@when('I try to patch a project consent category', target_fixture='request_result')
def partial_update_project_consent_category(client, project_consent_category):
    return client.patch(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk))
    )


@when('I try to partial update a project consent', target_fixture='request_result')
def partial_update_project_consent(client, project, project_consent, checkbox):
    return client.patch(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk)),
        data=dict(text_fragments=[checkbox]),
        format='json'
    )


@when('I try to retrieve a project consent', target_fixture='request_result')
def retrieve_project_consent(client, project, project_consent):
    return client.get(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk))
    )


@when('I try to retrieve a project consent category', target_fixture='request_result')
def retrieve_project_consent_category(client, project_consent_category):
    return client.get(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk))
    )


@when('I try to update a project consent', target_fixture='request_result')
def update_project_consent(client, project, project_consent, paragraph):
    return client.put(
        reverse('projectconsent-detail', kwargs=dict(project_pk=project.pk, pk=project_consent.pk)),
        data=dict(text_fragments=[paragraph]),
        format='json'
    )


@when('I try to update a project consent category', target_fixture='request_result')
def update_project_consent_category(client, project_consent_category):
    return client.put(
        reverse('projectconsentcategory-detail', kwargs=dict(pk=project_consent_category.pk)),
        data=dict(
            name='new name',
            template_text_fragments=project_consent_category.template_text_fragments,
        ),
        format='json'
    )
