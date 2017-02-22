from django.shortcuts import render
def index(request):

    return render(request, 'nidala/quiz.html')
