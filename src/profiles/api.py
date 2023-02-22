from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from rest_framework_api_key.permissions import HasAPIKey

from .serializers import UserQuePublicSerializer, UserListSerializer, UserSerializer, UserLoginSerializer, \
    ResetPasswordSerializer, ResetPasswordRequestSerializer
from .serializers import VerifyAccountSerializer
from rest_framework import permissions, status, viewsets
from .models import QueUser
from .tasks import check_age
from rest_framework.response import Response
from .emails import send_otp_to_email, generate_reset_password_otp, send_reset_password_otp_to_email


class UserQuePublicAPI(viewsets.ModelViewSet):
    """
    Output public user account
    """
    serializer_class = UserQuePublicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly & HasAPIKey]
    queryset = QueUser.objects.all()


class UserListAPI(viewsets.ModelViewSet):
    """
    Output list of users
    """
    serializer_class = UserListSerializer
    permission_classes = [HasAPIKey]
    queryset = QueUser.objects.all()


class TestCelery(CreateView):
    """
    Тестовый класс для celery
    """

    def form_valid(self, form):
        form.save()
        check_age.delay(form.instance.email)
        return super().form_valid(form)


class RegisterAPI(viewsets.ModelViewSet):
    """
    Registration by email
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            send_otp_to_email(serializer.data['email'])

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'You have been registered, check your email to finalize registration',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong'
            })


class VerifyOTP(viewsets.ModelViewSet):
    """
    The class with which the user confirms his mail
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyAccountSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            user = QueUser.objects.filter(email=email).first()
            if not user:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email',
                    'data': serializer.data
                })
            if not user.otp == otp:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Wrong otp',
                    'data': serializer.data
                })

            user.is_verified = True
            user.save()

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Your account has been verified',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong'
            })


class LoginAPI(viewsets.ModelViewSet):
    """
    User login API
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                # Login the user and return a success response
                login(request, user)
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Login successful',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                    }
                })
            else:
                # User is not active, return an error response
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'User account is not active',
                })
        else:
            # Email and/or password are incorrect, return an error response
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid email and/or password',
            })


class ResetPasswordRequestAPI(viewsets.ModelViewSet):
    """
    Class for handling password reset requests by email
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordRequestSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']

            user = QueUser.objects.filter(email=email).first()
            if not user:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email',
                    'data': serializer.data
                })
            reset_password_otp = generate_reset_password_otp()
            user.reset_password_otp = reset_password_otp
            user.save()
            send_reset_password_otp_to_email(email, reset_password_otp)

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Reset password OTP sent to your email',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Something went wrong'
            })


class ResetPasswordAPI(viewsets.ModelViewSet):
    """
    Class for handling password reset with OTP
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer
    queryset = QueUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            user = QueUser.objects.filter(email=email).first()
            if not user:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email',
                    'data': serializer.data
                })
            if not user.reset_password_otp == otp:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Wrong OTP',
                    'data': serializer.data
                })

            user.set_password(new_password)
            user.reset_password_otp = None
            user.save()

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Password reset successful',
                'data': serializer.data
            })
        except Exception as error:
            print(error)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Wrong',
            })
