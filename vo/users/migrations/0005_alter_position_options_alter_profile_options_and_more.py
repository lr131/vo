# Generated by Django 4.0 on 2022-09-10 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profileposition_end_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={'verbose_name': 'Должности'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профили'},
        ),
        migrations.AlterModelOptions(
            name='profileposition',
            options={'verbose_name': 'Профиль-должность'},
        ),
    ]
