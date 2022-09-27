# Generated by Django 4.0 on 2022-09-13 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_eventplan_start_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Мероприятие', 'verbose_name_plural': 'Список имеющихся мероприятий'},
        ),
        migrations.AlterModelOptions(
            name='eventplan',
            options={'verbose_name': 'План мероприятий', 'verbose_name_plural': 'План мероприятий'},
        ),
        migrations.AlterModelOptions(
            name='eventstate',
            options={'verbose_name': 'Справочник состояний мероприятий', 'verbose_name_plural': 'Справочник состояний мероприятий'},
        ),
        migrations.AlterModelOptions(
            name='eventtype',
            options={'verbose_name': 'Справочник типов мероприятий', 'verbose_name_plural': 'Справочник типов мероприятий'},
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'Место', 'verbose_name_plural': 'Места проведения'},
        ),
    ]
