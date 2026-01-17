"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name = 'register'),
    path('', views.trip_list, name = 'trip_list'),
    path('create-trip/', views.trip_create, name = 'trip_create'),
    path('trip/<int:pk>/', views.trip_detail, name = 'trip_detail'),
    path('api/add-expense/<int:trip_pk>/', views.add_expense_api, name = 'add_expense_api'),
    path('api/delete-expense/<int:expense_pk>/', views.delete_expense_api, name='delete_expense_api'),
    path('api/add-participant/<int:trip_pk>/', views.add_participant_api, name = 'add_participant_api'),
    path('trip/<int:pk>/finish/', views.finish_trip, name = 'trip_finish'),
    path('trip/<int:pk>/leave/', views.leave_trip, name='leave_trip'),
]
