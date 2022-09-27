# Generated by Django 4.0 on 2022-09-10 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_clientinterest_comment_clientmailing_call_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'База клиентов'},
        ),
        migrations.AlterModelOptions(
            name='clientinterest',
            options={'verbose_name': 'Клиенты интересуются'},
        ),
        migrations.AlterModelOptions(
            name='clientmailing',
            options={'verbose_name': 'Кому, что и как рассылать'},
        ),
        migrations.AlterModelOptions(
            name='clientproducts',
            options={'verbose_name': 'Кто что прошел (основные продукты)'},
        ),
        migrations.AlterModelOptions(
            name='state',
            options={'verbose_name': 'Статусы'},
        ),
        migrations.AlterField(
            model_name='client',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clientinterest',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='clientinterest',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='clientinterest',
            name='event',
            field=models.IntegerField(blank=True, null=True, verbose_name='Мероприятия'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='call',
            field=models.BooleanField(default=False, verbose_name='Звонить'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='sms',
            field=models.BooleanField(default=False, verbose_name='смс'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='tg',
            field=models.BooleanField(default=False, verbose_name='telegram'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='tg_group',
            field=models.BooleanField(default=False, verbose_name='Группа в тг'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='viber_group',
            field=models.BooleanField(default=False, verbose_name='Группа в viber'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='wa',
            field=models.BooleanField(default=False, verbose_name='whatsapp'),
        ),
        migrations.AlterField(
            model_name='clientmailing',
            name='wa_group',
            field=models.BooleanField(default=False, verbose_name='Группа в whatsapp'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='course_candidate',
            field=models.TextField(blank=True, null=True, verbose_name='Кандидаты на курс'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='future_assisting',
            field=models.BooleanField(default=True, verbose_name='Хочет на ассистирование'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='is_assisting',
            field=models.BooleanField(default=False, verbose_name='Клиент ассистировал'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='is_base_course',
            field=models.BooleanField(default=False, verbose_name='Курсовой'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='is_school_level_1',
            field=models.BooleanField(default=False, verbose_name='Выпускник ИШ1'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='is_school_level_2',
            field=models.BooleanField(default=False, verbose_name='Выпускник ИШ2'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='is_school_level_3',
            field=models.BooleanField(default=False, verbose_name='Выпускник ИШ3'),
        ),
        migrations.AlterField(
            model_name='clientproducts',
            name='tg',
            field=models.BooleanField(default=False, verbose_name='Выпускник терапевтической группы'),
        ),
    ]
