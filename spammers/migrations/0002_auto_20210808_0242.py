# Generated by Django 3.2.6 on 2021-08-08 05:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spammers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spamip',
            name='release_date',
        ),
        migrations.RemoveField(
            model_name='spammessage',
            name='release_date',
        ),
        migrations.AddField(
            model_name='spamip',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='spamip',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='spammessage',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='spammessage',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
