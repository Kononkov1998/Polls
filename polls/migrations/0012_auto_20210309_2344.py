# Generated by Django 2.2.10 on 2021-03-09 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20210309_2341'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set(),
        ),
    ]