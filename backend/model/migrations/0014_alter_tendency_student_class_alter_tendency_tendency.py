# Generated by Django 5.0.4 on 2024-05-28 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0013_tendency_student_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tendency',
            name='student_class',
            field=models.CharField(default='1-01', max_length=16),
        ),
        migrations.AlterField(
            model_name='tendency',
            name='tendency',
            field=models.CharField(default='1-01', max_length=16),
        ),
    ]
