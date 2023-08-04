from django.db import models
from django.contrib.auth.models import User
    
         
class Medium(models.Model):
    type_source = models.CharField(max_length=200)
    utm_medium = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, 
                              null=True, blank=True,
                              verbose_name="чья метка (из команды)")

    def __str__(self):
        return self.utm_medium
    
    class Meta:
        verbose_name = 'UTMMedium'
        verbose_name_plural = 'Метки UTMMedium'