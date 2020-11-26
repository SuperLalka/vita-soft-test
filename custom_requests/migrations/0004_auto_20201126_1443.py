# Generated by Django 3.1.3 on 2020-11-26 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_requests', '0003_auto_20201125_1935'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AssignedRoles',
        ),
        migrations.RemoveField(
            model_name='extendinguser',
            name='roles',
        ),
        migrations.AddField(
            model_name='extendinguser',
            name='roles',
            field=models.ManyToManyField(to='custom_requests.UserRoles'),
        ),
    ]
