# Generated by Django 4.0 on 2022-09-10 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_alter_client_city_alter_client_family_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientinterest',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clientmailing',
            name='call',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clientmailing',
            name='sms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clientmailing',
            name='tg',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clientmailing',
            name='viber',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clientmailing',
            name='wa',
            field=models.BooleanField(default=False),
        ),
    ]
