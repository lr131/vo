# events/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'list_client', views.PreviousListClientViewSet, basename='list_client')
# router.register(r'plan', views.EventPlanViewSet, basename='plan')

urlpatterns = [
    path('api/', include((router.urls, "router"), namespace="router")),
    path('', views.get_lists, name="get_lists"),
    path('lists', views.get_lists, name="get_lists"),
    path('list/<int:pk>', views.list_detail, name='list_detail'),
    path('list/add', views.add_prevlist, name="add_prevlist"),
    path('action/add', views.add_action, name="add_action"),
    path('add_visit', views.add_visit, name="visit_add"),
    path('complete', views.complete, name="complete"),
    path('active', views.active, name="active"),
    path('lids', views.get_lids, name="lids"),
    
    ]