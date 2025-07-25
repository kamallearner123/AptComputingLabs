# Generated by Django 5.1.7 on 2025-07-23 12:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectModel",
            fields=[
                ("project_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "phase",
                    models.CharField(
                        choices=[
                            ("Initiation", "Initiation"),
                            ("Planning", "Planning"),
                            ("Execution", "Execution"),
                            ("Monitoring", "Monitoring"),
                            ("Closure", "Closure"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "risk",
                    models.CharField(
                        choices=[
                            ("Low", "Low"),
                            ("Medium", "Medium"),
                            ("High", "High"),
                            ("Critical", "Critical"),
                        ],
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "hours",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("working_people", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="WorkTaskModel",
            fields=[
                ("task_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Not Started", "Not Started"),
                            ("In Progress", "In Progress"),
                            ("Completed", "Completed"),
                            ("On Hold", "On Hold"),
                        ],
                        max_length=50,
                    ),
                ),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "assigned_to",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="projects.projectmodel",
                    ),
                ),
            ],
        ),
    ]
