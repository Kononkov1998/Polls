# Generated by Django 2.2.10 on 2021-03-09 14:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_auto_20210309_2103'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userquestion',
            unique_together={('user', 'question')},
        ),
    ]
