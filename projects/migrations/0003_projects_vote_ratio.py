# Generated by Django 4.0.3 on 2022-06-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_tag_projects_vote_total_review_projects_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='vote_ratio',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
