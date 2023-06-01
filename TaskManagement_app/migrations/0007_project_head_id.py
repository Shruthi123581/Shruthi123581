# Generated by Django 3.0.7 on 2023-05-14 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManagement_app', '0006_remove_project_head_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='head_id',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
