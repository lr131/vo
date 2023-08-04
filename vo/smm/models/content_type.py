from django.db import models

# Это вид контента: информационный, развлекательный, анонс и тд
class ContentType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Тип контента'
        verbose_name_plural = 'Типы контента'
        db_table = 'content_type'

    def __str__(self):
        return self.name