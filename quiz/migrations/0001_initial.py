# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-18 11:20
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import quiz.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(default=quiz.models.hash_generate, editable=False, max_length=10, unique=True, verbose_name='Hash')),
                ('status', models.IntegerField(choices=[(0, 'Started'), (1, 'Passed'), (2, 'Failed')], default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Attempt',
                'verbose_name_plural': 'Attempts',
            },
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('JAVASCRIPT', 'Javascript'), ('JAVA', 'Java'), ('PYTHON', 'Python')], default='JAVASCRIPT', max_length=9)),
                ('input_usable', models.CharField(blank=True, max_length=3000, null=True)),
                ('input_shown', models.CharField(blank=True, max_length=3000, null=True)),
                ('start_code', models.CharField(blank=True, max_length=3000, null=True)),
                ('solution', models.CharField(blank=True, max_length=3000, null=True)),
                ('answer', models.CharField(max_length=1000, verbose_name='Answer')),
            ],
            options={
                'verbose_name': 'Alternative: Code',
                'verbose_name_plural': 'Alternative: Codes',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('CHECKBOX', 'Checkbox'), ('RADIOBOX', 'Radiobox'), ('TEXT', 'Text'), ('CODE', 'Code')], default='CHECKBOX', max_length=9)),
                ('order', models.IntegerField(default=0)),
                ('attempts', models.IntegerField(default=3)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(default=quiz.models.hash_generate, editable=False, max_length=10, unique=True, verbose_name='Hash')),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('exercise_number', models.IntegerField(default=1)),
                ('attempts', models.IntegerField(default=3)),
                ('pass_percent', models.IntegerField(default=40)),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=400, null=True, verbose_name='URL')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionResources', to='quiz.Question')),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
            },
        ),
        migrations.CreateModel(
            name='Select',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionBoxes', to='quiz.Question')),
            ],
            options={
                'verbose_name': 'Alternative: Selects',
                'verbose_name_plural': 'Alternative: Selects',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=7, unique=True, verbose_name='Subject')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('syllabus', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200, verbose_name='Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionTexts', to='quiz.Question')),
            ],
            options={
                'verbose_name': 'Alternative: Text',
                'verbose_name_plural': 'Alternative: Texts',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjectQuizes', to='quiz.Subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizQuestions', to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='code',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionCodes', to='quiz.Question'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizAttempts', to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userAttempts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attemptAnswers', to='quiz.Attempt'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionAnswers', to='quiz.Question'),
        ),
    ]
