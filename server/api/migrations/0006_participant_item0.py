# Generated by Django 4.2.7 on 2024-03-26 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_participant_item1_participant_item2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='item0',
            field=models.IntegerField(default=0),
        ),
    ]
