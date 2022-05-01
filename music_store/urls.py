"""music_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from authorization.views import RegistrationView, logout_view

urlpatterns = [
    path('', include('web_ui.urls'), name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='sing_in'),
    path('accounts/registration/', RegistrationView.as_view(), name='sing_up'),
    path('accounts/logout/', logout_view, name='logout'),
]
