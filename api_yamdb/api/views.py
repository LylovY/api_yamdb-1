import random

from django.core.mail import send_mail
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .permissions import IsAdmin
from .serializers import AuthUserSerializer, SelfUserSerializer, UserSerializer


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
            return Response('Код отправлен', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    username = request.data['username']
    code = int(request.data['confirmation_code'])
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if user.code == code and code > 0:
            user.is_active = True
            if user.is_superuser:
                user.role = 'admin'
            user.save()
            token = get_tokens_for_user(user)
            return Response({'token': token['access']})
        return Response('Отсутствует код или он некорректен',
                        status=status.HTTP_400_BAD_REQUEST)
    return Response('Пользователь не найден', status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination


# class SelfUserViewSet(mixins.RetrieveModelMixin,
#                       mixins.UpdateModelMixin,
#                       viewsets.GenericViewSet):
#     serializer_class = SelfUserSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return User.objects.filter(username=user)


class SelfUserViewSet(APIView):
    def get(self, request):
        username = self.request.user.username
        user = User.objects.get(username=username)
        serializer = SelfUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        username = self.request.user.username
        user = User.objects.get(username=username)
        serializer = SelfUserSerializer(
            user, data=request.data, partial=True, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
