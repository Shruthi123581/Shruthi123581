# Generated by Django 3.2.9 on 2023-05-22 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagement_app', '0025_auto_20230521_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_price',
        ),
        migrations.AddField(
            model_name='task',
            name='task_status',
            field=models.CharField(blank=True, choices=[('1', 'New'), ('2', 'Active'), ('3', 'Completed')], max_length=200, null=True),
        ),
    ]
