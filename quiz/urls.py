from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^quiz/(?P<quiz_hash>[a-f0-9]{10})/$', views.quizHash, name='quizHash'),
    url(r'^quiz/result/$', views.quizResult, name='quizResult'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^subjects/(?P<subject_id>[a-zA-Z]{3}[0-9]{4})/$', views.quizList, name='quizList'),
]
