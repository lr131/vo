from datetime import datetime
from django.db import models
from .client import Client
from .bot import TGBot

class User(models.Model):
    tgbot = models.ForeignKey(TGBot, on_delete = models.RESTRICT, verbose_name="Телеграм бот")
    chat_id = models.IntegerField(verbose_name="Идентификатор чата")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, 
                               blank=True, null=True,
                               verbose_name="Клиент из базы")
    
    class Meta:
        verbose_name = 'Пользователь бота телеграм'
        verbose_name_plural = 'Пользователи ботов телеграм'
        
    def __str__(self):
        return f"{self.bot_name} - {self.chat_id}"