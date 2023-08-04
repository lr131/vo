from django.db import models

class AuthData(models.Model):
    social = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    phone_own = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.social
    
    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'