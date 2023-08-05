from django.db import models

class Place(models.Model):
    addr = models.CharField(max_length=200,null=True,blank=True, verbose_name="Адрес")
    source =  models.CharField(max_length=200,null=True,blank=True, verbose_name="Название") # онлайн, зал, кабинет
    
    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места проведения"
        db_table = 'events_place'
        
    def __str__(self) -> str:
        return f"{self.addr}"