# Generated by Django 4.0 on 2022-11-21 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('smm', '0005_alter_mailing_options_mailing_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'verbose_name': 'Рассылка', 'verbose_name_plural': 'Список рассылок'},
        ),
        migrations.AlterField(
            model_name='mailingdetail',
            name='cuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='smm_cuser', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='mailingdetail',
            name='muser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='smm_muser', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='mailingdetail',
            name='puser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='smm_puser', to='auth.user', verbose_name='Кто выполнил'),
        ),
    ]
