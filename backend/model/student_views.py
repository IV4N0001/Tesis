import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Class, Student, User

@csrf_exempt
def student_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        class_name = data.get('class')
        subject = data.get('subject')
        student_name = data.get('student_name')
        grade_group = data.get('grade_group')
        father_education = data.get('father_education')
        mother_education = data.get('mother_education')
        family_income = data.get('family_income')
        high_school_GPA = data.get('high_school_GPA')
        defaulted_subjects = data.get('defaulted_subjects')
        current_GPA = data.get('current_GPA')
        study_preference = data.get('study_preference')
        preference_academic_activities = data.get('preference_academic_activities')
        study_frequency = data.get('study_frequency')

        # Verificar si el usuario existe
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=400)

        # Verificar si la clase existe
        clas = None
        if class_name:
            try:
                clas = Class.objects.get(class_name=class_name, id_user=user)
            except Class.DoesNotExist:
                return JsonResponse({'error': 'La clase no existe'}, status=400)

        # Crear el estudiante
        new_student = Student(
            user=user,
            student_name=student_name,
            grade_group=grade_group,
            father_education=father_education,
            mother_education=mother_education,
            family_income=family_income,
            high_school_GPA=high_school_GPA,
            defaulted_subjects=defaulted_subjects,
            current_GPA=current_GPA,
            study_preference=study_preference,
            preference_academic_activities=preference_academic_activities,
            study_frequency=study_frequency
        )
        new_student.save()

        # Asociar el estudiante a la clase si se proporciona
        #if clas:
        #    student.id_class.add(clas)

        # Asociar el estudiante a la materia si se proporciona
        #if subject_name:
            #estudiante.id_subject.create(subject_name=subject_name)

        return JsonResponse({'message': 'Estudiante registrado exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud POST'}, status=405)

@csrf_exempt
def get_students(request):
    students = list(Student.objects.values())
    return JsonResponse(students, safe=False)

@csrf_exempt
def add_student_to_class(request):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        username = data.get('username')
        class_name = data.get('class_name')
        student_name = data.get('student_name')

        try:
            # Buscar al usuario
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=400)

        try:
            # Buscar la clase del usuario
            clas = Class.objects.get(class_name=class_name, user_id=user)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'La clase no existe'}, status=400)

        try:
            # Buscar al estudiante
            student = Student.objects.get(student_name=student_name)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'El estudiante no existe'}, status=400)

        student.clas.add(clas)

        return JsonResponse({'message': 'Estudiante agregado a la clase exitosamente'})

    return JsonResponse({'error': 'Se espera una solicitud PATCH'}, status=405)

@csrf_exempt
def remove_student_from_class(request):
    if request.method == 'PATCH':
        data = json.loads(request.body)
        username = data.get('username')
        class_name = data.get('class_name')
        student_name = data.get('student_name')

        try:
            # Buscar al usuario
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=400)

        try:
            # Buscar la clase del usuario
            clas = Class.objects.get(class_name=class_name, user=user)
        except Class.DoesNotExist:
            return JsonResponse({'error': 'La clase no existe'}, status=400)

        try:
            # Buscar al estudiante
            student = Student.objects.get(student_name=student_name)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'El estudiante no existe'}, status=400)

        # Verificar si el estudiante está asociado a la clase
        if clas.students.filter(id_student=student.id_student).exists():
            # Remover al estudiante de la clase
            student.clas.remove(clas)
            return JsonResponse({'message': 'Estudiante eliminado de la clase exitosamente'})
        else:
            return JsonResponse({'error': 'El estudiante no está asociado a esta clase'}, status=400)

    return JsonResponse({'error': 'Se espera una solicitud PATCH'}, status=405)