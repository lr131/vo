from django.db import models

            
class Links(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True) # Дата создания ссылки
    link = models.CharField(max_length=200) # длинная ссылка
    short = models.CharField(max_length=200, blank=True, null=True) # сокращенная ссылка
    source = models.CharField(max_length=200) # источник
    utm_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_source")
    utm_type_source = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_source")
    utm_medium = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_medium")
    utm_type_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_type_content")
    utm_campaign = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_campaign")
    utm_term = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_term")
    utm_content = models.CharField(max_length=50, blank=True, null=True, verbose_name="utm_content")
    
    class Meta:
        managed = False
        db_table = 'smm_links'
        
    def __str__(self):
        return self.link