# Generated by Django 5.0.4 on 2024-04-14 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_rename_project_donation_project_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='value',
            new_name='rate',
        ),
    ]
