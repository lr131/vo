from django.db import models

from .user import User
from .bot import TGBot

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="Бот и чат")
    tgbot = models.ForeignKey(TGBot, on_delete = models.RESTRICT, verbose_name="Телеграм бот")
    date_time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(verbose_name="Текст сообщения или адрес картинки/документа", max_length=5000)
    mtype = models.CharField(verbose_name="Тип сообщения", max_length=50)
    
    class Meta:
        verbose_name = 'История сообщений'
        verbose_name_plural = 'Истории сообщений'
        
    def __str__(self):
        return f"{self.date_time} - {self.user} - {self.message[:100]}"