# Generated by Django 2.2.10 on 2021-03-09 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20210309_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
