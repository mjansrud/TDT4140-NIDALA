from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from quiz.models import *


class QuizesTestCase(TestCase):
    fixtures = ['data.json', ]
    def setUp(self):
        self.user = User.objects.get(username='test')
        #self.url = reverse('quizList', )
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_quiz_list_view(self):
        subject = Subject.objects.first()
        url = reverse('quizList', args=[subject.code])
        response = self.client.get(url)
        response_subject = response.context[-1]['subject']
        self.assertEqual(subject, response_subject, 'Checks that the requested subject matches the one in response')


    def test_subjects_view(self):
        subjects = Subject.objects.all().count()
        url = reverse('subjects')
        response = self.client.get(url)
        response_subjects = response.context[-1]['subjects'].count()
        self.assertEqual(subjects, response_subjects, 'Checks subjects list')

    def test_quiz_request_attempt_view(self):
        quiz = Quiz.objects.first()
        url = reverse('quizRequestAttempt', args=[quiz.hash])
        response = self.client.get(url)
        self.assertEqual(302, response.status_code) # Redirect

    def test_quiz_find_question_view(self):
        quiz = Quiz.objects.first()
        attempt = Attempt.objects.create(quiz=quiz, user=self.user)
        url = reverse('quizRequestAttempt', args=[quiz.hash])
        self.client.get(url) # Get attempt
        url = reverse('quizFindQuestion', args=[quiz.hash, attempt.hash])
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)  # Redirect

    def test_quiz_view(self):
        quiz = Quiz.objects.first()
        attempt = Attempt.objects.create(quiz=quiz, user=self.user)
        question = Question.objects.filter(quiz=quiz).first()
        url = reverse('quiz', args=[quiz.hash, attempt.hash, question.id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_quiz_result_view(self):
        quiz = Quiz.objects.first()
        attempt = Attempt.objects.create(quiz=quiz, user=self.user)
        url = reverse('quizResult', args=[quiz.hash, attempt.hash])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)


class QuizesAdminTestCase(TestCase):
    fixtures = ['data.json', ]
    def setUp(self):
        self.user = User.objects.get(username='test')
        #self.url = reverse('quizList', )
        self.client = Client()
        self.client.login(username='test', password='test')

    def test_subjects_view(self):
        url = reverse('quizAdmin')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_subject_view(self):
        subject = Subject.objects.first()
        url = reverse('quizAdminSubject', args=[subject.code])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_quiz_view(self):
        quiz = Quiz.objects.first()
        url = reverse('quizAdminQuiz', args=[quiz.hash])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)






