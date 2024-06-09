"""Module for permissions."""


from django.core.handlers.wsgi import WSGIRequest
from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    """
    Custom permission class that checks if the user is a superuser.

    This class extends Django's BasePermission and overrides the `has_permission` method
    to determine if the current user,
    identified through the given Django request object, possesses superuser privileges.
    It returns True if the user is a superuser,
    allowing them access based on this permission check; otherwise, it returns False, denying access.

    Attributes:
        - request: The Django HttpRequest object containing details about the incoming HTTP request.
          This object is used to identify the user making the request.

    Methods:
        has_permission(request: WSGIRequest, view) -> bool: Checks if the user is a superuser.
          - request: The Django request object.
          - view: The view function or class-based view that triggered the permission check.
                 This parameter is typically ignored in implementations of `has_permission`.
          - Returns: A boolean value indicating whether the user is a superuser. True indicates the user,
                    has superuser status granting them access;
                    False indicates the user does not have superuser status, denying them access.
    """

    def has_permission(self, request: WSGIRequest, _) -> bool:
        """
        Determine if the user is a superuser.

        Args:
            request: The Django request object containing information about the incoming HTTP request.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return request.user.is_superuser
