from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import *


class CreateEventPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            user = User.objects.get(username=request.user)
        except Exception as e:
            print(e)
            print('Error')
            return False
        try:
            manager = Manager.objects.get(user__username=user)
        except Exception as e:
            print(e)
            print('Did not get Manager')
            return False
        print(manager)
        return True

class JoinEventPerdoruesPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            perdorues = Perdorues.objects.get(user__username=request.user)
        except Exception as e:
            print(e)
            print('Not a Perdorues!!!')
            return False
        return True

class LogInPermission(BasePermission):

    def has_permission(self, request, view):
        b = IsAuthenticated()
        return not b.has_permission(request=request, view=view)