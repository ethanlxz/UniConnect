# Generated by Django 5.1.4 on 2025-05-20 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classing', '0004_class_max_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Class',
            name='max_students',
            field=models.PositiveIntegerField(),
        ),
    ]
