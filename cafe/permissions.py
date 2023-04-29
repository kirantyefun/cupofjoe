from rest_framework.permissions import BasePermission


class CafeOwnerRequired(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'cafe')
    

class CanCreateCafe(BasePermission):
    message = 'Cafe-owner account required with no cafe registered to register a new cafe.'

    def has_permission(self, request, view):
        return request.user.can_create_cafe()
    

class HasCafeRegistered(BasePermission):
    message = "No Cafe Registered for this account yet"
    
    def has_permission(self, request, view):
        return request.user.has_cafe_registered