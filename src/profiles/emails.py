import random
import string

from django.core.mail import send_mail
from django.conf import settings
from .models import QueUser


def send_otp_to_email(email):
    subject = "Your account verification email"
    otp = random.randint(1000, 9999)
    message = f"Your opt is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    user = QueUser.objects.get(email=email)
    user.otp = otp
    user.save()


def generate_reset_password_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_reset_password_otp_to_email(email, otp):
    subject = 'Password reset OTP'
    message = f'Your password reset OTP is: {otp}'
    from_email = settings.EMAIL_HOST
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
