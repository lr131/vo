from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Подробное описание задачи")
    links = models.CharField(max_length=1000, null=True,blank=True,verbose_name="Ссылки")
    files = models.CharField(max_length=1000, null=True,blank=True,verbose_name="Ссылки на файлы") # TODO
    red_line = models.DateTimeField(null=True, verbose_name="Срок, к какому выполнить (редлайн)")
    dead_line = models.DateTimeField(null=True, verbose_name="Крайний срок (дедлайн)")
    priorety = models.IntegerField(default=5, verbose_name="Важность по шкале 1-10")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               related_name='%(class)s_creator',
                               verbose_name="Кто поставил задачу")
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='%(class)s_performer',
                                  verbose_name="Исполнитель")
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = "Задачи"
