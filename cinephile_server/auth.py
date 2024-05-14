from rest_framework.authentication import TokenAuthentication
from .permissions import IsSuperUser

class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class LoginRequired:
    authentication_classes = [BearerAuthentication]

class SuperUserRequired:
    permission_classes = [IsSuperUser]

class LoginAdminRequired(LoginRequired, SuperUserRequired):
    pass