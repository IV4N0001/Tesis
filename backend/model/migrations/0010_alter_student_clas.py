# Generated by Django 5.0.4 on 2024-05-04 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0009_rename_study_frecuency_student_study_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='clas',
            field=models.ManyToManyField(blank=True, related_name='students', to='model.class'),
        ),
    ]
