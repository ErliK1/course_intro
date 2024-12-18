from rest_framework.permissions import BasePermission

from shared.models import ACIAdmin


class ACIAdminPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return ACIAdmin.objects.filter(user=request.user).exists()
    
class ACISuperUserPermission(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)