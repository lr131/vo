from django.db import models
from django.contrib import admin

class State(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = "Статусы"
        db_table = 'client_state'

    def __str__(self):
        return self.name
    
class Client(models.Model):
    family = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=250, null=True)
    patr = models.CharField(max_length=250, null=True, blank=True)
    birthday = models.DateTimeField(blank=True, null=True)
    city = models.CharField(max_length=250, null=True)
    phone = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    in_black_list = models.BooleanField(default=False)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True) # заметки, дополнительно

    class Meta:
        verbose_name = 'База клиентов'
        verbose_name_plural = 'База клиентов'
        
    def __str__(self):
        return f"{self.family} {self.name} ({self.city})"
    
    @admin.display(description='Статус')
    def get_state(self):
        return self.state
    
    @admin.display(description='Телефон')
    def get_phone(self):
        return self.phone
    
    @admin.display(description='Город')
    def get_city(self):
        return self.city
    
    @admin.display(description='ФИО')
    def get_abbr_fio(self):
        return f"{self.family} {self.name} {self.patr if self.patr else ''}"
    
    @admin.display(description='Примечания')
    def get_notes(self):
        return f"{self.comment if self.comment else ''}\n{self.note if self.note else ''}"
    
class ClientProducts(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='products')
    is_assisting = models.BooleanField(default=False,verbose_name="Клиент ассистировал") # Клиент уже ассистировал на БК
    future_assisting = models.BooleanField(default=True, verbose_name="Хочет на ассистирование") # клиент хочет на будущие ассистирования
    is_base_course = models.BooleanField(default=False,verbose_name="Курсовой")
    course_candidate = models.TextField(null=True, blank=True,verbose_name="Кандидаты на курс")
    is_school_level_1 = models.BooleanField(default=False,verbose_name="Выпускник ИШ1")
    is_school_level_2 = models.BooleanField(default=False,verbose_name="Выпускник ИШ2")
    is_school_level_3 = models.BooleanField(default=False, verbose_name="Выпускник ИШ3")
    tg = models.BooleanField(default=False,verbose_name="Выпускник терапевтической группы") # Клиент проходил терапевтическую группу
    
    class Meta:
        verbose_name = 'Кто что прошел (основные продукты)'
        verbose_name_plural = 'Кто что прошел (основные продукты)'
        db_table = 'client_products'
    
    def __str__(self):
        return (f" {self.client.family} " if self.client.family else ""
                f"{self.client.name} " if self.client.name else ""
                f"{self.course_candidate}" if self.course_candidate else "")
    
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
    
class ClientInterest(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               verbose_name="Клиент", related_name='interest')
    event = models.IntegerField(null=True, blank=True,verbose_name="Мероприятия")
    comment = models.TextField(null=True, blank=True,verbose_name="Примечания")

    class Meta:
        verbose_name = 'Клиенты интересуются'
        verbose_name_plural = 'Клиенты интересуются'
        db_table = 'client_interest'

    def __str__(self):
        return f"{self.comment}" if self.comment else f''
