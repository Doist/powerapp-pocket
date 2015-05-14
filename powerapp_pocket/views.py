# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from powerapp.core import django_forms, generic_views
from powerapp.core.models.oauth import AccessToken, EMPTY_SCOPE
from powerapp.core.web_utils import extend_qs

# getpocket API settings
POCKET_REQUEST_ENDPOINT = 'https://getpocket.com/v3/oauth/request'
POCKET_AUTHORIZE_ENDPOINT = 'https://getpocket.com/auth/authorize'
POCKET_ACCESS_TOKEN_ENDPOINT = 'https://getpocket.com/v3/oauth/authorize'
POCKET_ADD_URL_ENDPOINT = 'https://getpocket.com/v3/add'

class IntegrationForm(django_forms.IntegrationForm):
    service_label = 'powerapp_pocket'


class EditIntegrationView(generic_views.EditIntegrationView):
    access_token_client = 'pocket'
    service_label = 'powerapp_pocket'
    form = IntegrationForm

    def access_token_redirect(self, request):
        request.session['pocket_auth_redirect'] = request.path
        return redirect('powerapp_pocket:authorize_pocket')
        

@login_required
def authorize_pocket(request):
    resp = requests.post(POCKET_REQUEST_ENDPOINT, data={
        'consumer_key': settings.POCKET_CONSUMER_KEY,
        'redirect_uri': request.build_absolute_uri(reverse('web_oauth2cb')),
    }, headers={'X-Accept': 'application/json'})
    resp.raise_for_status()
    request.session['pocket_request_token'] = resp.json()['code']

    redirect_uri = request.build_absolute_uri(
        reverse('powerapp_pocket:authorize_pocket_done'))
    auth_uri = extend_qs(POCKET_AUTHORIZE_ENDPOINT,
                         request_token=request.session['pocket_request_token'],
                         redirect_uri=redirect_uri)

    return render(request, 'powerapp_pocket/authorize_pocket.html',
                  {'auth_uri': auth_uri})


@login_required
def authorize_pocket_done(request):
    request_token = request.session.pop('pocket_request_token', None)
    if not request_token:
        return redirect('powerapp_pocket:authorize_pocket')

    resp = requests.post(POCKET_ACCESS_TOKEN_ENDPOINT, data={
        'consumer_key': settings.POCKET_CONSUMER_KEY,
        'code': request_token,
    }, headers={'X-Accept': 'application/json'})

    if resp.status_code != 200:
        error = resp.headers.get('X-Error', 'Unknown Error')
        return render(request, 'powerapp_pocket/authorize_pocket_done.html', {'error': error})

    access_token = resp.json()['access_token']
    AccessToken.register(request.user, 'pocket', EMPTY_SCOPE, access_token)

    redirect_target = request.session.pop('pocket_auth_redirect', None)
    if not redirect_target:
        redirect_target = 'powerapp_pocket:add_integration'

    return redirect(redirect_target)
