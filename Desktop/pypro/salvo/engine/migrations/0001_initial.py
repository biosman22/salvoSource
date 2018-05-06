# Generated by Django 2.0.1 on 2018-05-06 01:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='downloaded',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=200)),
                ('content_type', models.CharField(max_length=50)),
                ('up_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('task_id', models.CharField(max_length=200)),
                ('unique_id', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='video_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('unique_id', models.CharField(max_length=20)),
                ('duration', models.IntegerField()),
                ('img_url', models.CharField(max_length=60)),
                ('uploader', models.CharField(max_length=60)),
                ('view_count', models.BigIntegerField()),
                ('up_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('counts', models.IntegerField(default=1)),
                ('average_rating', models.FloatField()),
                ('num', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-counts', '-up_date'],
            },
        ),
    ]