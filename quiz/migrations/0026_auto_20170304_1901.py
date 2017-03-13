# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-04 18:01
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0025_subject_syllabus'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='pass_percent',
            field=models.IntegerField(default=40),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='subject',
            name='syllabus',
            field=ckeditor.fields.RichTextField(),
        ),
    ]