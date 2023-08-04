from django.db import models

class EventState(models.Model):
    name = models.CharField(max_length=300, verbose_name="Статус")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        managed = False
        db_table = 'event_state'
        
    def __str__(self) -> str:
        return f"{self.name}"