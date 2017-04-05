from uuid import uuid4

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

# Constants
STATUS_QUESTION = settings.STATUS_QUESTION
STATUS_ATTEMPT = settings.STATUS_ATTEMPT

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
    # Internal information
    hash = models.CharField(
        verbose_name="Hash",
        max_length=10,
        unique=True,
        default=hash_generate,
        editable=False
    )

    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = RichTextField(
        blank=True,
        null=True)

    exercise_number = models.IntegerField(default=1)
    attempts = models.IntegerField(default=3)
    pass_percent = models.IntegerField(default=40)

    # Foreign relations
    subject = models.ForeignKey(Subject, related_name='subjectQuizes')

    def getRelevantQuestions(self, user, attempt):
        questions = Question.objects.filter(quiz=self).order_by('quiz__exercise_number', 'order')
        quizes = Quiz.objects.filter(subject=self.subject, exercise_number__lt=self.exercise_number)
        earlier_questions = Question.objects.filter(quiz__in=quizes)
        earlier_questions = earlier_questions.exclude(
            Q(questionAnswers__correct=True, questionAnswers__attempt__user = user) & ~Q(questionAnswers__attempt=attempt))
        questions = questions | earlier_questions

        #Add only if questions have alternatives
        #questions = questions.distinct().filter(
        #    Q(questionBoxes__isnull=False) | Q(questionTexts__isnull=False) | Q(questionCodes__isnull=False))

        return questions

    @staticmethod
    def setQuizStatus(quizes, user):
        for quiz in quizes:
            if Attempt.objects.filter(user=user, quiz__id=quiz.id, status=STATUS_ATTEMPT.PASSED).count() > 0:
                quiz.status = 'correct'
            elif Attempt.objects.filter(user=user, quiz__id=quiz.id,
                                        status=STATUS_ATTEMPT.FAILED).count() == quiz.attempts:
                quiz.status = 'uncorrect'
            else:
                quiz.status = 'started'

            if Attempt.objects.filter(user=user, quiz__id=quiz.id).count() < quiz.attempts:
                quiz.new_attempt = 'new-attempt'

    def hasFailedQuiz(self, user): 
        if Attempt.objects.filter(user=user, quiz=self, status=STATUS_ATTEMPT.PASSED).count() > 0:
            return False
        elif Attempt.objects.filter(user=user, quiz=self, status=STATUS_ATTEMPT.FAILED).count() == self.attempts:
            return True

    @staticmethod
    def getResources(quizes):
        for quiz in quizes:
            quiz.resources = Resource.objects.filter(question__quiz__id=quiz.id).distinct()

    @staticmethod
    def getAttempts(quizes, user):
        for quiz in quizes:
            quiz.attempts_list = [attempt for attempt in Attempt.objects.filter(user=user, quiz__id=quiz.id)]

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizes"

    def __str__(self):
        return self.title


class Question(models.Model):

    # Internal information
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
                            default="CHECKBOX",
                            verbose_name="Answer type")

    order = models.IntegerField(default=0)
    attempts = models.IntegerField(default=3)

    # Foreign relations
    quiz = models.ForeignKey(Quiz, related_name='quizQuestions')

    @staticmethod
    def setQuestionsStatus(questions, attempt):

        for question in questions:
            #Default
            question.status = 'unanswered'
            # Check which questions the user has answered correct
            if (Answer.objects.filter(question=question, correct=True, attempt__user=attempt.user, attempt=attempt).count()):
                question.status = 'correct'
            elif (Answer.objects.filter(question=question, correct=False, attempt__user=attempt.user, attempt=attempt).count()):
                question.status = 'uncorrect'

    def setNextQuestions(self, questions):

        #Attributes
        self.next = 0

        # Check which questions the user has answered correct
        for index, value in enumerate(questions):
            value.current = 'not-current'
            if value == self:
                value.current = 'current'
                if len(questions) - 1 > index:
                   self.next = Question.objects.get(id=questions[index + 1].id).id

    def setQuestionVariables(self, attempt):

        # Default
        self.finished = False
        self.status = 'unanswered'
        self.button = 'Svar'
        self.html = ''

        # Check how many attempts the user has tried
        self.user_attempts = Answer.objects.filter(question=self, attempt=attempt, attempt__user=attempt.user).count() + 1

        if self.user_attempts > self.attempts:
            self.finished = True
            self.button = 'Du har brukt for mange forsøk'
            self.html += ' class="disabled" disabled '
        # Check which questions the user has answered correct
        if (Answer.objects.filter(question=self, correct=True, attempt__user=attempt.user, attempt=attempt).count()):
            self.finished = True
            self.status = 'correct'
            self.button = 'Du har svart riktig'
            self.html += 'class="disabled" disabled '
        elif (Answer.objects.filter(question=self, correct=False, attempt__user=attempt.user, attempt=attempt).count()):
            self.status = 'uncorrect'

        #If attempt is passed / failed, show correct answers anyways
        if attempt.status != STATUS_ATTEMPT.STARTED:
            self.finished = True

        #If the user has answered correct or is out of attempts
        if self.finished:
            # Get answers based on type
            if self.type == "CODE":
                self.code = Code.objects.get(question=self).solution
            if self.type == "TEXT":
                self.html += ' value=' + Text.objects.get(question=self).answer

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.title


class Resource(models.Model):
    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = RichTextField(
        blank=True,
        null=True)

    url = models.CharField(
        verbose_name="URL",
        max_length=400,
        blank=True,
        null=True)

    # Foreign relations
    question = models.ForeignKey(Question, related_name='questionResources')

    # Functions
    def getResourcesByQuiz(self, quiz):
        questions = Question.filter(quiz=quiz)
        return self.filter(question__in=questions)

    @staticmethod
    def getResourcesByResult(questions, user):
        return Resource.objects.distinct().filter(question__in=questions, question__questionAnswers__correct=False, question__questionAnswers__attempt__user=user)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def __str__(self):
        return self.title


class Select(models.Model):
    title = models.CharField(
        verbose_name="Title",
        max_length=60)

    description = RichTextField(
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
    question = models.ForeignKey(Question, related_name='questionTexts')

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
    question = models.ForeignKey(Question, related_name='questionCodes')

    class Meta:
        verbose_name = "Alternative: Code"
        verbose_name_plural = "Alternative: Codes"

    def __str__(self):
        return self.answer


class Attempt(models.Model):
    # Internal information
    hash = models.CharField(
        verbose_name="Hash", 
        max_length=10,
        unique=True,
        default=hash_generate,
        editable=False
    )

    # Foreign relations
    quiz = models.ForeignKey(Quiz, related_name='quizAttempts')
    user = models.ForeignKey(User, related_name='userAttempts')

    TYPE_CHOICES = [
        (STATUS_ATTEMPT.STARTED, 'Started'),
        (STATUS_ATTEMPT.PASSED, 'Passed'),
        (STATUS_ATTEMPT.FAILED, 'Failed'),
    ]

    # Internal
    status = models.IntegerField(default=STATUS_ATTEMPT.STARTED, choices=TYPE_CHOICES)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attempt"
        verbose_name_plural = "Attempts"

    def __str__(self):
        return str(self.user.username + ' -> Forsøk ' + str(self.hash))


class Answer(models.Model):
    # Foreign relations
    question = models.ForeignKey(Question, related_name='questionAnswers')
    attempt = models.ForeignKey(Attempt, related_name='attemptAnswers')

    # Internal
    correct = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return str('Resultat ' + str(self.correct))


