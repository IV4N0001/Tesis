import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Class, Student, User

@csrf_exempt
def create_class(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        class_name = data.get('class_name')
        username = data.get('username')

        if not (class_name and username):
            return JsonResponse({'error': 'Se requieren todos los campos: class_name y username'}, status=400)

        # Verificar si el usuario existe
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=400)
        
        # Verificar si el usuario tiene una clase con el mismo nombre
        if Class.objects.filter(class_name=class_name, user=user).exists():
            return JsonResponse({'error': 'Ya existe una clase con este nombre para este usuario'}, status=400)

        # Crear la clase asociada al usuario
        new_class = Class(class_name=class_name, user=user)
        new_class.save()

        return JsonResponse({'message': 'Clase creada exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def get_classes(request):
    classes = list(Class.objects.values())
    return JsonResponse(classes, safe=False)

@csrf_exempt
def get_students_by_class(request, class_name):
    if request.method == 'GET':
        try:
            # Obtener el objeto de la clase por el nombre dado
            clas = Class.objects.get(class_name=class_name)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'La clase no existe'}, status=404)

        # Filtrar los estudiantes que pertenecen a esta clase
        students = Student.objects.filter(clas=clas)

        # Serializar los datos de los estudiantes si es necesario
        # student_data = [{'student_name': student.student_name, 'other_field': student.other_field} for student in students]

        # Retornar los datos de los estudiantes como JSON
        return JsonResponse({'students': list(students.values())})

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_classes_by_user(request, username):
    if request.method == 'GET':
        try:
            # Buscar al usuario
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)

        # Obtener todas las clases asociadas al usuario
        user_classes = Class.objects.filter(user=user)

        # Serializar los datos de las clases si es necesario
        # class_data = [{'class_name': class_obj.class_name, 'other_field': class_obj.other_field} for class_obj in user_classes]

        # Retornar los datos de las clases como JSON
        return JsonResponse({'classes': list(user_classes.values())})

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def update_class_name(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        class_name = data.get('class_name')
        new_class_name = data.get('new_class_name')
        username = data.get('username')

        if not (class_name and new_class_name and username):
            return JsonResponse({'error': 'Se requieren todos los campos: class_name, new_class_name, y username'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)

        try:
            clas = Class.objects.get(class_name=class_name, user=user)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'La clase no existe para este usuario'}, status=404)

        clas.class_name = new_class_name
        clas.save()

        return JsonResponse({'message': 'Nombre de la clase actualizado exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def delete_class(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        class_name = data.get('class_name')
        username = data.get('username')

        if not (class_name and username):
            return JsonResponse({'error': 'Se requieren todos los campos: class_name y username'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)

        try:
            clas = Class.objects.get(class_name=class_name, user=user)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'La clase no existe para este usuario'}, status=404)

        clas.delete()

        return JsonResponse({'message': 'Clase eliminada exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud DELETE'}, status=405)