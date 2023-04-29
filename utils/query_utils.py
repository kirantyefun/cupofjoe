from cafe.exceptions import custom_exception
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
def get_item_for_update_destroy(pk, request):
    if pk is None:
        raise ValidationError('Primary key not received.')
    return get_object_or_404(request.user.cafe.menu, pk=pk)
