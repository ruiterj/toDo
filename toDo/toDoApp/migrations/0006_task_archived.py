# Generated by Django 5.1.1 on 2024-10-08 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toDoApp', '0005_task_finished_date_task_team_alter_task_effort_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
