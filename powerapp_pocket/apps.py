# -*- coding: utf-8 -*-
"""
Creates a new project in your Todoist account and starts monitoring tasks in it.
As soon as you create a task there (or move the task from another project, such
as "Hacker News Reader"), URLs from it will be extracted and added to your
pocket account.
"""
import environ
from powerapp.core.apps import ServiceAppConfig


env = environ.Env()


class AppConfig(ServiceAppConfig):
    name = 'powerapp_pocket'
    verbose_name = 'Pocket integration'
    models_module = None
    url = 'https://getpocket.com'
    description = __doc__

    POCKET_CONSUMER_KEY = env('POCKET_CONSUMER_KEY', default=None)
