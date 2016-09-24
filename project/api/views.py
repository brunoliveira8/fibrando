#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import generics
from django.contrib.auth.models import User
from app.models import Task, Exercise, WorkoutPlan, Athlete, PersonalTrainer, BodyScreening
from api.serializers import TaskSerializer, ExerciseSerializer, UserSerializer, AthleteSerializer, WorkoutPlanSerializer, BodyScreeningSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
class TaskList(generics.ListCreateAPIView):
	queryset = Task.objects.order_by('name')
	serializer_class = TaskSerializer



@api_view(['GET', 'POST',])
def exercise_list(request, username):
	"""
	List all exercises, or create a new exercise.
	"""
	user = User.objects.get(username = username)
	athlete = Athlete.objects.get(user = user)
	workout_plan = WorkoutPlan.objects.get(user = user, is_current = True)

	#verifica se a requisição é feita pelo professor ou pelo proprio aluno
	if user == request.user or athlete.personal.user == request.user:

		if request.method == 'GET':
			exercises = Exercise.objects.filter(workout_plan = workout_plan)
			serializer = ExerciseSerializer(exercises, many=True)
			return Response(serializer.data)

		elif request.method == 'POST':
			serializer = ExerciseSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE',])
def exercise_detail(request, username, pk):
	"""
	List all exercises, or create a new exercise.
	"""
	user = User.objects.get(username = username)
	athlete = Athlete.objects.get(user = user)
	workout_plan = WorkoutPlan.objects.get(user = user, is_current = True)
	print request.method
	#verifica se a requisição é feita pelo professor ou pelo proprio aluno
	if user == request.user or athlete.personal.user == request.user:

		if request.method == 'GET':
			exercise = Exercise.objects.get(pk = pk)
			serializer = ExerciseSerializer(exercise)
			return Response(serializer.data)

		elif request.method == 'PUT':
			exercise = Exercise.objects.get(pk = pk)
			serializer = ExerciseSerializer(exercise, data=request.data)
			
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		elif request.method == 'DELETE':
			
			exercise = Exercise.objects.get(pk = pk)
        	exercise.delete()
        	return Response(status=status.HTTP_204_NO_CONTENT)

	return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def screenings_list(request, username):
	"""
	List all exercises, or create a new exercise.
	"""
	user = User.objects.get(username = username)
	athlete = Athlete.objects.get(user = user)

	#verifica se a requisição é feita pelo professor ou pelo proprio aluno
	if user == request.user or athlete.personal.user == request.user:

		if request.method == 'GET':
			screenings = athlete.screenings
			serializer = BodyScreeningSerializer(screenings, many=True)
			return Response(serializer.data)

	return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE',])
def screenings_detail(request, username, pk):
	"""
	List all exercises, or create a new exercise.
	"""
	user = User.objects.get(username = username)
	athlete = Athlete.objects.get(user = user)

	#verifica se a requisição é feita pelo professor ou pelo proprio aluno
	if user == request.user or athlete.personal.user == request.user:

		if request.method == 'GET':
			screening = BodyScreening.objects.get(pk = pk)
			print screening
			serializer = BodyScreeningSerializer(screening)
			return Response(serializer.data)

		elif request.method == 'PUT':
			screening = BodyScreening.objects.get(pk = pk)
			serializer = BodyScreeningSerializer(screening, data=request.data)
			
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		elif request.method == 'DELETE':
			
			screening = BodyScreening.objects.get(pk = pk)
        	screening.delete()
        	return Response(status=status.HTTP_204_NO_CONTENT)

	return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def current_user(request):
	if request.method == 'GET':
		user = User.objects.get(username = request.user.username)
		serializer = UserSerializer(user)
		return Response(serializer.data)

	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET',])
def alunos(request):
	if request.method == 'GET':
		user = User.objects.get(username = request.user.username)
		personal = PersonalTrainer.objects.get(user = user)
		athletes = Athlete.objects.filter(personal = personal)
		serializer = AthleteSerializer(athletes, many=True)
		print serializer.data
		return Response(serializer.data)

	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def current_workout_plan(request, username):
	"""
	List all exercises, or create a new exercise.
	"""
	user = User.objects.get(username = username)
	athlete = Athlete.objects.get(user = user)
	workout_plan = WorkoutPlan.objects.get(user = user, is_current = True)

	#verifica se a requisição é feita pelo professor ou pelo proprio aluno
	if user == request.user or athlete.personal.user == request.user:

		if request.method == 'GET':
			serializer = WorkoutPlanSerializer(workout_plan)
			return Response(serializer.data)


	return Response(status=status.HTTP_400_BAD_REQUEST)
