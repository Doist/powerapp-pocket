# -*- coding: utf-8 -*-
import requests
from logging import getLogger
from django.conf import settings
from django.dispatch.dispatcher import receiver
from .apps import AppConfig
from powerapp.core.models.oauth import OAuthToken
from powerapp.core.todoist_utils import get_personal_project, extract_urls
from powerapp_pocket.views import POCKET_ADD_URL_ENDPOINT


logger = getLogger(__name__)


PROJECT_NAME = 'Pocket task list'


@receiver(AppConfig.signals.todoist_task_added)
@receiver(AppConfig.signals.todoist_task_updated)
def on_task_added_edited(sender, integration=None, obj=None, **kw):
    project = get_personal_project(integration, PROJECT_NAME)
    if obj['project_id'] == project['id'] and not obj['checked']:
        process_item(integration, obj)


def process_item(integration, item):
    access_token_obj = OAuthToken.objects.filter(
        user=integration.user, client='pocket').first()
    if not access_token_obj:
        logger.warning('Pocket token for %s not found' % integration.user)
        return

    logger.debug('Pocket: processing %s' % item['content'])
    urls = extract_urls(item['content'])
    for url in urls:
        requests.post(POCKET_ADD_URL_ENDPOINT, data={
            'url': url.link,
            'title': url.title or '',
            'consumer_key': settings.POCKET_CONSUMER_KEY,
            'access_token': access_token_obj.token,
            'tags': 'todoist',
        })
        logger.debug('Pocket: added URL %s', url)
    item.complete()
    integration.api.commit()
