from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from post_office import mail

from .models import *

# Constants
STATUS_QUESTION = settings.STATUS_QUESTION
STATUS_ATTEMPT = settings.STATUS_ATTEMPT


# URL functions
@login_required
def quizList(request, subject_id):
    subject = get_object_or_404(Subject, code=subject_id)
    quizes = [quiz for quiz in Quiz.objects.filter(subject=subject)]

    Quiz.setQuizStatus(quizes, request.user)
    Quiz.getResources(quizes)
    Quiz.getAttempts(quizes, request.user)

    context = {
        'subject': subject,
        'quizes': quizes,
        'STATUS_ATTEMPT': STATUS_ATTEMPT,
    }

    return render(request, 'quiz/quizList.html', context)


@login_required
def quizFindQuestion(request, quiz_hash, attempt_hash):
    quiz = get_object_or_404(Quiz, hash=quiz_hash)
    attempt = get_object_or_404(Attempt, hash=attempt_hash, user=request.user)
    question = Question.objects.filter(quiz=quiz).order_by('order').first()
    answers = Answer.objects.filter(attempt=attempt, attempt__user=request.user)

    if (answers.count() > 0):
        return redirect('quiz', quiz_hash, attempt_hash, answers.last().question.id)

    return redirect('quiz', quiz_hash, attempt_hash, question.id)


@login_required
def quizRequestAttempt(request, quiz_hash):
    # Fetch from database
    quiz = get_object_or_404(Quiz, hash=quiz_hash)
    attempts = Attempt.objects.filter(quiz=quiz, user=request.user)

    if attempts.count() <= quiz.attempts - 1:
        question = Question.objects.filter(quiz=quiz).order_by('order').first()

        # Register that the user has answered a question
        Attempt.objects.create(quiz=quiz, user=request.user)
        return redirect('quiz', quiz_hash, Attempt.objects.latest('id').hash, question.id)

    # Find quiz
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def quiz(request, quiz_hash, attempt_hash, quiz_question):

    # Fetch from database
    quiz = get_object_or_404(Quiz, hash=quiz_hash)
    quizes = Quiz.objects.filter(subject=quiz.subject, exercise_number__lte=quiz.exercise_number)
    question = get_object_or_404(Question, id=quiz_question)
    attempt = get_object_or_404(Attempt, hash=attempt_hash, user=request.user)
    questions = [question for question in quiz.getRelevantQuestions(request.user, attempt)]
    resources = Resource.objects.filter(question=question)

    if (attempt.status != STATUS_ATTEMPT.STARTED):
        return redirect('quizResult', quiz_hash, attempt_hash)

    context = {
        'quiz': quiz,
        'quizes': quizes,
        'questions': questions,
        'resources': resources,
        'attempt': attempt,
        'STATUS_QUESTION': STATUS_QUESTION,
    }

    # For each question
    if question.type == 'CHECKBOX' or question.type == 'RADIOBOX':
        question.alternatives = Select.objects.filter(question=question.id)
    elif question.type == 'TEXT':
        question.alternative = get_object_or_404(Text, question=question.id)
    elif question.type == 'CODE':
        question.alternative = get_object_or_404(Code, question=question.id)

    #Check if a user has answered a question
    if (request.method == "POST"):

        # Defined variables
        user_answered = True
        user_current_answer_correct = True
        user_current_answers = request.POST.getlist('answer')

        if question.type == 'CHECKBOX':

            if (len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:

                # Convert to integers to use built in features
                user_current_answers = list(map(int, user_current_answers))

                for alternative in question.alternatives:
                    if (alternative.correct == True and alternative.id not in user_current_answers) or (
                                alternative.correct == False and alternative.id in user_current_answers):
                        user_current_answer_correct = False

        if question.type == 'RADIOBOX':

            if (len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:
                for alternative in question.alternatives:
                    if alternative.correct == True and alternative.id != int(user_current_answers[0]):
                        user_current_answer_correct = False

        if question.type == 'TEXT':

            if (len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:
                if question.alternative.answer != user_current_answers[0]:
                    user_current_answer_correct = False

        if question.type == 'CODE':

            if (len(user_current_answers) == 0):
                user_current_answer_correct = False
            else:
                if question.alternative.answer != user_current_answers[0]:
                    user_current_answer_correct = False

        # Attach new variables
        context['user_answered'] = user_answered
        context['user_current_answers'] = user_current_answers
        context['user_current_answer_correct'] = user_current_answer_correct

        # Register that the user has answered a question
        if Answer.objects.filter(question=question, attempt=attempt,
                                 attempt__user=request.user).count() + 1 <= question.attempts:
            Answer.objects.create(attempt=attempt, question=question, correct=user_current_answer_correct)

    # Run functions
    Question.setQuestionsStatus(questions, attempt)
    question.setQuestionVariables(attempt)
    question.setNextQuestions(questions)

    #Attach last variables after manipulation
    context['question'] = question

    return render(request, 'quiz/quiz.html', context)


@login_required
def quizResult(request, quiz_hash, attempt_hash):

    # Fetch from database
    quiz = get_object_or_404(Quiz, hash=quiz_hash)
    attempt = get_object_or_404(Attempt, hash=attempt_hash, user=request.user)
    questions = [question for question in quiz.getRelevantQuestions(request.user, attempt)]
    answers = Answer.objects.filter(question__in=questions, attempt=attempt, attempt__user=request.user)

    # Run update functions
    Question.setQuestionsStatus(questions, attempt)

    # Get resources for questions answered wrong.
    resources = Resource.getResourcesByResult(questions, request.user)

    # Count the number of questions the user has answered correct
    attempt.correct_count = 0
    for question in questions:
        for answer in answers:
            if question == answer.question and answer.correct:
                attempt.correct_count = attempt.correct_count + 1

    attempt.correct_percent = round(attempt.correct_count / len(questions) * 100, 1)

    # Add a grade to the students attempt
    attempt.grade = 'F'
    if attempt.correct_percent >= 88:
        attempt.grade = 'A'
    elif attempt.correct_percent >= 76:
        attempt.grade = 'B'
    elif attempt.correct_percent >= 64:
        attempt.grade = 'C'
    elif attempt.correct_percent >= 52:
        attempt.grade = 'D'
    elif attempt.correct_percent > quiz.pass_percent:
        attempt.grade = 'E'

    # Update the database
    if (attempt.grade != 'F'):
        attempt.status = STATUS_ATTEMPT.PASSED
        attempt.image = 'images/passed.png'
    else:
        attempt.status = STATUS_ATTEMPT.FAILED
        attempt.image = 'images/failed.png'

    attempt.save()

    if (quiz.hasFailedQuiz(request.user)):
        mail.send(
            'forelesere@nidala.no',  # List of email addresses also accepted
            'post@nidala.no',
            subject=request.user.username + ' is failing in ' + quiz.subject.code + "!",
            message='We have detected that the student has failed an attempt on a quiz in your class',
            html_message='We have detected that the student has failed an attempt on a quiz in your class',
        )

    context = {
        'quiz': quiz,
        'questions': questions,
        'attempt': attempt,
        'resources': resources,
    }

    return render(request, 'quiz/quizResult.html', context)


@login_required
def subjects(request):
    subjects = Subject.objects.all()

    context = {
        'subjects': subjects
    }

    return render(request, 'quiz/subjects.html', context)


@login_required
def quiz_admin(request):
    if not request.user.is_staff:
        raise Http404
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects
    }
    return render(request, 'quiz/quizAdmin.html', context)


@login_required
def quiz_admin_subject(request, subject_code):
    if not request.user.is_staff:
        raise Http404
    subject = get_object_or_404(Subject, code=subject_code)
    quizes = list(Quiz.objects.filter(subject=subject).prefetch_related('quizAttempts'))
    for quiz in quizes:
        quiz.attempts_count = quiz.quizAttempts.count()
        quiz.attempts_passed_count = quiz.quizAttempts.filter(status=STATUS_ATTEMPT.PASSED).count()

    users = list(User.objects.all())
    failing_users = []
    for user in users:
        passed_quizes = 0
        for quiz in quizes:

            if quiz.quizAttempts.filter(user=user, status=STATUS_ATTEMPT.PASSED).count() > 0:
                passed_quizes += 1
        user.attempts = user.userAttempts.filter(quiz__in=quizes).count()
        user.passed_quizes = passed_quizes
        if user.attempts:
            user.attempt_grade = (user.passed_quizes / user.attempts) * 100
        else:
            user.attempt_grade = 0.0
        failing_users.append(user)

    failing_users.sort(key=lambda x: x.attempt_grade)

    context = {
        'subject': subject,
        'quizes': quizes,
        'failing_users': failing_users,
    }

    return render(request, 'quiz/quizAdminSubject.html', context)


@login_required
def quiz_admin_quiz(request, quiz_hash):
    if not request.user.is_staff:
        raise Http404
    quiz = get_object_or_404(Quiz, hash=quiz_hash)
    questions = list(Question.objects.filter(quiz=quiz).prefetch_related('questionAnswers'))
    for question in questions:
        question.answer_count = Answer.objects.filter(question=question).count()
        question.correct_count = Answer.objects.filter(question=question, correct=True).count()
        if question.answer_count:
            question.correct_grade = (question.correct_count / question.answer_count) * 100
        else:
            question.correct_grade = 0.0
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz/quizAdminQuiz.html', context)
