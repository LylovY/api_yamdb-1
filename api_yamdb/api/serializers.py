from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(
        queryset=User.objects.all(),
        message='Такое имя пользователя уже существует')])
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=User.objects.all(), message='Такая почта уже существует')])

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                '"Me" не доступен для поля username')
        return value


class UserSerializer(AuthUserSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SelfUserSerializer(AuthUserSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)
