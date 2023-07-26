# Generated by Django 4.0 on 2023-07-26 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_webhook'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhook',
            name='cdate',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата добавления'),
        ),
        migrations.AddField(
            model_name='webhook',
            name='formid',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ID формы Тильды'),
        ),
        migrations.AddField(
            model_name='webhook',
            name='formname',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Форма Тильды'),
        ),
        migrations.AddField(
            model_name='webhook',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='webhook',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='webhook',
            name='tranid',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='№ заявки'),
        ),
    ]