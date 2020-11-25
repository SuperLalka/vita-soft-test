# Generated by Django 3.1.3 on 2020-11-25 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_requests', '0002_auto_20201125_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='status',
            field=models.CharField(choices=[('drf', 'draft'), ('snt', 'sent'), ('acc', 'accepted'), ('rej', 'rejected')], default='drf', help_text='Select requests status', max_length=20),
        ),
    ]