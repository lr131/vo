# clients/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'states', views.StateViewSet, basename='states')
router.register(r'client', views.ClientViewSet, basename='client')
router.register(r'products', views.ProductsViewSet, basename='products')
# router.register(r'p', views.ProductInterestViewSet)
router.register(r'mailing', views.MailingViewSet, basename='mailing')
router.register(r'interest', views.InterestViewSet, basename='interest')


urlpatterns = [
    path('', include((router.urls, "router"), namespace="router")),
    path('extra/', views.ClientExtraView.as_view(), name='extra'),
    path('history/<int:client_id>/', views.ClientProductsView.as_view(), name="history"),
    path('connect/<int:client_id>/', views.ClientMailingView.as_view(), name="connect"),
    
    path('interests/<int:client_id>/', views.ClientInterestView.as_view(), name="interests"),
    path('product/<int:event_id>/', views.ProductInterestView.as_view(), name="product"),    
]

print(urlpatterns)