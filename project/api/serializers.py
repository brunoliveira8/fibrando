from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Task, Exercise, WorkoutPlan, Athlete, BodyScreening
from rest_framework.fields import empty

class RelationModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        self.is_relation = kwargs.pop('is_relation', False)
        super(RelationModelSerializer, self).__init__(instance, data, **kwargs)

    def validate_empty_values(self, data):
        if self.is_relation:
            model = getattr(self.Meta, 'model')
            model_pk = model._meta.pk.name

            if not isinstance(data, dict):
                error_message = self.default_error_messages['invalid'].format(datatype=type(data).__name__)
                raise serializers.ValidationError(error_message)

            if not model_pk in data:
                raise serializers.ValidationError({model_pk: model_pk + ' is required'})

            try:
                instance = model.objects.get(pk=data[model_pk])
                return True, instance
            except:
                raise serializers.ValidationError({model_pk: model_pk + ' is not valid'})

        return super(RelationModelSerializer, self).validate_empty_values(data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class TaskSerializer(RelationModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name')


class BodyScreeningSerializer(RelationModelSerializer):
    class Meta:
        model = BodyScreening
        fields = ('__all__')

class WorkoutPlanSerializer(RelationModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = ('id', 'is_current', 'created_at')


class ExerciseSerializer(RelationModelSerializer):

    task = TaskSerializer(read_only=False, is_relation=True)
    workout_plan = WorkoutPlanSerializer(read_only=False, is_relation=True)

    class Meta:
        model = Exercise
        fields = ('id', 'task', 'weight', 'repetition', 'sets', 'division', 'workout_plan')

class AthleteSerializer(RelationModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Athlete
        fields = ('id', 'user', 'level', 'training_period', 'gender')