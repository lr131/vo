from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from .previous_list_client import PreviousListClient
from .lid import Lid
    
class Action(models.Model):
    plc = models.ForeignKey(PreviousListClient, on_delete=models.PROTECT,
                            null=True, blank=True,
                            verbose_name="Клиент из списка")
    lid = models.ForeignKey(Lid, on_delete=models.PROTECT,
                            related_name="lid_actions",
                            null=True, blank=True,
                            verbose_name="Лид заявки")
    cdate = models.DateTimeField(auto_now_add=True)
    mdate = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    action = models.CharField(max_length=250, verbose_name="Действие координатора")
    note = models.TextField(verbose_name="Резюме общения")
    stage = models.CharField(max_length=250, verbose_name="Этап")
    state = models.BooleanField(default=False, verbose_name="Завершены все этапы")
    # TODO сделать редактируемым только для того, кто создал
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
                               verbose_name="Координатор, кто берётся работать, ответственный")
    
    class Meta:
        verbose_name = "История взаимодействий с клиентами"
        verbose_name_plural = "История взаимодействий с клиентами"
        db_table = 'action'
        
    def __str__(self):
        return self.note

    @admin.display(description='Лид')
    def get_lid(self):
        return f"{self.lid.form_name}"
    
    @admin.display(description='Клиент')
    def get_client(self):
        return f"{self.lid.name}"