# -*- coding: utf-8 -*-
import requests
from logging import getLogger
from django.conf import settings
from powerapp.celery_local import app
from powerapp.core.models import Integration, OAuthToken
from powerapp.core.todoist_utils import extract_urls
from powerapp_pocket.views import POCKET_ADD_URL_ENDPOINT



logger = getLogger(__name__)


@app.task(ignore_result=True)
def process_item(integration_id, item_content, item_id):
    try:
        integration = Integration.objects.get(id=integration_id)
    except Integration.DoesNotExist:
        return

    access_token_obj = OAuthToken.objects.filter(
        user=integration.user, client='pocket').first()
    if not access_token_obj:
        logger.warning('Pocket token for %s not found' % integration.user)
        return

    logger.debug('Pocket: processing %s' % item_content)
    urls = extract_urls(item_content)
    for url in urls:
        resp = requests.post(POCKET_ADD_URL_ENDPOINT, data={
            'url': url.link,
            'title': url.title or '',
            'consumer_key': settings.POCKET_CONSUMER_KEY,
            'access_token': access_token_obj.access_token,
            'tags': 'todoist',
        })
        if resp.status_code == 401:
            # delete access token, it's not valid anymore
            logger.warning('Pocket token for %s invalid. Delete it' % integration.user)
            access_token_obj.delete()
            return

        resp.raise_for_status()
        logger.debug('Pocket: added URL %s', url)
    with integration.api.autocommit():
        integration.api.item_update(item_id, checked=True, in_history=True)
