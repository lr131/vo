from django.db import models


class Lid(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    lid_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Код заявки")
    block_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Код блока")
    form_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Форма на сайте")
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Имя")
    phone = models.CharField(max_length=250, blank=True, null=True, verbose_name="Телефон")
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name="Почта")
    utm_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_source")
    utm_type_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_source")
    utm_medium = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_medium")
    utm_type_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_content")
    utm_campaign = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_campaign")
    utm_term = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_term")
    utm_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_content")
    client_id = models.IntegerField(blank=True, null=True, verbose_name="Клиент (если новый, то пусто)")
    event_id = models.IntegerField(blank=True, null=True, verbose_name="Мероприятие (пусто, если клиент не знает чего хочет")
    action = models.CharField(max_length=250, verbose_name="Действие: позвонил, написал, оставил заявку через сайт и тд")
    source = models.CharField(max_length=250, verbose_name="Источник связи, ссылка")
    comment = models.TextField(blank=True, null=True, verbose_name="Примечания (внутренние)")
    target = models.CharField(blank=True, null=True, max_length=250, verbose_name="Целевое действие") # купил курс, зашел на марафон и тд
    
    class Meta:
        managed = False
        db_table = 'lid'
        
    def __str__(self):
        return f'{self.name} ({self.form_name}) {self.date}'