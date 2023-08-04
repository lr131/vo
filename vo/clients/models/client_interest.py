from django.db import models

from .client import Client

class ClientInterest(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               verbose_name="Клиент", related_name='interest')
    event = models.IntegerField(null=True, blank=True,verbose_name="Мероприятия")
    comment = models.TextField(null=True, blank=True,verbose_name="Примечания")

    class Meta:
        verbose_name = 'Клиенты интересуются'
        verbose_name_plural = 'Клиенты интересуются'
        db_table = 'client_interest'

    def __str__(self):
        return f"{self.comment}" if self.comment else f''
