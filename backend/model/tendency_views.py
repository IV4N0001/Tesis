from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from model.classifier_algorithm.classifier import classify_students
from model.models import Tendency, Student, User

@csrf_exempt
def predict_class(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            student_names = data.get('students', [])

            if not username:
                return JsonResponse({'error': 'No username provided'}, status=400)
            if not student_names:
                return JsonResponse({'error': 'No student names provided'}, status=400)

            students_data = []
            for student_name in student_names:
                student = Student.objects.get(student_name=student_name)
                students_data.append({
                    'father_education': student.father_education,
                    'mother_education': student.mother_education,
                    'family_income': student.family_income,
                    'high_school_GPA': student.high_school_GPA,
                    'current_GPA': student.current_GPA,
                    'study_preference': student.study_preference,
                    'preference_academic_activities': student.preference_academic_activities,
                    'study_frequency': student.study_frequency
                })

            predictions = classify_students(students_data)

            for student_name, prediction in zip(student_names, predictions):
                student = Student.objects.get(student_name=student_name)
                Tendency.objects.create(student=student, student_class=student.grade_group, tendency=prediction)

            return JsonResponse({'status': 'success', 'predictions': predictions}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_tendencys(request):
    tendencys = list(Tendency.objects.values())
    return JsonResponse(tendencys, safe=False)

@csrf_exempt
def get_tendencies_by_username(request, username):
    if request.method == 'GET':
        try:
            # Buscar el usuario por el nombre de usuario dado
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)

        # Obtener todos los estudiantes asociados a ese usuario
        students = user.student_set.all()

        # Obtener la última tendencia asociada a cada estudiante
        latest_tendencies = []
        for student in students:
            latest_tendency = student.tendency_set.latest('created_at')
            latest_tendencies.append({
                'id_tendency': latest_tendency.id_tendency,
                'student_id': latest_tendency.student.id_student if latest_tendency.student else None,
                'student_class': latest_tendency.student_class,
                'tendency': latest_tendency.tendency,
                'created_at': latest_tendency.created_at
            })

        # Retornar los datos de las últimas tendencias como JSON
        return JsonResponse({'tendencies': latest_tendencies}, status=200)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_student_tendency(request, username, student_name):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            student = user.student_set.get(student_name=student_name)
        except (User.DoesNotExist, Student.DoesNotExist):
            return JsonResponse({'error': 'El usuario o el estudiante no existe'}, status=404)

        # Obtener la última tendencia del estudiante
        latest_tendency = student.tendency_set.latest('created_at')

        # Serializar los datos de la última tendencia
        tendency_data = {
            'id_tendency': latest_tendency.id_tendency,
            'student_class': latest_tendency.student_class,
            'tendency': latest_tendency.tendency,
            'created_at': latest_tendency.created_at
        }

        return JsonResponse({'tendency': tendency_data}, status=200)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_group_tendency(request, username, grade_group):
    if request.method == 'GET':
        try:
            # Obtener todos los estudiantes del grupo registrados por el usuario
            students = Student.objects.filter(username=username, grade_group=grade_group)

            # Inicializar un diccionario para almacenar las últimas tendencias de cada estudiante
            latest_tendencies = {}

            # Recorrer cada estudiante para obtener su última tendencia
            for student in students:
                latest_tendency = student.tendency_set.latest('created_at')
                latest_tendencies[student.student_name] = {
                    'id_tendency': latest_tendency.id_tendency,
                    'student_class': latest_tendency.student_class,
                    'tendency': latest_tendency.tendency,
                    'created_at': latest_tendency.created_at
                }

            return JsonResponse({'tendencies': latest_tendencies}, status=200)

        except Student.DoesNotExist:
            return JsonResponse({'error': 'No hay estudiantes en este grupo'}, status=404)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_group_tendency_by_category(request, username, grade_group, tendency_category):
    if request.method == 'GET':
        try:
            # Obtener todos los estudiantes del grupo registrados por el usuario
            students = Student.objects.filter(username=username, grade_group=grade_group)

            # Inicializar un diccionario para almacenar las últimas tendencias de cada estudiante para la categoría especificada
            latest_tendencies = {}

            # Recorrer cada estudiante para obtener su última tendencia para la categoría especificada
            for student in students:
                latest_tendency = student.tendency_set.filter(tendency=tendency_category).latest('created_at')
                latest_tendencies[student.student_name] = {
                    'id_tendency': latest_tendency.id_tendency,
                    'student_class': latest_tendency.student_class,
                    'tendency': latest_tendency.tendency,
                    'created_at': latest_tendency.created_at
                }

            return JsonResponse({'tendencies': latest_tendencies}, status=200)

        except (Student.DoesNotExist, Tendency.DoesNotExist):
            return JsonResponse({'error': 'No hay estudiantes o tendencias para este grupo y categoría'}, status=404)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_student_tendency_by_category(request, username, tendency_category):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
            # Obtener el estudiante
            student = user.student_set.latest('created_at')
            # Obtener la última tendencia del estudiante para la categoría especificada
            latest_tendency = student.tendency_set.filter(tendency=tendency_category).latest('created_at')

            # Serializar los datos de la última tendencia
            tendency_data = {
                'id_tendency': latest_tendency.id_tendency,
                'student_class': latest_tendency.student_class,
                'tendency': latest_tendency.tendency,
                'created_at': latest_tendency.created_at
            }

            return JsonResponse({'tendency': tendency_data}, status=200)
        except (User.DoesNotExist, Student.DoesNotExist, Tendency.DoesNotExist):
            return JsonResponse({'error': 'No hay tendencias para este estudiante y categoría'}, status=404)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)

@csrf_exempt
def get_user_tendency_by_category(request, username, tendency_category):
    if request.method == 'GET':
        try:
            # Buscar el usuario por el nombre de usuario dado
            user = User.objects.get(username=username)

            # Obtener todos los estudiantes asociados al usuario
            students = Student.objects.filter(user=user)

            # Inicializar un diccionario para almacenar las últimas tendencias de cada estudiante para la categoría especificada
            latest_tendencies = {}

            # Recorrer cada estudiante para obtener su última tendencia para la categoría especificada
            for student in students:
                latest_tendency = student.tendency_set.filter(tendency=tendency_category).latest('created_at')
                latest_tendencies[student.student_name] = {
                    'id_tendency': latest_tendency.id_tendency,
                    'student_class': latest_tendency.student_class,
                    'tendency': latest_tendency.tendency,
                    'created_at': latest_tendency.created_at
                }

            return JsonResponse({'tendencies': latest_tendencies}, status=200)

        except (User.DoesNotExist, Student.DoesNotExist, Tendency.DoesNotExist):
            return JsonResponse({'error': 'No hay usuarios, estudiantes o tendencias para este usuario y categoría'}, status=404)

    return JsonResponse({'error': 'Se espera una solicitud GET'}, status=405)
