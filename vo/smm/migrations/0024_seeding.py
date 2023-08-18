# Generated by Django 4.0 on 2023-08-14 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smm', '0023_linkout'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seeding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('сdate', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('summary', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Что публиковали (кратко)')),
                ('price', models.IntegerField(default=0, verbose_name='Стоимость размещения')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Условия размещения этого конкретного поста')),
                ('link', models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка на пост')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.eventplan', verbose_name='Какое мероприятие рекламируем')),
                ('link_out', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.linkout', verbose_name='Где разместили')),
            ],
            options={
                'verbose_name': 'Посев в сообществе',
                'verbose_name_plural': 'Посевы по сообществам и группам',
            },
        ),
    ]