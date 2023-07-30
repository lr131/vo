from django.urls import path
from . import views
urlpatterns = [
    path('', views.mailing_list, name="mailing_list"),
    path('new/', views.mailing_new, name="mailing_new"),
    path('group/<int:pk>', views.mailing_group, name="mailing_group"),
    path('db/<int:pk>', views.mailing_db, name="mailing_db"),
    path('db/<int:pk>/create', views.mailing_db_new, name="mailing_db_new"),
    path('db/<int:pk>/wapico', views.get_mailing_db_file, name="wapico"),
    path('out/<int:pk>', views.mailing_myperson, name="mailing_myperson"),
    path('sp/', views.sp_list, name="sp_list"),
    path('sp/new/', views.sp_new, name="sp_new"),
    path('links/', views.link_list, name="link_list"),
    path('link/new/', views.link_new, name="link_new"),
]