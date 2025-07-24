from django.db import models
from django.urls import path
from accounts.models import EmployeeModel



# Create work task for the project model
class WorkTaskModel(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey('ProjectModel', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey('accounts.EmployeeModel', on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    status = models.CharField(max_length=50, choices=[
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ])
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class ProjectModel(models.Model):
    PHASE_CHOICES = [
        ('Initiation', 'Initiation'),
        ('Planning', 'Planning'),
        ('Execution', 'Execution'),
        ('Monitoring', 'Monitoring'),
        ('Closure', 'Closure'),
    ]

    RISK_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES)
    risk = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    working_people = models.ManyToManyField('accounts.EmployeeModel')
    notes = models.TextField(blank=True, null=True)
    hours = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
