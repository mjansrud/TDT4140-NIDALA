# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_auto_20170301_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='correct',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]