from django.db import models

class ClientEventHistory(models.Model):
    client_id = models.IntegerField(verbose_name="Клиент")
    event_plan_id = models.IntegerField(verbose_name="Мероприятие")
    note = models.CharField(max_length=512, blank=True, null=True, verbose_name="Примечания")
    
    class Meta:
        verbose_name = "История посещений мероприятий"
        verbose_name_plural = "История посещений мероприятий"
        db_table = 'client_event_history'
    
    def __str__(self):
        return self.note
