# Generated by Django 5.1.1 on 2024-10-09 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDoApp', '0006_task_archived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='archived',
        ),
        migrations.AddField(
            model_name='task',
            name='color_status',
            field=models.CharField(default='none', max_length=10),
        ),
    ]
