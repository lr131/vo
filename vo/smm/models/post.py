from django.db import models
from django.contrib.auth.models import User
import uuid

from .post_type import PostType
from .target import Target
from .rubric import Rubric
from .content_type import ContentType
from .content_place import ContentPlace
from .content_format import ContentFormat
from .content_form import ContentForm
from .tag import Tag

    
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
        return self.short_content