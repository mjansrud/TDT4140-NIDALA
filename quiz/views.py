from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *


@login_required
def quizList(request, subject_id):
    subject = Subject.objects.get(code=subject_id)
    quizes = Quiz.objects.filter(subject=subject)
    context = {
        'subject': subject,
        'quizes': quizes
    }

    return render(request, 'quiz/quizList.html', context)


@login_required
def quizID(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    context = {
        'quiz': quiz
    }
    return render(request, 'quiz/quiz.html', context)


@login_required
def quizResult(request):
    return render(request, 'quiz/quizResult.html')


@login_required
def subjects(request):
    context = {
        'subjects': Subject.objects.all()
    }

    return render(request, 'quiz/subjects.html', context)
