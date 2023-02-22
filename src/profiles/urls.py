from rest_framework.routers import DefaultRouter
from . import api

app_name = 'profiles'

router = DefaultRouter()

router.register(r'account', api.UserQuePublicAPI, basename='account')
router.register(r'users', api.UserListAPI, basename='users')
router.register(r'verify', api.VerifyOTP, basename='verify')
router.register(r'register', api.RegisterAPI, basename='register')
router.register(r'login', api.LoginAPI, basename='login')
router.register(r'reset-password', api.ResetPasswordRequestAPI, basename='reset-password')
router.register(r'verify-reset-password', api.ResetPasswordAPI, basename='verify-reset-password')
urlpatterns = router.urls
