from urllib import request
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from .models import User
from .authentication import check_password, send_token
import secrets
import json

@csrf_exempt
def user_registration(request):
    if request.method == 'POST':
        # Obtener los datos JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Validar que se hayan proporcionado todos los campos necesarios
        if not (username and password and email):
            return JsonResponse({'error': 'Se requieren todos los campos: username, password y email'}, status=400)

        # Verificar si ya existe un usuario con el mismo nombre de usuario o correo electrónico
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El nombre de usuario o correo electrónico ya están en uso'}, status=400)

        # Crear un nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password)
                # Guardar el usuario en la base de datos
        user.save()

        return JsonResponse({'message': '¡Registro exitoso!'}, status=201)

    # Si la solicitud no es de tipo POST, devolver un error
    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

def get_users(request):
    users = list(User.objects.values())
    return JsonResponse(users, safe=False)

def get_user_by_ID(request, user_ID):
    # Buscar el usuario por ID, si no se encuentra, devolver un error 404
    user = get_object_or_404(User, id_user=user_ID)

    # Convertir los datos del usuario en un diccionario serializable
    user_data = {
        'id': user.idUser,  # Usamos 'id' en lugar de 'idUser'
        'username': user.username,
        'email': user.email,
        'password': user.password
    }

    # Devolver los datos del usuario como una respuesta JSON
    return JsonResponse(user_data)

def get_user_by_email(user_email):
    # Buscar el usuario por ID, si no se encuentra, devolver un error 404
    user = get_object_or_404(User, email=user_email)
    # Devolver los datos del usuario como una respuesta JSON
    return user

def get_user_by_username(request, username):
    # Buscar el usuario por ID, si no se encuentra, devolver un error 404
    user = get_object_or_404(User, username=username)

    # Convertir los datos del usuario en un diccionario serializable
    user_data = {
        'id': user.idUser,  # Usamos 'id' en lugar de 'idUser'
        'username': user.username,
        'email': user.email,
        'password': user.password
    }

    # Devolver los datos del usuario como una respuesta JSON
    return JsonResponse(user_data)

@csrf_exempt
def request_token(request):
    if request.method == 'POST':
        # Obtener el correo electrónico del cuerpo de la solicitud JSON
        data = json.loads(request.body)
        email = data.get('email')

        # Generar un token de recuperación
        token = secrets.token_hex(20)

        # Verificar que se haya proporcionado un correo electrónico
        if not email:
            return JsonResponse({'error': 'Se requiere un correo electrónico'}, status=400)

        # Buscar al usuario por su dirección de correo electrónico
        user = get_user_by_email(email)
        if not user:
            return JsonResponse({'error': 'No existe un usuario con este correo electrónico'}, status=404)

        # Guardar el token generado en el usuario encontrado
        user.token = token
        user.save()

        # Llamar a la función sendToken para enviar el token de recuperación
        send_token(email, token)

        # Devolver una respuesta JSON indicando que se envió el token de recuperación
        return JsonResponse({'message': 'Token de recuperación enviado correctamente', 'token': token})

    # Si la solicitud no es de tipo POST, devolver un error
    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def restore_password(request):
    if request.method == 'POST':
        # Obtener el token y la nueva contraseña del cuerpo de la solicitud JSON
        data = json.loads(request.body)
        token = data.get('token')
        new_password = data.get('newPassword')

        # Verificar que se hayan proporcionado el token y la nueva contraseña
        if not (token and new_password):
            return JsonResponse({'error': 'Se requieren el token y la nueva contraseña'}, status=400)

        # Buscar al usuario por el token proporcionado
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El token proporcionado no es válido'}, status=400)

        # Cambiar la contraseña del usuario
        user.set_password(new_password)

        # Limpiar el campo de token después de cambiar la contraseña
        user.token = None
        user.save()

        # Devolver una respuesta JSON indicando que se cambió la contraseña con éxito
        return JsonResponse({'message': 'Contraseña cambiada exitosamente'})

    # Si la solicitud no es de tipo POST, devolver un error
    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Validar que se hayan proporcionado todos los campos necesarios
        if not (username and password):
            return JsonResponse({'error': 'Se requieren todos los campos: username y password'}, status=400)

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'El nombre de usuario o la contraseña son incorrectos'}, status=401)

        # Verificar si la contraseña coincide con la almacenada utilizando check_password
        if not check_password(password, user.password):
            return JsonResponse({'error': 'El nombre de usuario o la contraseña son incorrectos'}, status=401)
        
        login(request, user)

        # Devolver la respuesta con el mensaje de inicio de sesión exitoso y el token CSRF
        return JsonResponse({'message': 'Inicio de sesión exitoso'})

    # Si la solicitud no es de tipo POST, devolver un error
    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

def get_CSRF_Token(request):
    csrf_token = request.COOKIES.get('csrftoken')
    return JsonResponse({'token': csrf_token})

@login_required
def logout_user(request):
    logout(request)
    return JsonResponse({'message': '¡Cierre de sesión exitoso!'})

@login_required
def change_user_data(request):
    if request.method == 'POST':
        # Obtener el nombre de usuario del cuerpo JSON de la solicitud
        data = json.loads(request.body)
        username = data.get('username')

        # Verificar si se proporciona el nombre de usuario
        if not username:
            return JsonResponse({'error': 'Se requiere el nombre de usuario'}, status=400)

        # Buscar el usuario en la base de datos
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)

        # Obtener los nuevos datos del usuario
        new_email = data.get('email')
        new_password = data.get('password')

        # Verificar y actualizar el correo electrónico si se proporciona
        if new_email:
            user.email = new_email
        # Verificar y actualizar la contraseña si se proporciona
        if new_password:
            user.set_password(new_password)
            user.save()

        # Guardar los cambios en el usuario
        user.save()

        return JsonResponse({'message': '¡Datos de usuario actualizados correctamente!'})

    # Si la solicitud no es de tipo POST, devolver un error
    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)