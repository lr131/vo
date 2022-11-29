# events/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'events', views.EventViewSet, basename='events')
router.register(r'plan', views.EventPlanViewSet, basename='plan')

urlpatterns = [
    path('', include((router.urls, "router"), namespace="router")),
    path('extra/', views.EventPlanExtraView.as_view(), name='extra'),
    ]
