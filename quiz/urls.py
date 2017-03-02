from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]{10})/$', views.quizRequestAttempt, name='quizRequestAttempt'),
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]{10})/resultat/$', views.quizResult, name='quizResult'),
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]{10})/(?P<quiz_attempt>[a-f0-9]{10})/$', views.quizFindQuestion, name='quizFindQuestion'),
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]{10})/(?P<quiz_attempt>[a-f0-9]{10})/(?P<quiz_question>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^subjects/(?P<subject_id>[a-zA-Z]{3}[0-9]{4})/$', views.quizList, name='quizList'),
]
