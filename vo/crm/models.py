from multiprocessing import Event
from django.db import models
from django.contrib.auth.models import User

class PreviousList(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название")
    description = models.CharField(max_length=512, blank=True, null=True, verbose_name="Описание")
    cuser = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
                              verbose_name="Кто создал список")
    
    class Meta:
        verbose_name = "Список на мероприятие"
        verbose_name_plural = "Списки на мероприятия"
        
    def __str__(self):
        return (f" Список {self.name}"
                f"от {self.date.strftime('%d.%m.%Y')} " 
                f"(by {self.cuser.first_name} {self.cuser.last_name})")
    
class PreviousListClient(models.Model):
    prev_list = models.ForeignKey(PreviousList, on_delete=models.CASCADE)
    client_id = models.IntegerField()
    cuser = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
                              verbose_name="Кто добавил клиента в список")
    cdate = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Клиент из списка"
        verbose_name_plural = "Клиенты из списков"

        
    def __str__(self):
        return f"{self.prev_list}"
class Lid(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    lid_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Код заявки")
    block_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Код блока")
    form_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Форма на сайте")
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Имя")
    phone = models.CharField(max_length=250, blank=True, null=True, verbose_name="Телефон")
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name="Почта")
    utm_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_source")
    utm_medium = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_medium")
    utm_campaign = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_campaign")
    utm_term = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_term")
    client_id = models.IntegerField(blank=True, null=True, verbose_name="Клиент (если новый, то пусто)")
    event_id = models.IntegerField(blank=True, null=True, verbose_name="Мероприятие (пусто, если клиент не знает чего хочет")
    action = models.CharField(max_length=250, verbose_name="Действие: позвонил, написал, оставил заявку через сайт и тд")
    source = models.CharField(max_length=250, verbose_name="Источник связи, ссылка")
    comment = models.TextField(blank=True, null=True, verbose_name="Примечания (внутренние)")
    target = models.CharField(blank=True, null=True, max_length=250, verbose_name="Целевое действие") # купил курс, зашел на марафон и тд
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Координатор, кто берётся работать")
    
    class Meta:
        verbose_name = "Входящие обращения (Заявки)"
        verbose_name_plural = "Заявка"
        db_table = 'lid'
        
    def __str__(self):
        return self.name
    
    
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
    # TODO сделать редактируемым только для того, кто создал
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, 
                               verbose_name="Координатор, кто берётся работать, ответственный")
    
    class Meta:
        verbose_name = "История взаимодействий с клиентами"
        verbose_name_plural = "История взаимодействий с клиентами"
        db_table = 'action'
        
    def __str__(self):
        return self.note
    
class ClientEventHistory(models.Model):
    client_id = models.IntegerField(verbose_name="Клиент")
    event_plan_id = models.IntegerField(verbose_name="Мероприятие")
    note = models.CharField(max_length=512, blank=True, null=True, verbose_name="Примечания")
    
    class Meta:
        verbose_name = "История посещений мероприятий"
        verbose_name_plural = "История посещений мероприятий"
        db_table = 'client_event_history'
    
    def __str__(self):
        return self.note
