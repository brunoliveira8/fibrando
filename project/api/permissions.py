from rest_framework import permissions
from app.models import Exercise, WorkoutPlan, Athlete


class IsOwnerOrPersonal(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        print obj
        #workout = WorkoutPlan.objects.get(pk=obj.workout_plan)
        #athlete = Athlete.objects.get(user = obj.user)

        #return  request.user == workout.user or request.user == athlete.personal
        return False