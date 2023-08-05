from django.contrib import admin
from .models.category import Category
from .models.article import Article

admin.site.register(Article)
admin.site.register(Category)