# Generated by Django 5.1.4 on 2025-06-06 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_studentprofile_instagram_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='bio',
            field=models.TextField(default='Bio loading… please wait.', max_length=200),
        ),
    ]
