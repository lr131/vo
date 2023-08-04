from django.db import models
from .event_plan import EventPlan
from ..const import MAILING_SOURCE_TYPES



class Mailing(models.Model):
    name = models.CharField(max_length=100, 
                            verbose_name="Название рассылки")
    description = models.CharField(max_length=100, 
                            verbose_name="Описание рассылки")
    event_plan_id = models.ForeignKey(EventPlan, on_delete=models.SET_NULL, 
                                      null=True, blank=True, verbose_name="По поводу мероприятия")
    text = models.TextField(blank=True, null=True, verbose_name="текст рассылки без меток")
    source_type = models.CharField(max_length=100,
                                   choices=MAILING_SOURCE_TYPES,
                                   default='group',
                                   verbose_name="Тип рассылки")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = 'Список для рассылки'
        verbose_name_plural = 'Список рассылок'

    def __str__(self):
        return f"{self.name}"

