# Generated by Django 2.2.10 on 2021-03-09 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20210309_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
