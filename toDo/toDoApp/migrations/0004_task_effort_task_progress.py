# Generated by Django 5.1.1 on 2024-10-07 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDoApp', '0003_alter_task_priority_alter_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='effort',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='progress',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
