# Generated by Django 3.2.9 on 2023-05-19 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagement_app', '0019_task_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='document',
        ),
    ]
