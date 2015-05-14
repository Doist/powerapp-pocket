# -*- coding: utf-8 -*-
import requests
import datetime
from logging import getLogger
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from .apps import AppConfig
from powerapp.core.models.integration import Integration
from powerapp.core.models.oauth import AccessToken
from powerapp.core.todoist_utils import get_personal_project, extract_urls
from powerapp_pocket.views import POCKET_ADD_URL_ENDPOINT


logger = getLogger(__name__)


PROJECT_NAME = 'Pocket task list'


@receiver(post_save, sender=Integration)
def on_integration_save(sender, instance=None, created=None, **kw):
    # as integration saved, create a new personal project for it
    if created and instance.service_id == 'powerapp_pocket':
        get_personal_project(instance.user, instance, PROJECT_NAME)


@receiver(AppConfig.signals.todoist_task_added)
@receiver(AppConfig.signals.todoist_task_updated)
def on_task_added_edited(sender, user=None, service=None,
                         integration=None, obj=None, **kw):
    project = get_personal_project(user, integration, PROJECT_NAME)
    if obj['project_id'] != project['id']:
        return
    process_project(user, project)


@AppConfig.periodic_task(datetime.timedelta(minutes=60))
def periodic_update(user, integration):
    user.api.items.sync()
    project = get_personal_project(user, integration, PROJECT_NAME)
    process_project(user, project)


def process_project(user, project):
    access_token_obj = AccessToken.objects.filter(user=user, client='pocket').first()
    if not access_token_obj:
        logger.warning('Pocket token for %s not found' % user)
        return

    for item in user.api.items.all(lambda i: i['project_id'] == project['id'] and not i['checked']):
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

    user.api.commit()
