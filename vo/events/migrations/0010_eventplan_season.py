# Generated by Django 4.0 on 2023-07-26 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_remove_eventplan_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventplan',
            name='season',
            field=models.CharField(default='2022/2023', max_length=100, verbose_name='Сезон'),
        ),
    ]
