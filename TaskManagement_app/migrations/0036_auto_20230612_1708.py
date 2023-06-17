# Generated by Django 3.2.9 on 2023-06-12 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagement_app', '0035_auto_20230612_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamhead',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='teammem',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
    ]
