from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.middleware import get_user

from .previous_list import PreviousList
from .client import Client
    
class PreviousListClient(models.Model):
    prev_list = models.ForeignKey(PreviousList, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    cuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, 
                              blank=True, null=True, 
                              verbose_name="Кто добавил клиента в список")
    cdate = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Клиент из списка"
        verbose_name_plural = "Клиенты из списков"

        
    def __str__(self):
        return f"{self.prev_list}"