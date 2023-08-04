from django.db import models
       
# Цель поста: повысить охват, ещё что-нибудь такое 
class Target(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Цель поста'
        verbose_name_plural = 'Цели поста'
        db_table = 'target'

    def __str__(self):
        return self.name
