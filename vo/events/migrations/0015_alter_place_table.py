# Generated by Django 4.0 on 2023-08-14 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_alter_eventplan_period'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='place',
            table='events_place',
        ),
    ]