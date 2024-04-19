from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import check_password

def sendToken(email, token):
    # Construir el mensaje de correo electrónico
    subject = 'Token de recuperación de cuenta'
    message = f'Tu token de recuperación de cuenta es: {token}'
    sender = settings.EMAIL_HOST_USER  # Usar el correo electrónico configurado en tu proyecto Django

    # Enviar el correo electrónico
    send_mail(subject, message, sender, [email])

    # Devolver el token de recuperación en caso de que lo necesites para otro propósito
    #return token

def checkPassword(flatPassword, encodePassword):
    return check_password(flatPassword, encodePassword)

