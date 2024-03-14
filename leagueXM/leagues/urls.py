from django.contrib import admin
from django.urls import path, include

from leagues import views

urlpatterns = [
    path("menu", views.menu, name='menu'),
    path("classificacio/<int:lliga_id>",views.classificacio, name='classificacio'),
    # path('crearLliga',views.crearLliga, name="crearLliga"),
]