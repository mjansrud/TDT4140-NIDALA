# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-05 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0026_auto_20170304_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='input',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
