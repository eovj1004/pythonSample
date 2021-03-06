# Generated by Django 2.2 on 2019-04-20 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_auto_20190418_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='content',
            field=models.CharField(max_length=5000),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('write_date', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=5000)),
                ('parent_id', models.IntegerField()),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.Board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.User')),
            ],
        ),
    ]
