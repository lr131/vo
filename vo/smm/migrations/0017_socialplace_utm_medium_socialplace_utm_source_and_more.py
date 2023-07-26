# Generated by Django 4.0 on 2023-07-26 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smm', '0016_remove_socialplace_utm_medium_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialplace',
            name='utm_medium',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.medium', verbose_name='utm_medium (Тип трафика)'),
        ),
        migrations.AddField(
            model_name='socialplace',
            name='utm_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.utmsource', verbose_name='utm_source (Соцсеть или месседжер)'),
        ),
        migrations.AddField(
            model_name='socialplace',
            name='utm_type_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.typesourceutm', verbose_name='utm_type_source (группа/страница/канал/чат/direct)'),
        ),
        migrations.AddField(
            model_name='sourcemailing',
            name='utm_campaing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.campaingutm', verbose_name='utm_campaing (Название кампании))'),
        ),
        migrations.AddField(
            model_name='sourcemailing',
            name='utm_medium',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.medium', verbose_name='utm_medium (Тип трафика)'),
        ),
        migrations.AddField(
            model_name='sourcemailing',
            name='utm_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.utmsource', verbose_name='utm_source (Соцсеть или месседжер)'),
        ),
        migrations.CreateModel(
            name='UTMs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utm_campaing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.campaingutm', verbose_name='utm_campaing (Название кампании))')),
                ('utm_medium', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.medium', verbose_name='utm_medium (Тип трафика)')),
                ('utm_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.utmsource', verbose_name='utm_source (Источник кампании)')),
                ('utm_type_content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.typecontentutm', verbose_name='utm_type_content (Тип контента)')),
                ('utm_type_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='smm.typesourceutm', verbose_name='utm_type_source (группа/страница/канал/чат/direct)')),
            ],
            options={
                'verbose_name': 'Готовый набор UTM меток',
                'verbose_name_plural': 'Готовый набор UTM меток',
                'db_table': 'smm_utms',
            },
        ),
    ]