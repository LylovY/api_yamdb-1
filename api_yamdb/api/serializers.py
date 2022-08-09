from users.models import User
from rest_framework import serializers


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')
