from django.db import models
       
# рубрика
class Rubric(models.Model):
    name = models.CharField(max_length=300)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        db_table = 'rubric'

    def __str__(self):
        return self.name
    