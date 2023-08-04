from django.db import models
from .utm_source import UTMSource
from .utm_medium import Medium
from .utm_type_source import TypeSourceUTM

class SocialPlace(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=150, null=True, blank=True)
    social = models.CharField(max_length=20)
    utm_source = models.ForeignKey(UTMSource, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_source (Соцсеть или месседжер)")
    utm_type_source = models.ForeignKey(TypeSourceUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_type_source (группа/страница/канал/чат/direct)",)
    utm_medium = models.ForeignKey(Medium, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_medium (Тип трафика)")
   
    class Meta:
        verbose_name = 'Место размещения (соцсеть или лэндинг)'
        verbose_name_plural = 'Места размещения (соцсети и сайты)'
        db_table = 'social_place'

    def __str__(self):
        return self.name
    