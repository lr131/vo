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
from events import views as evens_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('', user_views.profile, name='profile'),
    path('', user_views.clients, name='clients'),
    path('clients/', user_views.clients, name='clients'),
    path('client/<int:pk>/', user_views.client, name="client"),
    path('client/create/', user_views.create_client, name="create_client"),
    path('api/clients/', include(('clients.urls', 'clients'), namespace='clients')),
    path('api/events/', include(('events.urls', 'events'), namespace='events'), name='events'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework'))
]
