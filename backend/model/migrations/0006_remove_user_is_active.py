# Generated by Django 5.0.4 on 2024-04-18 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0005_user_is_active_user_last_login_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
    ]
