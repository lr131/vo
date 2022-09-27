import profile
from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название должности")
    instruction = models.CharField(max_length=500, 
                                   blank=True, 
                                   null=True,
                                   verbose_name="Должностные обязательства",
                                   help_text="Ссылка на инструкцию к должности")
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = "Должности"
        
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    birthday = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    regalia = models.CharField(max_length=1500, blank=True, null=True, verbose_name="Регалии и звания")

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = "Профили"
        
    def __str__(self):
        return f'{self.user.username} Profile'
    
class ProfilePosition(models.Model):
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата начала работы")
    end_date = models.DateTimeField(blank=True, null=True,verbose_name="Дата окончания работы")
    profile = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, blank=True, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = 'Кто какую занимает должность'
        verbose_name_plural = 'Кто какую занимает должность'
        db_table = 'profile_position'
        
    def __str__(self):
        return f'{self.profile.user.first_name} {self.profile.user.last_name} - {self.position.name}'