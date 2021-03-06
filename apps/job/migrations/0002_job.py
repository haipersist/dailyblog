# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-21 12:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u804c\u4f4d\u540d\u79f0')),
                ('welfare', models.CharField(blank=True, max_length=255, verbose_name='\u798f\u5229')),
                ('requirement', models.TextField(blank=True, verbose_name='\u804c\u4f4d\u8981\u6c42')),
                ('link', models.CharField(max_length=255, verbose_name='\u94fe\u63a5')),
                ('pub_time', models.DateField(blank=True, default=b'2017-09-21')),
                ('load_time', models.DateTimeField(auto_now=True)),
                ('salary', models.CharField(blank=True, max_length=127, verbose_name='\u85aa\u8d44')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Company', verbose_name='\u516c\u53f8')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Website', verbose_name='\u62db\u8058\u7f51\u7ad9')),
            ],
            options={
                'verbose_name': '\u804c\u4f4d',
            },
        ),
    ]
