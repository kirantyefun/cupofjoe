from rest_framework.permissions import BasePermission


class CafeOwnerRequired(BasePermission):
    """
    Permission class that allows access to only cafe owners.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'cafe')
    

class CanCreateCafe(BasePermission):
    """
    Permission class that allows only users without a registered cafe to create a new cafe.

    Attributes:
        message (str): The message to display when permission is denied.

    """
    message = 'Cafe-owner account required with no cafe registered to register a new cafe.'

    def has_permission(self, request, view):
        return request.user.can_create_cafe()
    

class HasCafeRegistered(BasePermission):
    """
    Permission class that allows only users with a registered cafe to access a view.

    Attributes:
        message (str): The message to display when permission is denied.
    """
    message = "No Cafe Registered for this account yet"
    
    def has_permission(self, request, view):
        return request.user.has_cafe_registered