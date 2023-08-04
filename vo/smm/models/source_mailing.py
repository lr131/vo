from django.db import models
from ..const import MAILING_SOURCE_TYPES, MAILING_RESULT_CHOISES, SOURCE_MAILING_STATE

from .utm_source import UTMSource
from .utm_medium import Medium
from .utm_campaign import CampaingUTM

            
class SourceMailing(models.Model):
    name = models.CharField(max_length=200)
    utm_source = models.ForeignKey(UTMSource, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_source (Соцсеть или месседжер)")
    utm_medium = models.ForeignKey(Medium, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_medium (Тип трафика)")
    utm_campaign = models.ForeignKey(CampaingUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_campaign (Название кампании))")
    price = models.DecimalField(default=0, 
                                max_digits = 5,
                                decimal_places = 2,
                                verbose_name="Стоимость размещения")
    description = models.CharField(max_length=2000, 
                                   verbose_name="Короткое описание источника")
    state = models.CharField(max_length=10,
                            choices=SOURCE_MAILING_STATE,
                            default='actual')
    
    class Meta:
        verbose_name = 'Внешний ресурс для размещения'
        verbose_name_plural = 'Внешние ресурсы для размещения'

    def __str__(self):
        return f"{self.name} ({self.utm_source})"
