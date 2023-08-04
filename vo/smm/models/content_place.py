from datetime import datetime
from django.db import models

# где размещаем: сторис, посты, рилс, клипы
class ContentPlace(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Способ размещения контента'
        verbose_name_plural = 'Способы размещения контента'
        db_table = 'content_place'

    def __str__(self):
        return self.name