from django.db import models

from .post import Post
from .utm_medium import Medium


class PostPlan(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост") # TODO проверить тип
    source = models.ForeignKey(Medium, on_delete=models.CASCADE, verbose_name="Метка utm_source места публикации") # TODO проверить тип и указать, что это - место публикации
    pub_date = models.DateTimeField(blank=True, null=True, verbose_name="Когда опубликовать") 
    deadline_date = models.DateTimeField(null=True, blank=True, verbose_name="Крайний срок, дедлайн")
    disable_date = models.DateTimeField(blank=True, null=True, verbose_name="дата отмены поста") # дата отмены поста 
    state = models.CharField(max_length=200, blank=True, null=True, verbose_name="Стадия поста") # Состояние: в работе, опубликован, не опубликован, перенесен
    reasons = models.CharField(max_length=200, blank=True, null=True, verbose_name="Причина отмены публикации") # Причина отмены публикации
    is_published = models.BooleanField(default=False, verbose_name="Пост опубликован")
    link = models.TextField(blank=True, null=True, verbose_name="Ссылка на пост")
    
    class Meta:
        verbose_name = 'Контент-план'
        verbose_name_plural = 'Контент-план'
