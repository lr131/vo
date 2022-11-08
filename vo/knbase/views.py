from django.shortcuts import render

from .models import Article
 
 
def get_articles(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(request, "knbase/articles.html", context)
 
 
def get_article(request, pk):
    context = {
        'article': Article.objects.get(id=pk)
    }
    return render(request, "knbase/article.html", context)
