# Generated by Django 3.2.6 on 2021-08-21 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spammers', '0004_rename_emilfile_spammessage_emlfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='spammessage',
            name='state',
            field=models.CharField(choices=[('finished', 'finished'), ('queue', 'queue'), ('procesing', 'procesing'), ('todo', 'todo')], default='todo', max_length=16),
        ),
    ]
