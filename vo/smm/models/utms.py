from django.db import models
from .utm_source import UTMSource
from .utm_medium import Medium
from .utm_campaign import CampaingUTM
from .utm_type_source import TypeSourceUTM
from .utm_type_content import TypeContentUTM
            
    
class UTMs(models.Model):
    utm_source = models.ForeignKey(UTMSource, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_source (Источник кампании)")
    utm_type_source = models.ForeignKey(TypeSourceUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_type_source (группа/страница/канал/чат/direct)",)
    utm_medium = models.ForeignKey(Medium, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_medium (Тип трафика)")
    utm_type_content = models.ForeignKey(TypeContentUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_type_content (Тип контента)")
    utm_campaign = models.ForeignKey(CampaingUTM, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="utm_campaign (Название кампании))")
    
    class Meta:
        verbose_name = 'Готовый набор UTM меток'
        verbose_name_plural = 'Готовый набор UTM меток'
        db_table = 'smm_utms'
        
    def __str__(self):
        return f"{self.utm_source}-{self.utm_type_source}-{self.utm_medium}-{self.utm_type_content}-{self.utm_campaign}"
