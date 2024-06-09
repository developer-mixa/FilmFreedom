"""Module for mixins with auth."""


from rest_framework.authentication import TokenAuthentication

from .permissions import IsSuperUser


class BearerAuthentication(TokenAuthentication):
    """Custom authentication class that uses the Bearer scheme for authenticating users."""

    keyword = 'Bearer'


class LoginRequired:
    """Middleware class that requires authentication for accessing views."""

    authentication_classes = [BearerAuthentication]


class LoginAdminRequired(LoginRequired):
    """Class that combines login requirement with admin permissions."""

    permission_classes = [IsSuperUser]
