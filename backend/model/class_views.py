import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Class, User

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
        if Class.objects.filter(class_name=class_name, id_user= user).exists():
            return JsonResponse({'error': 'Ya existe una clase con este nombre para este usuario'}, status=400)

        # Crear la clase
        # Crear la clase asociada al usuario
        new_class = Class(class_name=class_name, id_user=user)
        new_class.save()

        return JsonResponse({'message': 'Clase creada exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def get_classes(request):
    classes = list(Class.objects.values())
    return JsonResponse(classes, safe=False)