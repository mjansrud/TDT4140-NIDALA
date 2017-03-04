from django import template
from django.conf import settings
register = template.Library()

#Constants
STATUS_QUESTION = settings.STATUS_QUESTION;
STATUS_ATTEMPT = settings.STATUS_ATTEMPT;

#custom filters
@register.filter
def filterAnswersByQuestion(answers, question):
    return answers.filter(question=question).count() + 1

@register.filter
def filterQuestionsByQuiz(questions, quiz):
    return questions.filter(quiz=quiz);

@register.filter
def filterResourcesByQuiz(resources, questions):
    return resources.filter(question__in=questions);

@register.filter
def filterAttemptsByQuizCount(attempts, quiz):
    return attempts.filter(quiz=quiz).count();

@register.filter
def filterAttemptsHasPassedQuiz(attempts, quiz):

    passed = False
    attempts = attempts.filter(quiz=quiz)

    for attempt in attempts:
        if attempt.status == STATUS_ATTEMPT.PASSED:
            passed = True

    return passed;

@register.filter
def filterResourcesCount(resources, questions):
    return resources.filter(question__in=questions).count();

@register.filter
def filterAnswersGetStatus(answers, question):

    STATUS = STATUS_QUESTION.UNANSWERED

    # Check which questions the user has answered correct
    for answer in answers:
            if answer.question == question:
                if answer.correct:
                    return STATUS_QUESTION.CORRECT
                else:
                    STATUS = STATUS_QUESTION.UNCORRECT
    return STATUS

@register.filter
def filterQuestionsFetchNext(questions, question):

    # Check which questions the user has answered correct
    for index, value in enumerate(questions):
        if value == question:
            if len(questions) - 1 > index:
                return questions.filter(id=list(questions.values_list('id', flat=True))[index + 1]).first().id;

    return False
