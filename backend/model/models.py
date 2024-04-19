from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.db import models

class User(AbstractBaseUser):
    idUser = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    token = models.CharField(max_length=100, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    objects = CustomUserManager()

    def __str__(self):
        return f'User: {self.username}'
    
    class Meta:
        db_table = 'user'

class Class(models.Model):
    idClass = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    className = models.CharField(max_length=100, null=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'class'

class Subject(models.Model):
    idSubject = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    idClass = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    subjectName = models.CharField(max_length=100, null=False)
    createdAt = models.DateTimeField(auto_now_add=True)

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

    StudyFrecuency = (
        (1, 'Diario'),
        (2, 'Una semana antes de un examen'),
        (3, 'Un día antes de un examen')
    )

    idStudent = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    idClass = models.ManyToManyField(Class, blank=True)
    idSubject = models.ManyToManyField(Subject, blank=True)
    studentName = models.CharField(max_length=100, null=False)
    gradeGroup = models.CharField(max_length=100, null=False)
    fatherEducation = models.IntegerField(choices=ParentsEducation, null=False)
    motherEducation = models.IntegerField(choices=ParentsEducation, null=False)
    familyIncome = models.IntegerField(choices=FamilyIncome, null=False)
    highSchoolGPA = models.IntegerField(choices=HSGPA, null=False)
    defaultedSubjects = models.IntegerField(choices=DefaultedSubjects)
    currentGPA = models.FloatField(null=False)
    studyPreference = models.IntegerField(choices=AcademicPreferences, null=False)
    preferenceAcademicActivities = models.IntegerField(choices=AcademicPreferences, null=False)
    studyFrecuency = models.IntegerField(choices=StudyFrecuency, null=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student'

class Tendency(models.Model):
    idTendency = models.AutoField(primary_key=True)
    idStudent = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    studentClass = models.IntegerField(null=False)
    tendencyToFail = models.FloatField(null=False)
    tendencyToApprove = models.FloatField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tendency'


