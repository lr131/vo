from datetime import datetime
from django.db import models

STATUS_CHOICES = [
    ('inactive', 'Не активен/Отключен'),
    ('in_development', 'В разработке'),
    ('active', 'Работает'),
]

class TGBot(models.Model):
    token = models.CharField(verbose_name="Токен", max_length=1500)
    bot_name = models.CharField(verbose_name="Какой бот", max_length=250)
    link= models.CharField(verbose_name="Ссылка на бота", max_length=250)
    description = models.CharField( blank=True, null=True,
                               verbose_name="Описание бота", max_length=1500)
    status = models.CharField(
        verbose_name="Cтатус бота",
        max_length=150,
        choices=STATUS_CHOICES,
        default='inactive'
    )
    
    class Meta:
        verbose_name = 'Telegram bot'
        verbose_name_plural = 'Telegram боты'
        
    def __str__(self):
        return f"{self.bot_name} ({self.status}) - {self.description}"