# Generated by Django 5.2 on 2025-05-20 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0003_academicsession_alter_exam_academic_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='academic_year',
            field=models.CharField(max_length=10),
        ),
        migrations.DeleteModel(
            name='AcademicSession',
        ),
    ]
