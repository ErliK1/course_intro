from rest_framework.permissions import BasePermission
from rest_framework.request import Request


from main.models import Manager, Visitor


class ManagerPermission(BasePermission):

    def has_permission(self, request: Request, view):
        return request.user.is_authenticated and Manager.objects.filter(user=request.user)


    def has_object_permission(self, request: Request, view, obj: Manager):
        return request.user.is_authenticated and obj.user == request.user


class VisitorPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request: Request, view, obj: Visitor):
        return request.user.is_authenticated and \
               (obj.user == request.user or
                Manager.objects.filter(user=request.user).exists())

