# Generated by Django 5.1.4 on 2025-05-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturerprofile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
