# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-11-09 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20171102_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='pub_time',
            field=models.DateField(blank=True, default=b'2017-11-09'),
        ),
    ]
