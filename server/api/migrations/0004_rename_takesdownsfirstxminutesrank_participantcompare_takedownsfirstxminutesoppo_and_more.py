# Generated by Django 4.2.7 on 2024-03-18 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_participantcompare'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participantcompare',
            old_name='takesdownsFirstXMinutesRank',
            new_name='takedownsFirstXMinutesOppo',
        ),
        migrations.RenameField(
            model_name='participantcompare',
            old_name='takesdownsFirstXMinutesOppo',
            new_name='takedownsFirstXMinutesRank',
        ),
    ]
