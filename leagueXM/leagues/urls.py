from django.contrib import admin
from django.urls import path, include

from leagues import views

urlpatterns = [
    path("menu", views.menu, name='menu'),
    path("classificacio/<int:lliga_id>",views.classificacio, name='classificacio'),
    path('crearLliga',views.crear_lliga, name="crearLliga"),
    path('crear_equipo/', views.crear_equipo, name='crear_equipo'),
    path("edita_equip",views.edita_equip, name="edita_equip"),
]