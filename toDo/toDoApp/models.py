from django.db import models
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Urgent', 'Urgent'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('To do', 'To do'),
        ('In progress', 'In progress'),
        ('Finished', 'Finished'),
    ]

    TEAM_CHOICES = [
        ('Roel', 'Roel'),
        ('Harry', 'Harry'),
    ]

    name = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    effort = models.IntegerField()
    progress = models.IntegerField(default=0)
    team = models.CharField(max_length=10, choices=TEAM_CHOICES, default='Roel')  # New team field
    finished_date = models.DateField(null=True, blank=True)  # New finished date field
    color_status = models.CharField(max_length=10, default='none')  # Field to store the task color

    def __str__(self):
        return self.name
