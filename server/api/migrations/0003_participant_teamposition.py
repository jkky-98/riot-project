# Generated by Django 4.2.7 on 2024-03-13 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_participant_participant_puuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='teamPosition',
            field=models.CharField(default='', max_length=1000),
        ),
    ]