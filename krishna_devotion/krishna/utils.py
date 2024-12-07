# utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user_email):
    subject = 'Welcome to Our Django App!'
    message = 'Thank you for registering with us. We hope you enjoy our services.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
