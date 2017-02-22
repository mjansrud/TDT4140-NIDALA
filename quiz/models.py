from django.db import models


# Create your models here.
class Subject(models.Model):

    code = models.CharField(
        verbose_name="Subject",
        max_length=7,
        unique=True)

    title = models.CharField(
        verbose_name="Title",
        max_length=100)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

class Quiz(models.Model):

    hash = models.CharField(
        verbose_name="Hash",
        max_length=8,
        unique=True)

    subject = models.ForeignKey(
        'Subject'
    )

    title = models.CharField(
        verbose_name="Title",
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name="Description",
        blank=True, help_text="a description of the quiz")

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"
