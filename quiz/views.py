from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import *

#Constants
STATUS_QUESTION = settings.STATUS_QUESTION;
STATUS_ATTEMPT = settings.STATUS_ATTEMPT;

#URL functions
@login_required
def quizList(request, subject_id):

    subject = Subject.objects.get(code=subject_id)
    quizes = Quiz.objects.distinct().filter(Q(subject=subject) & Q(quizQuestions__isnull  = False) & (Q(quizQuestions__questionBoxes__isnull=False) | Q(quizQuestions__questionTexts__isnull=False) | Q(quizQuestions__questionCodes__isnull=False)))
    questions = Question.objects.distinct().filter(quiz__in=quizes)
    resources = Resource.objects.distinct().filter(question__in=questions)
    attempts = Attempt.objects.filter(user=request.user)

    context = {
        'subject': subject,
        'quizes': quizes,
        'attempts': attempts,
        'questions': questions,
        'resources': resources,
        'STATUS_ATTEMPT': STATUS_ATTEMPT,
    }

    return render(request, 'quiz/quizList.html', context)


@login_required
def quizFindQuestion(request, quiz_hash, attempt_hash):

    quiz = Quiz.objects.filter(hash=quiz_hash)
    attempt = Attempt.objects.filter(hash=attempt_hash)
    question = Question.objects.filter(quiz=quiz).order_by('order').first()
    answers = Answer.objects.filter(attempt=attempt, user=request.user)

    if(answers.count() > 0):
        return redirect('quiz', quiz_hash, attempt_hash, answers.last().question.id)

    return redirect('quiz', quiz_hash, attempt_hash, question.id)


@login_required
def quizRequestAttempt(request, quiz_hash):

    #Fetch from database
    quiz = Quiz.objects.get(hash=quiz_hash)
    attempts = Attempt.objects.filter(quiz=quiz, user=request.user)

    if attempts.count() <= quiz.attempts - 1:

        question = Question.objects.filter(quiz=quiz).order_by('order').first()

        #Register that the user has answered a question
        Attempt.objects.create(quiz=quiz, user=request.user)
        return redirect('quiz', quiz_hash, Attempt.objects.latest('id').hash, question.id)

    #Find quiz
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def quiz(request, quiz_hash, attempt_hash, quiz_question):

    #Fetch from database
    quiz = Quiz.objects.get(hash=quiz_hash)
    quizes = Quiz.objects.filter(subject=quiz.subject, exercise_number__lte=quiz.exercise_number)
    question = Question.objects.get(id=quiz_question)
    attempt = Attempt.objects.get(quiz=quiz, hash=attempt_hash, user=request.user)
    questions = quiz.getRelevantQuestions(request.user, attempt)
    answers = Answer.objects.filter(question__in=questions, user=request.user)
    resources = Resource.objects.filter(question=question)

    context = {
        'quiz': quiz,
        'quizes': quizes,
        'question': question,
        'questions': questions,
        'resources': resources,
        'attempt': attempt,
        'answers': answers,
        'STATUS_QUESTION': STATUS_QUESTION,
    }

    #For each question
    if question.type == 'CHECKBOX' or question.type == 'RADIOBOX':
        alternative_boxes = Select.objects.filter(question=question.id)
        context['alternative_boxes'] = alternative_boxes
    elif question.type == 'TEXT':
        alternative_text = Text.objects.filter(question=question.id).first()
        context['alternative_text'] = alternative_text
    elif question.type == 'CODE':
        alternative_code = Code.objects.filter(question=question.id).first()
        context['alternative_code'] = alternative_code

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
                if alternative_text.answer != user_current_answers[0]:
                    user_current_answer_correct = False

        if question.type == 'CODE':

            if (len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:
                if alternative_code.answer != user_current_answers[0]:
                    user_current_answer_correct = False

        #Attach new variables
        context['user_answered'] = user_answered
        context['user_current_answers'] = user_current_answers
        context['user_current_answer_correct'] = user_current_answer_correct

        #Register that the user has answered a question
        if answers.filter(question=question).count() + 1 <= question.attempts:
            Answer.objects.create(attempt=attempt, question=question, correct=user_current_answer_correct, user=request.user)

    return render(request, 'quiz/quiz.html', context)

@login_required
def quizResult(request, quiz_hash, attempt_hash):


    #Fetch from database
    quiz = Quiz.objects.get(hash=quiz_hash)
    quizes = Quiz.objects.filter(subject=quiz.subject, exercise_number__lte=quiz.exercise_number)
    attempt = Attempt.objects.get(hash=attempt_hash)
    questions = quiz.getRelevantQuestions(request.user,attempt)
    answers = Answer.objects.filter(question__in=questions, attempt=attempt, user=request.user)
    resources = Resource.objects.distinct().filter(question__in=questions)

    correct = 0
    for question in questions:
        for answer in answers:
            if question == answer.question:
                if answer.correct:
                    correct = correct + 1

    correct_percent = round(correct/len(questions) * 100,1);

    #Add a grade to the students attempt
    grade = 'F';
    if correct_percent >= 88:
        grade = 'A';
    elif correct_percent >= 76:
        grade = 'B';
    elif correct_percent >= 64:
        grade = 'C';
    elif correct_percent >= 52:
        grade = 'D';
    elif correct_percent > quiz.pass_percent:
        grade = 'E';

    #Update the database
    if(grade != 'F'):
        attempt.status = STATUS_ATTEMPT.PASSED
    else:
        attempt.status = STATUS_ATTEMPT.FAILED
    attempt.save()

    context = {
        'quiz': quiz,
        'questions': questions,
        'attempt': attempt,
        'answers': answers,
        'resources': resources,
        'correct': correct,
        'correct_percent': correct_percent,
        'grade': grade,
        'STATUS_QUESTION': STATUS_QUESTION,
    }


    return render(request, 'quiz/quizResult.html', context)

@login_required
def subjects(request):

    subjects = Subject.objects.distinct().filter(Q(subjectQuizes__isnull  = False) & Q(subjectQuizes__quizQuestions__isnull = False) & (Q(subjectQuizes__quizQuestions__questionBoxes__isnull = False) | Q(subjectQuizes__quizQuestions__questionTexts__isnull = False) | Q(subjectQuizes__quizQuestions__questionCodes__isnull = False)))

    context = {
        'subjects': subjects
    }

    return render(request, 'quiz/subjects.html', context)
