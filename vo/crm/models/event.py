from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    addr = models.CharField(max_length=200,null=True,blank=True, verbose_name="Адрес")
    source =  models.CharField(max_length=200,null=True,blank=True, verbose_name="Название")
    
    class Meta:
        managed = False
        db_table = 'events_place'
        
    def __str__(self) -> str:
        return f"{self.addr}"

class EventState(models.Model):
    name = models.CharField(max_length=300, verbose_name="Статус")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        managed = False
        verbose_name = "Справочник состояний мероприятий"
        verbose_name_plural = "Справочник состояний мероприятий"
        db_table = 'event_state'
        
    def __str__(self) -> str:
        return f"{self.name}"

class EventType(models.Model):
    name = models.CharField(max_length=300, verbose_name="Тип мероприятия")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        managed = False
        db_table = 'event_types'
        
    def __str__(self) -> str:
        return f"{self.name}"

class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    state = models.ForeignKey(EventState, verbose_name="Статус", null=True, blank=True, on_delete=models.SET_NULL) # проводится, не проводится, в архиве и тд
    event_type = models.ForeignKey(EventType, verbose_name="Тип мероприятия",  null=True, blank=True, on_delete=models.SET_NULL) # Тренинг, программа, марафон и тд
    description = models.TextField(null=True,blank=True, verbose_name="Описание")
    short = models.CharField(max_length=500, blank=True, null=True, verbose_name="Короткое описание (до 500 знаков)")
    payment = models.CharField(max_length=200,null=True,blank=True, verbose_name="Стоимость")
    continuance = models.CharField(max_length=200,null=True,blank=True, verbose_name="Продолжительность") # продолжительность
    about = models.TextField(null=True,blank=True, verbose_name="Какие боли закрывает?") # какие боли закрывает
    country = models.IntegerField(default=5, verbose_name="Сколько человек по плану") # количество человек по плану
    next_step = models.TextField(null=True,blank=True, verbose_name="Следующий шаг по продуктам") # следующий шаг по продуктам TODO
    prev_step = models.TextField(null=True,blank=True, verbose_name="Предыдущий шаг по продуктам") # предыдущий шаг / бесплатные материалы TODO
    created_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата создания")
    site = models.CharField(max_length=500, null=True, blank=True, verbose_name="Ссылка на лендинг")
    
    class Meta:
        managed = False
        db_table = 'events_event'
        
    def __str__(self) -> str:
        return f"{self.name} ({self.event_type}) - {self.state}"