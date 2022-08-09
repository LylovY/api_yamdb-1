from django.urls import path, include
from .views import create_user_send_code, get_token

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', create_user_send_code, name='create_user'),
]
