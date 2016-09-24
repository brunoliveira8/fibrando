from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework import routers

urlpatterns = [
    url(r'^tasks/$',  views.TaskList.as_view()),
    url(r'^current_user/$',  views.current_user),
    url(r'^exercises/(?P<username>\w+)/$',  views.exercise_list),
    url(r'^exercises/(?P<username>\w+)/(?P<pk>[0-9]+)/$', views.exercise_detail),
    url(r'^screenings/(?P<username>\w+)/$',  views.screenings_list),
    url(r'^screenings/(?P<username>\w+)/(?P<pk>[0-9]+)/$', views.screenings_detail),
    url(r'^alunos/$',  views.alunos),
    url(r'^current_workout_plan/(?P<username>\w+)/$',  views.current_workout_plan),
   
    #url(r'^tasks/(?P<pk>[0-9]+)$', views.task_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
