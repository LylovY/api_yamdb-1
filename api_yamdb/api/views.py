from django.shortcuts import render

# Create your views here.
import random

from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import AuthUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


def generate_code():
    random.seed()
    return str(random.randint(100000, 999999))


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


@api_view(['POST'])
def create_user_send_code(request):
    if request.method == 'POST':
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = generate_code()
            serializer.validated_data['code'] = confirmation_code
            serializer.save()
            message = confirmation_code
            to_email = serializer.data['email']
            send_mail('Код подтверждения Yamdb',
                      message,
                      'from@example.com',
                      [to_email],
                      fail_silently=False)
            return Response('Код отправлен')


@api_view(['POST'])
def get_token(request):
    username = request.data['username']
    code = request.data['confirmation_code']
    if User.objects.get(username=username).exists():
        user = User.objects.get(username=username)
        if user.code == code:
            user.is_active = True
            get_tokens_for_user(user)
