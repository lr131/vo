# clients/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'states', views.StateViewSet, basename='states')
router.register(r'clients', views.ClientViewSet)
router.register(r'products', views.ClientProductsViewSet)
router.register(r'mailing', views.ClientMailingViewSet)
router.register(r'interest', views.ClientInterestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('extra/', views.ClientExtraView.as_view(), name='extra'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]