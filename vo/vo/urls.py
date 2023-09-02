"""vo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from users import views as user_views
from clients import views as client_views
from events import views as events_views
from smm import views as smm_views
from crm import views as crm_views
from tgbots import views as tgbots_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('', user_views.profile, name='profile'),
    path('', client_views.clients, name='clients'),
    path('webhook/tglr131', tgbots_views.telegram_webhook_lr131bot, name='tglr131_webhook'),
    path('webhook/tg/psy20/marathon', tgbots_views.telegram_webhook_psy20_marathon, name='marathon_psy20_webhook'),
    path('webhook/tg/psy20/intensive', tgbots_views.telegram_webhook_psy20_intensive, name='intensive_psy20_webhook'),
    path('clients/', client_views.clients, name='clients'),
    path('client/<int:pk>/', client_views.client, name="client"),
    path('client/create/', client_views.create_client, name="create_client"),
    path('api/clients/', include(('clients.urls', 'clients'), namespace='clients')),
    path('api/events/', include(('events.urls', 'events'), namespace='events'), name='events'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    path('schedule', events_views.get_plan, name="events"),
    path('schedule/upcoming', events_views.upcoming_events, name="upcoming"),
    path('schedule/education', events_views.top_session, name="top_session"),
    path('schedule/add', events_views.create_or_edit_to_plan, name="schedule_add"),
    path('events/add', events_views.create_or_edit_event, name="events_add"),
    path('users', user_views.get_active_users, name='users'),
    path('users/past', user_views.get_prev_users, name='users_past'),
    path('webhook/tilda', crm_views.tilda_webhook, name='tilda_webhook'),
    path('kn/', include(('knbase.urls', 'knbase'), namespace="knbase"), name="knbase"),
    path('smm/', include(('smm.urls', 'smm'), namespace="smm"), name="smm"),
    path('crm/', include(('crm.urls', 'crm'), namespace="crm"), name="crm"),
    path('tgbots/', include(('tgbots.urls', 'tgbots'), namespace="tgbots"), name="tgbots"),
]
