from multiprocessing import Event
from django.db import models
from django.contrib.auth.models import User

class Lid(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client_id = models.IntegerField()
    event_id = models.IntegerField()
    action = models.CharField(max_length=250, verbose_name="Действие")
    source = models.CharField(max_length=250, verbose_name="Источник связи")
    comment = models.TextField(blank=True, null=True)
    note = models.TextField(verbose_name="Резюме разговора")
    stage = models.CharField(max_length=250, verbose_name="Этап")
    target = models.CharField(blank=True, null=True, max_length=250, verbose_name="Целевое действие") # купил курс, зашел на марафон и тд
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Координатор")
    
