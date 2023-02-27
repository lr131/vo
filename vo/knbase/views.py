from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


from .models import Article
 
# @login_required
class ArticleList(ListView):
    login_required = True
    model = Article
    template_name = "knbase/articles.html"
    context_object_name = 'articles'
    paginate_by = 10
    
    
# @login_required
# def get_articles(request):
#     context = {
#         'articles': Article.objects.all()
#     }
#     return render(request, "knbase/articles.html", context)
 
@login_required 
def get_article(request, pk):
    context = {
        'article': Article.objects.get(id=pk)
    }
    return render(request, "knbase/article.html", context)
