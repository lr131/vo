from datetime import datetime
from django.db import models

from .client_state import State


class Client(models.Model):
    family = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=250, null=True)
    patr = models.CharField(max_length=250, null=True, blank=True)
    birthday = models.DateTimeField(blank=True, null=True,
                                    default=datetime(1900, 1, 1, hour=16))
    city = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250, null=True)
    in_black_list = models.BooleanField(default=False,
                                        verbose_name="В черном списке")
    state = models.ForeignKey(State, 
                              on_delete=models.SET_NULL, 
                              null=True, blank=True, 
                              default=8,
                              verbose_name="Статус")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарии")
    note = models.TextField(null=True, blank=True, verbose_name="Заметки") # заметки, дополнительно
    group = models.CharField(max_length=10, default='irk', verbose_name="База",)
    working = models.CharField(max_length=250,
                               null=True, blank=True,
                               verbose_name="Сфера деятельности",)
    have_kids = models.BooleanField(default=False, verbose_name="Есть дети",)
    kids = models.CharField(max_length=1000, 
                            null=True, blank=True,
                            verbose_name="Дети, подробности",)
    class Meta:
        managed = False
        db_table = 'clients_client'
        
    def __str__(self):
        return f"{self.family} {self.name} ({self.city})"
    
    @property
    def fio(self):
        return f"{self.family} {self.name} {self.patr if self.patr else ''}"
