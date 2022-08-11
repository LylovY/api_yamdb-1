import random

from django.core.mail import send_mail
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (IsAdminOrSuperuser,
                          IsAuthorOrReadOnly, IsAdminOrReadOnly)
from .serializers import (AuthUserSerializer, CategorySerializer,
                          GenreSerializer, ReviewSerializer,
                          SelfUserSerializer, TitlePostSerializer,
                          TitleSerializer, UserSerializer, UserTokenSerializer)


def generate_code():
    random.seed()
    return str(random.randint(100000, 999999))


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


@api_view(['POST'])
def create_user_send_code(request):
    if request.method == 'POST':
        serializer = AuthUserSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = generate_code()
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if user.username == username and user.email == email:
                    message = confirmation_code
                    user.code = confirmation_code
                    user.save()
                    send_mail(
                        'Код подтверждения Yamdb',
                        message,
                        'from@example.com',
                        [email],
                        fail_silently=False,
                    )
                    return Response('Код отправлен', status=status.HTTP_200_OK)
            serializer.validated_data['code'] = confirmation_code
            serializer.save()
            message = confirmation_code
            to_email = serializer.data['email']
            send_mail(
                'Код подтверждения Yamdb',
                message,
                'from@example.com',
                [to_email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = UserTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        code = int(serializer.validated_data['confirmation_code'])
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.code == code and code > 0:
                if user.is_superuser:
                    user.role = 'admin'
                user.save()
                token = get_tokens_for_user(user)
                return Response({'token': token['access']})
            return Response(
                'Отсутствует код или он некорректен',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    permission_classes = (IsAdminOrSuperuser,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination


class SelfUserViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        username = self.request.user.username
        user = User.objects.get(username=username)
        serializer = SelfUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        username = self.request.user.username
        user = User.objects.get(username=username)
        serializer = SelfUserSerializer(
            user, data=request.data, partial=True, many=False
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CategoryGenreViewSet(CreateListDestroyViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg(F('reviews__score')))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer
