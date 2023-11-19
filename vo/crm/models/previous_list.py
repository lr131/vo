from django.db import models
from django.contrib.auth.models import User

from.event import Event
from .event_plan import EventPlan

class PreviousList(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название")
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name="Описание")
    cuser = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
                              verbose_name="Кто создал список")
    event_plan_id = models.ForeignKey(EventPlan, on_delete=models.SET_NULL, 
                                      null=True, blank=True, verbose_name="Мероприятие с известной датой")
    event_id = models.ForeignKey(Event, on_delete=models.SET_NULL, 
                                 null=True, blank=True, verbose_name="Мероприятие без даты")
    
    class Meta:
        verbose_name = "Список на мероприятие"
        verbose_name_plural = "Списки на мероприятия"
        
    def __str__(self):
        return (f" Список {self.name} "
                f"от {self.date.strftime('%d.%m.%Y')} " 
                f"(by {self.cuser.first_name} {self.cuser.last_name})")