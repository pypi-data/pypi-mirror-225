import re
import string
import unicodedata

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import generic
from weasyprint import HTML

from huscy.consents.forms import SignatureForm
from huscy.consents.views import SignConsentView
from huscy.project_consents.forms import TokenForm
from huscy.project_consents.models import ProjectConsentFile, ProjectConsentToken
from huscy.project_consents.services import create_project_consent_token


def sanitize_string(_string):
    # replace umlauts
    _string = re.sub('[ä]', 'ae', _string)
    _string = re.sub('[Ä]', 'Ae', _string)
    _string = re.sub('[ö]', 'oe', _string)
    _string = re.sub('[Ö]', 'Oe', _string)
    _string = re.sub('[ü]', 'ue', _string)
    _string = re.sub('[Ü]', 'Ue', _string)
    _string = re.sub('[ß]', 'ss', _string)

    # remove accents
    _string = ''.join(c for c in unicodedata.normalize('NFKD', _string)
                      if not unicodedata.combining(c))

    # remove punctuation
    _string = _string.translate(str.maketrans('', '', string.punctuation))

    return _string


class CreateTokenView(LoginRequiredMixin, generic.FormView):
    form_class = TokenForm
    template_name = 'project_consents/project_consent_token.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        token = create_project_consent_token(
            creator=self.request.user,
            project=form.cleaned_data.get('project'),
            subject=form.cleaned_data.get('subject'),
        )
        return HttpResponseRedirect(
            '{}?token={}'.format(reverse('create-project-consent-token'), token.id)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'token' in self.request.GET:
            token = get_object_or_404(ProjectConsentToken, pk=self.request.GET.get('token'))

            protocol = self.request.scheme
            host = self.request.get_host()
            url = reverse('sign-project-consent', kwargs=dict(token=token.id))

            context['sign_project_consent_url'] = f'{protocol}://{host}{url}'
        return context


class SignProjectConsentView(SignConsentView):
    form_class = formset_factory(SignatureForm, extra=2)
    template_name = 'project_consents/sign_project_consent.html'

    def dispatch(self, request, *args, **kwargs):
        self.token = get_object_or_404(ProjectConsentToken, pk=self.kwargs['token'])
        self.project = self.token.project
        self.subject = self.token.subject
        self.consent = self.project.projectconsent  # required by parent class
        return super(SignConsentView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experimenter'] = self.token.created_by
        context['project'] = self.project
        context['subject'] = self.subject
        return context

    def form_valid(self, form):
        html_template = get_template('project_consents/signed_project_consent.html')

        custom_data = dict((key, value)
                           for key, value in self.request.POST.items()
                           if key.startswith('textfragment'))
        rendered_html = html_template.render({
            'consent': self.consent,
            'custom_data': custom_data,
            'experimenter': self.token.created_by,
            'form': form,
            'project': self.project,
            'subject': self.subject,
        })
        content = HTML(string=rendered_html, base_url=self.request.build_absolute_uri()).write_pdf()

        filename = '_'.join([
            *sanitize_string(self.subject.contact.display_name).split(),
            self.subject.contact.date_of_birth.strftime("%Y%m%d")
        ]) + '.pdf'
        filehandle = SimpleUploadedFile(
            name=filename,
            content=content,
            content_type='application/pdf'
        )
        ProjectConsentFile.objects.create(
            consent=self.consent,
            consent_version=self.consent.version,
            filehandle=filehandle,
            subject=self.subject
        )
        self.token.delete()

        return HttpResponse(content, content_type="application/pdf")
