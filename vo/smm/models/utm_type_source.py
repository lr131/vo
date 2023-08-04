from django.db import models

class TypeSourceUTM(models.Model):
    title = models.CharField(max_length=200)
    utm_type_source = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)


    def __str__(self):
        return self.utm_type_source
    
    class Meta:
        verbose_name = 'UTM Type Source (тип ресурса, группа, канал, сообщение или что)'
        verbose_name_plural = 'Метки UTM Type Source'
        db_table = 'smm_utm_type_source'