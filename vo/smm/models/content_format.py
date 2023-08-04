from django.db import models

# Видео, аудио, текст
class ContentFormat(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Вид контента'
        verbose_name_plural = 'Виды контента'
        db_table = 'content_format'

    def __str__(self):
        return self.name