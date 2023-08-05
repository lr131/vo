from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from .event import Event
from .place import Place
        
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