# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-11-02 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='\u6807\u9898')),
                ('desc', models.TextField(verbose_name='\u63cf\u8ff0')),
                ('url', models.CharField(max_length=512, verbose_name='\u94fe\u63a5')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('finish', models.IntegerField(default=0, verbose_name='\u8f6c\u8f7d\u72b6\u6001')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u5fae\u4fe1\u5728\u7ebf\u6587\u7ae0',
            },
        ),
    ]
