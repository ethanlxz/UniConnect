# Generated by Django 5.1.4 on 2025-06-21 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_studentprofile_instagram_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturerprofile',
            name='profile_image',
            field=models.ImageField(default='lecturer_profile_image/default.jpg', upload_to='lecturer_profile_image/'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='profile_image',
            field=models.ImageField(default='student_profile_image/default.jpg', upload_to='student_profile_image/'),
        ),
    ]
