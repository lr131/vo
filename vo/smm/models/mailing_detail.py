from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import urllib.parse

from ..const import MAILING_RESULT_CHOISES
from .mailing import Mailing
from .source_mailing import SourceMailing
from .client import Client
from .lid import Lid

    
class MailingDetail(models.Model):
    mailing = models.ForeignKey(Mailing,
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    
    source = models.ForeignKey(SourceMailing, 
                               on_delete=models.RESTRICT,
                               null=True, blank=True,
                               verbose_name="Источник указываем для групп")
    text = models.TextField()
    link = models.CharField(max_length=500, null=True, blank=True,
                            verbose_name="Ссылка, если есть, без меток")
    outer_text = models.TextField(verbose_name="Готовый текст для whatsapp, сформируется автоматически")
    outer_text_vi = models.TextField(null=True, blank=True,
                                     verbose_name="Готовый текст для viber, сформируется автоматически")
    outer_text_tg = models.TextField(null=True, blank=True,
                                     verbose_name="Готовый текст для viber, сформируется автоматически")
    
    cdate = models.DateTimeField(auto_now_add=True)
    cuser = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.RESTRICT,
                              related_name='smm_cuser')
    
    mdate = models.DateTimeField(auto_now=True)
    muser = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.RESTRICT,
                              related_name='smm_muser')
    
    pdate = models.DateTimeField(verbose_name="Дата выполнения",
                                 null=True, blank=True)
    puser = models.ForeignKey(User, on_delete=models.RESTRICT, 
                              null=True, blank=True,
                              verbose_name="Кто выполнил",
                              related_name='smm_puser')
    
    link_messeger = models.TextField(null=True, blank=True,
                                     verbose_name="Месседжер")
    client = models.ForeignKey(Client, on_delete=models.RESTRICT,
                               null=True, blank=True,verbose_name="Клиент")
    phone = models.CharField(max_length=20, null=True, blank=True,
                                    verbose_name="Номер телефона клиента")
    result = models.CharField(max_length=100,
                                   choices=MAILING_RESULT_CHOISES,
                                   default='Ожидает отправки')
    lid_id = models.ForeignKey(Lid, on_delete=models.SET_NULL,
                               null=True, blank=True,verbose_name="Связь с заявкой")
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Клиент в рассылке'
        verbose_name_plural = 'Клиенты в рассылках'

    def __str__(self):
        
        s = []
        s.append(f"{self.mailing.name} ({self.mailing.description}) ")
        if self.pdate:
            s.append(f"{self.pdate:%d.%m.%Y} ")
        s.append(f"{self.client} | ")
        if self.link_messeger:
            s.append(f"{self.link_messeger} - ")
        s.append(f"{self.result}")
        if self.comment:
            s.append(f"({self.comment})")
        return ''.join(s)

    
    @property
    def link_wa_pc(self):
        query = {
            'text': f"{self.outer_text}"
        }
        params = urllib.parse.urlencode(query)
        return f'https://web.whatsapp.com/send/?phone={self.phone}&{params}&type=phone_number&app_absent=0'
    
    @property
    def link_wa(self):
        query = {
            'text': f"{self.outer_text}"
        }
        params = urllib.parse.urlencode(query)
        return f"https://wa.me/{self.phone}?{params}"
    
    @property
    def link_vi(self):
        # https://viber.click/номертелефона
        # <a href="viber://chat?number=%2B79501476150">Viber</a>
        return f"viber://chat?number=%2B{self.phone}"
    
    @property
    def link_tg(self):
        # https://t.me/+79834631106
        # tg://resolve?domain=username
        return f"https://t.me/+{self.phone}"