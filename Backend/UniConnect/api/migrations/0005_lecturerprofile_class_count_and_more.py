# Generated by Django 5.1.4 on 2025-05-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_otp_profile_remove_studentprofile_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturerprofile',
            name='class_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='joined_class_count',
            field=models.IntegerField(default=0),
        ),
    ]
