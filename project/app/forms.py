# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.contrib.auth.models import User
from app.models import User, Athlete, Tracker, Exercise, PersonalTrainer, BodyScreening, Gym, Subscribe
from django.db.models import Q
from registration.forms import RegistrationFormUniqueEmail

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password', 'email']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username','password', 'email', 'first_name', 'last_name')

class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control"}))
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"}))

    class Meta:
        model = User
        fields = ('password', )


class AthleteForm(forms.ModelForm):

    level = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}), choices=Athlete.LEVELS)
    training_period = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}), choices=Athlete.TRAINING_PERIOD)
    gender = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}), choices=Athlete.GENDERS)

    class Meta:
        model = Athlete
        fields = ('level', 'training_period', 'gender')

class PersonalTrainerForm(forms.ModelForm):
    gender = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}), choices=Athlete.GENDERS)
    class Meta:
        model = PersonalTrainer
        fields = ('gender',)

class ExerciseForm(forms.ModelForm):
    weight = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    repetition = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    sets = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = Exercise
        fields = ('weight','repetition', 'sets')

class BodyScreeningForm(forms.ModelForm):
    class Meta:
        model = BodyScreening
        exclude = ['criado_em', 'imc']

class AthleteSelectForm(forms.Form):

    athlete = forms.ModelChoiceField(queryset=User.objects.filter(Q(groups__name='athlete')), empty_label='...', to_field_name='username', widget=forms.Select(attrs={'class': "form-control"}))


class UserTypeForm(forms.Form):

    GROUPS = (
        ('regular', 'Aluno'),
        ('personal_trainer', 'Professor'),
    )
    group = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices=GROUPS, required=True, label='User Type')


class UserGenderForm(forms.Form):
    GENDERS = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )
    gender = forms.ChoiceField(
        widget=forms.Select(attrs={'class': "form-control"}), choices=GENDERS,
        required=True,
        initial='F'
        )


class RegisterForm(RegistrationFormUniqueEmail):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label="Usuário")
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label="Senha",widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password2 = forms.CharField(label="Confirmar senha",widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    #first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    #last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    GENDERS = (
        ('F', 'Feminino'),
        ('M', 'Masculino'),
    )

    gender = forms.ChoiceField(
        widget=forms.Select(attrs={'class': "form-control"}), choices=GENDERS,
        required=True,
        initial='F',
        label="Sexo"
    )

    GROUPS = (
        ('athlete', 'Aluno'),
        ('trainer', 'Professor'),
    )
    group = forms.ChoiceField(widget=forms.Select(attrs={'class': "form-control"}),choices=GROUPS, required=True, label='Tipo de conta')

    #gym = forms.ModelChoiceField(label="Academia", queryset=Gym.objects.all(), widget=forms.Select(attrs={'class': "form-control"}))

    class Meta:
        model = User
        #fields = ('username','password1','password2', 'email', 'gender', 'group', 'gym')
        fields = ('username','password1','password2', 'email', 'gender', 'group')

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe

