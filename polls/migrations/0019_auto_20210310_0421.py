# Generated by Django 2.2.10 on 2021-03-09 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20210310_0409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='user',
        ),
        migrations.AddField(
            model_name='useranswer',
            name='poll',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
            preserve_default=False,
        ),
    ]
