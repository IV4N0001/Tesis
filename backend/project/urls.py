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
from model import student_views, user_views, class_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/user-registration', user_views.user_registration),
    path('user/get-users', user_views.get_users),
    path('user/get-user-by-ID/<int:userID>', user_views.get_user_by_ID),
    path('user/get-user-by-email/<str:userEmail>', user_views.get_user_by_email),
    path('user/get-user-by-username/<str:username>', user_views.get_user_by_username),
    path('user/request-token', user_views.request_token),
    path('user/restore-password', user_views.restore_password),
    path('user/login', user_views.login_user),
    path('user/logout', user_views.logout_user),
    path('user/get-CSRF-token', user_views.get_CSRF_Token),
    path('user/change-user-data', user_views.change_user_data),
    path('class/create-class', class_views.create_class),
    path('class/get-classes', class_views.get_classes),
    path('student/student-registration', student_views.student_registration),
    path('student/get-students', student_views.get_students)
]
