# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

# URL patterns have to contain at least two records: one to add integration,
# and another one to edit it, as provided below. You are welcome to add more
# endpoints if you need it.

urlpatterns = [
    url(r'^integrations/add/$', views.EditIntegrationView.as_view(), name='add_integration'),
    url(r'^integrations/(?P<integration_id>\d+)/$', views.EditIntegrationView.as_view(), name='edit_integration'),
    url(r'^authorize_pocket/$', views.authorize_pocket, name='authorize_pocket'),
    url(r'^authorize_pocket/done/$', views.authorize_pocket_done, name='authorize_pocket_done'),
]
