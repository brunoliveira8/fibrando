from django.contrib import admin
from app.models import Task, Athlete, PersonalTrainer, Gym, Exercise, BodyScreening, Subscribe
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Task)
admin.site.register(Permission)
admin.site.register(Athlete)
admin.site.register(PersonalTrainer)
admin.site.register(Gym)
admin.site.register(Exercise)
admin.site.register(BodyScreening)
admin.site.register(Subscribe)


