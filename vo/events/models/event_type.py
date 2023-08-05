from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=300, verbose_name="Тип мероприятия")
    description = models.CharField(max_length=200,null=True,blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Справочник типов мероприятий"
        verbose_name_plural = "Справочник типов мероприятий"
        db_table = 'event_types'
        
    def __str__(self) -> str:
        return f"{self.name}"