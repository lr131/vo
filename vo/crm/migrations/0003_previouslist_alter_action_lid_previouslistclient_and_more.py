# Generated by Django 4.0 on 2022-11-22 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('crm', '0002_clienteventhistory_alter_lid_options_remove_lid_note_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreviousList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Назывние')),
                ('description', models.CharField(blank=True, max_length=512, null=True, verbose_name='Описание')),
                ('cuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user', verbose_name='Кто создал список')),
            ],
        ),
        migrations.AlterField(
            model_name='action',
            name='lid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lid_actions', to='crm.lid', verbose_name='Лид заявки'),
        ),
        migrations.CreateModel(
            name='PreviousListClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.IntegerField()),
                ('cdate', models.DateTimeField(auto_now_add=True)),
                ('cuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user', verbose_name='Кто добавил клиента в список')),
                ('prev_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.previouslist')),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='plc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='crm.previouslistclient', verbose_name='Клиент из списка'),
        ),
    ]
