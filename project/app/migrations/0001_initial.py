# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(default=b'BG', max_length=2, choices=[(b'BG', b'Iniciante'), (b'IN', b'Intermedi\xc3\xa1rio'), (b'AD', b'Avan\xc3\xa7ado')])),
                ('training_period', models.CharField(default=b'MO', max_length=2, choices=[(b'MO', b'Manh\xc3\xa3'), (b'AF', b'Tarde'), (b'NI', b'Noite')])),
                ('gender', models.CharField(default=b'M', max_length=2, choices=[(b'M', b'Masculino'), (b'F', b'Feminino')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BodyScreening',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criado_em', models.DateField(default=datetime.datetime.now)),
                ('altura', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('peso', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('perimetria', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('peitoral', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('braco_direito', models.DecimalField(default=0, verbose_name=b'Bra\xc3\xa7o direito', max_digits=6, decimal_places=2)),
                ('braco_esquerdo', models.DecimalField(default=0, verbose_name=b'Bra\xc3\xa7o esquerdo', max_digits=6, decimal_places=2)),
                ('cintura', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('abdomen', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('quadril', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('coxa_direita', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('coxa_esquerda', models.DecimalField(default=0, max_digits=6, decimal_places=2)),
                ('bodyfat', models.DecimalField(default=0, verbose_name=b'Percentagem de godura', max_digits=6, decimal_places=2)),
                ('imc', models.DecimalField(default=0, max_digits=6, decimal_places=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.CharField(max_length=100)),
                ('repetition', models.CharField(max_length=100)),
                ('sets', models.CharField(max_length=100)),
                ('division', models.CharField(default=b'A', max_length=2, choices=[(b'A', b'Div A'), (b'B', b'Div B'), (b'C', b'Div C'), (b'D', b'Div D'), (b'E', b'Div E')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailBox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sbj', models.CharField(max_length=50)),
                ('body', models.TextField(max_length=500)),
                ('src', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalTrainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(default=b'M', max_length=2, choices=[(b'M', b'Masculino'), (b'F', b'Feminino')])),
                ('gym', models.ForeignKey(to='app.Gym')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tracker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startWeightDate', models.DateField(auto_now_add=True)),
                ('startWeight', models.IntegerField(default=0, max_length=4)),
                ('previousWeightDate', models.DateField(auto_now=True)),
                ('previousWeight', models.IntegerField(default=0, max_length=4)),
                ('currentWeightDate', models.DateField(auto_now=True)),
                ('currentWeight', models.IntegerField(default=170, max_length=4)),
                ('goalWeight', models.IntegerField(default=160, max_length=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_current', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mailbox',
            name='messages',
            field=models.ManyToManyField(to='app.Message'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='task',
            field=models.ForeignKey(to='app.Task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exercise',
            name='workout_plan',
            field=models.ForeignKey(to='app.WorkoutPlan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athlete',
            name='gym',
            field=models.ForeignKey(to='app.Gym'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athlete',
            name='personal',
            field=models.ForeignKey(blank=True, to='app.PersonalTrainer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athlete',
            name='screenings',
            field=models.ManyToManyField(to='app.BodyScreening', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athlete',
            name='tracker',
            field=models.OneToOneField(to='app.Tracker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='athlete',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
