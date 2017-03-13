# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-05 15:11
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0028_auto_20170305_1536'),
    ]

    operations = [
        migrations.RenameField(
            model_name='code',
            old_name='input',
            new_name='input_shown',
        ),
        migrations.AddField(
            model_name='code',
            name='input_usable',
            field=models.CharField(default=1, max_length=3000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]