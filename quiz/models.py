from django.db import models


# Create your models here.
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
    hash = models.CharField(
        verbose_name="Hash",
        max_length=8,
        blank=True,
        null=True)

    subject = models.ForeignKey(Subject, related_name='quizes')

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"
