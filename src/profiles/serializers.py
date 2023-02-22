from django.contrib.auth.hashers import make_password
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import QueUser, Education, ZodiacSign, InterestedInRelation, SocialLink, UserPreference, UserPhotos


# TODO: https://hakibenita.com/django-rest-framework-slow

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ZodiacSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZodiacSign
        fields = '__all__'


class InterestedInRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestedInRelation
        fields = '__all__'


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = '__all__'


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhotos
        fields = '__all__'


class UserQuePublicSerializer(serializers.ModelSerializer):
    """
    Output a subset of info about our user for public use
    """

    education = EducationSerializer()
    zodiac_sign = ZodiacSignSerializer()
    interested_in_relation = InterestedInRelationSerializer(many=True)
    social_links = SocialLinkSerializer(many=True)
    user_preference = UserPreferenceSerializer()
    user_photo = UserPhotoSerializer(many=True)

    class Meta:
        model = QueUser
        exclude = (
            'password',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'phone',
            'updated_at',
        )


class CreateUser(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = QueUser
        fields = ['id', 'username', 'password', 'first_name', 'city', 'birthday', 'gender',
                  'interested_in_gender', 'phone', 'language', 'email']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueUser
        fields = ('id', 'username', 'is_registered')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = QueUser
        fields = ['id', 'username', 'password', 'first_name', 'city', 'birthday', 'gender',
                  'interested_in_gender', 'phone', 'language', 'email']
        ref_name = 'ProfileUser'

    def create(self, validated_data: dict):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class VerifyAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        model = QueUser
        fields = ('email', 'otp')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
