# Generated by Django 4.0.3 on 2022-07-09 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_message_unreadcount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='unreadCount',
        ),
    ]
