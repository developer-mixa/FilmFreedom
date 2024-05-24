from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from cinephile_server.views import UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include('cinephile_server.urls')),
]
