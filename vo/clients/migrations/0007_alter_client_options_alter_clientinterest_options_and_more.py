# Generated by Django 4.0 on 2022-09-13 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_alter_clientinterest_client_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'База клиентов', 'verbose_name_plural': 'База клиентов'},
        ),
        migrations.AlterModelOptions(
            name='clientinterest',
            options={'verbose_name': 'Клиенты интересуются', 'verbose_name_plural': 'Клиенты интересуются'},
        ),
        migrations.AlterModelOptions(
            name='clientmailing',
            options={'verbose_name': 'Кому, что и как рассылать', 'verbose_name_plural': 'Кому, что и как рассылать'},
        ),
        migrations.AlterModelOptions(
            name='clientproducts',
            options={'verbose_name': 'Кто что прошел (основные продукты)', 'verbose_name_plural': 'Кто что прошел (основные продукты)'},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'verbose_name': 'Статус', 'verbose_name_plural': 'Статусы'},
        ),
        migrations.AlterField(
            model_name='client',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.state'),
        ),
    ]
