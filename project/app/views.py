# -*- coding: UTF-8 -*-
from __future__ import division
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from app.models import Athlete, Task, User, Tracker, Exercise, WorkoutPlan, MailBox,  PersonalTrainer, BodyScreening
from app.forms import *
from datetime import datetime
from decimal import Decimal
import urllib2, urllib
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.views.generic import ListView, View
import json
from django.utils.decorators import method_decorator

# Create your views here.
#This is the First Page's view.
def home(request):
    return render(request, 'index.html')

@login_required
def index(request):

	# Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    context_dict = {'boldmessage': "Excuse us, programmers working :)", 'group': group}

    if group == "athlete":
        return HttpResponseRedirect("/workout_plan/")
    elif group == "trainer":
        return HttpResponseRedirect("/alunos/")

    return render(request, 'app/index.html', context_dict)

@login_required
def edit(request):

    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        user = User.objects.get(username = request.user.username)
        user_form = UserEditForm(data=request.POST, instance = user)

        if group == "athlete":
            athlete = Athlete.objects.get(user = request.user)
            user_logged = AthleteForm(data=request.POST, instance = athlete)
        elif group == "trainer":
            personal = PersonalTrainer.objects.get(user = request.user)
            user_logged = PersonalTrainerForm(data=request.POST, instance = personal)

        # If the forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user_form.save()
            user_logged.save()
            context_dict = {'boldmessage': "Edit successful", 'group': group}
            return HttpResponseRedirect("/index/")

        else:
            print user_form.errors

    else:

        user_form = UserEditForm(instance = request.user)
        if group == "athlete":
            athlete = Athlete.objects.get(user = request.user)
            user_logged = AthleteForm(instance = athlete)
        elif group == "trainer":
            personal = PersonalTrainer.objects.get(user = request.user)
            user_logged = PersonalTrainerForm(instance = personal)

        #profile_form = UserProfileForm()

        # Render the template depending on the context.
        return render(request,
            'app/edit.html',
            {'user_form': user_form, 'user_logged': user_logged, 'group': group} )

@login_required
def change_password(request):
    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        user = User.objects.get(username = request.user.username)
        user_form = ChangePasswordForm(data=request.POST, instance = user)


        # If the forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            # Save the user's form data to the database.
            user = user_form.save(commit=False)
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            context_dict = {'boldmessage': "Edit successful", 'group': group}
            return render(request, 'app/index.html', context_dict)

        else:
            print user_form.errors

    else:
        user_form = ChangePasswordForm(instance = request.user)
        # Render the template depending on the context.
        return render(request,
            'gym_app/change_password.html',
            {'user_form': user_form, 'group': group} )

@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='athlete')).count() == 1, login_url='/permission_denied/')
def tracker(request):
    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    #User and tracker created at same time
    #Should always have the same ID but may be changed later
    user = User.objects.get(username = request.user.username)
    athlete = Athlete.objects.get(user = request.user)
    tracker = athlete.tracker
    progress=0
    result=0
    goal=0

    #update the weights
    if request.method == 'POST':
        newCurrentWeight = int(request.POST.get('currentWeight'))
        tracker.previousWeight=tracker.currentWeight
        tracker.currentWeight=newCurrentWeight
        tracker.previousWeightDate=tracker.currentWeightDate
        tracker.currentWeightDate=datetime.now()

        newGoalWeight = int(request.POST.get('goalWeight'))
        if tracker.goalWeight != newGoalWeight:
            tracker.startWeightDate = datetime.now()
            tracker.startWeight = newCurrentWeight
            tracker.goalWeight = newGoalWeight

    if tracker.goalWeight < tracker.startWeight: #lose weight goal
        goal = float(tracker.startWeight - tracker.goalWeight)
        result = float(tracker.startWeight - tracker.currentWeight)
    else:
        if tracker.goalWeight > tracker.startWeight: #gain weight goal
            goal = float(tracker.goalWeight - tracker.startWeight)
            result = float(tracker.currentWeight - tracker.startWeight)

    if goal == 0 or result > goal:
        progress = 100.0
    else:
        if result < 0:
            progress = 0.0
        else:
            progress = (result / goal) * 100.0

    progress = round(Decimal(progress), 1)

    tracker.save()

    context = {'tracker' : tracker, 'progress': progress, 'group': group}

    return render(request, 'app/tracker.html', context)

@login_required
def members(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!

    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    u_list = User.objects.all()

    context = {'user_list' : u_list, 'group': group}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'app/members.html', context)

@login_required
def message(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        user = User.objects.get(username = request.user.username)
        user_email = user.email
        to_email = request.POST.get('username')
        msg = request.POST.get('msg')
        sbj = request.POST.get('subject')

        send_mail(sbj, msg, user_email,
        [to_email], fail_silently=False)
        #send_mail(sbj, msg, from_email,
        #['pent.alef@gmail.com'], fail_silently=False)
        return HttpResponseRedirect('/members/')


@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='athlete')).count() == 1, login_url='/permission_denied/')
def buddy_match(request):

    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    user = User.objects.get(username = request.user.username)
    athlete = Athlete.objects.get(user = request.user)
    buddy_list = Athlete.objects.filter(level = athlete.level, training_period = athlete.training_period).exclude(user = user)
    buddy_matched = 0;
    context = {'buddy_list' : buddy_list, 'buddy_matched' : buddy_matched, 'group': group}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'app/buddy_match.html', context)

def message_match(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        user = User.objects.get(username = request.user.username)
        user_email = user.email
        to_email = request.POST.get('username')
        msg = "The user {0} wish workout with you!".format(user)
        sbj = "Buddy Match Message"

        send_mail(sbj, msg, user_email,
        [to_email], fail_silently=False)
        #send_mail(sbj, msg, from_email,
        #['pent.alef@gmail.com'], fail_silently=False)
        buddy_matched = 1;
        message = 'You have sent a Buddy Match request for: {0}!'.format(User.objects.get(email = to_email).username)
        context = {'message' : message, 'buddy_matched' : buddy_matched}

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
        return render(request, 'app/buddy_match.html', context)

@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='athlete')).count() == 1, login_url='/permission_denied/')
def workout_plan(request):

    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    user = User.objects.get(username = request.user.username)
    athlete = Athlete.objects.get(user = request.user)

    # Render the template depending on the context.
    return render(request,
        'app/workout_plan.html', {'group': group})

@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='athlete')).count() == 1, login_url='/permission_denied/')
def workout_day(request, div = 'A'):
    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        user = User.objects.get(username = request.user.username)
        exercise_form = ExerciseForm(data=request.POST)
        athlete = Athlete.objects.get(user = request.user)

        # If the forms are valid...
        if exercise_form.is_valid():
            # Save the user's form data to the database.
            exercise = exercise_form.save(commit=False)
            task = Task.objects.get(name = task_name)
            exercise.task = task
            exercise.div = div
            exercise.save()
            athlete.workout_plan.exercises.add(exercise)
            athlete.save()

            path = '/workout/days/{0}'.format(div)
            print path

            return redirect(path)

        else:
            return HttpResponse('There are errors in the fields: {0}'.format(exercise_form.errors))

    else:
        t_list = Task.objects.all()
        #user = User.objects.get(username = request.user.username)
        athlete = Athlete.objects.get(user = request.user)
        exercises = athlete.workout_plan.exercises.filter( division = div.upper())
        exercise_form = ExerciseForm()

        # Render the template depending on the context.
        return render(request, 'app/workout_day.html',
            {'exercise_form': exercise_form, 'task_list' : t_list, 'exercises' : exercises, 'day': div,'group' : group})


def delete_exercise(request):
    exercise_id = int(request.POST.get("delete"))
    Exercise.objects.filter(id = exercise_id).delete()
    path = '/workout/days/{0}'.format(request.POST.get("day"))
    return redirect(path)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/permission_denied/')
def plan_manage(request):

    if request.user.is_superuser:
        group = 'admin'
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name
        except:
            group = 'none'

    messages = MailBox.objects.get(owner = 'admin').messages.all()
    context = {'messages' : messages, 'group' : group}
    return render(request, 'app/plan_manage.html', context)


def permission_denied(request):

    if request.user.is_superuser:
        group = 'admin'
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name
        except:
            group = 'none'

    return render(request, 'app/permission_denied.html', {'group' : group})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/permission_denied/')
def delete_plan_msg(request):
    message_id = int(request.POST.get("delete"))
    MailBox.objects.get(owner = 'admin').del_msg(message_id)
    return HttpResponseRedirect('/plan_manage/')

@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='athlete')).count() == 1, login_url='/permission_denied/')
def delete_athlete_msg(request):
    message_id = int(request.POST.get("delete"))
    MailBox.objects.get(owner = request.user.username).del_msg(message_id)
    return HttpResponseRedirect('/manage_personal/')



@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='athlete') | Q(name='trainer')).count() == 1, login_url='/permission_denied/')
def create_screening(request, username):

    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    user = User.objects.get(username = username)
    athlete = Athlete.objects.get(user = user)
    workout_plan = WorkoutPlan.objects.get(user = user, is_current = True)
    permission = False

    if group == 'trainer':
        if athlete.personal is not None:
            permission = athlete.personal.user == request.user
    elif group == 'athlete':
        permission = request.user == user

    #verifica se a requisição é feita pelo professor do aluno
    if permission:

        if request.method == 'POST':
            screening_form = BodyScreeningForm(data=request.POST)

            if screening_form.is_valid():
                try:
                    user = User.objects.get(username = request.POST.get('username'))
                except:
                    user = User.objects.get(username = request.POST.get('user'))
                screening = screening_form.save(commit=False)
                screening.save()
                athlete = Athlete.objects.get(user = user.id)

                athlete.tracker.previousWeight=athlete.tracker.currentWeight
                athlete.tracker.currentWeight=screening.peso
                athlete.tracker.previousWeightDate=athlete.tracker.currentWeightDate
                athlete.tracker.currentWeightDate=datetime.now()
                athlete.tracker.save()
                screening.imc = screening.peso / (screening.altura*screening.altura)
                screening.save()
                athlete.screenings.add(screening)
                athlete.save()

                context_dict = {}
                context_dict['message'] = "Avaliação adicionada com sucesso."
                context_dict['group'] = group

                return render(request, 'app/success_message.html', context_dict)


            return render(request, 'app/create_screening.html', {'screening_form': screening_form, 'group': group, 'username' : username})


        screenings = Athlete.objects.get(user = user.id).screenings.all()
        if len(screenings) > 0:
            current_screening = screenings[len(screenings)-1]
            screening_form = BodyScreeningForm(instance=current_screening)
        else:
            screening_form = BodyScreeningForm()
        # Render the template depending on the context.
        return render(request, 'app/create_screening.html', {'screening_form': screening_form, 'group': group, 'username' : username})

    else:
        context_dict = {}
        context_dict['message'] = "Usuário inválido ou você não tem permissão."
        context_dict['group'] = group

        return render(request, 'app/message.html', context_dict)


@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='athlete') | Q(name='trainer')).count() == 1, login_url='/permission_denied/')
def screenings(request, username = None):

    if request.user.is_superuser:
        group = 'admin';
    else:
        try:
            group = User.objects.get(username=request.user.username).groups.all()[0].name;
        except:
            group = 'none'

    if username is  None:
        username = request.user.username

    user = User.objects.get(username = username)
    athlete = Athlete.objects.get(user = user)
    workout_plan = WorkoutPlan.objects.get(user = user, is_current = True)

    if athlete.personal is not None:

        #verifica se a requisição é feita pelo professor do aluno ou pelo aluno
        if athlete.personal.user == request.user or request.user == user:

            screenings = athlete.screenings.all()
            return render(request, 'app/screenings.html', {'screenings': screenings, 'group': group, 'username' : username})

        else:
            context_dict = {}
            context_dict['message'] = "Usuário inválido ou você não tem permissão."
            context_dict['group'] = group

            return render(request, 'app/message.html', context_dict)

    else:
            #verifica se a requisição é feita pelo aluno
            if request.user == user:

                screenings = athlete.screenings.all()
                return render(request, 'app/screenings.html', {'screenings': screenings, 'group': group, 'username' : username})

            else:
                context_dict = {}
                context_dict['message'] = "Usuário inválido ou você não tem permissão."
                context_dict['group'] = group

                return render(request, 'app/message.html', context_dict)



@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='trainer') | Q(name='athlete')).count() == 1, login_url='/permission_denied/')
def delete_screening(request):
    screening_id = int(request.POST.get("delete"))
    BodyScreening.objects.filter(id = screening_id).delete()
    path = '/screenings/'
    return redirect(path)


class AlunoList(ListView):
    context_object_name = 'alunos'
    template_name = 'app/alunos.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            group = 'admin';
        else:
            try:
                group = User.objects.get(username=self.request.user.username).groups.all()[0].name;
            except:
                group = 'none'
        # Call the base implementation first to get a context
        context = super(AlunoList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['group'] = group
        return context

    def get_queryset(self):
        self.personal = PersonalTrainer.objects.get(user = self.request.user)
        return Athlete.objects.filter(personal=self.personal)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlunoList, self).dispatch(*args, **kwargs)


@login_required
@user_passes_test(lambda u: u.groups.filter(Q(name='trainer')).count() == 1, login_url='/permission_denied/')
def alunos_list_json(request):
    if request.is_ajax():

        query = request.GET.get('term', '')
        name = query.split()
        personal = PersonalTrainer.objects.get(user = request.user)
        gym = personal.gym

        for term in name:
            atletas = gym.athlete_set.filter( Q(user__username__icontains = term) & Q( user__groups__name__in=['athlete']))

        results = []
        for atleta in atletas:
            aluno_json = {}
            aluno_json['id'] = atleta.user.pk
            aluno_json['label'] = atleta.user.username
            aluno_json['value'] = atleta.user.username
            results.append(aluno_json)
        data = json.dumps(results)
    else:

        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


class AddAluno(View):

    def get(self, request):
        if request.user.is_superuser:
            group = 'admin';
        else:
            try:
                group = User.objects.get(username=request.user.username).groups.all()[0].name;
            except:
                group = 'none'

        context_dict = {}
        context_dict['message'] = "Usuário inválido. Tente de novo"
        context_dict['group'] = group

        return render(request, 'app/message.html', context_dict)

    def post(self, request):

        if request.user.is_superuser:
            group = 'admin';
        else:
            try:
                group = User.objects.get(username=request.user.username).groups.all()[0].name;
            except:
                group = 'none'

        username = request.POST['aluno']
        context_dict = {}

        try:
            user = User.objects.get(username = username)
            mail_box = MailBox.objects.get(owner = user.username)
            mail_box.add_msg('{0} {1} ({2}) gostaria de ser seu professor.'.format(request.user.first_name, request.user.last_name, request.user.username), 'Novo Professor' , request.user.username)

            context_dict['message'] = "A requisição foi enviada. Aguarde a resposta do(a) aluno(a)."
            context_dict['group'] = group

            return render(request, 'app/success_message.html', context_dict)

        except:
            return HttpResponseRedirect('/add_aluno')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddAluno, self).dispatch(*args, **kwargs)



class ManageWorkout(View):

    def get(self, request, username):
        print username
        if request.user.is_superuser:
            group = 'admin';
        else:
            try:
                group = User.objects.get(username=request.user.username).groups.all()[0].name;
            except:
                group = 'none'

        context_dict = {}
        context_dict['group'] = group

        return render(request, 'app/manage_workout.html', context_dict)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ManageWorkout, self).dispatch(*args, **kwargs)

class ManagePersonal(View):

    def get(self, request):
        if request.user.is_superuser:
            group = 'admin';
        else:
            try:
                group = User.objects.get(username=request.user.username).groups.all()[0].name;
            except:
                group = 'none'

        context_dict = {}
        context_dict['group'] = group
        context_dict['has_personal'] =  False
        messages = MailBox.objects.get(owner = request.user.username).messages.all()
        print messages
        context_dict['messages'] =  messages

        athlete = Athlete.objects.get(user = request.user)

        if athlete.personal is None:
            context_dict['message'] = "Você não possui um personal trainer ainda."
        else:
            context_dict['message'] = "{0} {1} ({2})".format(athlete.personal.user.first_name, athlete.personal.user.last_name, athlete.personal.user.username)
            context_dict['has_personal'] =  True

        return render(request, 'app/manage_personal.html', context_dict)

    def  post(self, request):
        personal_username = request.POST.get("add_personal")
        user_personal = User.objects.get(username = personal_username)
        personal = PersonalTrainer.objects.get(user = user_personal)
        athlete = Athlete.objects.get(user = request.user)
        athlete.personal = personal
        athlete.save()

        message_id = int(request.POST.get("msg_id"))
        MailBox.objects.get(owner = request.user.username).del_msg(message_id)

        return HttpResponseRedirect('/manage_personal/')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ManagePersonal, self).dispatch(*args, **kwargs)

class SubscribeView(View):
    def post(self, request):
        form = SubscribeForm(request.POST)
        print form
        if form.is_valid():

            subs = form.save()
            return JsonResponse({'status':'sucesso'})
        else:
            return JsonResponse({'status':'falhou'})

