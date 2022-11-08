from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.get_articles, name='get_articles'),
    path('articles', views.get_articles),
    path('article/<int:pk>', views.get_article, name='get_article'),
]