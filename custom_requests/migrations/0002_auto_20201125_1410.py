# Generated by Django 3.1.3 on 2020-11-25 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_requests', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userroles',
            old_name='role',
            new_name='role_name',
        ),
    ]