# Generated by Django 4.0 on 2023-02-24 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_alter_task_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='dead_line',
            field=models.DateTimeField(null=True, verbose_name='Крайний срок (дедлайн)'),
        ),
        migrations.AlterField(
            model_name='task',
            name='red_line',
            field=models.DateTimeField(null=True, verbose_name='Срок, к какому выполнить (редлайн)'),
        ),
    ]
