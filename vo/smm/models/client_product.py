from django.db import models
from .client import Client


class ClientProducts(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='products')
    is_assisting = models.BooleanField(default=False,verbose_name="Клиент ассистировал") # Клиент уже ассистировал на БК
    future_assisting = models.BooleanField(default=False, verbose_name="Хочет на ассистирование") # клиент хочет на будущие ассистирования
    is_base_course = models.BooleanField(default=False,verbose_name="Курсовой")
    course_candidate = models.TextField(null=True, blank=True,verbose_name="Кандидаты на курс")
    is_school_level_1 = models.BooleanField(default=False,verbose_name="Выпускник ИШ1")
    is_school_level_2 = models.BooleanField(default=False,verbose_name="Выпускник ИШ2")
    is_school_level_3 = models.BooleanField(default=False, verbose_name="Выпускник ИШ3")
    tg = models.BooleanField(default=False,verbose_name="Выпускник терапевтической группы") # Клиент проходил терапевтическую группу
    
    class Meta:
        managed = False
        db_table = 'client_products'
    
    def __str__(self):
        return (f" {self.client.family} " if self.client.family else ""
                f"{self.client.name} " if self.client.name else ""
                f"{self.course_candidate}" if self.course_candidate else "")
