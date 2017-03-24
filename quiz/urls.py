from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]+)/$', views.quizRequestAttempt, name='quizRequestAttempt'),
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]+)/(?P<attempt_hash>[a-f0-9]+)/resultat/$', views.quizResult,
        name='quizResult'),
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]+)/(?P<attempt_hash>[a-f0-9]+)/$', views.quizFindQuestion,
        name='quizFindQuestion'),
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]+)/(?P<attempt_hash>[a-f0-9]+)/(?P<quiz_question>[0-9]+)/$', views.quiz,
        name='quiz'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^subjects/(?P<subject_id>[a-zA-Z0-9]+)/$', views.quizList, name='quizList'),
]
