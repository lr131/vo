from django.db import models

class WebHook(models.Model):
    body = models.TextField()
    formid = models.CharField(max_length=50, verbose_name="ID формы Тильды", null=True, blank=True)
    formname = models.CharField(max_length=100, verbose_name="Форма Тильды", null=True, blank=True)
    tranid = models.CharField(max_length=50, verbose_name="№ заявки", null=True, blank=True)
    name = models.CharField(max_length=500, verbose_name="Имя", null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name="Телефон", null=True, blank=True)
    cdate = models.DateTimeField(auto_now_add=True, null=True,
                                 verbose_name="Дата добавления")
    
    class Meta:
        managed = False
        db_table = 'crm_webhook'
    
    def __str__(self):
        return f"{self.body}"