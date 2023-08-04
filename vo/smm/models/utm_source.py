from django.db import models
     
class UTMSource(models.Model):
    social = models.CharField(max_length=200)
    utm_source = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.social
    
    class Meta:
        verbose_name = 'UTMSource'
        verbose_name_plural = 'Список UTMSource'