from rest_framework.permissions import BasePermission
from rest_framework import permissions 
from datetime import date, timezone

class Permission(BasePermission):
    massage = "you can't login"
    def has_object_permission(self, request, view, obj):
        if not request.user.is_staff or not request.user == obj.user:
            return False
        return True
        
class ModifiedBokking(permissions.BasePermission):
    massage = "edit booking"
    def has_object_permission(self, request, view,obj):
        if request.user.is_staff or request.user == obj.user:
            current_time = date.today() 
            depature = obj.date
            if (depature - current_time).days > 3:
                return True
            return False
        return False

        
        