from django.db import models


class PostType(models.Model):
    post_type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=800, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Тип поста'
        verbose_name_plural = 'Типы постов'
        
    def __str__(self):
        return self.name

