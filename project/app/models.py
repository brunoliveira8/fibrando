# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from registration.signals import user_registered
from django.contrib.auth.models import Group
from django.utils import timezone

# Create your models here.
class Gym(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return u'%s' % (self.name)

class Task(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return u'%s' % (self.name)

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User)
    is_current = models.BooleanField(default = True)
    created_at = models.DateTimeField(default=timezone.now)

class Exercise(models.Model):
    task = models.ForeignKey(Task)
    weight = models.CharField(max_length=100)
    repetition = models.CharField(max_length=100)
    sets = models.CharField(max_length=100)

    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

    DIV = (
        (A, 'Div A'),
        (B, 'Div B'),
        (C, 'Div C'),
        (D, 'Div D'),
        (E, 'Div E'),
    )

    division = models.CharField(max_length=2, choices=DIV, default=A)

    workout_plan = models.ForeignKey(WorkoutPlan)

    def __unicode__(self):
        return u'%d' % (self.id)



class BodyScreening(models.Model):

    criado_em = models.DateField(default=datetime.now)
    altura = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    peso = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    perimetria = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    peitoral = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    braco_direito = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Braço direito")
    braco_esquerdo = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Braço esquerdo")
    cintura = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    abdomen = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    quadril = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    coxa_direita = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    coxa_esquerda = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    bodyfat = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Percentagem de godura")
    imc = models.DecimalField(max_digits=6, decimal_places=1, default=0)

    def __unicode__(self):
        return u'%d' % (self.id)

class PersonalTrainer(models.Model):
    user = models.OneToOneField(User)

    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (MALE, 'Masculino'),
        (FEMALE, 'Feminino'),
    )
    gender = models.CharField(max_length=2,
                                      choices=GENDERS,
                                      default=MALE)

    gym = models.ForeignKey(Gym)

    def __unicode__(self):
        if self.user.username:
            return u'%s' % (self.user.username)

class Tracker(models.Model):
    startWeightDate = models.DateField(auto_now_add=True)
    startWeight = models.IntegerField(max_length=4, default=0)
    previousWeightDate = models.DateField(auto_now=True)
    previousWeight = models.IntegerField(max_length=4, default=0)
    currentWeightDate = models.DateField(auto_now=True)
    currentWeight = models.IntegerField(max_length=4, default=170)
    goalWeight = models.IntegerField(default=160, max_length=4)


class Athlete(models.Model):
    user = models.OneToOneField(User) #Inheritance of User model
    tracker = models.OneToOneField(Tracker)

    BEGGINER = 'BG'
    INTERMEDIATE = 'IN'
    ADVANCED = 'AD'
    LEVELS = (
        (BEGGINER, 'Iniciante'),
        (INTERMEDIATE, 'Intermediário'),
        (ADVANCED, 'Avançado'),
    )
    level = models.CharField(max_length=2,
                                      choices=LEVELS,
                                      default=BEGGINER)

    MORNING = 'MO'
    AFTERNOON = 'AF'
    NIGHT = 'NI'
    TRAINING_PERIOD = (
        (MORNING, 'Manhã'),
        (AFTERNOON, 'Tarde'),
        (NIGHT, 'Noite'),
    )
    training_period = models.CharField(max_length=2,
                                      choices=TRAINING_PERIOD,
                                      default=MORNING)

    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (MALE, 'Masculino'),
        (FEMALE, 'Feminino'),
    )
    gender = models.CharField(max_length=2,
                                      choices=GENDERS,
                                      default=MALE)

    screenings = models.ManyToManyField(BodyScreening, null=True, blank = True)

    personal = models.ForeignKey(PersonalTrainer, blank=True, null = True)

    gym = models.ForeignKey(Gym)

    def __unicode__(self):
        if self.user.username:
            return u'%s' % (self.user.username)

#Message System
class Message(models.Model):
    sbj = models.CharField(max_length=50)
    body = models.TextField(max_length = 500)
    src = models.CharField(max_length=50)


class MailBox(models.Model):
    owner = models.CharField(max_length=50)
    messages = models.ManyToManyField(Message)

    def add_msg(self, body, sbj, src):
        self.messages.create(body = body, sbj = sbj, src = src)

    def get_msg(self):
        pass

    def del_msg(self, id):
        Message.objects.filter(id = id).delete()

#end Message System

#Business Logic
def user_registered_callback(sender, user, request, **kwargs):
    type = request.POST["group"]
    group = Group.objects.get(name=type)
    user.groups.add(group)
    mail_box = MailBox()
    mail_box.owner = user.username
    mail_box.save()

    mail_box_admin = MailBox.objects.get(owner = "admin")
    mail_box_admin.add_msg('SIGN UP', "Sign Up Request.", user.username)

    if type == 'athlete':
        athlete = Athlete()

        athlete.user = user

        workout_plan = WorkoutPlan()
        workout_plan.user = user
        workout_plan.save()

        tracker = Tracker()
        tracker.save()
        athlete.tracker = tracker

        athlete.gender = request.POST['gender']

        gym = Gym.objects.get(pk=int(request.POST['gym']))
        athlete.gym = gym

        athlete.save()
    else:
        personal = PersonalTrainer()
        personal.user = user
        personal.gender = request.POST['gender']
        gym = Gym.objects.get(pk=int(request.POST['gym']))
        personal.gym = gym
        personal.save()

user_registered.connect(user_registered_callback)
