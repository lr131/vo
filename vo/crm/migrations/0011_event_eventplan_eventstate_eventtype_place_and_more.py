# Generated by Django 4.0 on 2023-08-02 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_previouslist_event_id_previouslist_event_plan_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('short', models.CharField(blank=True, max_length=500, null=True, verbose_name='Короткое описание (до 500 знаков)')),
                ('payment', models.CharField(blank=True, max_length=200, null=True, verbose_name='Стоимость')),
                ('continuance', models.CharField(blank=True, max_length=200, null=True, verbose_name='Продолжительность')),
                ('about', models.TextField(blank=True, null=True, verbose_name='Какие боли закрывает?')),
                ('country', models.IntegerField(default=5, verbose_name='Сколько человек по плану')),
                ('next_step', models.TextField(blank=True, null=True, verbose_name='Следующий шаг по продуктам')),
                ('prev_step', models.TextField(blank=True, null=True, verbose_name='Предыдущий шаг по продуктам')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('site', models.CharField(blank=True, max_length=500, null=True, verbose_name='Ссылка на лендинг')),
            ],
            options={
                'db_table': 'events_event',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EventPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(blank=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('season', models.CharField(max_length=100)),
                ('is_period', models.BooleanField(default=False)),
                ('site', models.CharField(blank=True, max_length=500, null=True)),
                ('period', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'event_plan',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EventState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Статус')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник состояний мероприятий',
                'verbose_name_plural': 'Справочник состояний мероприятий',
                'db_table': 'event_state',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Тип мероприятия')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание')),
            ],
            options={
                'db_table': 'event_types',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес')),
                ('source', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название')),
            ],
            options={
                'db_table': 'events_place',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='previouslist',
            name='event_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Мероприятие без даты'),
        ),
        migrations.AlterField(
            model_name='previouslist',
            name='event_plan_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Мероприятие с известной датой'),
        ),
    ]