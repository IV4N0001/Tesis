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
from model import user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/registration', user_views.userRegistration),
    path('user/getUsers', user_views.getUsers),
    path('user/getUserByID/<int:userID>', user_views.getUserByID),
    path('user/getUserByEmail/<str:userEmail>', user_views.getUserByEmail),
    path('user/getUserByUsername/<str:username>', user_views.getUserByUsername),
    path('user/requestToken', user_views.requestToken),
    path('user/restorePassword', user_views.restorePassword),
    path('user/login', user_views.loginUser),
    path('user/logout', user_views.logoutUser),
    path('user/getToken', user_views.getCSRFToken),
    path('user/changeUserData', user_views.changeUserData)
]
