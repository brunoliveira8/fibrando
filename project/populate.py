# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from app.models import Task, MailBox, Gym
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType



def populate():
    Task.objects.all().delete()
    add_task(name="Esteira")
    add_task(name="Elíptico")
    add_task(name="Bicicleta")
    add_task(name="Rosca Inversa")
    add_task(name="Rosca Concentrada")
    add_task(name="Rosca Martelo")
    add_task(name="Rosca Direta")
    add_task(name="Rosca Alternada")
    add_task(name="Remada Unilateral")
    add_task(name="Puxada na Frente com Triângulo e Polia Alta")
    add_task(name="Puxada na Frente com Polia Alta")
    add_task(name="Puxada Alta com Braços Estendidos")
    add_task(name="Chest fly")
    add_task(name="Crucifixo")
    add_task(name="Crossover")
    add_task(name="Supino Inclinado")
    add_task(name="Supino Reto")
    add_task(name="Glúteos Quatro Apoios e Perna Estendida")
    add_task(name="Abdução de Quadril")
    add_task(name="Mesa Flexora")
    add_task(name="Cadeira Extensora")
    add_task(name="Cadeira Abdutora")
    add_task(name="Leg Press Inclinado")
    add_task(name="Remada Alta")
    add_task(name="Desenvolvimento com Halteres")
    add_task(name="Elevação Frontal")
    add_task(name="Elevação Lateral")

    add_group('athlete')
    add_group('trainer')

    add_mail_box('admin')

    add_gym('MANAGYMENT')

    print Task.objects.all()

def add_task(name):
    a = Task.objects.get_or_create(name = name)[0]
    a.save()
    return a

def add_group(name):
    g = Group.objects.get_or_create(name = name)[0]
    g.save()

def add_permission(codename, name):
    content_type = ContentType.objects.get_for_model(Permission)
    p = Permission.objects.get_or_create(codename = codename, content_type = content_type)[0]
    p.name = name
    p.save()

def add_mail_box(owner):
    g = MailBox.objects.get_or_create(owner = owner)[0]
    g.save()

def add_gym(name):
    g = Gym.objects.get_or_create(name = name)[0]
    g.save()

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    populate()
