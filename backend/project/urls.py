"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Agrega 'include' para incluir las URLs de autenticación
from model import student_views, user_views, class_views, subject_views, tendency_views
#from model.classifier_algorithm import classifier, logistic_regression_model

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/user-registration', user_views.user_registration),
    path('user/get-users', user_views.get_users),
    path('user/get-user-by-ID/<int:user_ID>', user_views.get_user_by_ID),
    path('user/get-user-by-email/<str:user_email>', user_views.get_user_by_email),
    path('user/get-user-by-username/<str:username>', user_views.get_user_by_username),
    path('user/request-token', user_views.request_token),
    path('user/restore-password', user_views.restore_password),
    path('user/login', user_views.login_user),
    path('user/logout', user_views.logout_user),
    path('user/get-CSRF-token', user_views.get_CSRF_Token),
    path('user/change-user-data', user_views.change_user_data),
    path('class/create-class', class_views.create_class),
    path('class/get-classes', class_views.get_classes),
    path('class/get-students-by-class/<str:class_name>', class_views.get_students_by_class),
    path('class/get-classes-by-user/<str:username>', class_views.get_classes_by_user),
    path('class/update-class-name', class_views.update_class_name),
    path('class/delete-class', class_views.delete_class),
    path('student/student-registration', student_views.student_registration),
    path('student/get-students', student_views.get_students),
    path('student/get-students-by-subject/<str:subject_name>', student_views.get_students_by_subject),
    path('student/get-students-by-username/<str:username>', student_views.get_students_by_username),
    path('student/add-student-to-class', student_views.add_student_to_class),
    path('student/remove-student-from-class', student_views.remove_student_from_class),
    path('student/remove-student-from-subject', student_views.remove_student_from_subject),
    path('student/add-student-to-subject', student_views.add_student_to_subject),
    path('subject/create-subject', subject_views.create_subject),
    path('subject/get-subjects', subject_views.get_subjects),
    path('subject/get-subjects-by-class/<str:class_name>', subject_views.get_subjects_by_class),
    path('subject/add-subject-to-class', subject_views.add_subject_to_class),
    path('subject/delete-subject', subject_views.delete_subject),
    #path('algorithm/classify-students', classifier.classify_students),
    path('tendency/predict-class', tendency_views.predict_class),
    path('tendency/get-tendencys', tendency_views.get_tendencys),
    path('tendency/get-tendencies-by-username/<str:username>/', tendency_views.get_tendencies_by_username),
    path('tendency/get-student-tendency/<str:username>/<str:student_name>/', tendency_views.get_student_tendency),
    path('tendency/get-group-tendencys/<str:username>/<str:grade_group>/', tendency_views.get_group_tendency),
    path('tendency/get-user-tendency-by-category/<str:username>/<str:tendency_category>/', tendency_views.get_user_tendency_by_category),
    path('tendency/get-group-tendency-by-category/<str:username>/<str:grade_group>/<str:tendency_category>/', tendency_views.get_group_tendency_by_category),
]
