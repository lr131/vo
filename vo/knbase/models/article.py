from django.db import models
from django.contrib.auth.models import User 

from .category import Category
 
class Article(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    author = models.ManyToManyField(User)
    title = models.CharField(max_length=50)
    text = models.TextField()
    data = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
 
    def __str__(self):
        return self.title