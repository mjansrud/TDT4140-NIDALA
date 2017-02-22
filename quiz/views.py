from django.shortcuts import render


def quizList(request):

    return render(request, 'nidala/quizList.html')

def quizID(request):
    return render(request, 'nidala/quiz.html')

def quizResult(request):
    return render(request, 'nidala/quizResult.html')

def subjects(request):
    return render(request, 'nidala/subjects.html')

