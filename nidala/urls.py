from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^user/', include('usermanagement.urls', namespace='user')),
]
