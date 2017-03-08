from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField
from uuid import uuid4
from django.db.models import Q

#Constants
STATUS_QUESTION = settings.STATUS_QUESTION;
STATUS_ATTEMPT = settings.STATUS_ATTEMPT;

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

    syllabus = RichTextField()

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.code + ' - ' + self.title

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

    exercise_number = models.IntegerField(default=1)
    attempts = models.IntegerField(default=3)
    pass_percent = models.IntegerField(default=40)

    #Foreign relations
    subject = models.ForeignKey(Subject, related_name='subjectQuizes')


    def getRelevantQuestions(self, user, attempt):

        questions = Question.objects.filter(quiz=self)
        quizes = Quiz.objects.filter(subject=self.subject, exercise_number__lt=self.exercise_number)
        earlier_questions = Question.objects.filter(quiz__in=quizes)
        earlier_questions = earlier_questions.exclude(Q(questionAnswers__correct=True) & ~Q(questionAnswers__attempt = attempt))
        questions = questions | earlier_questions
        questions = questions.distinct().filter(Q(questionBoxes__isnull=False) | Q(questionTexts__isnull=False) | Q(questionCodes__isnull=False))

        return questions

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"

    def __str__(self):
        return self.title

class Question(models.Model):


    #Internal information
    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = RichTextField(
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

    order = models.IntegerField(default=0)
    attempts = models.IntegerField(default=3)

    #Used just for displaying which questions the user has correct
    status = models.IntegerField(default=STATUS_QUESTION.UNANSWERED, editable=False)

    # Foreign relations
    quiz = models.ForeignKey(Quiz, related_name='quizQuestions')

    def userAnsweredCorrectly(self, attempt):

        STATUS = STATUS_QUESTION.UNANSWERED

        # Check which questions the user has answered correct
        if (Answer.objects.filter(question=self, correct=True, user=attempt.user, attempt=attempt).count()):
            STATUS = STATUS_QUESTION.CORRECT
        elif(Answer.objects.filter(question=self, correct=False, user=attempt.user, attempt=attempt).count()):
            STATUS = STATUS_QUESTION.UNCORRECT

        return STATUS

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
    question = models.ForeignKey(Question, related_name='questionResources')

    # Functions
    def getResourcesByQuiz(self, quiz):
        questions = Question.filter(quiz=quiz);
        return self.filter(question__in=questions);

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self):
        return self.title

class Select(models.Model):

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True)

    correct = models.BooleanField(default=False)

    # Foreign relations
    question = models.ForeignKey(Question, related_name='questionBoxes')

    class Meta:
        verbose_name = "Alternative: Selects"
        verbose_name_plural = "Alternative: Selects"

    def __str__(self):
        return self.title

class Text(models.Model):

    answer = models.CharField(
        verbose_name="Answer",
        max_length=200)

    # Foreign relations
    question = models.ForeignKey(Question, related_name='questionTexts', unique=True)

    class Meta:
        verbose_name = "Alternative: Text"
        verbose_name_plural = "Alternative: Texts"

    def __str__(self):
        return self.answer

class Code(models.Model):

    LANGUAGE_CHOICES = (
        ("JAVASCRIPT", "Javascript"),
        ("JAVA", "Java"),
        ("PYTHON", "Python"),
    )

    language = models.CharField(max_length=9,
                                choices=LANGUAGE_CHOICES,
                                default="JAVASCRIPT")

    input_usable = models.CharField(
        max_length=3000,
        blank=True,
        null=True)

    input_shown = models.CharField(
        max_length=3000,
        blank=True,
        null=True)

    start_code = models.CharField(
        max_length=3000,
        blank=True,
        null=True)

    solution = models.CharField(
        max_length=3000,
        blank=True,
        null=True)

    answer = models.CharField(
        verbose_name="Answer",
        max_length=1000)

    # Foreign relationss
    question = models.ForeignKey(Question, related_name='questionCodes', unique=True)

    class Meta:
        verbose_name = "Alternative: Code"
        verbose_name_plural = "Alternative: Codes"

    def __str__(self):
        return self.answer

class Attempt(models.Model):

    # Internal information
    hash = models.CharField(
        verbose_name="Hash",
        max_length=8,
        unique=True,
        default=hash_generate,
        editable=False
    )

    # Foreign relations
    quiz = models.ForeignKey(Quiz, related_name='quizAttempts')
    user = models.ForeignKey(User, related_name='userAttempts')

    # Internal
    status = models.IntegerField(default=STATUS_ATTEMPT.STARTED)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attempt"
        verbose_name_plural = "Attempts"

    def __str__(self):
        return str(self.user.username + ' : ' + str(self.quiz.subject.code) + ' -> ' + str(self.quiz.title)  + ' -> Forsøk '+ str(self.hash))

class Answer(models.Model):

    # Foreign relations
    question = models.ForeignKey(Question, related_name='questionAnswers')
    attempt = models.ForeignKey(Attempt, related_name='attemptAnswers')
    user = models.ForeignKey(User, related_name='userAnswers')

    # Internal
    correct = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return str(self.user.username + ' : ' + str(self.question.quiz.subject.code) + ' -> ' + str(self.question.quiz.title) + ' -> ' + str(self.question.title) + ' -> Forsøk '+ str(self.attempt.hash) + ' -> Resultat ' + str(self.correct))




