from rest_framework.authentication import TokenAuthentication

class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class LoginRequired:
    authentication_classes = [BearerAuthentication]
