# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-27 08:25
from __future__ import unicode_literals

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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avator', models.ImageField(blank=True, upload_to='userimg')),
                ('age', models.IntegerField(blank=True, default=0, null=True)),
                ('school', models.CharField(blank=True, max_length=48)),
                ('gender', models.CharField(choices=[('\u5973', 'girl'), ('\u7537', 'boy')], default='\u7537', max_length=10)),
                ('hobby', models.CharField(blank=True, max_length=255)),
                ('motto', models.CharField(blank=True, max_length=255)),
                ('self_introduction', models.TextField(blank=True)),
                ('birthday', models.DateField(blank=True, default='2000-01-01', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
