# Generated by Django 4.0.3 on 2022-06-27 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_projects_featured_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Projects',
            new_name='Project',
        ),
    ]
