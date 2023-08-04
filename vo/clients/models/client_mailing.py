from django.db import models
from django.contrib import admin

from .client import Client

class ClientMailing(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='mailing')
    viber_group = models.BooleanField(default=False, verbose_name="Группа в viber")
    tg_group = models.BooleanField(default=False, verbose_name="Группа в тг")
    wa_group = models.BooleanField(default=False, verbose_name="Группа в whatsapp")
    viber = models.BooleanField(default=False)
    tg = models.BooleanField(default=False, verbose_name="telegram")
    wa = models.BooleanField(default=False, verbose_name="whatsapp")
    sms = models.BooleanField(default=False,verbose_name="смс")
    call = models.BooleanField(default=False,verbose_name="Звонить")
    comment = models.TextField(null=True, blank=True,verbose_name="Примечания")
    
    class Meta:
        verbose_name = 'Кому, что и как рассылать'
        verbose_name_plural = 'Кому, что и как рассылать'
        db_table = 'client_mailing'

    def __str__(self):
        return (f" {self.client.family} " if self.client.family else ""
                f"{self.client.name} " if self.client.name else ""
                f"{self.comment}" if self.comment else "")
    
    @admin.display(description='В каких группах состоит:')
    def get_msg_groups(self):
        return (f"viber\n" if self.viber_group else f''
                f"whatsapp\n" if self.wa_group else f''
                f"telegram\n" if self.tg_group else f'')
    
    @admin.display(description='Способ связи (рассылка)')
    def get_messengers(self):
        return (f"viber\n" if self.viber else f''
                f"whatsapp\n" if self.wa else f''
                f"telegram\n" if self.tg else f''
                f"смс\n" if self.sms else f''
                f"Звонить\n" if self.call else f'')
    