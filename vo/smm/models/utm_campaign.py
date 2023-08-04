from django.db import models


class CampaingUTM(models.Model):
    type_source = models.CharField(max_length=200)
    utm_campaign = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.utm_campaign
    
    class Meta:
        verbose_name = 'UTMCampaign'
        verbose_name_plural = 'Метки UTMCampaign'
        db_table = 'smm_utm_campaing'