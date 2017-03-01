from django.shortcuts import render

from .models import *


def quizList(request, subject_id):
    subject = Subject.objects.get(code=subject_id)
    quizes = Quiz.objects.filter(subject=subject)
    context = {
        'subject': subject,
        'quizes': quizes
    }
    return render(request, 'quiz/quizList.html', context)


def quizHash(request, quiz_hash):
    context = {
        'quiz_hash': quiz_hash
    }
    return render(request, 'quiz/quiz.html', context)


def quizResult(request):
    return render(request, 'quiz/quizResult.html')


def subjects(request):
    context = {
        'subjects': Subject.objects.all()
    }

    return render(request, 'quiz/subjects.html', context)
