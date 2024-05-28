import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subject, User, Class

@csrf_exempt
def create_subject(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        subject_name = data.get('subject_name')

        if not (subject_name and username):
            return JsonResponse({'error': 'Se requieren todos los campos: subject_name y username'}, status=400)

        # Verificar si el usuario existe
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=400)
        
        # Verificar si el usuario tiene una materia con el mismo nombre
        if Subject.objects.filter(subject_name=subject_name, user=user).exists():
            return JsonResponse({'error': 'Ya existe una materia con este nombre para este usuario'}, status=400)

        # Crear la materia asociada al usuario
        new_subject = Subject(subject_name=subject_name, user=user)
        new_subject.save()

        return JsonResponse({'message': 'Materia creada exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def get_subjects(request):
    if request.method == 'GET':
        subjects = list(Subject.objects.values())
        return JsonResponse({'subjects': subjects}, safe=False)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_subjects_by_user(request, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)

        subjects = list(Subject.objects.filter(user=user).values())
        return JsonResponse({'subjects': subjects}, safe=False)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_subjects_by_class(request, class_name):
    if request.method == 'GET':
        try:
            clas = Class.objects.get(class_name=class_name)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'La clase no existe'}, status=404)

        subjects = list(Subject.objects.filter(clas=clas).values())
        return JsonResponse({'subjects': subjects}, safe=False)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def add_subject_to_class(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject_name = data.get('subject_name')
        username = data.get('username')
        class_name = data.get('class_name')

        if not (subject_name and username and class_name):
            return JsonResponse({'error': 'Se requieren todos los campos: subject_name, username, y class_name'}, status=400)

        # Verificar si el usuario existe
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=400)

        # Verificar si la materia existe para el usuario
        try:
            subject = Subject.objects.get(subject_name=subject_name, user=user)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'La materia no existe para este usuario'}, status=400)

        # Verificar si la clase existe
        try:
            clas = Class.objects.get(class_name=class_name, user=user)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'La clase no existe para este usuario'}, status=400)

        # Añadir la materia a la clase
        subject.clas = clas
        subject.save()

        return JsonResponse({'message': 'Materia añadida a la clase exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def delete_subject(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        username = data.get('username')
        subject_name = data.get('subject_name')

        if not (username and subject_name):
            return JsonResponse({'error': 'Se requieren todos los campos: username y subject_name'}, status=400)

        # Verificar si el usuario existe
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)

        # Verificar si la materia existe para el usuario
        try:
            subject = Subject.objects.get(subject_name=subject_name, user=user)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'La materia no existe para este usuario'}, status=404)

        # Eliminar la materia
        subject.delete()

        return JsonResponse({'message': 'Materia eliminada exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud DELETE'}, status=405)