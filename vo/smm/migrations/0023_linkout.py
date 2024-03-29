# Generated by Django 4.0 on 2023-08-14 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smm', '0022_alter_mailingdetail_result_alter_place_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания ссылки')),
                ('link', models.CharField(max_length=500, verbose_name='Ссылка на источник')),
                ('name', models.CharField(max_length=500, verbose_name='Наименование источника')),
                ('contact', models.CharField(max_length=1000, verbose_name='Контакт для размещения')),
                ('conditions', models.TextField(verbose_name='Условия размещения')),
                ('conditions_date', models.DateTimeField(auto_now_add=True, verbose_name='Обновили условия размещения')),
                ('topic', models.CharField(blank=True, max_length=100, null=True, verbose_name='Тематика')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Город/Регион')),
                ('views', models.IntegerField(blank=True, null=True, verbose_name='Просмотров')),
                ('views_date', models.DateTimeField(auto_now_add=True, verbose_name='Обновили показатели просмотров')),
                ('reach', models.IntegerField(blank=True, null=True, verbose_name='Охват')),
                ('reach_date', models.DateTimeField(auto_now_add=True, verbose_name='Обновили показатели охвата')),
                ('followers', models.IntegerField(blank=True, null=True, verbose_name='Подписчиков')),
                ('followers_date', models.DateTimeField(auto_now_add=True, verbose_name='Обновили показатели охвата')),
                ('actual', models.BooleanField(default=True, verbose_name='Используемый источник')),
                ('note', models.CharField(max_length=2000, verbose_name='Короткий комметарий, если нужно')),
                ('utm_medium', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.medium', verbose_name='utm_medium (метка трафика)')),
                ('utm_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.utmsource', verbose_name='utm_source (метка источника)')),
            ],
            options={
                'verbose_name': 'Внешняя ссылка для размещения',
                'verbose_name_plural': 'Внешние источники размещения',
            },
        ),
    ]
