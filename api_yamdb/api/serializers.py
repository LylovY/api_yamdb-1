from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import CHOICES_SCORE, Review
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


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.IntegerField()


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    score = serializers.ChoiceField(choices=CHOICES_SCORE)

    # +добавить проверку что можно оставить один отзыв на произведение

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Можно оставить только один отзыв.'
            )
        ]
