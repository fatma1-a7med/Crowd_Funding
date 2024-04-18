# Generated by Django 5.0.4 on 2024-04-17 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('projects', '0014_comment_is_reported_project_is_reported'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allprojects', to='categories.category'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]