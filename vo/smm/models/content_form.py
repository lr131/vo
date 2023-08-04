from django.db import models

# Стаьтя, лонгрид, короткий пост, картинка, карусель, кружочек, голосовое, подкаст и тд?
class ContentForm(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Формат контента'
        verbose_name_plural = 'Форматы контента'
        db_table = 'content_form'

    def __str__(self):
        return self.name