# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-09-17 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('\u5973', 'girl'), ('\u7537', 'boy')], default='\u7537', max_length=10),
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='user_profile',
        ),
    ]
