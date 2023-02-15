from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import QueUser
from rest_framework import permissions

# TODO: https://hakibenita.com/django-rest-framework-slow
class UserQueSerializer(serializers.ModelSerializer):
    """
    Output info about our user
    """
    avatar = serializers.ImageField(write_only=True)

    class Meta:
        model = QueUser
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "phone",
        )


class UserQuePublicSerializer(serializers.ModelSerializer):
    """
    Output public info about our user
    """

    photo1 = serializers.ImageField(write_only=True)
    photo2 = serializers.ImageField(write_only=True)
    photo3 = serializers.ImageField(write_only=True)
    photo4 = serializers.ImageField(write_only=True)
    photo5 = serializers.ImageField(write_only=True)
    photo6 = serializers.ImageField(write_only=True)

    class Meta:

        model = QueUser
        exclude = (
            "email",
            "phone",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_verified",
            "groups",
            "user_permissions"
        )


class CreateUser(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = QueUser
        fields = ['id', 'username', 'password', 'first_name', 'city', 'birthday', 'gender',
                  'interested_in_gender', 'phone', 'photo1', 'language', 'email']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueUser
        fields = ('id', 'username', 'is_registered')


class UserSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.AllowAny]

    class Meta(UserCreateSerializer.Meta):
        model = QueUser
        fields = ['id', 'username', 'password', 'first_name', 'city', 'birthday', 'gender',
                  'interested_in_gender', 'phone', 'photo1', 'language', 'email']


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


