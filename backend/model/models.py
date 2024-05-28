from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.db import models

class User(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    token = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    objects = CustomUserManager()

    def __str__(self):
        return f'User: {self.username}'
    
    class Meta:
        db_table = 'user'

class Class(models.Model):
    id_class = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    class_name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'class'

class Subject(models.Model):
    id_subject = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    clas = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    subject_name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subject'

class Student(models.Model):
    ParentsEducation = (
        (1, 'Primaria y secundaria'),
        (2, 'Media superior'),
        (3, 'Superior o mayor'),
    )

    FamilyIncome = (
        (1, '< 5000'),
        (2, '5000 - 10000'),
        (3, '> 10000'),
    )

    HSGPA = (
        (1, '< 7.5'),
        (2, '7.5 - 8.5'),
        (3, '> 8.5'),
    )

    DefaultedSubjects = (
        (1, '0'),
        (2, '1'),
        (3, '> 2'),
    )

    AcademicPreferences = (
        (1, 'Solo'),
        (2, 'Con otra persona'),
        (3, 'En grupo'),
    )

    StudyFrequency = (
        (1, 'Diario'),
        (2, 'Una semana antes de un examen'),
        (3, 'Un día antes de un examen')
    )

    id_student = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    clas = models.ManyToManyField(Class, related_name='students', blank=True)
    subject = models.ManyToManyField(Subject, blank=True)
    student_name = models.CharField(max_length=100, null=False)
    grade_group = models.CharField(max_length=100, null=False)
    father_education = models.IntegerField(choices=ParentsEducation, null=False)
    mother_education = models.IntegerField(choices=ParentsEducation, null=False)
    family_income = models.IntegerField(choices=FamilyIncome, null=False)
    high_school_GPA = models.IntegerField(choices=HSGPA, null=False)
    defaulted_subjects = models.IntegerField(choices=DefaultedSubjects)
    current_GPA = models.FloatField(null=False)
    study_preference = models.IntegerField(choices=AcademicPreferences, null=False)
    preference_academic_activities = models.IntegerField(choices=AcademicPreferences, null=False)
    study_frequency = models.IntegerField(choices=StudyFrequency, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'student'

class Tendency(models.Model):
    id_tendency = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    student_class = models.CharField(max_length=16, null=False, default='1-01')
    tendency = models.CharField(max_length=16, null=False, default='0')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tendency'


