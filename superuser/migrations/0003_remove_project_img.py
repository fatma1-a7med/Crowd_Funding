# Generated by Django 5.0.4 on 2024-04-21 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0002_project_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='img',
        ),
    ]