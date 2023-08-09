# events/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'list_client', views.PreviousListClientViewSet, basename='list_client')
# router.register(r'plan', views.EventPlanViewSet, basename='plan')

urlpatterns = [
    path('api/', include((router.urls, "router"), namespace="router")),
    path('', views.get_lists, name="get_lists"),
    path('lists', views.get_lists, name="get_lists"),
    path('list/<int:pk>', views.list_detail, name='list_detail'),
    path('list/add', views.add_prevlist, name="add_prevlist"),
    path('list/<int:pk>/remove', views.remove_from_list, name='remove_from_list'),
    path('action/add', views.add_action, name="add_action"),
    path('action/<int:pk>', views.edit_action, name='edit_action'),
    path('add_visit', views.add_visit, name="visit_add"),
    path('complete', views.complete, name="complete"),
    path('active', views.active, name="active"),
    path('lids', views.get_lids, name="lids"),
    path('stat', views.get_stat, name="get_stat"),
    path('lid/add', views.add_lid, name="add_lid"),
    path('tilda', views.get_tilda, name="tilda"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)