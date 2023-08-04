from django.db import models
from django.contrib.auth.models import User

from .event import Event, Place


class EventPlan(models.Model):
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True, null=True)
    season = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, blank=True, null=True)
    is_period = models.BooleanField(default=False)
    site = models.CharField(max_length=500, null=True, blank=True)
    period = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'event_plan'
    
    def __str__(self):
        return (f" {self.event.name} " if self.event.name else ""
                f"{self.place} " if self.place else ""
                f"{self.start_date}" if self.start_date else "")