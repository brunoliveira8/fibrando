# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index),
        url(r'^index/', views.index),
        url(r'^edit/', views.edit),
        url(r'^tracker/', views.tracker),
        url(r'^members/', views.members),
        url(r'^send/', views.message),
        url(r'^buddy_match/', views.buddy_match),
        url(r'^send_match/', views.message_match),
        url(r'^workout_plan/', views.workout_plan),
        url(r'^workout/days/(?P<div>\w+)/$', views.workout_day),
        url(r'^delete_exercise/', views.delete_exercise),
        url(r'^plan_manage/', views.plan_manage),
        url(r'^permission_denied/', views.permission_denied),
        url(r'^delete_plan_msg/', views.delete_plan_msg),
        url(r'^screenings/(?P<username>\w+)/$', views.screenings),
        url(r'^screenings/$', views.screenings),
        url(r'^create_screening/(?P<username>\w+)/$', views.create_screening),    
        url(r'^delete_screening/', views.delete_screening),
        url(r'^alunos/$', views.AlunoList.as_view()),
        url(r'^alunos_list/$', views.alunos_list_json),
        url(r'^add_aluno/$', views.AddAluno.as_view()),
        url(r'^manage_workout/(?P<username>\w+)/$', views.ManageWorkout.as_view()),
)