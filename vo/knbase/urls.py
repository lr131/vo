from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.ArticleList.as_view(), name='get_articles'),
    # path('articles', views.get_articles),
    path('articles', views.ArticleList.as_view()),
    path('article/<int:pk>', views.get_article, name='get_article'),
]