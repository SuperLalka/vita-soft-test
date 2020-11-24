# Generated by Django 3.1.3 on 2020-11-24 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='Enter the text of your application', max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('drf', 'draft'), ('snt', 'sent'), ('acc', 'accepted'), ('rej', 'rejected')], default='drf', editable=False, help_text='Select requests status', max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User request',
                'verbose_name_plural': 'User requests',
                'ordering': ['creation_date'],
            },
        ),
        migrations.CreateModel(
            name='ExtendingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_user', models.BooleanField(default=True, help_text='Select to assign user as ordinary user')),
                ('is_operator', models.BooleanField(default=False, help_text='Select to assign user as operator')),
                ('is_admin', models.BooleanField(default=False, help_text='Select to assign user as admin')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extending User info',
                'verbose_name_plural': 'Extending User info',
                'ordering': ['user'],
            },
        ),
    ]