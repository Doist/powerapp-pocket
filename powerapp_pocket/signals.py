# -*- coding: utf-8 -*-
from logging import getLogger
from django.dispatch.dispatcher import receiver
from .apps import AppConfig
from .tasks import process_item
from powerapp.core.todoist_utils import get_personal_project

logger = getLogger(__name__)


PROJECT_NAME = 'Pocket task list'


@receiver(AppConfig.signals.todoist_task_added)
@receiver(AppConfig.signals.todoist_task_updated)
def on_task_added_edited(sender, integration=None, obj=None, **kw):
    project = get_personal_project(integration, PROJECT_NAME)
    if obj['project_id'] == project['id'] and not obj['checked']:
        process_item.delay(integration.id, obj['content'], obj['id'])
