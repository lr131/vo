# events/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    ]
