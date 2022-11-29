# events/urls.py
from django.urls import include, path
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'events', views.EventViewSet, basename='events')
# router.register(r'plan', views.EventPlanViewSet, basename='plan')

urlpatterns = [
    path('add', views.add_visit, name="visit_add"),
    path('history', views.get_list, name="get_list"),
    ]