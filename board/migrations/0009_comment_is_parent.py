# Generated by Django 2.2 on 2019-04-22 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_auto_20190420_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_parent',
            field=models.BooleanField(default=False),
        ),
    ]
