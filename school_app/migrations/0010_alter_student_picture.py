# Generated by Django 5.2 on 2025-05-29 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0009_alter_calendar_options_calendar_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='media/students'),
        ),
    ]
