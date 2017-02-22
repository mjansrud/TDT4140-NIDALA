from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^quiz/1/$', views.quizID, name='quizID'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^subjects/tdt4120/$', views.quizList, name='quizList'),
]
