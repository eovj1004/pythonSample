# Generated by Django 2.2 on 2019-04-12 02:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20190411_0752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pw',
            new_name='password',
        ),
    ]
