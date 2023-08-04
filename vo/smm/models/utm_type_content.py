from django.db import models

class TypeContentUTM(models.Model):
    title = models.CharField(max_length=200)
    utm_type_content = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)


    def __str__(self):
        return self.utm_type_content
    
    class Meta:
        verbose_name = 'UTM Type Content (post/stories/header)'
        verbose_name_plural = 'Метки UTM Type Content'
        db_table = 'smm_utm_type_Content'