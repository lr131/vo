from django.db import models

from .link_out import LinkOut
from .event_plan import EventPlan
from .lid import Lid

class Seeding(models.Model):
    """Посевы рекламные"""
    сdate = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата публикации")
    date = models.DateTimeField(blank=True, null=True, verbose_name="Дата публикации")
    link_out = models.ForeignKey(LinkOut, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="Где разместили")
    summary = models.CharField(max_length=1500, blank=True, null=True, verbose_name="Что публиковали (кратко)")
    price = models.IntegerField(default=0, verbose_name="Стоимость размещения")
    description = models.CharField(max_length=500, null=True, blank=True, 
                                   verbose_name="Условия размещения этого конкретного поста")
    link = models.CharField(max_length=500, null=True, blank=True, verbose_name="Ссылка на пост")
    event = models.ForeignKey(EventPlan, on_delete=models.RESTRICT,
                              null=True, blank=True, verbose_name="Какое мероприятие рекламируем")
    
    @property
    def lead_count(self):
        return Lid.objects.filter(event_id=self.event.pk, 
                                  utm_source=self.link_out.utm_source.utm_source,
                                  utm_medium=self.link_out.utm_medium.utm_medium).count()
    
    # TODO добавить рассчет тех, кто дошел

    @property
    def lead_cost(self):
        if self.lead_count > 0: 
            return self.price / self.lead_count
        else:
            return 0
   
   
    class Meta:
        verbose_name = 'Посев в сообществе'
        verbose_name_plural = 'Посевы по сообществам и группам'
        
    def __str__(self):
        return f"{self.date} ({self.link_out})"