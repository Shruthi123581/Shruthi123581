# Generated by Django 3.2.9 on 2023-05-18 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagement_app', '0018_auto_20230517_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='document',
            field=models.FileField(default=1, upload_to='documents/'),
            preserve_default=False,
        ),
    ]
