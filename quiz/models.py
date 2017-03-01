from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Creates unique URLS
def hash_generate():
    return uuid4().hex[:10]

# Subjects like TDT
class Subject(models.Model):

    code = models.CharField(
        verbose_name="Subject",
        max_length=7,
        unique=True)

    title = models.CharField(
        verbose_name="Title",
        max_length=100,
        blank=True,
        null=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.code

class Quiz(models.Model):

    #Internal information
    hash = models.CharField(
        verbose_name="Hash",
        max_length=8,
        unique=True,
        default=hash_generate,
        editable=False
    )

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True)

    #Foreign relations
    subject = models.ForeignKey(Subject, related_name='quizes')

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"

    def __str__(self):
        return self.title

class Question(models.Model):

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True)

    TYPE_CHOICES = (
        ("CHECKBOX", "Checkbox"),
        ("RADIOBOX", "Radiobox"),
        ("TEXT", "Text"),
        ("CODE", "Code"),
    )

    type = models.CharField(max_length=9,
                  choices=TYPE_CHOICES,
                  default="CHECKBOX")

    # Foreign relations
    quiz = models.ForeignKey(Quiz, related_name='questions')

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.title

class Resource(models.Model):

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True)

    url = models.TextField(
        verbose_name="URL",
        blank=True,
        null=True)

    # Foreign relations
    question = models.ForeignKey(Question, related_name='resources')

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self):
        return self.title

class Alternative(models.Model):

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True)

    # Foreign relations
    question = models.ForeignKey(Question, related_name='alternatives')

    class Meta:
        verbose_name = "Alternative"
        verbose_name_plural = "Alternatives"

    def __str__(self):
        return self.title

class Checkbox(models.Model):

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    correct = models.BooleanField

    # Foreign relations
    alternative = models.ForeignKey(Alternative, related_name='checkboxes')

    class Meta:
        verbose_name = "Checkbox"
        verbose_name_plural = "checkboxes"

    def __str__(self):
        return self.title


class Radiobox(models.Model):

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    correct = models.BooleanField

    # Foreign relations
    alternative = models.ForeignKey(Alternative, related_name='radioboxes')

    class Meta:
        verbose_name = "Radiobox"
        verbose_name_plural = "Radioboxes"

    def __str__(self):
        return self.title

class Text(models.Model):

    answer = models.CharField(
        verbose_name="Answer",
        max_length=200)

    # Foreign relations
    alternative = models.ForeignKey(Alternative, related_name='texts')

    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"

class Code(models.Model):

    answer = models.CharField(
        verbose_name="Answer",
        max_length=1000)

    # Foreign relations
    alternative = models.ForeignKey(Alternative, related_name='codes')

    class Meta:
        verbose_name = "Code"
        verbose_name_plural = "Codes"

class Answer(models.Model):

    correct = models.BooleanField

    # Foreign relations
    question = models.ForeignKey(Question, related_name='answers')
    user = models.ForeignKey(User, related_name='answers')

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"




