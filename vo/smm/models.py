from cgitb import enable, text
from datetime import datetime
from os import link
from tabnanny import verbose    
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from .const import MAILING_SOURCE_TYPES, MAILING_RESULT_CHOISES, SOURCE_MAILING_STATE
import uuid


class AuthData(models.Model):
    social = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    phone_own = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.social
    
    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'

# Это вид контента: информационный, развлекательный, анонс и тд
class ContentType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Тип контента'
        verbose_name_plural = 'Типы контента'
        db_table = 'content_type'

    def __str__(self):
        return self.name

# Все наши места, где мы размещаемся
class SocialPlace(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=150, null=True, blank=True)
    social = models.CharField(max_length=20)
    class Meta:
        verbose_name = 'Место размещения (соцсеть)'
        verbose_name_plural = 'Места размещения (соцсети)'
        db_table = 'social_place'

    def __str__(self):
        return self.name
  
# где размещаем: сторис, посты, рилс, клипы
class ContentPlace(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Способ размещения контента'
        verbose_name_plural = 'Способы размещения контента'
        db_table = 'content_place'

    def __str__(self):
        return self.name

# Видео, аудио, текст
class ContentFormat(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Вид контента'
        verbose_name_plural = 'Виды контента'
        db_table = 'content_format'

    def __str__(self):
        return self.name

# Стаьтя, лонгрид, короткий пост, картинка, карусель, кружочек, голосовое, подкаст и тд?
class ContentForm(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Формат контента'
        verbose_name_plural = 'Форматы контента'
        db_table = 'content_form'

    def __str__(self):
        return self.name
       
# Цель поста: повысить охват, ещё что-нибудь такое 
class Target(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Цель поста'
        verbose_name_plural = 'Цели поста'
        db_table = 'target'

    def __str__(self):
        return self.name

# рубрика
class Rubric(models.Model):
    name = models.CharField(max_length=300)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        db_table = 'rubric'

    def __str__(self):
        return self.name
    
      
class UTMSource(models.Model):
    social = models.CharField(max_length=200)
    utm_source = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.social
    
    class Meta:
        verbose_name = 'UTMSource'
        verbose_name_plural = 'Список UTMSource'
    
class Medium(models.Model):
    type_source = models.CharField(max_length=200)
    utm_medium = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.utm_medium
    
    class Meta:
        verbose_name = 'UTMMedium'
        verbose_name_plural = 'Метки UTMMedium'
    
class Links(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True) # Дата создания ссылки
    link = models.CharField(max_length=200) # длинная ссылка
    short = models.CharField(max_length=200, blank=True, null=True) # сокращенная ссылка
    source = models.CharField(max_length=200) # источник
    utm_source = models.CharField(max_length=200)
    utm_medium = models.CharField(max_length=200, blank=True, null=True)
    utm_campaign = models.CharField(max_length=200, blank=True, null=True)
    utm_content = models.CharField(max_length=200, blank=True, null=True)
    utm_term = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Готовые ссылки'
        verbose_name_plural = 'Готовые ссылки'
        
    def __str__(self):
        return self.link
    
    


class PostType(models.Model):
    post_type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=800, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Тип поста'
        verbose_name_plural = 'Типы постов'
        
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        verbose_name = 'Теги к постам (для внутр.использования!!)'
        verbose_name_plural = 'Теги к постам (для внутр.использования!!)'
        
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name 

    
class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата создания поста")
    create_user = models.CharField(max_length=200, blank=True, null=True) # TODO поменять тип
    modify_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Дата редактирования поста")
    modify_user = models.CharField(max_length=200, blank=True, null=True, verbose_name="Кто редактировал пост") # TODO поменять тип
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.CharField(max_length=800, blank=True, null=True, verbose_name="Кратко - о чем")
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Тип поста") # TODO проверить тип
    description = models.CharField(max_length=800, blank=True, null=True, verbose_name="Описание")
    text = models.TextField(max_length=4800, blank=True, null=True, verbose_name="Пост")
    attachments = models.CharField(max_length=200, blank=True, null=True, verbose_name="Вложения") # TODO поменять тип
    performer = models.ManyToManyField(User, blank=True, verbose_name="Исполнитель(-и)")
    target_fk = models.ForeignKey(Target, db_column='target_fk', on_delete=models.SET_NULL,  null=True, verbose_name="Цель поста")
    rubric_fk = models.ForeignKey(Rubric, db_column='rubric_fk', on_delete=models.SET_NULL,  null=True, verbose_name="Рубрика")
    content_place_fk = models.ForeignKey(ContentPlace, db_column='content_place_fk', on_delete=models.CASCADE, verbose_name="Где размещать")
    content_form_fk = models.ForeignKey(ContentForm, db_column='content_form_fk', on_delete=models.CASCADE,verbose_name="Формат контента")
    content_format_fk = models.ForeignKey(ContentFormat, db_column='content_format_fk', on_delete=models.CASCADE, verbose_name="Вид контента")
    content_type_fk = models.ForeignKey(ContentType, db_column='content_type_fk', on_delete=models.CASCADE, default=1, verbose_name="Тип контента")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    
    class Meta:
        verbose_name = 'База постов'
        verbose_name_plural = 'База постов'
    
    def __str__(self):
        return self.name


class PostPlan(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост") # TODO проверить тип
    source = models.ForeignKey(Medium, on_delete=models.CASCADE, verbose_name="Метка utm_source места публикации") # TODO проверить тип и указать, что это - место публикации
    pub_date = models.DateTimeField(blank=True, null=True, verbose_name="Когда опубликовать") 
    deadline_date = models.DateTimeField(null=True, blank=True, verbose_name="Крайний срок, дедлайн")
    disable_date = models.DateTimeField(blank=True, null=True, verbose_name="дата отмены поста") # дата отмены поста 
    state = models.CharField(max_length=200, blank=True, null=True, verbose_name="Стадия поста") # Состояние: в работе, опубликован, не опубликован, перенесен
    reasons = models.CharField(max_length=200, blank=True, null=True, verbose_name="Причина отмены публикации") # Причина отмены публикации
    is_published = models.BooleanField(default=False, verbose_name="Пост опубликован")
    link = models.TextField(blank=True, null=True, verbose_name="Ссылка на пост")
    
    class Meta:
        verbose_name = 'Контент-план'
        verbose_name_plural = 'Контент-план'


class SourceMailing(models.Model):
    name = models.CharField(max_length=200)
    social_place = models.ForeignKey(UTMSource, 
                                     on_delete=models.RESTRICT, 
                                     verbose_name="Соцсеть или месседжер")
    utm_medium = models.ForeignKey(Medium, 
                                   on_delete=models.RESTRICT, 
                                   verbose_name="метка UTMMedium")
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
        return f"{self.name} ({self.social_place})"


class Mailing(models.Model):
    name = models.CharField(max_length=100, 
                            verbose_name="Название рассылки")
    description = models.CharField(max_length=100, 
                            verbose_name="Описание рассылки")
    source_type = models.CharField(max_length=100,
                                   choices=MAILING_SOURCE_TYPES,
                                   default='group',
                                   verbose_name="Тип рассылки")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = 'Список для рассылки'
        verbose_name_plural = 'Список рассылок'

    def __str__(self):
        return f"{self.name}"
    
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
    outer_text = models.TextField(verbose_name="Готовый текст, сформируется автоматичесик")
    
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
    client_id = models.IntegerField(null=True, blank=True,
                                    verbose_name="Клиент")
    phone = models.CharField(max_length=20, null=True, blank=True,
                                    verbose_name="Номер телефона клиента")
    result = models.CharField(max_length=100,
                                   choices=MAILING_RESULT_CHOISES,
                                   default='Ожидает отправки')
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Клиент в рассылке'
        verbose_name_plural = 'Клиенты в рассылках'

    def __str__(self):
        return f"{self.phone}"