from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^quiz/(?P<quiz_id>[0-9]+)/$', views.quizID, name='quizID'),
    url(r'^quiz/result/$', views.quizResult, name='quizResult'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^subjects/(?P<subject_id>[a-zA-Z]{3}[0-9]{4})/$', views.quizList, name='quizList'),
]
