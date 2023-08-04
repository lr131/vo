from django.db import models
from .event_place import Place
from .event import Event

class EventPlan(models.Model):
    start_date = models.DateTimeField(blank=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата завершения")
    season = models.CharField(max_length=100, default="2023/2024", verbose_name="Сезон")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Мероприятие")
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Где")
    is_period = models.BooleanField(default=False, verbose_name="Это периодичное мероприятие?")
    site = models.CharField(max_length=500, null=True, blank=True, verbose_name="Ссылка на лендинг (перекроет ссылку тренинга)")
    period = models.PositiveIntegerField(null=True,blank=True, verbose_name="Введите период (в днях)") # через сколько дней если что повторять
    
    class Meta:
        managed = False
        db_table = 'event_plan'
    
    def __str__(self):
        return (f" {self.event.name} " if self.event.name else ""
                f"{self.place} " if self.place else ""
                f"{self.start_date}" if self.start_date else "")
