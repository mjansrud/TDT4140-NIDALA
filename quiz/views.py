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
def quiz(request, quiz_hash, quiz_question):

    #Fetch from database
    quiz = Quiz.objects.get(hash=quiz_hash)
    question = Question.objects.get(id=quiz_question)
    questions = Question.objects.filter(quiz=quiz)


    #For each question
    alternative_boxes = Select.objects.filter(question=question.id)
    alternative_text = Text.objects.filter(question=question.id)
    alternative_code = Code.objects.filter(question=question.id)

    context = {
        'quiz': quiz,
        'question': question,
        'questions': questions,
        'alternative_boxes': alternative_boxes,
        'alternative_text': alternative_text,
        'alternative_code': alternative_code,
    }

    if(request.method == "POST"):

        # Defined variables
        user_answered = True
        user_current_answer_correct = True
        user_current_answers = request.POST.getlist('answer')

        if question.type == 'CHECKBOX':

            if(len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:

                # Convert to integers to use built in features
                user_current_answers = list(map(int, user_current_answers))

                for alternative in alternative_boxes:
                     if (alternative.correct == True and alternative.id not in user_current_answers) or (alternative.correct == False and alternative.id in user_current_answers):
                         user_current_answer_correct = False

        if question.type == 'RADIOBOX':

            if(len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:
                for alternative in alternative_boxes:
                    if alternative.correct == True and alternative.id != int(user_current_answers[0]):
                        user_current_answer_correct = False

        if question.type == 'TEXT':

            if (len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:
                if alternative_text.first().answer != user_current_answers[0]:
                    user_current_answer_correct = False

        if question.type == 'CODE':

            if (len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:
                if alternative_code.first().answer != user_current_answers[0]:
                    user_current_answer_correct = False

        #Attach new variables
        context['user_answered'] = user_answered
        context['user_current_answers'] = user_current_answers
        context['user_current_answer_correct'] = user_current_answer_correct

        #Register that the user has answered a question
        Answer.objects.create(question=question, user=request.user, correct=user_current_answer_correct)

    # Get users answers only for this specific quiz
    user_quiz_answers = Answer.objects.filter(question__in=questions, user=request.user)

    # Check which questions the user has answered correct
    for user_quiz_answer in user_quiz_answers:
        for temp_question in questions:
            if user_quiz_answer.question.id == temp_question.id:
                if user_quiz_answer.correct:
                    temp_question.status = 1
                else:
                    temp_question.status = 2

    context['user_quiz_answers'] = user_quiz_answers

    return render(request, 'quiz/quiz.html', context)

@login_required
def quizResult(request, quiz_hash):
    return render(request, 'quiz/quizResult.html')

@login_required
def subjects(request):
    context = {
        'subjects': Subject.objects.all()
    }

    return render(request, 'quiz/subjects.html', context)
