# Generated by Django 4.0 on 2023-07-28 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_lid_utm_content_lid_utm_type_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='state',
            field=models.BooleanField(default=False, verbose_name='Завершены все этапы'),
        ),
    ]