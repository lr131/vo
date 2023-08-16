from django.db import models

from .utm_source import UTMSource
from .utm_medium import Medium

            
class LinkOut(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата создания ссылки")
    link = models.CharField(max_length=500, verbose_name="Ссылка на источник")
    name = models.CharField(max_length=500, verbose_name="Наименование источника")
    contact = models.CharField(max_length=1000, verbose_name="Контакт для размещения")
    conditions = models.TextField(verbose_name="Условия размещения")
    conditions_date = models.DateTimeField(auto_now_add=True,blank=True, 
                                      verbose_name="Обновили условия размещения")
    topic = models.CharField(max_length=100, verbose_name="Тематика", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Город/Регион", blank=True, null=True)
    
    utm_source = models.ForeignKey(UTMSource, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_source (метка источника)")
    utm_medium = models.ForeignKey(Medium, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_medium (метка трафика)")
    
    views = models.IntegerField(null=True, blank=True,verbose_name="Просмотров")
    views_date = models.DateTimeField(auto_now_add=True,blank=True, 
                                      verbose_name="Обновили показатели просмотров")
    reach = models.IntegerField(null=True, blank=True,verbose_name="Охват")
    reach_date = models.DateTimeField(auto_now_add=True,blank=True, 
                                      verbose_name="Обновили показатели охвата")
    followers = models.IntegerField(null=True, blank=True,verbose_name="Подписчиков")
    followers_date = models.DateTimeField(auto_now_add=True,blank=True, 
                                      verbose_name="Обновили показатели охвата")
    actual = models.BooleanField(default=True, verbose_name="Используемый источник")
    note = models.CharField(max_length=2000,null=True, blank=True, verbose_name="Короткий комметарий, если нужно")
    
    
    class Meta:
        verbose_name = 'Внешняя ссылка для размещения'
        verbose_name_plural = 'Внешние источники размещения'
        
    def __str__(self):
        return f"{self.name} ({self.utm_source.social})"
