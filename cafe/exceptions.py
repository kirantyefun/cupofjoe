from django.db import IntegrityError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound


def generic_exception_handler(exc, context):
    if isinstance(exc, IntegrityError):
        return Response({'error': 'Integrity Error occurred'}, status=status.HTTP_400_BAD_REQUEST)
    response = exception_handler(exc, context)
    return response


def custom_exception(detail, status_code):
    return Response({"error": detail}, status=status_code)