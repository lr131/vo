# from django.db import models
# from django.conf import settings


# class UTMSource(models.Model):
#     social = models.CharField(max_length=200)
#     utm_source = models.CharField(max_length=200)
#     description = models.CharField(max_length=200, blank=True, null=True)

#     def __str__(self):
#         return self.social
    
#     class Meta:
#         verbose_name = 'UTMSource'
#         verbose_name_plural = 'Список UTMSource'
    
# class Medium(models.Model):
#     type_source = models.CharField(max_length=200)
#     utm_medium = models.CharField(max_length=200)
#     description = models.CharField(max_length=200, blank=True, null=True)
#     enable = models.BooleanField(default=True)

#     def __str__(self):
#         return self.utm_medium
    
#     class Meta:
#         verbose_name = 'UTMMedium'
#         verbose_name_plural = 'Метки UTMMedium'

# class SourceMailing(models.Model):
#     name = models.CharField(max_length=200)
#     social_place = models.ForeignKey(UTMSource, 
#                                      on_delete=models.RESTRICT, 
#                                      verbose_name="Соцсеть или месседжер")
#     utm_medium = models.ForeignKey(Medium, 
#                                    on_delete=models.RESTRICT, 
#                                    verbose_name="метка UTMMedium")
#     price = models.DecimalField(default=0, 
#                                 max_digits = 5,
#                                 decimal_places = 2,
#                                 verbose_name="Стоимость размещения")
#     description = models.CharField(max_length=2000, 
#                                    verbose_name="Короткое описание источника")
#     state = models.CharField(max_length=10,
#                             default='actual')

# class Mailing(models.Model):
#     name = models.CharField(max_length=100, 
#                             verbose_name="Название рассылки")
#     description = models.CharField(max_length=100, 
#                             verbose_name="Описание рассылки")
#     source_type = models.CharField(max_length=100,
#                                    default='group',
#                                    verbose_name="Тип рассылки")
#     date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
#     class Meta:
#         verbose_name = 'Список для рассылки'
#         verbose_name_plural = 'Список рассылок'

#     def __str__(self):
#         return f"{self.name}"


# class MailingDetail(models.Model):
#     mailing = models.ForeignKey(Mailing,
#                                 on_delete=models.CASCADE,
#                                 null=True, blank=True)
    
#     source = models.ForeignKey(SourceMailing, 
#                                on_delete=models.RESTRICT,
#                                null=True, blank=True,
#                                verbose_name="Источник указываем для групп")
#     text = models.TextField()
#     link = models.CharField(max_length=500, null=True, blank=True,
#                             verbose_name="Ссылка, если есть, без меток")
#     outer_text = models.TextField(verbose_name="Готовый текст, сформируется автоматичесик")
    
#     cdate = models.DateTimeField(auto_now_add=True)
#     cuser = models.ForeignKey(settings.AUTH_USER_MODEL, 
#                               on_delete=models.RESTRICT,
#                               related_name='smm_cuser')
    
#     mdate = models.DateTimeField(auto_now=True)
#     muser = models.ForeignKey(settings.AUTH_USER_MODEL, 
#                               on_delete=models.RESTRICT,
#                               related_name='smm_muser')
    
#     pdate = models.DateTimeField(verbose_name="Дата выполнения",
#                                  null=True, blank=True)
#     puser = models.ForeignKey(User, on_delete=models.RESTRICT, 
#                               null=True, blank=True,
#                               verbose_name="Кто выполнил",
#                               related_name='smm_puser')
    
#     link_messeger = models.TextField(null=True, blank=True,
#                                      verbose_name="Месседжер")
#     client = models.ForeignKey(Client, on_delete=models.RESTRICT,
#                                null=True, blank=True,verbose_name="Клиент")
#     phone = models.CharField(max_length=20, null=True, blank=True,
#                                     verbose_name="Номер телефона клиента")
#     result = models.CharField(max_length=100,
#                                    default='Ожидает отправки')
#     comment = models.TextField(null=True, blank=True)
    
#     class Meta:
#         verbose_name = 'Клиент в рассылке'
#         verbose_name_plural = 'Клиенты в рассылках'

#     def __str__(self):
#         return f"{self.phone}"