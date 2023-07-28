from tabnanny import verbose
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Place(models.Model):
    addr = models.CharField(max_length=200,null=True,blank=True, verbose_name="Адрес")
    source =  models.CharField(max_length=200,null=True,blank=True, verbose_name="Название") # онлайн, зал, кабинет
    
    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места проведения"
        
    def __str__(self) -> str:
        return f"{self.addr}"
    
class EventState(models.Model):
    name = models.CharField(max_length=300, verbose_name="Статус")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Справочник состояний мероприятий"
        verbose_name_plural = "Справочник состояний мероприятий"
        db_table = 'event_state'
        
    def __str__(self) -> str:
        return f"{self.name}"


class EventType(models.Model):
    name = models.CharField(max_length=300, verbose_name="Тип мероприятия")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Справочник типов мероприятий"
        verbose_name_plural = "Справочник типов мероприятий"
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
        verbose_name = "Мероприятие"
        verbose_name_plural = "Список имеющихся мероприятий"
        
    def __str__(self) -> str:
        return f"{self.name} ({self.event_type}) - {self.state}"

class EventPlan(models.Model):
    start_date = models.DateTimeField(blank=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата завершения")
    season = models.CharField(max_length=100, default="2023/2024", verbose_name="Сезон")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Мероприятие")
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Где")
    user = models.ManyToManyField(User, blank=True, verbose_name="Кто ведёт")
    is_period = models.BooleanField(default=False, verbose_name="Это периодичное мероприятие?")
    site = models.CharField(max_length=500, null=True, blank=True, verbose_name="Ссылка на лендинг (перекроет ссылку тренинга)")
    period = models.PositiveIntegerField(null=True,blank=True, verbose_name="Введите период (в днях)") # через сколько дней если что повторять
    
    class Meta:
        verbose_name = "План мероприятий"
        verbose_name_plural = "План мероприятий"
        db_table = 'event_plan'

    def __str__(self):
        return f"{self.start_date.strftime('%d.%m.%Y')} - {self.end_date.strftime('%d.%m.%Y')} {self.event.event_type} {self.event.name} ({self.place.addr})"
    
    @admin.display(description='Мероприятие')
    def get_event_name(self):
        return f"{self.event.name}"
    
    @admin.display(description='Тип')
    def get_event_type(self):
        return f"{self.event.event_type}"
    
    @admin.display(description='Даты')
    def get_dates(self):
        return f"{self.start_date.strftime('%d.%m.%Y %H:%M')} - {self.end_date.strftime('%d.%m.%Y %H:%M')}"
    
    @admin.display(description='Где')
    def get_place(self):
        return f"{self.place}"
    
    @admin.display(description='Мероприятие')
    def get_info(self):
        return f"{self.event.name} (минимум {self.event.country} человек)"