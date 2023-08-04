from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import datetime as dt

from .state import State
    
class Client(models.Model):
    family = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=250, null=True)
    patr = models.CharField(max_length=250, null=True, blank=True)
    birthday = models.DateTimeField(blank=True, null=True,
                                    default=dt.datetime(1900, 1, 1, hour=16))
    city = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, 
                             null=True, blank=True)
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
    cuser = models.ForeignKey(User, on_delete=models.PROTECT,
                              verbose_name="Кто добавил в базу",
                              related_name='client_cuser',
                              blank=True)
    cdate = models.DateTimeField(auto_now_add=True,
                                 verbose_name="Дата добавления")
    muser = models.ForeignKey(User, on_delete=models.PROTECT,
                              verbose_name="Кто обновил информацию",
                              related_name='client_muser',
                              blank=True)
    mdate = models.DateTimeField(auto_now=True,
                                 verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = 'База клиентов'
        verbose_name_plural = 'База клиентов'
        
    def __str__(self):
        return f"{self.family} {self.name} ({self.city})"
    
    @admin.display(description='Статус')
    def get_state(self):
        return self.state
    
    @admin.display(description='Телефон')
    def get_phone(self):
        return self.phone
    
    @admin.display(description='Город')
    def get_city(self):
        return self.city
    
    @admin.display(description='ФИО')
    def get_abbr_fio(self):
        return f"{self.family} {self.name} {self.patr if self.patr else ''}"
    
    @admin.display(description='Примечания')
    def get_notes(self):
        return f"{self.comment if self.comment else ''}\n{self.note if self.note else ''}"
    