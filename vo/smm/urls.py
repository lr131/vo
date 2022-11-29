from django.urls import path
from . import views
urlpatterns = [
    path('', views.mailing_new, name="mailing_new")
]